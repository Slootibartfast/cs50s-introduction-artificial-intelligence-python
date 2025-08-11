import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    
    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")
    
    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    print(f"Source: {source} -> Target {target}")

    # Initial State
    ## We have the Source's (actor's) ID, the initial state of the stack is empty
    #frontier = StackFrontier()
    frontier = QueueFrontier()
    frontier.add(Node((0,source)))

    #We want list of explored nodes so we don't go backwards or into a loop.
    explored = set()

    # Actions: legal moves from state.
    ## We will search for the source's neighbors' ID

    # Transition Model: what action leads to what state.

    # Path Cost: cumulative cost to reach a state.
    ## This isn't needed since each code from source to other sources is 1

    while True:
        #print("---------- Current frontier ----------")
        #print(f"{frontier}")
        if frontier.empty():
            print("No solution found")
            return None

        node = frontier.remove()
        print(f"Exploring: {node.state}. Does {node.state[1]} == {target}? {node.state[1] == target}", end="\r")

        # if the current node that was pulled matches with the goal
        # This is the Goal Test         
        if node.state[1] == target:
            #need to return a list pair of (movie_id, person_id)
            path = []
            while node.parent is not None:
                path.append(node.state)
                node = node.parent
            path.reverse()
            return path;  

        # once it's pulled off the list, we'll state that it's explored. 
        # since it's a set, it'll only contain unique values
        explored.add(node.state[1])

        # We're going to expand off the current node to search deeper
        neighbors = neighbors_for_person(node.state[1])

        # We'll loop through the neighbors to 
        for neighbor in neighbors:
            # we need to see if the neighbor is in the explored so we're not 
            #  continually looking at the same node over and over
            is_neighbor_in_explored = (neighbor[1] in explored)

            # we should also check if it's already in the list of nodes to explore
            is_neighbor_in_frontier = frontier.contains_state(neighbor)

            # if it hasn't been explored and if hasn't in the list to search
            #  then lets add it to the frontier to seach
            if not is_neighbor_in_explored and not is_neighbor_in_frontier:
                #print(f"Search on ID: {neighbor[1]}")
                frontier.add(Node(neighbor, node, f"Search on ID: {neighbor[1]}"))




def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
