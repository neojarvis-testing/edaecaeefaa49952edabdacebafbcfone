import unittest
from unittest.mock import patch
from main import add_book, query_books, update_stock, delete_book, list_books, connect_to_mongodb


class TestLibraryManagementSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up MongoDB connection and clear the test collection."""
        cls.client = connect_to_mongodb()
        cls.db = cls.client["Library"]
        cls.books_collection = cls.db["Books"]
        cls.books_collection.delete_many({})  # Clear collection before tests

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests."""
        cls.books_collection.delete_many({})  # Clear collection after tests
        cls.client.close()

    def test_add_book(self):
        """Test adding a book to the collection."""
        book_id = add_book("The Great Gatsby", "F. Scott Fitzgerald", "Fiction", 10)
        book = self.books_collection.find_one({"_id": book_id})
        self.assertIsNotNone(book)
        self.assertEqual(book["title"], "The Great Gatsby")

    def test_query_books_by_title(self):
        """Test querying books by title."""
        self.books_collection.insert_one({"title": "1984", "author": "George Orwell", "genre": "Dystopian", "stock": 5})
        books = query_books("title", "1984")
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]["author"], "George Orwell")

    def test_query_books_by_author(self):
        """Test querying books by author."""
        self.books_collection.insert_one({"title": "Animal Farm", "author": "George Orwell", "genre": "Fiction", "stock": 8})
        books = query_books("author", "George Orwell")
        self.assertGreaterEqual(len(books), 1)
        self.assertTrue(any(book["title"] == "Animal Farm" for book in books))

    def test_update_stock(self):
        """Test updating the stock of a book."""
        self.books_collection.insert_one({"title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Fiction", "stock": 7})
        success = update_stock("To Kill a Mockingbird", 15)
        self.assertTrue(success)
        book = self.books_collection.find_one({"title": "To Kill a Mockingbird"})
        self.assertEqual(book["stock"], 15)

    def test_delete_book(self):
        """Test deleting a book from the collection."""
        self.books_collection.insert_one({"title": "Moby Dick", "author": "Herman Melville", "genre": "Fiction", "stock": 3})
        success = delete_book("Moby Dick")
        self.assertTrue(success)
        book = self.books_collection.find_one({"title": "Moby Dick"})
        self.assertIsNone(book)

    def test_list_books(self):
        """Test listing all books."""
        self.books_collection.insert_many([
            {"title": "Book A", "author": "Author A", "genre": "Genre A", "stock": 10},
            {"title": "Book B", "author": "Author B", "genre": "Genre B", "stock": 5}
        ])
        books = list_books()
        self.assertEqual(len(books), 2)
        titles = [book["title"] for book in books]
        self.assertIn("Book A", titles)
        self.assertIn("Book B", titles)


if __name__ == "__main__":
    unittest.main()
