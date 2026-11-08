# Graph Traversal Assignment: Six Degrees of Connection

This repository contains implementations for analyzing graph traversal algorithms (BFS and DFS) on social network data.

## Setup

1. Clone this repository
2. Navigate to the repository directory
3. Generate the test datasets:
   ```bash
   python network_generator.py
   ```

This creates a `data/` directory with social network datasets of various sizes (100, 500, 1000 users).

## Running the Code

The assignment asks you to run three different commands:

### 1. Test BFS Implementation
```bash
python graph_traversal.py --test-bfs
```
Tests your breadth-first search implementation on a 100-user network, finding paths between random user pairs.

### 2. Test DFS Implementation
```bash
python graph_traversal.py --test-dfs
```
Tests your depth-first search implementation on a 100-user network, exploring reachable users from random starting points.

### 3. Benchmark Both Algorithms
```bash
python graph_traversal.py --benchmark
```
Compares BFS and DFS performance across networks of size 100, 500, and 1000 users.

## File Structure

```
.
├── README.md                  # This file
├── network_generator.py       # Generates test datasets
├── graph_traversal.py        # BFS and DFS implementations and testing utilities
└── data/                     # Generated test datasets
    ├── network_100.json
    ├── network_500.json
    └── network_1000.json
```

## Implementation Guide

### BFS (Breadth-First Search)
- Located in `graph_traversal.py` under PART 1
- Should use a queue to explore neighbors level by level
- Returns shortest path from start to target as a list
- Use `collections.deque` for efficient queue operations

### DFS (Depth-First Search)
- Located in `graph_traversal.py` under PART 2
- Should use recursion or a stack to explore deeply before backtracking
- Returns set of all reachable users from start
- Track visited nodes to avoid infinite loops