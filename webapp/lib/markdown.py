import frontmatter
from django.conf import settings
from django.template import loader
from django.template import TemplateDoesNotExist


def parse_frontmatter(markdown_content):
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


def get_page_data(pages, root_path=None):
    template_root = ''.join([
        getattr(settings, 'TEMPLATE_FINDER_PATH', ''), '/'
    ])

    page_data = []
    for path in pages:
        # If trying to lookup relative path
        if root_path and not path.startswith('/'):
            path = '/'.join([root_path, path])
        # We don't need any slashes at the ends
        path.strip('/')

        try:
            template_path = ''.join([template_root, path, '.md'])
            template = loader.get_template(template_path)
        except TemplateDoesNotExist:
            template_path = ''.join([template_root, path, '/index.md'])
            template = loader.get_template(template_path)

        with open(template.origin.name, 'r') as f:
            metadata = parse_frontmatter(f.read())
            metadata['path'] = path
            page_data.append(metadata)

    return page_data
