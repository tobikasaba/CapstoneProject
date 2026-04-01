# Import Django's admin framework utilities.
from django.contrib import admin
# Import the application models that will be exposed in the admin site.
from .models import Concert, ConcertAttending, Photo, Song


# Full access for Concert management
# Register the Concert model with the default admin configuration.
admin.site.register(Concert)


# Read-only access for debugging attendance
# Register a custom admin configuration for the ConcertAttending model.
@admin.register(ConcertAttending)
# Define how ConcertAttending objects should appear in the admin site.
class ConcertAttendingAdmin(admin.ModelAdmin):
    # Show these fields in the admin list view for attendance records.
    list_display = ['concert', 'user', 'attending']
    # Add a sidebar filter so admins can filter by attending status.
    list_filter = ['attending']
    # Enable admin search by the related user's username.
    search_fields = ['user__username']

    # Block manual creation of attendance records from the admin UI.
    def has_add_permission(self, request):
        # Return False so new attendance records can only be created in the frontend.
        return False

    # Block editing of existing attendance records from the admin UI.
    def has_change_permission(self, request, obj=None):
        # Return False to prevent admins from changing attendance state directly.
        return False

    # Allow deletion checks for attendance records in the admin UI.
    def has_delete_permission(self, request, obj=None):
        # Only allow deletion when the logged-in user is a superuser.
        return request.user.is_superuser  # Only superusers can delete


# Read-only for external microservice data (optional but useful)
# Register a custom admin configuration for the Photo model.
@admin.register(Photo)
# Define a read-only admin view for Photo records.
class PhotoAdmin(admin.ModelAdmin):
    # Show the photo ID, event city, and event date in the admin list view.
    list_display = ['id', 'event_city', 'event_date']

    # Disallow creating Photo records from the admin UI.
    def has_add_permission(self, request):
        # Return False because this data should not be added manually here.
        return False

    # Disallow editing Photo records from the admin UI.
    def has_change_permission(self, request, obj=None):
        # Return False to keep externally sourced data read-only.
        return False

    # Disallow deleting Photo records from the admin UI.
    def has_delete_permission(self, request, obj=None):
        # Return False so Photo records remain untouched in admin.
        return False


# Register a custom admin configuration for the Song model.
@admin.register(Song)
# Define a read-only admin view for Song records.
class SongAdmin(admin.ModelAdmin):
    # Show the song ID and title in the admin list view.
    list_display = ['id', 'title']

    # Disallow creating Song records from the admin UI.
    def has_add_permission(self, request):
        # Return False because songs are not meant to be added manually in admin.
        return False

    # Disallow editing Song records from the admin UI.
    def has_change_permission(self, request, obj=None):
        # Return False to keep Song data read-only in admin.
        return False

    # Disallow deleting Song records from the admin UI.
    def has_delete_permission(self, request, obj=None):
        # Return False so Song records cannot be removed in admin.
        return False
