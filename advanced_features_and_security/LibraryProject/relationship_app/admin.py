from django.contrib import admin
from .models import Author, Book, Library, Librarian, UserProfile  # Remove CustomUser from here
from django.contrib.auth import get_user_model

# Get the user model (which now points to bookshelf.CustomUser)
User = get_user_model()

# Register your models here
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
    exclude = ('books',)
    
    def get_librarian(self, obj):
        if hasattr(obj, 'librarian'):
            return obj.librarian.user.get_full_name()
        return "No librarian"
    get_librarian.short_description = 'Librarian'
    
    def get_book_count(self, obj):
        return obj.books.count()
    get_book_count.short_description = 'Number of Books'


@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('get_user_name', 'library')
    list_filter = ('library',)
    
    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_user_name.short_description = 'Librarian Name'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('get_user_email', 'role')
    list_filter = ('role',)
    
    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'Email'