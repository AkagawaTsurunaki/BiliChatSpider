from typing import List


class ReplyNode:
    def __init__(self, username: str, content: str):
        self.username: str = username
        self.content: str = content
        self.children: List[ReplyNode] = []

    def dict(self):
        return {
            "username": self.username,
            "content": self.content,
            "children": [child.dict() for child in self.children]
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
