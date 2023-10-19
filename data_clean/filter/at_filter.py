from core.data_structure import ReplyNode
import re

at_regex = re.compile('^@.+\s(.+)$')


def at_filter(node: ReplyNode):
    for child in node.children.copy():
        result = at_regex.match(child.content)
        if result is None:
            node.children.remove(child)
        else:
            child.content = result.group(1)
            at_filter(child)