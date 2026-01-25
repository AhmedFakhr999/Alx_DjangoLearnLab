
### **Step 10: Test Everything Works**

```bash
# Go to project directory
cd LibraryProject

# Test migrations
python manage.py makemigrations bookshelf
python manage.py migrate

# Test the model
python manage.py shell -c "
from bookshelf.models import Book
import sys

# Test Create
book = Book.objects.create(title='Test Book', author='Test Author', publication_year=2024)
print(f'Created: {book.id}')

# Test Retrieve
retrieved = Book.objects.get(id=book.id)
print(f'Retrieved: {retrieved.title}')

# Test Update
retrieved.title = 'Updated Title'
retrieved.save()
print(f'Updated: {retrieved.title}')

# Test Delete
retrieved.delete()
count = Book.objects.count()
print(f'Deleted. Remaining: {count}')

if count == 0:
    print('SUCCESS: All CRUD operations work')
    sys.exit(0)
else:
    print('ERROR: CRUD operations failed')
    sys.exit(1)
"