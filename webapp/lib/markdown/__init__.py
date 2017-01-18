from __future__ import absolute_import

import frontmatter
import markdown as _markdown

from django.conf import settings
from django.template import loader
from yaml.scanner import ScannerError
from yaml.parser import ParserError

from .extensions.vanilla_toc import VanillaTocExtension


markdown_extensions = [
    'markdown.extensions.attr_list',
    'markdown.extensions.def_list',
    'markdown.extensions.fenced_code',
    'markdown.extensions.meta',
    'markdown.extensions.tables',
    'mdx_callouts',
    'mdx_anchors_away',
    'mdx_foldouts',
    VanillaTocExtension(marker=''),
]


def parse_frontmatter(markdown_content):
    metadata = {}

    try:
        file_parts = frontmatter.loads(markdown_content)
        metadata = file_parts.metadata
        markdown_content = file_parts.content
    except (ScannerError, ParserError):
        """
        If there's a parsererror, it's because frontmatter had to parse
        the entire file (not finding frontmatter at the top)
        and encountered an unexpected format somewhere in it.
        This means the file has no frontmatter, so we can simply continue.
        """
        pass

    return markdown_content, metadata


def parse_markdown(markdown_content):
    markdown_content, metadata = parse_frontmatter(markdown_content)
    markdown_parser = _markdown.Markdown(extensions=markdown_extensions)
    parsed_markdown = markdown_parser.convert(markdown_content)
    metadata['table_of_contents_items'] = markdown_parser.toc_items

    return parsed_markdown, metadata


def get_page_data(pages, root_path=None):
    template_root = ''.join([
        getattr(settings, 'TEMPLATE_FINDER_PATH', ''), '/'
    ])

    page_data = []
    for path in pages:
        # If trying to lookup relative path
        if root_path and not path.startswith('/'):
            root_path = root_path.strip('/')
            path = '/'.join([root_path, path])
        # We don't need any slashes at the ends
        path = path.strip('/')
        if path.endswith('/index'):
            path = path[:-6]

        template_paths = [
            ''.join([template_root, path, '.md']),
        ]
        template = loader.select_template(template_paths)

        with open(template.origin.name, 'r') as f:
            markdown_content, metadata = parse_frontmatter(f.read())
            metadata['path'] = '/' + path
            page_data.append(metadata)

    return page_data
