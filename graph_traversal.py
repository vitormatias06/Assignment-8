
"""
Graph traversal algorithms: BFS and DFS implementations.
Includes testing and benchmarking utilities for social network analysis.
"""

import json
import time
import random
import sys
import tracemalloc
from pathlib import Path
from collections import deque

# ============================================================================
# PART 1: BREADTH-FIRST SEARCH (BFS)
# ============================================================================

def bfs(graph, start, target):
    """
    Find shortest path between two users using breadth-first search.

    Args:
        graph: Dictionary where graph[user_id] = list of friend IDs
        start: Starting user ID
        target: Target user ID

    Returns:
        List representing shortest path from start to target,
        or empty list if no path exists.
    """

    if start not in graph or target not in graph:
        return []

    queue = deque([start])
    visited = {start}
    parents = {start: None}

    while queue:
        current = queue.popleft()

        if current == target:
            path = []
            node = target

            while node is not None:
                path.append(node)
                node = parents[node]

            return path[::-1]

        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                parents[neighbor] = current
                queue.append(neighbor)

    return []


# ============================================================================
# PART 2: DEPTH-FIRST SEARCH (DFS)
# ============================================================================

def dfs(graph, start):
    """
    Find all users reachable from a starting user using depth-first search.

    Args:
        graph: Dictionary where graph[user_id] = list of friend IDs
        start: Starting user ID

    Returns:
        Set of all user IDs reachable from start.
    """

    if start not in graph:
        return set()

    visited = set()
    stack = [start]

    while stack:
        current = stack.pop()

        if current not in visited:
            visited.add(current)

            for neighbor in graph.get(current, []):
                if neighbor not in visited:
                    stack.append(neighbor)

    return visited


# ============================================================================
# TESTING AND BENCHMARKING UTILITIES
# ============================================================================

def load_network(size):
    """Load social network dataset of given size."""

    filename = f'data/network_{size}.json'

    if not Path(filename).exists():
        print(f"Error: {filename} not found. Run network_generator.py first.")
        sys.exit(1)

    with open(filename, 'r') as f:
        data = json.load(f)

    graph = {int(k): v for k, v in data['graph'].items()}

    return graph, data['num_users']


# ============================================================================
# BFS TEST
# ============================================================================

def test_bfs():
    """Test BFS implementation on small network with known paths."""

    print("\n" + "=" * 70)
    print("TESTING: Breadth-First Search (BFS)")
    print("=" * 70)

    graph, num_users = load_network(100)

    test_cases = 5

    print(f"\nTesting {test_cases} random paths in 100-user network...\n")

    for i in range(test_cases):

        start = random.randint(0, num_users - 1)
        target = random.randint(0, num_users - 1)

        path = bfs(graph, start, target)

        if path:
            print(f"Test {i+1}: Path from User {start} to User {target}")
            print(f"  Length: {len(path) - 1} connections")

            print(
                f"  Path: {' → '.join(map(str, path[:5]))}"
                f"{'...' if len(path) > 5 else ''}"
            )

            valid = True

            for j in range(len(path) - 1):
                if path[j+1] not in graph.get(path[j], []):
                    valid = False
                    break

            status = "✓ Valid" if valid else "✗ Invalid"

            print(f"  Status: {status}\n")

        else:
            print(
                f"Test {i+1}: No path from User {start} "
                f"to User {target}\n"
            )


# ============================================================================
# DFS TEST
# ============================================================================

def test_dfs():
    """Test DFS implementation on small network."""

    print("\n" + "=" * 70)
    print("TESTING: Depth-First Search (DFS)")
    print("=" * 70)

    graph, num_users = load_network(100)

    test_cases = 5

    print(f"\nTesting {test_cases} explorations in 100-user network...\n")

    for i in range(test_cases):

        start = random.randint(0, num_users - 1)

        reachable = dfs(graph, start)

        print(f"Test {i+1}: Exploration from User {start}")
        print(f"  Reachable users: {len(reachable)}")

        percentage = (len(reachable) / num_users) * 100

        print(f"  Percentage of network: {percentage:.1f}%")

        if start in reachable:
            print("  Status: ✓ Valid (includes start node)\n")
        else:
            print("  Status: ✗ Invalid (missing start node)\n")


# ============================================================================
# BENCHMARK BFS
# ============================================================================

