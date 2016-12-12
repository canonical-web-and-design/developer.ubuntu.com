# Core modules
import fnmatch
import os
from copy import deepcopy

# Third party modules
from django.conf import settings

# Local modules
from webapp.lib.markdown import get_page_data


class Sitemap:
    def __init__(self):
        self.sitemap = {}

    def _get_template_path(self):
        template_path = getattr(settings, 'TEMPLATE_PATH')
        pages_path = getattr(settings, 'TEMPLATE_FINDER_PATH')
        if pages_path and not pages_path.startswith('/'):
            template_path = os.path.join(template_path, pages_path)
        return template_path

    def _build_metadata(self, path):
        if path.endswith('/'):
            path = path[:-1]
        metadata = get_page_data([path])[0]
        return {
            'title': metadata.get('title'),
            'description': metadata.get('description'),
            'path': metadata.get('path'),
        }

    def _parse_markdown_files(self, root_path=None):
        default_node = {'children': {}}
        nodes = {}

        path = self._get_template_path()
        walk_path = path
        if root_path:
            walk_path = os.path.join(path, root_path)

        for root, dirnames, filenames in os.walk(walk_path):
            relative_path = os.path.relpath(root, path)
            if relative_path == '.':
                relative_path = ''

            for filename in fnmatch.filter(filenames, '*.md'):
                if not filename:
                    continue

                is_index = False
                if filename == 'index.md':
                    is_index = True

                file_path = os.path.join(relative_path, filename)
                if file_path.endswith('.md'):
                    file_path = file_path[:-3]

                metadata = self._build_metadata(file_path)

                # Nest path parts as a dictionary.
                # As it loops, we update the current_node reference to the
                # next level of dictionary.
                path_parts = file_path.split('/')
                current_node = nodes
                for part in path_parts[:-1]:
                    # Split up levels by using a 'children' key.
                    if current_node is not nodes:
                        current_node = current_node['children']
                    # Creates a node if it does not exist
                    current_node = current_node.setdefault(
                        part, deepcopy(default_node)
                    )

                if is_index:
                    current_node.update(metadata)
                    continue

                current_node = current_node['children']
                if current_node.get(path_parts[-1]):
                    current_node[path_parts[-1]].update(metadata)
                else:
                    current_node[path_parts[-1]] = metadata

        return nodes

    def _generate_sitemap(self, root_path):
        """
        Generate a sitemap, starting from an optional given root_path.
        This will return the whole sitemap upon completion.
        """
        markdown_files = self._parse_markdown_files(root_path)

        tree = markdown_files
        print tree
        if root_path:
            self.sitemap[root_path] = tree['core']

        return self.sitemap

    def get(self, root_path=None):
        if root_path:
            full_map = self._generate_sitemap(root_path)
            return full_map[root_path]
        return self._generate_sitemap()


sitemap = Sitemap()
