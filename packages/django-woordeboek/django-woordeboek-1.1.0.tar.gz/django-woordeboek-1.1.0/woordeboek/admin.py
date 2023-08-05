from pprint import pformat

from django.contrib import admin
from django.core.cache import cache
from django.utils.html import format_html

from .models import Credentials, Query, QueryResult
from .utils import VIVA_COOKIES_CACHE_KEY


class CredentialsAdmin(admin.ModelAdmin):
    readonly_fields = ['session_cookies']
    list_display = [
        'username',
        'password',
        'active'
    ]

    def session_cookies(self, obj):
        return format_html('<pre>{}</pre>', pformat(cache.get(VIVA_COOKIES_CACHE_KEY)))


class QueryAdmin(admin.ModelAdmin):
    search_fields = [
        'query',
    ]

    list_display = [
        'query',
        'response_time',
        'num_results',
        'cached',
    ]

    list_filter = [
        'cached',
    ]


class QueryResultAdmin(admin.ModelAdmin):

    search_fields = [
        'query',
    ]

    list_display = [
        'query',
        'time_created',
        'data_length',
    ]

    exclude = ['data']

    readonly_fields = [
        'data_formatted',
    ]

    def data_formatted(self, obj):
        return format_html('<pre>{}</pre>', pformat(obj.data))

    def data_length(self, obj):
        return len(obj.data)

admin.site.register(Credentials, CredentialsAdmin)
admin.site.register(Query, QueryAdmin)
admin.site.register(QueryResult, QueryResultAdmin)
