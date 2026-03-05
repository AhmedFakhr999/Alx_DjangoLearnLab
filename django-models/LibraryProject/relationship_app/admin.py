from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Author, Book, Library, Librarian, UserProfile

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    """Admin interface for the CustomUser model"""
    
    # Fields to display in list view
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    # Fieldsets for detail view
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'date_of_birth', 'profile_photo', 'bio', 'phone_number')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important Dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fieldsets for add form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'date_of_birth', 'profile_photo'),
        }),
    )
    
    # Readonly fields
    readonly_fields = ('last_login', 'date_joined')
    
    # Custom actions
    actions = ['activate_users', 'deactivate_users']
    
    def activate_users(self, request, queryset):
        """Activate selected users"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} users activated.')
    activate_users.short_description = "Activate selected users"
    
    def deactivate_users(self, request, queryset):
        """Deactivate selected users"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} users deactivated.')
    deactivate_users.short_description = "Deactivate selected users"

# Register CustomUser with custom admin
admin.site.register(CustomUser, CustomUserAdmin)

# Inline for UserProfile in CustomUser admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'
    fk_name = 'user'

# Extended CustomUserAdmin with UserProfile inline
class ExtendedCustomUserAdmin(CustomUserAdmin):
    inlines = (UserProfileInline,)
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

# Re-register with extended admin
admin.site.unregister(CustomUser)
admin.site.register(CustomUser, ExtendedCustomUserAdmin)

# Register other models
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
        return obj.user.get_full_name()
    get_user_name.short_description = 'Librarian Name'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'get_user_email')
    list_filter = ('role',)
    search_fields = ('user__email', 'user__username')
    
    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'Email'