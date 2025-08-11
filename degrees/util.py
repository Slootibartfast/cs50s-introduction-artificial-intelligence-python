class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action

    def __str__(self):
        parent_state = getattr(self.parent, "state", None)
        return f"State: {self.state}, Parent: {parent_state}, Action: {self.action}"

class StackFrontier:
    def __init__(self):
        self.stack = []

    def add(self, node):
        self.stack.append(node)  # Push to stack

    def contains_state(self, state):
        return any(node.state == state for node in self.stack)

    def empty(self):
        return len(self.stack) == 0

    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        return self.stack.pop()  # Pop last added
    
    def __str__(self):
        if not self.stack:
            return "StackFrontier([])"
        lines = ["StackFrontier(["]
        for index, item in enumerate(self.stack):
            lines.append(f"  {index}: {item}")
        lines.append("])")
        return "\n".join(lines)


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.stack[0]
            self.stack = self.stack[1:]
            return node
