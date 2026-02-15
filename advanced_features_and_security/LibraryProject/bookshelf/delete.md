
#### **File 4: `delete.md`**
```markdown
# Delete Operation

## Python Command:
```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
print("Book deleted successfully")

# Verify deletion
books = Book.objects.all()
print(f"Remaining books: {books.count()}")