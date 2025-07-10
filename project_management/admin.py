from django.contrib import admin
from django.utils.html import format_html
from .models import ProjectManagement
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import SimpleListFilter
from datetime import datetime

@admin.register(ProjectManagement)
class ProjectManagementAdmin(admin.ModelAdmin):
    list_display = ['project_id', 'project_name', 'image_preview', 'description_preview', 'modified_date', 'status', 'action_buttons']
    search_fields = ['project_name', 'description']
    readonly_fields = ['modified_date']
    change_list_template = "admin/project_management/project_management_change_list.html"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        # Handle status filter
        status = request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # Handle modified date filter
        modified_date = request.GET.get('modified_date')
        if modified_date:
            try:
                date = datetime.strptime(modified_date, '%Y-%m-%d')
                queryset = queryset.filter(modified_date__date=date)
            except ValueError:
                pass

        return queryset

    def image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;" />', obj.featured_image.url)
        return _("No Image")
    image_preview.short_description = _('Image')

    def description_preview(self, obj):
        from django.utils.html import strip_tags
        clean_description = strip_tags(obj.description)
        return clean_description[:100] + '...' if len(clean_description) > 100 else clean_description
    description_preview.short_description = _('Description')

    def action_buttons(self, obj):
        return format_html(
            '<a class="button" href="{}" style="margin-right: 5px;">{}</a>'
            '<a class="button" href="{}" style="color: red;">{}</a>',
            f'/admin/project_management/projectmanagement/{obj.pk}/change/',
            _('Edit'),
            f'/admin/project_management/projectmanagement/{obj.pk}/delete/',
            _('Delete')
        )
    action_buttons.short_description = _('Actions')

    class Media:
        css = {
            'all': (
                'https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap',
                )
        }

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['project_name'].widget.attrs.update({
            'dir': 'auto',
            'class': 'bilingual-field'
        })
        form.base_fields['description'].widget.attrs.update({
            'dir': 'auto',
            'class': 'bilingual-field'
        })
        return form