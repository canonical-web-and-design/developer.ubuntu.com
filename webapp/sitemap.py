from collections import defaultdict, OrderedDict


temporary_tree = OrderedDict([
    ('core', {
        'path': '/core',
        'title': 'Core home',
        'children': OrderedDict((
            ('get-started', {
                'path': '/core/get-started',
                'title': 'Get started',
            }),
            ('tutorials', {
                'path': '/core/tutorials',
                'title': 'Tutorials',
            }),
            ('examples', {
                'path': '/core/examples',
                'title': 'Examples',
                'children': {
                    'gadget-snaps': {
                        'path': '/core/examples/gadget-snaps',
                        'title': 'Gadget snaps',
                    },
                    'interfaces': {
                        'path': '/core/examples/interfaces',
                        'title': 'Interfaces',
                    },
                    'hooks': {
                        'path': '/core/examples/hooks',
                        'title': 'Hooks',
                    },
                    'assertions': {
                        'path': '/core/examples/assertions',
                        'title': 'Assertions',
                    },
                },
            }),
            ('publish-and-distribute', {
                'path': '/core/',
                'title': 'Publish and distribute',
                'children': {
                    'publish': {
                        'path': '/core/publish-and-distribute/publish',
                        'title': 'Publish',
                    },
                    'distribute': {
                        'path': '/core/publish-and-distribute/distribute',
                        'title': 'Distribute',
                    },
                },
            }),
            ('documentation', {
                'path': '/core/documentation',
                'title': 'Documentation',
            }),
            ('troubleshooting', {
                'path': '/core/troubleshooting',
                'title': 'Troubleshooting',
            }),
        )),
    }),
])


class SitemapTree(defaultdict):
    def __init__(self):
        pass


class Sitemap:
    def __init__(self):
        self.sitemap = {}

    def _generate_sitemap(self, root_path):
        """
        Generate a sitemap, starting from an optional given root_path.
        This will return the whole sitemap upon completion.
        """
        tree = temporary_tree
        if root_path:
            self.sitemap[root_path] = tree['core']

        return self.sitemap

    def get(self, root_path=None):
        if root_path:
            full_map = self._generate_sitemap(root_path)
            return full_map[root_path]
        return self._generate_sitemap()


sitemap = Sitemap()
