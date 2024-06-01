# admin.py
from django.contrib import admin
from .models import Contact, Message

class MessageInline(admin.TabularInline):
    model = Message
    extra = 1
    readonly_fields = ('created_at',)
    fields = ('user', 'text', 'created_at')

class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'listing', 'contact_date')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'email', 'listing')
    list_per_page = 25
    inlines = [MessageInline]

# Make sure to register the Contact model only once
admin.site.register(Contact, ContactAdmin)
admin.site.register(Message)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'contact', 'user', 'text', 'created_at')
    list_display_links = ('id',)
    list_filter = ('contact',)
    search_fields = ('text', 'contact__listing')

   