from django.http.response import JsonResponse
from django.views import generic

from .query import query, validate_query
from .models import Query, QueryResult
from time import time
import json


class QueryView:
    source = 'web'

    def get_query_response(self, q):
        q = q.strip()
        cached_results = QueryResult.objects.filter(query=q).first()
        include_raw = self.request.GET.get('raw')
        start = time()

        if cached_results:
            results = json.loads(cached_results.data)
            cached = True
        else:
            cached = False
            results = query(q, include_raw=include_raw)
            if len(results) > 0:
                # only cache when a result is found
                # as any error will cause an empty list to be returned
                QueryResult.objects.create(query=q, data=json.dumps(results))

        response_time = round(time() - start, 3)
        num_results = len(results)

        country = self.request.META.get('HTTP_CF_IPCOUNTRY', 'XX')
        Query.objects.create(
            query=q,
            num_results=num_results,
            response_time=response_time,
            country=country,
            cached=cached,
            source=self.source,
        )
        return results


class IndexView(QueryView, generic.TemplateView):
    template_name = 'woordeboek/index.html'
    source = 'web'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q is None:
            return context
        valid, message = validate_query(q)
        context['q'] = q
        context['message'] = message
        if valid:
            context['results'] = self.get_query_response(q)
        return context


class APIView(QueryView, generic.View):
    source = 'api'

    def get(self, request):
        q = request.GET.get('q', '')
        valid, message = validate_query(q)
        if not valid:
            return JsonResponse({
                'success': False,
                'message': message
            })
        return JsonResponse({
            'success': True,
            'results': self.get_query_response(q),
        })


class StatsView(generic.TemplateView):
    template_name = 'woordeboek/stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['queries'] = Query.objects.all().order_by('-time_created')[:100]
        return context
