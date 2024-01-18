from django.contrib import admin
from django.utils.html import escape, mark_safe
from sqs.components.gisquery.models import Layer, LayerRequestLog, Task

@admin.register(Layer)
class LayerAdmin(admin.ModelAdmin):
    list_display = ["name", "url", "layer_version", "active"] #, 'link_to_geojson']
    list_filter = ["active"]
    search_fields = ['name__icontains']
    #readonly_fields = ('geojson',)
    exclude = ['geojson']

    def layer_version(self, obj):
        if obj.name:
            return mark_safe(f'<a href="/api/v1/layers/{obj.name}/geojson.json/" target="_blank">{obj.version}</a>' )
        return obj.version
    layer_version.allow_tags=True

#    def link_to_geojson(self, obj):
#        if obj.name:
#            return mark_safe(f'<a href="/api/v1/layers/{obj.name}/geojson.json/" target="_blank">{obj.name}</a>' )
#        return None
#    link_to_geojson.allow_tags=True

#    def get_fields(self, request, obj=None):
#        fields = super(LayerAdmin, self).get_fields(request, obj)
#        fields_list = list(fields)
#        if obj:
#            fields_list.remove('geojson')
#        fields_tuple = tuple(fields_list)
#        return fields_tuple

@admin.register(LayerRequestLog)
class LayerRequestLogAdmin(admin.ModelAdmin):
    list_display = ["id", "system", "app_id", "when"]
    list_filter = ["system"]
    search_fields = ['system', 'app_id', 'when']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['description', 'script', 'task_status', 'priority', 'position', 'link_to_request_log_api']
    list_filter = ["status", "priority"]
    search_fields = ['description', 'script', 'status', 'priority']
    readonly_fields = ('start_time', 'end_time', 'time_taken', 'stdout', 'stderr', 'description', 'parameters', 'created_date') #, 'data')
    exclude = ['data', 'request_log']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter().order_by('-created')

    def time_taken(self, obj):
        return obj.time_taken()

    def position(self, obj):
        return obj.position

#    def link_to_request_log_admin(self, obj):
#        if obj.request_log:
#            return mark_safe(f'<a href="/admin/sqs/layerrequestlog/{obj.request_log.id}/change/" target="_blank">Admin {obj.request_log.id}</a>' )
#        return None
#    link_to_request_log_admin.allow_tags=True

    def link_to_request_log_api(self, obj):
        if obj.request_log:
            return mark_safe(f'<a href="/api/v1/logs/{obj.request_log.id}/request_log/" target="_blank">API {obj.request_log.id}</a>' )
        return None
    link_to_request_log_api.allow_tags=True

    def task_status(self, obj):
        if obj.request_log:
            return mark_safe(f'<a href="/admin/sqs/layerrequestlog/{obj.request_log.id}/change/" target="_blank">{obj.status}</a>' )
        return obj.status
    task_status.allow_tags=True


