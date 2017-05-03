# Core modules
import fnmatch
import os
from copy import deepcopy

# Third party modules
import yaml
from django.conf import settings

# Local modules
from webapp.lib.markdown import get_page_data


DEFAULT_NAVIGATION_OPTIONS = {
    'nesting_limit': 3,
}


class Sitemap:
    def __init__(self):
        self.sitemap = {}

    def _get_template_path(self):
        template_path = getattr(settings, 'TEMPLATE_PATH')
        pages_path = getattr(settings, 'TEMPLATE_FINDER_PATH')
        if pages_path and not pages_path.startswith('/'):
            template_path = os.path.join(template_path, pages_path)
        return template_path

    def _split_path(self, path):
        path = path.strip('/')
        parts = path.split('/')
        return parts

    def _split_path_full(self, path):
        """
        This will take a path such as /1/2/3 and create:
        [
            '/1',
            '/1/2',
            '/1/2/3',
        ]
        """
        path_list = []
        path = path.strip('/')
        parts = path.split('/')
        current = ''
        for part in parts:
            current = '{current}/{new}'.format(current=current, new=part)
            path_list.append(current)
        return path_list

    def _find_navigation_item(self, nav_items, path):
        if not path:
            return
        if not isinstance(path, list):
            path = self._split_path_full(path)

        found = None
        for item in nav_items:
            if not path:
                break
            if 'path' in item and item['path'] == path[0]:
                path.pop(0)
                if not path:
                    found = item
                elif 'children' in item:
                    found = self._find_navigation_item(item['children'], path)
            elif 'path' not in item and 'children' in item:
                found = self._find_navigation_item(item['children'], path)
        return found

    def _set_active_navigation_items(self, nav_items, path):
        if not path:
            return
        if not isinstance(path, list):
            path = self._split_path_full(path)

        last_path = path[-1]
        current_path = path.pop(0)

        item = self._find_navigation_item(nav_items, [current_path])
        if item:
            if last_path == item['path']:
                item['active'] = True
                item['class'] = 'active'
            else:
                item['active_parent'] = True
                item['class'] = 'active-parent'
            if 'children' in item:
                self._set_active_navigation_items(item['children'], path)

    def _populate_navigation(self, config, sitemap, options=None):
        """
        Recurse through config and lookup keys from sitemap.
        Put these keys in a new list of dictionaries. As it iterates through,
        pass reference to the current nesting level of sorted/unsorted dicts.
        """
        options = options or DEFAULT_NAVIGATION_OPTIONS
        nesting_limit = options['nesting_limit']
        remaining_depth = options.get('remaining_depth', nesting_limit)

        nav_items = []
        for config_item in config:
            # Set node context
            is_root = True
            remaining_node_depth = remaining_depth
            node_options = deepcopy(options)

            # Set new defaults for current and any children
            if '_options' in config_item:
                new_options = config_item['_options']
                if is_root and 'nesting_limit' in new_options:
                    new_nesting_limit = new_options['nesting_limit']
                    node_options['nesting_limit'] = new_nesting_limit
                    remaining_node_depth = new_nesting_limit
                    node_options['remaining_depth'] = remaining_node_depth

            # Set options for only this node
            if '_options_local' in config_item:
                local_options = config_item['_options_local']
                if is_root and 'nesting_limit' in local_options:
                    remaining_node_depth = local_options['nesting_limit']
                    node_options['remaining_depth'] = remaining_node_depth

            # Normalise nested string path items
            if isinstance(config_item, dict) and '_type' not in config_item:
                for k, v in config_item.items():
                    config_item = {
                        '_path': k,
                        '_items': v,
                    }

            # Normalise simple string path items
            if isinstance(config_item, str):
                config_item = {'_path': config_item}

            if config_item.get('_type') == 'section':
                new = {
                    'type': 'section',
                    'title': config_item.get('_title', ''),
                    'description': config_item.get('_description', ''),
                }
                # Section is a wrapper that does not count as
                # a level. Pass the current level of sitemap
                new['children'] = self._populate_navigation(
                    config_item['_items'],
                    sitemap,
                    options=node_options,
                )
            else:
                key = config_item['_path']
                new = {
                    'path': sitemap[key]['path'],
                    'title': config_item.get('_title', sitemap[key]['title']),
                    'description': sitemap[key]['description'],
                }
                if remaining_node_depth and '_items' in config_item:
                    remaining_node_depth -= 1
                    node_options['remaining_depth'] = remaining_node_depth
                    new['children'] = self._populate_navigation(
                        config_item['_items'],
                        sitemap[key]['children'],
                        options=node_options,
                    )

            nav_items.append(new)
        return nav_items

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

    def _generate_sitemap(self):
        """
        Generate a sitemap, starting from an optional given root_path.
        This will return the whole sitemap upon completion.
        """
        markdown_files = self._parse_markdown_files()

        self.sitemap = markdown_files

        return self.sitemap

    def get(self):
        if not self.sitemap:
            self._generate_sitemap()
        return self.sitemap

    def build_navigation(self, current_path=None):
        """
        Order the sitemap using a yaml config.
        Return a sitemap built with OrderedDict
        """
        template_path = getattr(settings, 'TEMPLATE_PATH')
        config_path = os.path.join(
            template_path,
            'includes',
            'navigation.yaml'
        )
        config = []
        if os.path.exists(config_path):
            with open(config_path, 'r') as navigation_file:
                config = yaml.load(navigation_file)

        sitemap = self.get()

        options = {}
        if isinstance(config, dict) and '_items' in config:
            config_items = config['_items']

            # TODO: Abstract duplicate logic from _populate_navigation
            if '_options' in config:
                options = config['_options']
            # Set options for only root node
            if '_options_local' in config:
                local_options = config['_options_local']
                if 'nesting_limit' in local_options:
                    remaining_node_depth = local_options['nesting_limit']
                    options['remaining_depth'] = remaining_node_depth
        else:
            config_items = config
        sorted_tree = self._populate_navigation(
            config_items,
            sitemap,
            options=options
        )

        # Determine current path and only load correct section
        current_path = current_path.strip('/')
        root_path = None
        if current_path:
            root_path = current_path.split('/')[0]
            self._set_active_navigation_items(sorted_tree, current_path)
        if root_path:
            sorted_tree = [self._find_navigation_item(sorted_tree, root_path)]
            back_link = [{
                'type': 'back',
                'path': '/',
            }]
            sorted_tree = back_link + sorted_tree

        return sorted_tree


sitemap = Sitemap()
