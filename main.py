"""
Quick Draw - A feature-rich drawing application
Created for GitHub Quick Draw achievement
"""

import pygame
import sys
import math
import random
from datetime import datetime

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (255, 0, 255), (0, 255, 255),
    (128, 0, 0), (0, 128, 0), (0, 0, 128)
]

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quick Draw - GitHub Achievement Project")
screen.fill(WHITE)

# Drawing variables
drawing = False
last_pos = None
current_color = BLACK
brush_size = 5
current_tool = "pen"  # pen, eraser, spray, rectangle, circle
fill_shape = False

# Undo functionality
undo_stack = []
undo_limit = 20

def save_state():
    if len(undo_stack) >= undo_limit:
        undo_stack.pop(0)
    undo_stack.append(screen.copy())

def undo():
    if undo_stack:
        screen.blit(undo_stack.pop(), (0, 0))
        pygame.display.flip()

# Main game loop
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 16)

save_state()  # Save initial state

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Keyboard events
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                undo()
            elif event.key == pygame.K_c:
                current_tool = "pen"
            elif event.key == pygame.K_e:
                current_tool = "eraser"
            elif event.key == pygame.K_s:
                current_tool = "spray"
            elif event.key == pygame.K_r:
                current_tool = "rectangle"
            elif event.key == pygame.K_o:
                current_tool = "circle"
            elif event.key == pygame.K_f:
                fill_shape = not fill_shape
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                brush_size = min(50, brush_size + 1)
            elif event.key == pygame.K_MINUS:
                brush_size = max(1, brush_size - 1)
            elif event.key == pygame.K_1:
                current_color = COLORS[0]
            elif event.key == pygame.K_2:
                current_color = COLORS[1]
            elif event.key == pygame.K_3:
                current_color = COLORS[2]
            elif event.key == pygame.K_4:
                current_color = COLORS[3]
            elif event.key == pygame.K_5:
                current_color = COLORS[4]
            elif event.key == pygame.K_6:
                current_color = COLORS[5]
            elif event.key == pygame.K_7:
                current_color = COLORS[6]
            elif event.key == pygame.K_8:
                current_color = COLORS[7]
            elif event.key == pygame.K_9:
                current_color = COLORS[8]
            elif event.key == pygame.K_0:
                current_color = BLACK
            elif event.key == pygame.K_n:
                screen.fill(WHITE)
                save_state()
        
        # Mouse events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                drawing = True
                last_pos = event.pos
                if current_tool in ["rectangle", "circle"]:
                    start_pos = event.pos
                save_state()
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left click release
                drawing = False
                if current_tool == "rectangle":
                    end_pos = event.pos
                    rect = pygame.Rect(
                        min(start_pos[0], end_pos[0]),
                        min(start_pos[1], end_pos[1]),
                        abs(end_pos[0] - start_pos[0]),
                        abs(end_pos[1] - start_pos[1])
                    )
                    if fill_shape:
                        pygame.draw.rect(screen, current_color, rect)
                    else:
                        pygame.draw.rect(screen, current_color, rect, brush_size)
                    save_state()
                elif current_tool == "circle":
                    end_pos = event.pos
                    radius = int(math.hypot(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
                    if fill_shape:
                        pygame.draw.circle(screen, current_color, start_pos, radius)
                    else:
                        pygame.draw.circle(screen, current_color, start_pos, radius, brush_size)
                    save_state()
        
        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                if current_tool == "pen":
                    if last_pos:
                        pygame.draw.line(screen, current_color, last_pos, event.pos, brush_size)
                    last_pos = event.pos
                elif current_tool == "eraser":
                    if last_pos:
                        pygame.draw.line(screen, WHITE, last_pos, event.pos, brush_size)
                    last_pos = event.pos
                elif current_tool == "spray":
                    for _ in range(brush_size * 2):
                        angle = random.uniform(0, math.pi * 2)
                        radius = random.uniform(0, brush_size)
                        x = event.pos[0] + radius * math.cos(angle)
                        y = event.pos[1] + radius * math.sin(angle)
                        pygame.draw.circle(screen, current_color, (int(x), int(y)), 1)
    
    # Draw UI
    pygame.draw.rect(screen, (240, 240, 240), (0, 0, WIDTH, 30))
    
    # Display current tool and color
    tool_text = font.render(f"Tool: {current_tool.capitalize()}", True, BLACK)
    color_text = font.render(f"Color: {current_color}", True, BLACK)
    size_text = font.render(f"Size: {brush_size}", True, BLACK)
    fill_text = font.render(f"Fill: {'ON' if fill_shape else 'OFF'}", True, BLACK)
    
    screen.blit(tool_text, (10, 5))
    screen.blit(color_text, (150, 5))
    screen.blit(size_text, (300, 5))
    screen.blit(fill_text, (400, 5))
    
    # Display instructions
    instructions = font.render("1-9: Colors | 0: Black | +/-: Size | C: Pen | E: Eraser | S: Spray | R: Rectangle | O: Circle | F: Toggle Fill | N: New | Ctrl+Z: Undo", True, BLACK)
    screen.blit(instructions, (10, HEIGHT - 20))
    
    pygame.display.flip()
    clock.tick(60)
