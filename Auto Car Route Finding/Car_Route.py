import pygame
import sys
import heapq
import random
import math

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 20
GRID_WIDTH = 40
GRID_HEIGHT = 30
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 10

# Colors
BLACK = (0, 0, 0)
BG_COLOR = (230, 230, 230)
GRID_COLOR = (200, 200, 200)
PATH_COLOR = (200, 200, 200)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 150, 255)

# Pygame Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Route Simulation with Images")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# Load images and scale to CELL_SIZE
car_img = pygame.image.load("car.png").convert_alpha()
car_img = pygame.transform.scale(car_img, (CELL_SIZE, CELL_SIZE))

moving_obstacle_img = pygame.image.load("moving_obstacle.png").convert_alpha()
moving_obstacle_img = pygame.transform.scale(moving_obstacle_img, (CELL_SIZE, CELL_SIZE))

static_obstacle_img = pygame.image.load("static_obstacle.png").convert_alpha()
static_obstacle_img = pygame.transform.scale(static_obstacle_img, (CELL_SIZE, CELL_SIZE))

destination_img = pygame.image.load("destination.png").convert_alpha()
destination_img = pygame.transform.scale(destination_img, (CELL_SIZE, CELL_SIZE))

# Positions
car_pos = (0, 0)
destination = None

# Obstacles
NUM_MOVING_OBSTACLES = 10
NUM_STATIC_OBSTACLES = 50
static_obstacles = set()
moving_obstacles = set()
obstacle_directions = {}

def generate_obstacles():
    while len(static_obstacles) < NUM_STATIC_OBSTACLES:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos != car_pos and pos not in static_obstacles:
            static_obstacles.add(pos)
    while len(moving_obstacles) < NUM_MOVING_OBSTACLES:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos != car_pos and pos not in static_obstacles and pos not in moving_obstacles:
            moving_obstacles.add(pos)
            obstacle_directions[pos] = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])

generate_obstacles()

def draw_grid():
    screen.fill(BG_COLOR)
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

def draw_image(pos, img):
    x, y = pos
    screen.blit(img, (x * CELL_SIZE, y * CELL_SIZE))

def move_moving_obstacles():
    global moving_obstacles, obstacle_directions
    new_positions = set()
    new_directions = {}
    for (x, y) in list(moving_obstacles):
        dx, dy = obstacle_directions.get((x, y), (0, 0))
        new_x, new_y = x + dx, y + dy
        if (0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT and
            (new_x, new_y) not in moving_obstacles and
            (new_x, new_y) not in static_obstacles and
            (new_x, new_y) != car_pos):
            new_pos = (new_x, new_y)
        else:
            dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
            new_pos = (x + dx, y + dy)
            if not (0 <= new_pos[0] < GRID_WIDTH and 0 <= new_pos[1] < GRID_HEIGHT):
                new_pos = (x, y)
                dx, dy = 0, 0
        new_positions.add(new_pos)
        new_directions[new_pos] = (dx, dy)
    moving_obstacles = new_positions
    obstacle_directions = new_directions

def neighbors(pos):
    x, y = pos
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if (0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and
            (nx, ny) not in static_obstacles and
            (nx, ny) not in moving_obstacles):
            yield (nx, ny)

def dijkstra(start, goal):
    queue = [(0, start)]
    cost_so_far = {start: 0}
    came_from = {}
    visited = set()
    while queue:
        cost, current = heapq.heappop(queue)
        if current == goal:
            break
        visited.add(current)
        for neighbor in neighbors(current):
            new_cost = cost_so_far[current] + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                heapq.heappush(queue, (new_cost, neighbor))
                came_from[neighbor] = current
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from.get(current)
        if current is None:
            return [], visited
    path.append(start)
    path.reverse()
    return path, visited

def draw_path_with_animation(path, tick):
    for i, pos in enumerate(path):
        x, y = pos
        pulse = 0.6 + 0.3 * math.sin(tick * 0.15 + i)
        radius = int(CELL_SIZE * 0.3 * pulse)
        center = (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2)
        pygame.draw.circle(screen, PATH_COLOR, center, radius)

def draw_arrival_animation(pos, tick):
    x, y = pos
    center = (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2)
    radius = int(CELL_SIZE * 0.3 * (1 + 0.5 * math.sin(tick * 0.2)))
    pygame.draw.circle(screen, BLUE, center, radius)

def countdown():
    for i in range(3, 0, -1):
        screen.fill(BLACK)
        draw_grid()
        msg = font.render(f"Starting in {i}...", True, YELLOW)
        rect = msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(msg, rect)
        pygame.display.flip()
        pygame.time.delay(1000)

def show_message(text, color=GREEN, duration=1000):
    screen.fill(BLACK)
    draw_grid()
    msg = font.render(text, True, color)
    rect = msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(msg, rect)
    pygame.display.flip()
    pygame.time.delay(duration)

def ask_restart():
    while True:
        screen.fill(BLACK)
        msg1 = font.render("Reached destination!", True, GREEN)
        msg2 = font.render("Click anywhere to move again, or press Q to quit.", True, YELLOW)
        screen.blit(msg1, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20))
        screen.blit(msg2, (SCREEN_WIDTH // 2 - 240, SCREEN_HEIGHT // 2 + 20))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return

# Main loop
running = True
countdown()
tick = 0

while running:
    draw_grid()
    move_moving_obstacles()

    for pos in static_obstacles:
        draw_image(pos, static_obstacle_img)
    for pos in moving_obstacles:
        draw_image(pos, moving_obstacle_img)

    draw_image(car_pos, car_img)
    if destination:
        draw_image(destination, destination_img)

    if destination:
        path, visited = dijkstra(car_pos, destination)
        if path:
            draw_path_with_animation(path, tick)
            if len(path) > 1:
                car_pos = path[1]
        else:
            destination = None

        if car_pos == destination:
            pause_ticks = pygame.time.get_ticks()
            while pygame.time.get_ticks() - pause_ticks < 2000:
                draw_grid()
                for pos in static_obstacles:
                    draw_image(pos, static_obstacle_img)
                for pos in moving_obstacles:
                    draw_image(pos, moving_obstacle_img)
                draw_image(car_pos, car_img)
                draw_arrival_animation(car_pos, tick)
                pygame.display.flip()
                clock.tick(FPS)
                tick += 1
            show_message("You reached the destination!", GREEN, duration=1000)
            destination = None
            ask_restart()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not destination and event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            gx, gy = mx // CELL_SIZE, my // CELL_SIZE
            if (gx, gy) not in static_obstacles and (gx, gy) not in moving_obstacles and (gx, gy) != car_pos:
                destination = (gx, gy)

    pygame.display.flip()
    clock.tick(FPS)
    tick += 1

pygame.quit()
