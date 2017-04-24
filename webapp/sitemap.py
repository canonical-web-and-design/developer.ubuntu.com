# Core modules
import fnmatch
import os
from collections import OrderedDict
from copy import deepcopy

# Third party modules
import yaml
from django.conf import settings

# Local modules
from webapp.lib.markdown import get_page_data


# def dict_representer(dumper, data):
#     return dumper.represent_dict(data.iteritems())
#
#
# def dict_constructor(loader, node):
#     return OrderedDict(loader.construct_pairs(node))
#
#
# _mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG
# yaml.add_representer(OrderedDict, dict_representer)
# yaml.add_constructor(_mapping_tag, dict_constructor)


# def gen_dict_extract(key, var):
#     if hasattr(var, 'iteritems'):
#         for k, v in var.iteritems():
#             if k == key:
#                 yield v
#             if isinstance(v, dict):
#                 for result in gen_dict_extract(key, v):
#                     yield result
#             elif isinstance(v, list):
#                 for d in v:
#                     for result in gen_dict_extract(key, d):
#                         yield result


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

    def _find_navigation_item(self, nav_items, path):
        if not path:
            return
        if not isinstance(path, list):
            path = self._split_path(path)

        for item in nav_items.iteritems():
            if 'path' in item and item['path'] == path[0]:
                path.pop(0)
                if not path:
                    return item
                if 'children' in item:
                    self._find_navigation_item(item['children'], path)
            elif 'path' not in item and 'children' in nav_items:
                self._find_navigation_item(item['children'], path)
        return False

    def _set_active_navigation_items(self, nav_items, path):
        if not path:
            return
        if not isinstance(path, list):
            path = self._split_path(path)

        item = self._find_navigation_item(nav_items, path[0])
        if item:
            path.pop(0)
            if not path:
                item['active'] = True
                item['class'] = 'active'
            else:
                item['active_parent'] = True
                item['class'] = 'active-parent'
            if 'children' in item:
                self._set_active_navigation_items(item['children'], path)

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

        unsorted_tree = self.get()
        sorted_tree = []

        def sort_tree(config, unsorted, sorting):
            """
            Recurse through config dictionary and lookup keys from sitemap.
            Put these keys in a new OrderedDict. As it iterates through, pass
            reference to the current nesting level of sorted/unsorted dicts.
            """
            unsorted = unsorted['children']
            sorting = sorting['children']
            for key, value in config.iteritems():
                sorting[key] = OrderedDict({
                    'path': unsorted[key]['path'],
                    'title': unsorted[key]['title'],
                    'description': unsorted[key]['description'],
                    'children': [],
                })
                if isinstance(value, OrderedDict):
                    sort_tree(value, unsorted[key], sorting[key])

        sort_tree(config, unsorted_tree, sorted_tree)

        # Determine current path and abstract section of sitemap
        current_path = current_path.strip('/')
        root_path = None
        if current_path:
            root_path = current_path.split('/')[0]
        if root_path:
            sorted_tree = self._find_navigation_item(sorted_tree, root_path)
            if root_path == current_path:
                current_path = None
            elif current_path.startswith(root_path):
                current_path = current_path[len(root_path):]

        # Mark current items as active if there is a path set
        if current_path:
            self._set_active_navigation_items(sorted_tree, current_path)
            # active_path_keys = self._split_path(current_path)
            # final_key = active_path_keys.pop()
            #
            # current_tree_branch = sorted_tree['children']
            # for key in active_path_keys:
            #     current_tree_branch = current_tree_branch[key]
            #     if current_tree_branch.get('children'):
            #         current_tree_branch['active_parent'] = True
            #         current_tree_branch['class'] = 'active-parent'
            #         current_tree_branch = current_tree_branch['children']
            #     else:
            #         continue
            #
            # if final_key in current_tree_branch:
            #     current_tree_branch[final_key]['active'] = True
            #     current_tree_branch[final_key]['class'] = 'active'

        return sorted_tree


sitemap = Sitemap()
