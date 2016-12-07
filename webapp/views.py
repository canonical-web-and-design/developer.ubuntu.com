from django.conf import settings
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404
from django.template import (
    Context,
    loader,
    RequestContext,
    TemplateDoesNotExist,
)
from django.views.generic import TemplateView

from webapp.lib.markdown import parse_frontmatter


def custom_404(request):
    t = loader.get_template('error/404.html')
    context = RequestContext(request, {'request_path': request.path})
    return HttpResponseNotFound(t.render(context))


def custom_500(request):
    t = loader.get_template('error/500.html')
    return HttpResponseServerError(t.render(Context({})))


class MarkdownView(TemplateView):
    def __init__(self, *args, **kwargs):
        self.metadata = []
        self.page_type_template = None
        return super(MarkdownView, self).__init__(*args, **kwargs)

    def get_template_names(self):
        return self.page_type_template or self._get_base_template_name()

    def _get_base_template_name(self):
        return self.template_name or self.kwargs['template_name']

    def _find_template(self, path):
        template_root = getattr(settings, 'TEMPLATE_FINDER_PATH', None)
        if template_root:
            path = ''.join([template_root, '/', path])

        template_paths = [
            ''.join([path, '.md']),
        ]
        try:
            template = loader.select_template(template_paths)
            template_path = template.origin.name
        except TemplateDoesNotExist:
            raise Http404("Can't find page for: %s" % path)

        return template, template_path if template else None

    def _get_page_type_template(self, page_type):
        return 'includes/markdown_page_types/{0}.html'.format(page_type)

    def get_context_data(self, **kwargs):
        request_path = self.kwargs['path']
        template, template_path = self._find_template(request_path)
        with open(template_path, 'r') as f:
            metadata = parse_frontmatter(f.read())

        self.template_name = metadata.get('template')
        page_type = metadata.get('page_type')
        if page_type:
            self.page_type_template = self._get_page_type_template(page_type)

        context = super(MarkdownView, self).get_context_data(**kwargs)
        # We want to preserve context keys. So do it backwards and flip around
        metadata.update(context)
        context = metadata
        # More specific overrides and defaults.
        context['base_template'] = self._get_base_template_name()
        context['markdown_path'] = template_path
        context['page_type'] = page_type
        context['title'] = metadata.get('title', '')
        return context
