from datetime import datetime

class Book:
    all_books = []

    def __init__(self, title):
        self.title = title
        self._contracts = []  # List to store contracts of the book
        Book.all_books.append(self)

    def contracts(self):
        return self._contracts.copy()

    def authors(self):
        return [contract.author for contract in self._contracts]  # Return a list of authors associated with the book


class Author:
    all_authors = []

    def __init__(self, name):
        self.name = name
        self._contracts = []  # List to store contracts of the author
        Author.all_authors.append(self)

    def contracts(self):
        return self._contracts.copy()

    def books(self):
        return [contract.book for contract in self._contracts]

    def sign_contract(self, book, date, royalties):
        if not isinstance(book, Book):
            raise Exception("book must be an instance of Book")
        contract = Contract(self, book, date, royalties)
        self._contracts.append(contract)
        book._contracts.append(contract)  # Associate the contract with the corresponding book
        return contract

    def total_royalties(self):
        return sum(contract.royalties for contract in self._contracts)


class Contract:
    all_contracts = []

    def __init__(self, author, book, date, royalties):
        if not isinstance(author, Author) or not isinstance(book, Book):
            raise Exception("author and book must be instances of Author and Book classes, respectively")
        if not isinstance(date, str):
            raise Exception("date must be of type str")
        if not isinstance(royalties, int):
            raise Exception("royalties must be of type int")

        # Ensure the date is in the correct format "MM/DD/YYYY" for sorting
        self.date = datetime.strptime(date, "%m/%d/%Y").strftime("%m/%d/%Y")
        
        self.author = author
        self.book = book
        self.royalties = royalties
        Contract.all_contracts.append(self)
        author._contracts.append(self)  # Associate the contract with the corresponding author
        book._contracts.append(self)    # Associate the contract with the corresponding book

    @classmethod
    def contracts_by_date(cls, date=None):
        if date:
            # Return contracts with the specified date
            return [contract for contract in cls.all_contracts if contract.date == datetime.strptime(date, "%m/%d/%Y")]
        else:
            # Sort all contracts by date in ascending order
            return sorted(cls.all_contracts, key=lambda contract: contract.date)

    def __eq__(self, other):
        if not isinstance(other, Contract):
            return False
        return (
            self.author == other.author and
            self.book == other.book and
            self.date == other.date and
            self.royalties == other.royalties
        )