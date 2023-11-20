import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('ebookstore.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create the 'books' table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT,
        author TEXT,
        qty INTEGER
    )
''')

# Populate the table with initial values
cursor.executemany('''
    INSERT INTO books (id, title, author, qty)
    VALUES (?, ?, ?, ?)
''', [
    (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
    (3002, "Harry Potter and the Philosopher's Stone", 'J.K. Rowling', 40),
    (3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25),
    (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
    (3005, 'Alice in Wonderland', 'Lewis Carroll', 12),
])

# Commit the changes to the database
conn.commit()

def print_menu():
    print("\nMenu:")
    print("1. Enter book")
    print("2. Update book")
    print("3. Delete book")
    print("4. Search books")
    print("0. Exit")

def enter_book():
    id = int(input("Enter book ID: "))
    title = input("Enter book title: ")
    author = input("Enter author: ")
    qty = int(input("Enter quantity: "))

    # Check if the book with the given ID already exists
    cursor.execute("SELECT * FROM books WHERE id = ?", (id,))
    existing_book = cursor.fetchone()

    if existing_book:
        print("Book with ID {} already exists.".format(id))
    else:
        cursor.execute("INSERT INTO books VALUES (?, ?, ?, ?)", (id, title, author, qty))
        print("Book added successfully.")

    conn.commit()

def update_book():
    id = int(input("Enter the ID of the book to update: "))
    qty = int(input("Enter the new quantity: "))

    cursor.execute("UPDATE books SET qty = ? WHERE id = ?", (qty, id))
    if cursor.rowcount > 0:
        print("Book updated successfully.")
    else:
        print("Book with ID {} not found.".format(id))

    conn.commit()

def delete_book():
    choice = input("Delete by ID (1) or Title (2): ")

    if choice == '1':
        id = int(input("Enter the ID of the book to delete: "))
        cursor.execute("DELETE FROM books WHERE id = ?", (id,))
    elif choice == '2':
        title = input("Enter the title of the book to delete: ")
        cursor.execute("DELETE FROM books WHERE title = ?", (title,))
    else:
        print("Invalid choice.")
        return

    if cursor.rowcount > 0:
        print("Book deleted successfully.")
    else:
        print("Book not found.")

    conn.commit()

def search_books():
    keyword = input("Enter book ID or Title to search: ")
    cursor.execute("SELECT * FROM books WHERE id = ? OR title LIKE ?", (keyword, f"%{keyword}%"))
    results = cursor.fetchall()

    if results:
        for row in results:
            print(row)
    else:
        print("No matching books found.")

def main():
    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            enter_book()
        elif choice == '2':
            update_book()
        elif choice == '3':
            delete_book()
        elif choice == '4':
            search_books()
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

# Close the database connection when the program exits
conn.close()
