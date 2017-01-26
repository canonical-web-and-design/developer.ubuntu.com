# Third party modules
from django.conf import settings
from django.http import (
    Http404,
    HttpResponse,
    HttpResponseNotFound,
    HttpResponseServerError,
)
from django.template import (
    Context,
    loader,
    RequestContext,
    Template,
    TemplateDoesNotExist,
)
from django.template.engine import Engine
from django.views.generic import TemplateView

# Local modules
from webapp.lib.markdown import parse_markdown
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
        context['page_template'] = self.get_template_names()
        context['markdown'] = markdown
        context['page_type'] = metadata.get('page_type')
        context['table_of_contents_title'] = metadata.get(
            'table_of_contents_title',
            'In this page'
        )
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

        markdown_template = Template(markdown.join((
            "{% extends page_template %} \n{% block markdown %}",
            "\n{% endblock %}",
        )))
        return HttpResponse(
            markdown_template.render(RequestContext(request, context)),
            content_type='text/html',
        )
