from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import BookForm

# Ensure all views use @permission_required for access control

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    List all books. Controlled by 'can_view' permission.
    """
    books = Book.objects.all()
    # Safe rendering of data
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    """
    Create a new book. Controlled by 'can_create' permission.
    Uses proper form validation to prevent XSS and SQL injection.
    """
    if request.method == 'POST':
        form = BookForm(request.POST) # Django forms sanitize input
        if form.is_valid():
            form.save() # Uses ORM which is safe against SQL injection
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    """
    Edit a book. Controlled by 'can_edit' permission.
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/form_example.html', {'form': form})

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    """
    Delete a book. Controlled by 'can_delete' permission.
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

