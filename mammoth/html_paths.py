import cobble

from . import html


def path(elements):
    return HtmlPath(elements)


def element(names, class_names=None, fresh=None, separator=None, attrs={}):
    attributes = {}
    if class_names is None:
        class_names = []
    if fresh is None:
        fresh = False
    
    attributes = {"class": " ".join(class_names)}
    attributes = attrs | attributes #This prioritizes the class key from the class_names arg

    return HtmlPathElement(html.tag(
        tag_names=names,
        attributes=attributes,
        collapsible=not fresh,
        separator=separator,
    ))


@cobble.data
class HtmlPath(object):
    elements = cobble.field()
    
    def wrap(self, generate_nodes):
        nodes = generate_nodes()

        for element in reversed(self.elements):
            nodes = element.wrap_nodes(nodes)
        
        return nodes


@cobble.data
class HtmlPathElement(object):
    tag = cobble.field()

    def wrap(self, generate_nodes):
        return self.wrap_nodes(generate_nodes())

    def wrap_nodes(self, nodes):
        element = html.Element(self.tag, nodes)
        return [element]

empty = path([])


class ignore(object):
    @staticmethod
    def wrap(generate_nodes):
        return []
