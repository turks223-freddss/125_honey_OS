import pygame

class Calculator:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 300
        self.height = 320
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.font = pygame.font.SysFont(None, 36)
        self.input = ""
        self.buttons = self.create_buttons()

    def create_buttons(self):
        buttons = []
        labels = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3','+'],
            ['0', 'C', '=', '-']
        ]
        button_w = 60
        button_h = 50
        gap = 10

        for row_index, row in enumerate(labels):
            for col_index, label in enumerate(row):
                bx = self.x + col_index * (button_w + gap) + 10
                by = self.y + row_index * (button_h + gap) + 80
                rect = pygame.Rect(bx, by, button_w, button_h)
                buttons.append((rect, label))
        return buttons

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for rect, label in self.buttons:
                if rect.collidepoint(mouse_pos):
                    if label == 'C':
                        self.input = ''
                    elif label == '=':
                        try:
                            self.input = str(eval(self.input))
                        except Exception:
                            self.input = 'Error'
                    else:
                        self.input += label

    def draw(self, screen):
        # Draw calculator background
        pygame.draw.rect(screen, (180, 180, 180), self.rect, border_radius=10)

        # Draw input display
        display_rect = pygame.Rect(self.x + 10, self.y + 10, self.width - 20, 50)
        pygame.draw.rect(screen, (255, 255, 255), display_rect)
        text_surf = self.font.render(self.input, True, (0, 0, 0))
        screen.blit(text_surf, (display_rect.x + 10, display_rect.y + 10))

        # Draw buttons
        for rect, label in self.buttons:
            pygame.draw.rect(screen, (220, 220, 220), rect)
            pygame.draw.rect(screen, (100, 100, 100), rect, 2)
            label_surf = self.font.render(label, True, (0, 0, 0))
            label_rect = label_surf.get_rect(center=rect.center)
            screen.blit(label_surf, label_rect)
        
    def remove_buttons(self):
        self.buttons = []
    
    def restore_buttons(self):
        self.buttons = self.create_buttons()
