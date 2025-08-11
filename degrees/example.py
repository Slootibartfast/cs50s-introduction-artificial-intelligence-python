from collections import deque

class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action
        pstate = getattr(parent, "state", None)
        print(f"[Node.__init__] Created Node(state={state}, parent_state={pstate}, action={action})")

    def __str__(self):
        parent_state = getattr(self.parent, "state", None)
        return f"State: {self.state}, Parent: {parent_state}, Action: {self.action}"

class StackFrontier:
    def __init__(self):
        self.stack = []
        print("[StackFrontier.__init__] Initialized empty stack")

    def add(self, node):
        print(f"[StackFrontier.add] Pushing node -> {node}")
        self.stack.append(node)
        print(f"[StackFrontier.add] New stack states: {[n.state for n in self.stack]}")

    def contains_state(self, state):
        states = [n.state for n in self.stack]
        found = any(n.state == state for n in self.stack)
        print(f"[StackFrontier.contains_state] Check '{state}' in {states} -> {found}")
        return found

    def empty(self):
        is_empty = len(self.stack) == 0
        print(f"[StackFrontier.empty] len={len(self.stack)} -> {is_empty}")
        return is_empty

    def remove(self):
        if self.empty():
            print("[StackFrontier.remove] ERROR: Empty frontier")
            raise Exception("Empty frontier")
        node = self.stack.pop()
        print(f"[StackFrontier.remove] Popped node -> {node}")
        print(f"[StackFrontier.remove] New stack states: {[n.state for n in self.stack]}")
        return node
    
    def __str__(self):
        if not self.stack:
            return "StackFrontier([])"
        lines = ["StackFrontier(["]
        for index, item in enumerate(self.stack):
            lines.append(f"  {index}: {item}")
        lines.append("])")
        return "\n".join(lines)

# -------- Problem definition --------
start = "A"
goal = "E"

graph = {
    "A": ["B", "B", "C", "F"],
    "B": ["D", "E"],
    "C": ["F", "A"],
    "D": ["C"],
    "E": [],
    "F": []
}

print("\n[Setup] Start:", start, "Goal:", goal)
print("[Setup] Graph:", graph)

# -------- DFS search with verbose tracing --------
frontier = StackFrontier()
frontier.add(Node(start))
explored = set()
step = 0

while True:
    step += 1
    print("\n========== STEP", step, "==========")
    print("Current frontier:\n", frontier)
    if frontier.empty():
        print("[Main] No solution found. Frontier is empty.")
        break

    node = frontier.remove()
    print(f"[Main] Exploring node.state='{node.state}' (parent={getattr(node.parent, 'state', None)}, action={node.action})")

    # Goal test
    if node.state == goal:
        print(f"[Goal Test] Reached goal: {node.state}")
        # Reconstruct path
        actions = []
        states = []
        cursor = node
        print("[Reconstruct] Backtracking path from goal to start...")
        while cursor is not None:
            print(f"  - At Node(state={cursor.state}, parent={getattr(cursor.parent, 'state', None)}, action={cursor.action})")
            states.append(cursor.state)
            actions.append(cursor.action)
            cursor = cursor.parent
        states.reverse()
        actions.reverse()
        actions = actions[1:]  # drop the first None
        print("[Reconstruct] States:", states)
        print("[Reconstruct] Actions:", actions)
        print("Solution path:", " -> ".join(states))
        break

    # Mark explored
    explored.add(node.state)
    print(f"[Explore] Added '{node.state}' to explored -> {explored}")

    # Expand neighbors (Actions + Transition Model)
    neighbors = graph[node.state]
    print(f"[Expand] Neighbors of '{node.state}': {neighbors}")
    for neighbor in neighbors:
        print(f"  [Neighbor] Considering '{neighbor}' from '{node.state}'")
        in_frontier = frontier.contains_state(neighbor)
        in_explored = neighbor in explored
        print(f"    - In frontier? {in_frontier}")
        print(f"    - In explored? {in_explored}")
        if not in_frontier and not in_explored:
            action = f"Move to {neighbor}"
            child = Node(neighbor, parent=node, action=action)
            frontier.add(child)
        else:
            print(f"    - Skipping '{neighbor}' (already seen)")
