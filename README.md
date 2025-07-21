# Auto Snake Game with Graph-based Dijkstra Pathfinding

This is an automated Snake game built in Python using Pygame that uses **Dijkstra’s Algorithm** to find the shortest path to the food on the grid. It is a practical project aimed at practicing Data Structures and Algorithms (DSA) with hands-on implementation.

---

## Features

- Fully autonomous snake movement using Dijkstra’s shortest path algorithm
- Dynamic graph construction representing the game grid while avoiding snake body collisions
- Efficient data structures: `deque` for the snake body, `heapq` priority queue for Dijkstra
- Collision detection with walls and self
- Score and high score tracking with persistent storage
- Visual grid rendering with snake and food images

---

## Technologies Used

- Python 3
- Pygame for game rendering and UI
- Core Python data structures: deque, defaultdict, heapq

---

## How It Works

1. The game grid is represented as a graph where each free cell is a node.
2. The snake’s current body cells are treated as obstacles and excluded from the graph.
3. Dijkstra’s algorithm calculates the shortest path from the snake’s head to the food.
4. The snake moves automatically step-by-step along this shortest path.
5. On eating the food, the snake grows, and a new food is placed randomly.
6. The game ends if the snake collides with itself or walls or if no valid path to food exists.

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/auto-snake-dijkstra.git
   cd auto-snake-dijkstra
