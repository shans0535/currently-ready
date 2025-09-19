import heapq
import pandas as pd


import heapq


def dijkstra(graph, start):
    """
    Dijkstra's algorithm for shortest paths in a weighted graph.

    Parameters:
        graph (dict): adjacency list representation of the graph.
                      {node: [(neighbor, weight), ...]}
        start (hashable): starting node

    Returns:
        dict: shortest distances from start to each node
        dict: predecessors for reconstructing shortest paths
    """
    # Distance table, initialized to infinity
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    # Predecessor table (to reconstruct paths)
    predecessors = {node: None for node in graph}

    # Min-heap priority queue
    pq = [(0, start)]  # (distance, node)

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        # Skip if we found a shorter path already
        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight

            # If a shorter path is found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    return distances, predecessors


def dijkstra_visual(graph, start):
    # Distance table, initialized to infinity
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    predecessors = {node: None for node in graph}
    pq = [(0, start)]
    step = 0

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_distance > distances[current_node]:
            continue

        print(
            f"\n🔹 Step {step}: Visiting {current_node} (current distance {current_distance})")
        step += 1

        # Show current distance table
        df = pd.DataFrame([distances])
        print(df.to_string(index=False))

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            if distance < distances[neighbor]:
                print(
                    f"   → Updating {neighbor}: {distances[neighbor]} → {distance}")
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    return distances, predecessors


def shortest_path(predecessors, target):
    """Reconstruct shortest path from predecessors dictionary."""
    path = []
    while target is not None:
        path.insert(0, target)
        target = predecessors[target]
    return path


# Example usage
if __name__ == "__main__":
    graph = {
        'A': [('B', 1), ('C', 4)],
        'B': [('A', 1), ('C', 2), ('D', 5)],
        'C': [('A', 4), ('B', 2), ('D', 1)],
        'D': [('B', 5), ('C', 1)]
    }

    distances, predecessors = dijkstra_visual(graph, 'A')

    print("\n✅ Final shortest distances:", distances)
    print("✅ Shortest path A → D:", shortest_path(predecessors, 'D'))
