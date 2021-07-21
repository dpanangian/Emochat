from django.contrib.admin import ModelAdmin, site
from core.models import MessageModel, Visibility
import csv
from django.http import HttpResponse

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export selected messages as CSV"

class MessageModelAdmin(ModelAdmin, ExportCsvMixin):
    readonly_fields = ('timestamp',)
    search_fields = ('id', 'body', 'user__username', 'recipient__username')
    list_display = ('id', 'user', 'recipient', 'timestamp', 'characters')
    list_display_links = ('id',)
    list_filter = ('user', 'recipient')
    date_hierarchy = 'timestamp'
    actions = ["export_as_csv"]


site.register(MessageModel, MessageModelAdmin)


class GroupAdmin(ModelAdmin, ExportCsvMixin):
      list_display    = ['group']

site.register(Visibility, GroupAdmin)
