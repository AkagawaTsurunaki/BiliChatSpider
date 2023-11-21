from typing import List


class ReplyNode:
    def __init__(self, username: str, content: str):
        self.username: str = username
        self.content: str = content
        self.children: List[ReplyNode] = []

    def to_dict(self):
        return {
            "username": self.username,
            "content": self.content,
            "children": [child.to_dict() for child in self.children]
        }

    @staticmethod
    def from_dict(d):
        node = ReplyNode(d['username'], d['content'])
        children = d.get('children', [])
        for child in children:
            node.children.append(ReplyNode.from_dict(child))
        return node

    def __len__(self):
        if self is None:
            return 0
        count = 1
        for child in self.children:
            count += len(child)
        return count

    @staticmethod
    def leaf_nodes_count(node):
        """
        Suppose you call this function in certain node.
        :return: The number of the leaf nodes from this node.
        """
        if not node.children:  # 如果节点没有子节点，则为末尾节点
            return 1
        else:
            count = 0
            for child in node.children:
                count += node.leaf_nodes_count(child)
            return count

    def add(self, node):
        if node is not None:
            self.children.append(node)

    def find(self, username):
        if self.username == username:
            return self

        for node in self.children:
            result = node.find(username)
            if result is not None:
                return result

        return None
