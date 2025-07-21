import pygame
import random
from collections import deque, defaultdict
import heapq
import os

# Game constants
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
WIDTH = CELL_SIZE * GRID_WIDTH
HEIGHT = CELL_SIZE * GRID_HEIGHT + 40  # Extra for score
SCOREBOARD_HEIGHT = 40

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)  # lighter gray for grid

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Auto Snake Game with Graph-based Dijkstra")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)

# Load food image
food_image = pygame.image.load("apple.png")
food_image = pygame.transform.scale(food_image, (CELL_SIZE, CELL_SIZE))

# Snake and food
snake = deque([(5, 5)])
score = 0
high_score = 0

def save_high_score(score):
    with open("high_score.txt", "w") as f:
        f.write(str(score))

def load_high_score():
    if os.path.exists("high_score.txt"):
        with open("high_score.txt", "r") as f:
            return int(f.read())
    return 0

def draw_grid():
    for x in range(GRID_WIDTH + 1):
        pygame.draw.line(screen, GRAY, (x * CELL_SIZE, SCOREBOARD_HEIGHT), (x * CELL_SIZE, HEIGHT))
    for y in range(GRID_HEIGHT + 1):
        pygame.draw.line(screen, GRAY, (0, y * CELL_SIZE + SCOREBOARD_HEIGHT), (WIDTH, y * CELL_SIZE + SCOREBOARD_HEIGHT))

def draw_snake():
    for segment in snake:
        x, y = segment
        pygame.draw.rect(screen, DARK_GREEN, (x * CELL_SIZE, y * CELL_SIZE + SCOREBOARD_HEIGHT, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, GREEN, (x * CELL_SIZE + 2, y * CELL_SIZE + 2 + SCOREBOARD_HEIGHT, CELL_SIZE - 4, CELL_SIZE - 4))

def draw_food():
    screen.blit(food_image, (food[0] * CELL_SIZE, food[1] * CELL_SIZE + SCOREBOARD_HEIGHT))

def draw_score():
    score_text = font.render(f"Score: {score}  High Score: {high_score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def neighbors(pos):
    x, y = pos
    for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
            yield (nx, ny)

def build_graph(snake_body):
    graph = defaultdict(list)
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if (x, y) in snake_body:
                continue
            for n in neighbors((x, y)):
                if n not in snake_body:
                    graph[(x, y)].append(n)
    return graph

def dijkstra(graph, start, goal):
    queue = []
    heapq.heappush(queue, (0, start))
    distances = {start: 0}
    previous = {start: None}

    while queue:
        dist, current = heapq.heappop(queue)
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = previous[current]
            path.reverse()
            return path

        for neighbor in graph[current]:
            alt = dist + 1  # uniform cost
            if neighbor not in distances or alt < distances[neighbor]:
                distances[neighbor] = alt
                previous[neighbor] = current
                heapq.heappush(queue, (alt, neighbor))
    return []

def move_snake_auto():
    snake_body = list(snake)[1:]  # exclude head
    graph = build_graph(snake_body)
    path = dijkstra(graph, snake[0], food)
    if len(path) > 1:
        next_move = path[1]
        return (next_move[0] - snake[0][0], next_move[1] - snake[0][1])
    else:
        return (0, 0)  # no path found

# Load previous high score
high_score = load_high_score()

# Initial food position
food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
while food in snake:
    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

# Game loop
running = True
while running:
    clock.tick(10)
    screen.fill(BLACK)

    draw_grid()
    draw_score()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    snake_dir = move_snake_auto()
    if snake_dir == (0, 0):
        print("No valid path to food. Game Over!")
        running = False
        break

    new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])

    # Collision check
    if new_head in snake or not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
        print("Snake bit itself or hit wall. Game Over!")
        running = False
        break

    snake.appendleft(new_head)

    if new_head == food:
        score += 1
        if score > high_score:
            high_score = score
            save_high_score(high_score)
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if food not in snake:
                break
    else:
        snake.pop()

    draw_snake()
    draw_food()

    pygame.display.flip()

pygame.quit()
