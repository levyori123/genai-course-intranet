from django.contrib import admin

from .models import Announcement, CourseInfo, Lecture


@admin.register(CourseInfo)
class CourseInfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not CourseInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "published_at", "pinned", "is_published")
    list_filter = ("pinned", "is_published")
    search_fields = ("title", "body")


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ("number", "title", "date")
    search_fields = ("title",)
