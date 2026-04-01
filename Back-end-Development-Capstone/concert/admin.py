from django.contrib import admin
from .models import Concert, ConcertAttending, Photo, Song


admin.site.register(Concert)


@admin.register(ConcertAttending)
class ConcertAttendingAdmin(admin.ModelAdmin):
    list_display = ['concert', 'user', 'attending']
    list_filter = ['attending']
    search_fields = ['user__username']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'event_city', 'event_date']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
