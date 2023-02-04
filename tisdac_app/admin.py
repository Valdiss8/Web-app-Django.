from django.contrib import admin, messages
from .models import About, Events, Department, Service, Visitor, News, Feedback, Resource
from datetime import date, datetime
# Register your models here.


@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    exclude = ['slug']
    list_display = ['date', 'title', 'department', 'summary', 'status']
    ordering = ['date']
    list_per_page = 20
    search_fields = ['title', 'description']
    list_filter = ['department']
    filter_horizontal = ['visitors']

    @admin.display(ordering='date', description='Status')
    def status(self, ev: Events):
        now = datetime.now()
        if ev.date:
            if ev.date.timestamp() < now.timestamp():
                return 'Completed'
            elif ev.date.timestamp() > now.timestamp():
                return 'Upcoming'
        else:
            return 'Wrong dates'

    #@admin.action(description='Set Group Visibility')
    #def set

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    exclude = ['slug']
    list_display = ['date', 'title', 'department', 'summary', 'publish']
    ordering = ['date']
    list_per_page = 20
    search_fields = ['title', 'description']
    list_filter = ['department']
    filter_horizontal = ['visitors']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    exclude = ['slug']
    list_display = ['name', 'summary', 'status']
    ordering = ['name']
    list_per_page = 20
    list_editable = ['status']

@admin.register(Service)
class DepartmentAdmin(admin.ModelAdmin):
    exclude = ['slug']
    list_display = ['name', 'summary', 'status']
    ordering = ['name']
    list_per_page = 20
    list_editable = ['status']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'date', 'feedback']
    ordering = ['date']
    list_per_page = 20


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'get_events']
    ordering = ['email']
    search_fields = ['name', 'email', 'phone']

    def get_events(self, visitor):
        return Events.objects.filter(visitors=visitor).order_by('date')


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['title', 'article']
    #list_editable = ['article']
#admin.site.register(About, AboutAdmin)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'summary', 'webpage']


