import pygame
import sys
import json

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Customization")

font = pygame.font.SysFont(None, 50)

WHITE = (255, 255, 255)
GRAY = (170, 170, 170)
BLACK = (0, 0, 0)

# Load data
DATA_FILE = "player_data.json"
def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"score": 0, "selected_skin": "car1.png"}

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

data = load_data()

# Available skins
skins = ["cars1.png", "cars2.png", "cars3.png"]
skin_costs = {"cars1.png": 0, "cars2.png": 10, "cars3.png": 20}

def customization_screen():
    running = True
    while running:
        screen.fill(WHITE)
        mx, my = pygame.mouse.get_pos()

        back_button = pygame.Rect(50, 500, 150, 60)
        pygame.draw.rect(screen, GRAY if back_button.collidepoint((mx, my)) else BLACK, back_button)
        draw_text("Back", font, WHITE, screen, 125, 530)
        
        y_offset = 150
        for skin in skins:
            button = pygame.Rect(300, y_offset, 200, 60)
            color = GRAY if skin_costs[skin] > data["score"] else BLACK
            pygame.draw.rect(screen, color if button.collidepoint((mx, my)) else BLACK, button)
            draw_text(skin, font, WHITE, screen, 400, y_offset + 30)
            y_offset += 100

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint((mx, my)):
                    running = False
                y_offset = 150
                for skin in skins:
                    button = pygame.Rect(300, y_offset, 200, 60)
                    if button.collidepoint((mx, my)) and data["score"] >= skin_costs[skin]:
                        data["selected_skin"] = skin
                        save_data(data)
                    y_offset += 100

        pygame.display.flip()

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

if __name__ == "__main__":
    customization_screen()
