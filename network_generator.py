"""
Generates social network test datasets for graph traversal analysis.
Creates JSON files with networks of varying sizes (100, 500, 1000 users).
"""

import json
import random
from pathlib import Path

def generate_social_network(num_users, avg_friends=10, seed=42):
    """
    Generate a random social network graph.
    
    Args:
        num_users: Number of users in the network
        avg_friends: Average number of friends per user
        seed: Random seed for reproducibility
        
    Returns:
        Dictionary containing adjacency list representation of graph
    """
    random.seed(seed)
    
    # Initialize adjacency list
    graph = {i: [] for i in range(num_users)}
    
    # Generate friendships (undirected edges)
    # Each user gets approximately avg_friends connections
    num_edges = (num_users * avg_friends) // 2
    
    edges_created = 0
    attempts = 0
    max_attempts = num_edges * 10  # Prevent infinite loops
    
    while edges_created < num_edges and attempts < max_attempts:
        user1 = random.randint(0, num_users - 1)
        user2 = random.randint(0, num_users - 1)
        
        # No self-loops, no duplicate edges
        if user1 != user2 and user2 not in graph[user1]:
            graph[user1].append(user2)
            graph[user2].append(user1)
            edges_created += 1
        
        attempts += 1
    
    # Ensure graph is connected by creating a spanning path
    # This guarantees no isolated components
    for i in range(num_users - 1):
        if i + 1 not in graph[i]:
            graph[i].append(i + 1)
            graph[i + 1].append(i)
    
    # Create user metadata
    first_names = ['Alex', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Riley', 
                   'Jamie', 'Avery', 'Quinn', 'Sage', 'River', 'Sky']
    
    users = []
    for i in range(num_users):
        users.append({
            'id': i,
            'name': f'{random.choice(first_names)} User{i}',
            'friends': graph[i]
        })
    
    return {
        'num_users': num_users,
        'num_friendships': sum(len(friends) for friends in graph.values()) // 2,
        'users': users,
        'graph': graph
    }

def main():
    """Generate all test datasets."""
    # Create data directory if it doesn't exist
    Path('data').mkdir(exist_ok=True)
    
    # Generate networks of various sizes
    sizes = [
        (100, 10),   # 100 users, ~10 friends each
        (500, 12),   # 500 users, ~12 friends each
        (1000, 15),  # 1000 users, ~15 friends each
    ]
    
    print("Generating social network datasets...")
    for num_users, avg_friends in sizes:
        data = generate_social_network(num_users, avg_friends)
        filename = f'data/network_{num_users}.json'
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"  Created {filename}")
        print(f"    Users: {data['num_users']}, Friendships: {data['num_friendships']}")
    
    print("\nDataset generation complete!")
    print("Files created in 'data/' directory")

if __name__ == '__main__':
    main()