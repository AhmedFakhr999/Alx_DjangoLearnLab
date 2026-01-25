
import os
import django
import sys
from relationship_app.models import Author, Book, Library, Librarian

def query_books_by_author(author_name):
    """
    Query all books by a specific author
    
    Args:
        author_name (str): Name of the author to search for
    """
    print(f"\n=== Books by Author: {author_name} ===")
    
    try:
        # Get the author object
        author = Author.objects.get(name=author_name)
        
        # Get all books by this author using the ForeignKey reverse relationship
        books = Book.objects.filter(author=author)
        
        # Alternative way: Use the reverse relationship from Author to Book
        # books = author.book_set.all()
        
        for book in books:
            print(f"Title: {book.title}")
            print(f"Author: {book.author.name}")
            print("-" * 40)
            
        if not books:
            print(f"No books found for author: {author_name}")
            
        return books
        
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found in database")
        return []
    except Author.MultipleObjectsReturned:
        print(f"Multiple authors found with name containing '{author_name}'")
        authors = Author.objects.filter(name__icontains=author_name)
        for author in authors:
            books = Book.objects.filter(author=author)
            print(f"\nAuthor: {author.name}")
            for book in books:
                print(f"  - {book.title}")
        return []

def list_all_books_in_library(library_name):
    """
    List all books in a specific library
    
    Args:
        library_name (str): Name of the library
    """
    print(f"\n=== All Books in Library: {library_name} ===")
    
    try:
        # Get the library object
        library = Library.objects.get(name=library_name)
        
        # Get all books in this library using the ManyToMany relationship
        books = library.books.all()
        
        print(f"Library: {library.name}")
        print("-" * 40)
        
        for book in books:
            print(f"Title: {book.title}")
            print(f"Author: {book.author.name}")
            print("-" * 30)
            
        if not books:
            print(f"No books found in library: {library_name}")
            
        return books
        
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found in database")
        return []

def retrieve_librarian_for_library(library_name):
    """
    Retrieve the librarian for a specific library
    
    Args:
        library_name (str): Name of the library
    """
    print(f"\n=== Librarian for Library: {library_name} ===")
    
    try:
        # Get the library object
        library = Library.objects.get(name=library_name)
        
        # Get the librarian using the OneToOne relationship
        # This will raise Librarian.DoesNotExist if no librarian is assigned
        librarian = Librarian.objects.get(library=library)
        
        print(f"Library: {library.name}")
        print(f"Librarian: {librarian.name}")
        
        return librarian
        
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found in database")
        return None
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to library: {library_name}")
        return None

def create_sample_data():
    """Create sample data for testing"""
    print("\n=== Creating Sample Data ===")
    
    # Create authors
    author1, _ = Author.objects.get_or_create(name="J.K. Rowling")
    author2, _ = Author.objects.get_or_create(name="George Orwell")
    author3, _ = Author.objects.get_or_create(name="Harper Lee")
    
    # Create books
    book1, _ = Book.objects.get_or_create(
        title="Harry Potter and the Philosopher's Stone",
        author=author1
    )
    book2, _ = Book.objects.get_or_create(
        title="1984",
        author=author2
    )
    book3, _ = Book.objects.get_or_create(
        title="Animal Farm",
        author=author2
    )
    book4, _ = Book.objects.get_or_create(
        title="To Kill a Mockingbird",
        author=author3
    )
    
    # Create libraries
    library1, _ = Library.objects.get_or_create(name="Central Library")
    library2, _ = Library.objects.get_or_create(name="City Library")
    
    # Add books to libraries (ManyToMany relationship)
    library1.books.add(book1, book2, book3)
    library2.books.add(book2, book4)
    
    # Create librarians and assign to libraries (OneToOne relationship)
    librarian1, _ = Librarian.objects.get_or_create(
        name="Sarah Johnson",
        library=library1
    )
    librarian2, _ = Librarian.objects.get_or_create(
        name="Michael Chen",
        library=library2
    )
    
    print("Sample data created successfully!")
    return True

def main():
    """Main function to demonstrate all queries"""
    print("=" * 60)
    print("DJANGO ORM QUERY SAMPLES")
    print("=" * 60)
    
    # Uncomment to create sample data if your database is empty
    # create_sample_data()
    
    # Example 1: Query books by a specific author
    query_books_by_author("George Orwell")
    
    # Example 2: List all books in a library
    list_all_books_in_library("Central Library")
    
    # Example 3: Retrieve librarian for a library
    retrieve_librarian_for_library("Central Library")
    
    # Additional examples
    print("\n" + "=" * 60)
    print("ADDITIONAL QUERY EXAMPLES")
    print("=" * 60)
    
    # Example 4: Find all libraries containing a specific book
    print("\n=== Libraries containing '1984' ===")
    try:
        book = Book.objects.get(title__icontains="1984")
        libraries_with_book = book.library.all()  # Using related_name='library'
        for lib in libraries_with_book:
            print(f"- {lib.name}")
    except Book.DoesNotExist:
        print("Book '1984' not found")
    
    # Example 5: Count books by each author
    print("\n=== Book Count by Author ===")
    authors = Author.objects.all()
    for author in authors:
        book_count = Book.objects.filter(author=author).count()
        print(f"{author.name}: {book_count} book(s)")
    
    # Example 6: All librarians with their libraries
    print("\n=== All Librarians and Their Libraries ===")
    librarians = Librarian.objects.select_related('library').all()
    for lib in librarians:
        print(f"Librarian: {lib.name} → Library: {lib.library.name}")

if __name__ == "__main__":
    main()