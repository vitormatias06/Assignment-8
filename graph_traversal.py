"""
Graph traversal algorithms: BFS and DFS implementations.
Includes testing and benchmarking utilities for social network analysis.
"""

import json
import time
import random
import sys
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
        or empty list if no path exists
        
    Example:
        graph = {0: [1, 2], 1: [0, 3], 2: [0], 3: [1]}
        bfs(graph, 0, 3) returns [0, 1, 3]
    """
    # TODO: Implement BFS
    # Hints:
    # - Use a queue (deque) to track nodes to visit
    # - Track visited nodes to avoid cycles
    # - Track parent pointers to reconstruct path
    # - Return path from start to target as a list
    
    pass


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
        Set of all user IDs reachable from start (including start itself)
        
    Example:
        graph = {0: [1, 2], 1: [0, 3], 2: [0], 3: [1], 4: [5], 5: [4]}
        dfs(graph, 0) returns {0, 1, 2, 3}
    """
    # TODO: Implement DFS
    # Hints:
    # - Use recursion or a stack to explore deeply
    # - Track visited nodes to avoid infinite loops
    # - Return a set of all reachable user IDs
    
    pass


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
    
    # Convert graph to simple adjacency list (remove metadata)
    graph = {int(k): v for k, v in data['graph'].items()}
    return graph, data['num_users']

def test_bfs():
    """Test BFS implementation on small network with known paths."""
    print("\n" + "="*70)
    print("TESTING: Breadth-First Search (BFS)")
    print("="*70)
    
    # Load smallest network
    graph, num_users = load_network(100)
    
    # Test multiple random paths
    test_cases = 5
    print(f"\nTesting {test_cases} random paths in 100-user network...\n")
    
    for i in range(test_cases):
        start = random.randint(0, num_users - 1)
        target = random.randint(0, num_users - 1)
        
        path = bfs(graph, start, target)
        
        if path:
            print(f"Test {i+1}: Path from User {start} to User {target}")
            print(f"  Length: {len(path) - 1} connections")
            print(f"  Path: {' → '.join(map(str, path[:5]))}{'...' if len(path) > 5 else ''}")
            
            # Verify path is valid
            valid = True
            for j in range(len(path) - 1):
                if path[j+1] not in graph[path[j]]:
                    valid = False
                    break
            
            status = "✓ Valid" if valid else "✗ Invalid"
            print(f"  Status: {status}\n")
        else:
            print(f"Test {i+1}: No path from User {start} to User {target}\n")

def test_dfs():
    """Test DFS implementation on small network."""
    print("\n" + "="*70)
    print("TESTING: Depth-First Search (DFS)")
    print("="*70)
    
    # Load smallest network
    graph, num_users = load_network(100)
    
    # Test from multiple starting points
    test_cases = 5
    print(f"\nTesting {test_cases} explorations in 100-user network...\n")
    
    for i in range(test_cases):
        start = random.randint(0, num_users - 1)
        
        reachable = dfs(graph, start)
        
        print(f"Test {i+1}: Exploration from User {start}")
        print(f"  Reachable users: {len(reachable)}")
        print(f"  Percentage of network: {(len(reachable)/num_users)*100:.1f}%")
        
        # Verify start is in reachable set
        if start in reachable:
            print(f"  Status: ✓ Valid (includes start node)\n")
        else:
            print(f"  Status: ✗ Invalid (missing start node)\n")

def benchmark_bfs(graph, num_users, num_trials=10):
    """Benchmark BFS performance."""
    total_time = 0
    
    for _ in range(num_trials):
        start = random.randint(0, num_users - 1)
        target = random.randint(0, num_users - 1)
        
        start_time = time.time()
        bfs(graph, start, target)
        total_time += time.time() - start_time
    
    return total_time / num_trials

def benchmark_dfs(graph, num_users, num_trials=10):
    """Benchmark DFS performance."""
    total_time = 0
    
    for _ in range(num_trials):
        start = random.randint(0, num_users - 1)
        
        start_time = time.time()
        dfs(graph, start)
        total_time += time.time() - start_time
    
    return total_time / num_trials

def run_benchmarks():
    """Compare BFS and DFS performance across different network sizes."""
    print("\n" + "="*70)
    print("BENCHMARKING: BFS vs DFS Performance")
    print("="*70)
    print("\nRunning 10 trials per algorithm on each network size...")
    
    sizes = [100, 500, 1000]
    
    print(f"\n{'Size':<8} {'Algorithm':<12} {'Avg Time (ms)':<15} {'Operations'}")
    print("-" * 70)
    
    for size in sizes:
        graph, num_users = load_network(size)
        
        # Benchmark BFS
        bfs_time = benchmark_bfs(graph, num_users)
        bfs_ops = f"~{num_users + sum(len(friends) for friends in graph.values())}"
        print(f"{size:<8} {'BFS':<12} {bfs_time*1000:<15.3f} {bfs_ops}")
        
        # Benchmark DFS
        dfs_time = benchmark_dfs(graph, num_users)
        dfs_ops = f"~{num_users + sum(len(friends) for friends in graph.values())}"
        print(f"{size:<8} {'DFS':<12} {dfs_time*1000:<15.3f} {dfs_ops}")
        print()
    
    print("="*70)
    print("Note: Both algorithms have O(V + E) time complexity.")
    print("Performance differences come from implementation details and graph structure.")
    print("="*70)

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
    
    # Check if data files exist
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