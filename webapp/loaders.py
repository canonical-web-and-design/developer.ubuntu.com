import hashlib
import os

from django.conf import settings
from django.template import Origin
from django.template.base import Template
from django.template.engine import Engine
from django.template.exceptions import TemplateDoesNotExist
from django.template.loaders.base import Loader
from yaml.scanner import ScannerError
from yaml.parser import ParserError

from webapp.lib.markdown import parse_markdown

find_template_loader = Engine.get_default().find_template_loader


def make_origin(display_name, loader, name, dirs):
    return Origin(
        name=display_name,
        template_name=name,
        loader=loader,
    )


class MarkdownLoader(Loader):
    is_usable = True

    def __init__(self, engine, loaders):
        self.template_cache = {}
        self._loaders = loaders
        self._cached_loaders = []
        self._find_template_loader = find_template_loader

    @property
    def loaders(self):
        if not self._cached_loaders:
            cached_loaders = []
            for loader in self._loaders:
                cached_loaders.append(self._find_template_loader(loader))
            self._cached_loaders = cached_loaders
        return self._cached_loaders

    def find_template(self, name, dirs=None):
        for loader in self.loaders:
            try:
                template, display_name = loader(name, dirs)
                origin = make_origin(display_name, loader, name, dirs)
                return (template, origin)
            except TemplateDoesNotExist:
                pass
        raise TemplateDoesNotExist(name)

    def load_template_source(self, template_name, template_dirs=None):
        template_name_parts = template_name.split('.md')
        template_name_index = ''.join([template_name_parts[0], '/index.md'])
        template_names = [
            template_name,
            template_name_index,
        ]
        for loader in self.loaders:
            for template_name in template_names:
                try:
                    return loader.load_template_source(
                        template_name, template_dirs
                    )
                except TemplateDoesNotExist:
                    pass
        raise TemplateDoesNotExist(template_name)

    def load_template(self, template_name, template_dirs=None):
        key = template_name
        if template_dirs:
            dirs_hash = hashlib.sha1('|'.join(template_dirs)).hexdigest()
            key = '-'.join([template_name, dirs_hash])

        if settings.DEBUG or key not in self.template_cache:
            template, origin = self._generate_template(
                template_name, template_dirs
            )
            if not hasattr(template, 'render'):
                try:
                    template = Template(source, origin, template_name)
                except (TemplateDoesNotExist, UnboundLocalError):
                    return template, origin
            self.template_cache[key] = template
        return self.template_cache[key], None

    def _generate_template(self, template_name, template_dirs=None):
        if not os.path.splitext(template_name)[1] in ('.md',):
            return self.find_template(template_name, template_dirs)

        try:
            source, display_name = self.load_template_source(
                template_name, template_dirs
            )
            source = parse_markdown(source)
            origin = make_origin(
                display_name,
                self.load_template_source,
                template_name,
                template_dirs,
            )
            template = Template(source, origin, template_name)
        except NotImplementedError:
            template, origin = self.find_template(template_name, template_dirs)
        return template, origin

    def reset(self):
        "Empty the template cache."
        self.template_cache.clear()
