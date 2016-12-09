# Core modules
import json
import os
try:
    from urllib.error import URLError
except ImportError:
    from urllib2 import URLError

# Third party modules
from django.conf import settings
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404
from django.template import (
    Context,
    loader,
    RequestContext,
    TemplateDoesNotExist,
)
from django.template.engine import Engine
from django.views.generic import TemplateView

# Local modules
from webapp.lib.markdown import parse_markdown
from webapp.lib.gsa import GSAParser
from webapp.loaders import MarkdownLoader


def custom_404(request):
    t = loader.get_template('error/404.html')
    context = RequestContext(request, {'request_path': request.path})
    return HttpResponseNotFound(t.render(context))


def custom_500(request):
    t = loader.get_template('error/500.html')
    return HttpResponseServerError(t.render(Context({})))


class MarkdownView(TemplateView):
    def __init__(self, *args, **kwargs):
        self.page_type_template = None
        self.markdown_loader = self._find_markdown_loader()
        return super(MarkdownView, self).__init__(*args, **kwargs)

    def get_template_names(self):
        return self.page_type_template or self._get_base_template_name()

    def _get_base_template_name(self):
        return self.template_name or self.kwargs['template_name']

    def _find_markdown_loader(self):
        loaders = Engine.get_default().template_loaders
        for loader_instance in loaders:
            if isinstance(loader_instance, MarkdownLoader):
                return loader_instance
        raise Exception("Could not find MarkdownLoader")

    def _find_template_source(self, path):
        template_root = getattr(settings, 'TEMPLATE_FINDER_PATH', None)
        if template_root:
            path = ''.join([template_root, '/', path])

        template_path = ''.join([path, '.md'])
        try:
            markdown_loader = self.markdown_loader
            markdown, template_path = markdown_loader.load_template_source(
                template_path
            )
        except TemplateDoesNotExist:
            raise Http404("Can't find page for: %s" % path)

        return markdown, template_path

    def _get_page_type_template(self, page_type):
        return 'includes/markdown_page_types/{0}.html'.format(page_type)

    def _parse_markdown(self, path):
        markdown, template_path = self._find_template_source(path)
        parsed_markdown, metadata = parse_markdown(markdown)

        self.template_name = metadata.get('template')
        page_type = metadata.get('page_type')
        if page_type:
            self.page_type_template = self._get_page_type_template(page_type)

        return parsed_markdown, metadata

    def get_context_data(self, markdown, metadata, **kwargs):
        context = super(MarkdownView, self).get_context_data(**kwargs)
        # We want to preserve context keys. So do it backwards and flip around
        metadata.update(context)
        context = metadata
        # More specific overrides and defaults.
        context['base_template'] = self._get_base_template_name()
        context['markdown'] = markdown
        context['page_type'] = metadata.get('page_type')
        context['title'] = metadata.get('title', '')
        return context

    def get(self, request, *args, **kwargs):
        request_path = self.kwargs['path']
        markdown, metadata = self._parse_markdown(request_path)

        context = self.get_context_data(
            markdown=markdown,
            metadata=metadata,
            **kwargs
        )
        return self.render_to_response(context)


class SearchView(TemplateView):
    '''
    Return search results from the Google Search Appliance

    Requests should be formatted: <url>?q=<string>&offset=<num>&limit=<num>

    I've used "offset" and "limit" for pagination,
    following the "Web API Design" standard:
    https://pages.apigee.com/web-api-design-ebook.html

    This gets results from Canonical's Google Search Appliance,
    currently located at: butlerov.internal (10.22.112.8)
    '''

    template_name = "pages/search.html"

    def get_context_data(self, **kwargs):
        """
        Extend CMSPageView.get_context_data to parse query parameters
        and return search results from the Google Search Appliance (GSA)

        E.g.: http://example.com/search?q=juju&limit=10&offset=10

        Query parameters:
        - q: the search query to be passed to the GSA
        - limit: number of results to return, "page size" (default: 10)
        - offset: where to start results at (default: 0)
        """

        # On live the GSA domain will be butlerov.internal
        # but on dev, we need to access GSA through localhost
        # (see GSASearchView docstring above)
        gsa_domain = 'butlerov.internal'

        parser = GSAParser(gsa_domain)

        # Import context from parent
        context = super(SearchView, self).get_context_data(**kwargs)

        # defaults + GET params
        context.update({
            'query': self.request.GET.get('q', ''),
            'results': [],
            'request_succeeded': True,
            'parse_succeeded': True,
            'start': 0,
            'end': 0,
            'limit': int(self.request.GET.get('limit', '10')),
            'offset': int(self.request.GET.get('offset', '0')),
            'total': 0,
            'nav_items': []
        })

        # return self.context
        try:
            if getattr(settings, 'DEBUG', False):
                # Use a local file
                example_filepath = os.path.join(
                    os.path.dirname(__file__),
                    'search.example'
                )

                with open(example_filepath) as example_file:
                    gsa_results = json.load(example_file)
            else:
                gsa_results = parser.fixed_results(
                    context['query'],
                    start=context['offset'],
                    num=context['limit']
                )

            nav_url = "{path}?q={query}".format(
                path=self.request.path,
                query=context['query']
            )

            results = self.parse_gsa_results(gsa_results)
            context.update(results)

            context['nav_items'] = self.build_nav_items(
                context,
                nav_url
            )

        except URLError:
            context['request_succeeded'] = False
        except ValueError:
            context['parse_succeeded'] = False

        return context

    def parse_gsa_results(self, gsa_results):

        results_meta = gsa_results['results_nav']

        data = {}

        # Parse data
        if 'results' in gsa_results:
            data['results'] = gsa_results['results']

        if results_meta['total_results'].isdigit():
            data['total'] = int(results_meta['total_results'])

        if results_meta['results_start'].isdigit():
            data['start'] = int(results_meta['results_start'])

        if results_meta['results_end'].isdigit():
            data['end'] = int(results_meta['results_end'])

        data['have_next'] = bool(results_meta.get('have_next', '0'))

        return data

    def build_nav_items(self, data, url):
        """
        Create an array of navigational items
        from results data
        """

        items = []

        first_offset = 0
        offset = data['start'] - 1
        previous_offset = offset - data['limit']
        next_offset = data['end']

        remainder = data['total'] % data['limit']

        if remainder == 0:
            last_offset = data['total'] - data['limit']
        else:
            last_offset = data['total'] - remainder

        base_item = {
            "url": url + '&limit=' + str(data['limit'])
        }

        if first_offset < offset:
            first = self.build_item(base_item, 'First', first_offset, 'back')
            first['class'] = 'item-extreme'
            items.append(first)

        if previous_offset > first_offset and previous_offset < offset:
            items.append(self.build_item(
                base_item,
                'Previous',
                previous_offset,
                'back'
            ))

        if data['have_next'] and next_offset < last_offset:
            items.append(self.build_item(
                base_item,
                'Next',
                next_offset,
                'forward'
            ))

        if data['have_next'] and offset < last_offset:
            last = self.build_item(base_item, 'Last', last_offset, 'forward')
            last['class'] = 'item-extreme'
            items.append(last)

        return items

    def build_item(self, base_item, name, offset, direction):
        """
        Build one navigational item
        """

        item = base_item.copy()
        item['name'] = name
        item['url'] = item['url'] + '&offset=' + str(offset)
        item['direction'] = direction

        return item
