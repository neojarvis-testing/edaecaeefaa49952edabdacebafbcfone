from pymongo import MongoClient

# Connect to MongoDB
def connect_to_mongodb():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        print("Connected to MongoDB!")
        return client
    except Exception as e:
        print(f"Connection failed: {e}")
        exit()

# Database and Collection Initialization
client = connect_to_mongodb()
db = client["Library"]
books_collection = db["Books"]

# Core Functions
def add_book(title, author, genre, stock):
    book = {"title": title, "author": author, "genre": genre, "stock": stock}
    result = books_collection.insert_one(book)
    return result.inserted_id

def query_books(query_type, value):
    if query_type == "title":
        query = {"title": value}
    elif query_type == "author":
        query = {"author": value}
    else:
        return []
    return list(books_collection.find(query))

def update_stock(title, new_stock):
    result = books_collection.update_one(
        {"title": title},
        {"$set": {"stock": new_stock}}
    )
    return result.modified_count > 0

def delete_book(title):
    result = books_collection.delete_one({"title": title})
    return result.deleted_count > 0

def list_books():
    return list(books_collection.find().sort("title"))

# Menu-driven application
def main_menu():
    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Query Books")
        print("3. Update Stock")
        print("4. Delete Book")
        print("5. List All Books")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter author name: ")
            genre = input("Enter genre: ")
            stock = int(input("Enter number of copies: "))
            book_id = add_book(title, author, genre, stock)
            print(f"Book added with ID: {book_id}")
        elif choice == "2":
            query_type = input("Search by (1) Title or (2) Author? ")
            if query_type == "1":
                title = input("Enter book title: ")
                books = query_books("title", title)
            elif query_type == "2":
                author = input("Enter author name: ")
                books = query_books("author", author)
            else:
                print("Invalid choice.")
                continue
            if books:
                for book in books:
                    print(book)
            else:
                print("No books found.")
        elif choice == "3":
            title = input("Enter book title: ")
            new_stock = int(input("Enter new stock quantity: "))
            success = update_stock(title, new_stock)
            print("Stock updated successfully." if success else "No matching book found.")
        elif choice == "4":
            title = input("Enter book title to delete: ")
            success = delete_book(title)
            print("Book deleted successfully." if success else "No matching book found.")
        elif choice == "5":
            books = list_books()
            if books:
                for book in books:
                    print(book)
            else:
                print("No books found in the library.")
        elif choice == "6":
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main_menu()
