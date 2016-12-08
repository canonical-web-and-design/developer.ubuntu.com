from markdown.util import etree
from markdown.extensions.toc import TocExtension, TocTreeprocessor


class VanillaTocTreeprocessor(TocTreeprocessor):
    def build_toc_div(self, toc_list):
        """ Return a string div given a toc list. """
        div = etree.Element("div")
        div.attrib["class"] = "p-toc"

        if len(toc_list) > 1:
            raise SyntaxError('More than one top-level heading detected.')

        ul = etree.SubElement(div, "ul")
        ul.attrib['class'] = 'p-toc__list'

        if len(toc_list) == 1 and 'children' in toc_list[0]:
            second_level_headings = toc_list[0]['children']

            for item in second_level_headings:
                # List item link, to be inserted into the toc div
                li = etree.SubElement(ul, "li")
                li.attrib['class'] = 'p-toc__item'
                link = etree.SubElement(li, "a")
                link.text = item.get('name', '')
                link.attrib['class'] = 'p-toc__link'
                link.attrib["href"] = '#' + item.get('id', '')

        prettify = self.markdown.treeprocessors.get('prettify')
        prettify.run(div)

        return div


class VanillaTocExtension(TocExtension):
    TreeProcessorClass = VanillaTocTreeprocessor


def makeExtension(*args, **kwargs):
    return VanillaTocExtension(*args, **kwargs)
