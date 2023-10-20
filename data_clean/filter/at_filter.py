from core.data_structure import ReplyNode
import re

at_regex = re.compile('@.+?\s*')

def at_filter(node: ReplyNode) -> ReplyNode:
    new_node = ReplyNode(node.username, at_regex.sub('', node.content).strip())
    if new_node.content == '':
        return None

    for child in node.children:
        new_child = at_filter(child)
        if new_child is not None:
            new_node.children.append(new_child)

    return new_node
