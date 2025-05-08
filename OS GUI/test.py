import pygame
from calculator import Calculator

# Initialize Pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((400, 500))
pygame.display.set_caption("Calculator Test")

# Create clock and calculator instance
clock = pygame.time.Clock()
calculator = Calculator(80, 80)  # Adjust position to center nicely

# Game loop
running = True
while running:
    screen.fill((30, 30, 30))  # Clear screen with dark gray

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                calculator.remove_buttons()
            elif event.key == pygame.K_t:
                calculator.restore_buttons()
        calculator.handle_event(event)

    calculator.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
