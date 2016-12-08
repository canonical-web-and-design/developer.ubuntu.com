# Core
import re

# Third party
from markdown.util import string_type
from markdown.extensions.toc import (
    stashedHTML2text,
    TocExtension,
    TocTreeprocessor,
    unique
)


class VanillaTocTreeprocessor(TocTreeprocessor):
    """
    A version of the standard TOC plugin, with the following changes:
    - Only collect second-level headings
    - Instead or returning HTML, return an object of list items,
      so you can craft the HTML yourself
    """

    def run(self, doc):
        # Get a list of id attributes
        used_ids = set()
        for el in doc.iter():
            if "id" in el.attrib:
                used_ids.add(el.attrib["id"])

        toc_items = []
        for el in doc.iter():
            if isinstance(el.tag, string_type) and re.match(
                "[hH]2",
                el.tag
            ):
                self.set_level(el)
                text = ''.join(el.itertext()).strip()

                # Do not override pre-existing ids
                if "id" not in el.attrib:
                    innertext = stashedHTML2text(text, self.markdown)
                    el.attrib["id"] = unique(
                        self.slugify(innertext, self.sep),
                        used_ids
                    )

                toc_items.append({
                    'id': el.attrib["id"],
                    'name': text
                })

                if self.use_anchors:
                    self.add_anchor(el, el.attrib["id"])
                if self.use_permalinks:
                    self.add_permalink(el, el.attrib["id"])

        self.markdown.toc_items = toc_items


class VanillaTocExtension(TocExtension):
    TreeProcessorClass = VanillaTocTreeprocessor


def makeExtension(*args, **kwargs):
    return VanillaTocExtension(*args, **kwargs)
