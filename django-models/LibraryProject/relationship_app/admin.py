from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Author, Book, Library, Librarian, UserProfile

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

# Inline for UserProfile in User admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

# Extend User admin
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff')
    
    def get_role(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.role
        return "No role"
    get_role.short_description = 'Role'
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)