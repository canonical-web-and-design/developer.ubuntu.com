import frontmatter
from django.conf import settings
from django.http import HttpResponseNotFound, HttpResponseServerError, Http404
from django.template import (
    Context,
    loader,
    RequestContext,
    TemplateDoesNotExist,
)
from django.views.generic import TemplateView


def custom_404(request):
    t = loader.get_template('error/404.html')
    context = RequestContext(request, {'request_path': request.path})
    return HttpResponseNotFound(t.render(context))


def custom_500(request):
    t = loader.get_template('error/500.html')
    return HttpResponseServerError(t.render(Context({})))


class MarkdownView(TemplateView):
    template_name = 'includes/base_markdown.html'

    def _parse_frontmatter(self, markdown_content):
        metadata = {}
        try:
            file_parts = frontmatter.loads(markdown_content)
            metadata = file_parts.metadata
        except (ScannerError, ParserError):
            """
            If there's a parsererror, it's because frontmatter had to parse
            the entire file (not finding frontmatter at the top)
            and encountered an unexpected format somewhere in it.
            This means the file has no frontmatter, so we can simply continue.
            """
            pass
        return metadata

    def _find_template(self, path):
        template_root = getattr(settings, 'TEMPLATE_FINDER_PATH', None)
        if template_root:
            path = ''.join([template_root, '/', path])

        template = None
        template_path = None
        try:
            template_path = ''.join([path, '.md'])
            template = loader.get_template(template_path)
        except TemplateDoesNotExist:
            pass
        if not template:
            try:
                template_path = ''.join([path, '/index.md'])
                template = loader.get_template(template_path)
            except TemplateDoesNotExist:
                pass
        if not template:
            raise Http404("Can't find page for: %s" % path)

        return template, template_path if template else None

    def get_context_data(self, **kwargs):
        path = self.kwargs['path']
        template, template_path = self._find_template(path)
        with open(template.origin.name, 'r') as f:
            metadata = self._parse_frontmatter(f.read())

        context = super(MarkdownView, self).get_context_data(**kwargs)
        context['title'] = metadata.get('title', '')
        context['markdown_path'] = template_path
        return context