def benchmark_bfs(graph, num_users, num_trials=10):
    """Benchmark BFS execution time and memory usage."""

    total_time = 0
    total_memory = 0

    for _ in range(num_trials):

        start = random.randint(0, num_users - 1)
        target = random.randint(0, num_users - 1)

        tracemalloc.start()

        start_time = time.perf_counter()

        bfs(graph, start, target)

        elapsed_time = time.perf_counter() - start_time

        _, peak_memory = tracemalloc.get_traced_memory()

        tracemalloc.stop()

        total_time += elapsed_time
        total_memory += peak_memory

    average_time = total_time / num_trials
    average_memory = total_memory / num_trials

    return average_time, average_memory


# ============================================================================
# BENCHMARK DFS
# ============================================================================

def benchmark_dfs(graph, num_users, num_trials=10):
    """Benchmark DFS execution time and memory usage."""

    total_time = 0
    total_memory = 0

    for _ in range(num_trials):

        start = random.randint(0, num_users - 1)

        tracemalloc.start()

        start_time = time.perf_counter()

        dfs(graph, start)

        elapsed_time = time.perf_counter() - start_time

        _, peak_memory = tracemalloc.get_traced_memory()

        tracemalloc.stop()

        total_time += elapsed_time
        total_memory += peak_memory

    average_time = total_time / num_trials
    average_memory = total_memory / num_trials

    return average_time, average_memory


# ============================================================================
# RUN BENCHMARKS
# ============================================================================

def run_benchmarks():
    """Compare BFS and DFS performance across different network sizes."""

    print("\n" + "=" * 80)
    print("BENCHMARKING: BFS vs DFS Performance")
    print("=" * 80)

    print("\nRunning 10 trials per algorithm on each network size...\n")

    sizes = [100, 500, 1000]

    print(
        f"{'Size':<10}"
        f"{'Algorithm':<12}"
        f"{'Avg Time (ms)':<18}"
        f"{'Peak Memory (KB)':<18}"
        f"{'Operations'}"
    )

    print("-" * 80)

    for size in sizes:

        graph, num_users = load_network(size)

        operations = num_users + sum(
            len(friends) for friends in graph.values()
        )

        # BFS benchmark
        bfs_time, bfs_memory = benchmark_bfs(graph, num_users)

        print(
            f"{size:<10}"
            f"{'BFS':<12}"
            f"{bfs_time * 1000:<18.3f}"
            f"{bfs_memory / 1024:<18.2f}"
            f"~{operations}"
        )

        # DFS benchmark
        dfs_time, dfs_memory = benchmark_dfs(graph, num_users)

        print(
            f"{size:<10}"
            f"{'DFS':<12}"
            f"{dfs_time * 1000:<18.3f}"
            f"{dfs_memory / 1024:<18.2f}"
            f"~{operations}"
        )

        print()

    print("=" * 80)
    print("Note: Both algorithms have O(V + E) time complexity.")
    print("Memory measurements represent approximate peak memory")
    print("used by each algorithm during execution.")
    print("=" * 80)


# ============================================================================
# MAIN INTERFACE
# ============================================================================

def print_usage():
    """Print usage instructions."""

    print("\nUsage: python graph_traversal.py [option]")

    print("\nOptions:")
    print("  --test-bfs      Test BFS implementation on small network")
    print("  --test-dfs      Test DFS implementation on small network")
    print("  --benchmark     Compare BFS and DFS performance")
    print("  --help          Show this help message")

    print("\nFor the assignment, run these commands in order:")

    print("  1. python graph_traversal.py --test-bfs")
    print("  2. python graph_traversal.py --test-dfs")
    print("  3. python graph_traversal.py --benchmark")


def main():
    """Main entry point for running tests and benchmarks."""

    if len(sys.argv) < 2:
        print_usage()
        return

    option = sys.argv[1]

    if not Path('data/network_100.json').exists():
        print("\nError: Data files not found!")
        print("Please run: python network_generator.py")
        print("This will create the required test datasets.")
        sys.exit(1)

    if option == '--test-bfs':
        test_bfs()

    elif option == '--test-dfs':
        test_dfs()

    elif option == '--benchmark':
        run_benchmarks()

    elif option == '--help':
        print_usage()

    else:
        print(f"\nError: Unknown option '{option}'")
        print_usage()


if __name__ == '__main__':
    main()
