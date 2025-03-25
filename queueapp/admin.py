from django.contrib import admin
from .models import Business, Queue, QueueParticipant

# Inline admin for Queue inside Business
class QueueInline(admin.TabularInline):  
    model = Queue
    extra = 1  

# Inline admin for Participants inside Queue
class QueueParticipantInline(admin.TabularInline):  
    model = QueueParticipant
    extra = 1  

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', )
    search_fields = ('name', 'owner')
    inlines = [QueueInline]  

@admin.register(Queue)
class QueueAdmin(admin.ModelAdmin):
    list_display = ('name', 'business', )
    search_fields = ('name', 'business__name')
    list_filter = ('business',)
    inlines = [QueueParticipantInline]  

@admin.register(QueueParticipant)
class QueueParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'queue', 'get_business', 'position', )
    search_fields = ('name', 'email', 'queue__name', 'queue__business__name')
    list_filter = ('queue', 'queue__business')

    def get_business(self, obj):
        return obj.queue.business.name  # Show business name in participant list

    get_business.short_description = "Business"  # Column Name in Admin Panel
