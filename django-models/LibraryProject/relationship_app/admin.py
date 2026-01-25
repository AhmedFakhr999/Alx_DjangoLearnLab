from django.contrib import admin
from .models import Author, Book, Library, Librarian

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    list_filter = ('author',)
    search_fields = ('title', 'author__name')

class BookInline(admin.TabularInline):
    model = Library.books.through
    extra = 1

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_librarian', 'get_book_count')
    inlines = [BookInline]
    exclude = ('books',)  # Exclude the many-to-many field from the main form
    
    def get_librarian(self, obj):
        if hasattr(obj, 'librarian'):
            return obj.librarian.name
        return "No librarian"
    get_librarian.short_description = 'Librarian'
    
    def get_book_count(self, obj):
        return obj.books.count()
    get_book_count.short_description = 'Number of Books'

@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('name', 'library')
    list_filter = ('library',)