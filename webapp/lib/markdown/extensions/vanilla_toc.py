from markdown.extensions.toc import *


class VanillaTocTreeprocessor(TocTreeprocessor):
    def build_toc_div(self, toc_list):
        """ Return a string div given a toc list. """
        div = etree.Element("div")
        div.attrib["class"] = "p-toc"

        # Add title to the div
        if self.title:
            header = etree.SubElement(div, "span")
            header.attrib["class"] = "toctitle"
            header.text = self.title

        def build_etree_ul(toc_list, parent):
            ul = etree.SubElement(parent, "ul")
            ul.attrib['class'] = 'p-toc__list'
            for item in toc_list:
                # List item link, to be inserted into the toc div
                li = etree.SubElement(ul, "li")
                li.attrib['class'] = 'p-toc__item'
                link = etree.SubElement(li, "a")
                link.text = item.get('name', '')
                link.attrib['class'] = 'p-toc__link'
                link.attrib["href"] = '#' + item.get('id', '')
                if item['children']:
                    build_etree_ul(item['children'], li)
            return ul

        build_etree_ul(toc_list, div)
        prettify = self.markdown.treeprocessors.get('prettify')
        if prettify:
            prettify.run(div)
        return div


class VanillaTocExtension(TocExtension):
    TreeProcessorClass = VanillaTocTreeprocessor


def makeExtension(*args, **kwargs):
    return VanillaTocExtension(*args, **kwargs)
