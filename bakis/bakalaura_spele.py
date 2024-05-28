import pygame
import random
import time
import os

# Sākt Pygame
pygame.init()

# Ekrāna izmērs
screen = pygame.display.set_mode((800, 700))

# Nosaukums un ikona
pygame.display.set_caption("Sportistu atlases simulators")

# Krāsas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_GREEN = (102, 255, 178)
HOVER_GREEN = (51, 204, 102)

# Fonts
font_path = 'C:\\Users\\Lietotajs\\Desktop\\bakis\\Inter\\static\\Inter-Regular.ttf'

# Pārbaudīt, vai fails eksistē un ielādēt fontu
if os.path.exists(font_path):
    font = pygame.font.Font(font_path, 24)
else:
    font = pygame.font.Font(None, 36)

# Sportistu dotumu klases
class Athlete:
    def __init__(self, name):
        self.name = name
        self.speed = random.randint(50, 99)
        self.strength = random.randint(50, 99)
        self.endurance = random.randint(50, 99)
    
    @property
    def total_score(self):
        return self.speed + self.strength + self.endurance

# Funkcija jaunu sportistu ģenerēšanai
def generate_athletes():
    return [Athlete(f"Sportists {i+1}") for i in range(4)]

# Ģenerēt sākotnējo sportistu komplektu
athletes = generate_athletes()

# Noteikt "pareizo" sportistu (ar visaugstāko kopējo rezultātu)
def determine_right_player(athletes):
    return max(athletes, key=lambda athlete: athlete.total_score)

right_player = determine_right_player(athletes)

# Funkcija skautu ziņojuma attēlošanai
def display_scouting_report(athlete, x, y):
    report = [
        f"Vārds: {athlete.name}",
        f"Ātrums: {athlete.speed}",
        f"Spēks: {athlete.strength}",
        f"Izturība: {athlete.endurance}",
    ]
    for line in report:
        text = font.render(line, True, WHITE)
        screen.blit(text, (x, y))
        y += 40

# Funkcija taisnstūra zīmēšanai
def draw_rounded_rect(surface, color, rect, corner_radius):
    if rect.width < 2 * corner_radius or rect.height < 2 * corner_radius:
        raise ValueError("Gan augstumam, gan platumam jābūt > 2 * stūra radius")
    pygame.draw.rect(surface, color, rect)
    pygame.draw.circle(surface, color, (rect.left + corner_radius, rect.top + corner_radius), corner_radius)
    pygame.draw.circle(surface, color, (rect.right - corner_radius, rect.top + corner_radius), corner_radius)
    pygame.draw.circle(surface, color, (rect.left + corner_radius, rect.bottom - corner_radius), corner_radius)
    pygame.draw.circle(surface, color, (rect.right - corner_radius, rect.bottom - corner_radius), corner_radius)

# Funkcija sportistu izvēļu attēlošanai ar pogām
def display_athlete_choices():
    button_height = 50
    button_width = 150
    square_size = 250
    gap = 50
    buttons = []
    positions = [(gap, gap), 
                 (screen.get_width() - square_size - gap, gap), 
                 (gap, screen.get_height() - square_size - gap), 
                 (screen.get_width() - square_size - gap, screen.get_height() - square_size - gap)]
    
    for i, (x, y) in enumerate(positions):
        pygame.draw.rect(screen, GRAY, (x, y, square_size, square_size))
        display_scouting_report(athletes[i], x + 10, y + 10)
        button_rect = pygame.Rect(x + (square_size - button_width) // 2, y + square_size - button_height - 10, button_width, button_height)
        buttons.append(button_rect)
        mouse_pos = pygame.mouse.get_pos()
        button_color = LIGHT_GREEN if button_rect.collidepoint(mouse_pos) else HOVER_GREEN
        draw_rounded_rect(screen, button_color, button_rect, 25)
        button_text = font.render("Izvēlēties", True, WHITE)
        screen.blit(button_text, (button_rect.x + (button_width - button_text.get_width()) // 2, button_rect.y + (button_height - button_text.get_height()) // 2))
    
    return buttons

# Funkcija gala rezultātu ekrāna attēlošanai
def display_final_result(correct, incorrect):
    screen.fill(BLACK)
    result_text = font.render(f"Gala rezultāts: {correct} pareizas, {incorrect} nepareizas atbildes", True, WHITE)
    screen.blit(result_text, (screen.get_width() // 2 - result_text.get_width() // 2, screen.get_height() // 2 - 50))
    restart_button = pygame.Rect(screen.get_width() // 2 - 150, screen.get_height() // 2 + 50, 300, 50)
    mouse_pos = pygame.mouse.get_pos()
    button_color = LIGHT_GREEN if restart_button.collidepoint(mouse_pos) else HOVER_GREEN
    draw_rounded_rect(screen, button_color, restart_button, 25)
    button_text = font.render("Sākt no sākuma", True, WHITE)
    screen.blit(button_text, (restart_button.x + (300 - button_text.get_width()) // 2, restart_button.y + (50 - button_text.get_height()) // 2))
    return restart_button

# Funkcija nākamās kārtas ekrāna attēlošanai
def display_next_round_screen(message):
    screen.fill(BLACK)
    message_text = font.render(message, True, WHITE)
    screen.blit(message_text, (screen.get_width() // 2 - message_text.get_width() // 2, screen.get_height() // 2 - 50))
    next_round_button = pygame.Rect(screen.get_width() // 2 - 75, screen.get_height() // 2 + 50, 150, 50)
    mouse_pos = pygame.mouse.get_pos()
    button_color = LIGHT_GREEN if next_round_button.collidepoint(mouse_pos) else HOVER_GREEN
    draw_rounded_rect(screen, button_color, next_round_button, 25)
    button_text = font.render("Nākamā lapa", True, WHITE)
    screen.blit(button_text, (next_round_button.x + (150 - button_text.get_width()) // 2, next_round_button.y + (50 - button_text.get_height()) // 2))
    return next_round_button

# Funkcija ievada ekrāna attēlošanai
def display_intro_screen():
    screen.fill(BLACK)
    intro_text1 = font.render("Spēles mērķis ir izvēlēties vislabāko sportistu", True, WHITE)
    intro_text2 = font.render("pēc to tehniskajiem dotumiem", True, WHITE)
    screen.blit(intro_text1, (screen.get_width() // 2 - intro_text1.get_width() // 2, screen.get_height() // 2 - 80))
    screen.blit(intro_text2, (screen.get_width() // 2 - intro_text2.get_width() // 2, screen.get_height() // 2 - 40))
    intro_button = pygame.Rect(screen.get_width() // 2 - 75, screen.get_height() // 2 + 50, 150, 50)
    mouse_pos = pygame.mouse.get_pos()
    button_color = LIGHT_GREEN if intro_button.collidepoint(mouse_pos) else HOVER_GREEN
    draw_rounded_rect(screen, button_color, intro_button, 25)
    button_text = font.render("Sākt spēli", True, WHITE)
    screen.blit(button_text, (intro_button.x + (150 - button_text.get_width()) // 2, intro_button.y + (50 - button_text.get_height()) // 2))
    return intro_button

# Funkcija sākuma ekrāna attēlošanai
def display_start_screen():
    screen.fill(BLACK)
    start_text = font.render("Šis ir jauno sportistu atlases simulātors", True, WHITE)
    screen.blit(start_text, (screen.get_width() // 2 - start_text.get_width() // 2, screen.get_height() // 2 - 50))
    start_button = pygame.Rect(screen.get_width() // 2 - 75, screen.get_height() // 2 + 50, 150, 50)
    mouse_pos = pygame.mouse.get_pos()
    button_color = LIGHT_GREEN if start_button.collidepoint(mouse_pos) else HOVER_GREEN
    draw_rounded_rect(screen, button_color, start_button, 25)
    button_text = font.render("Nākamais", True, WHITE)
    screen.blit(button_text, (start_button.x + (150 - button_text.get_width()) // 2, start_button.y + (50 - button_text.get_height()) // 2))
    return start_button

# Galvenais loops
running = True
game_started = False
show_intro_screen = False
selected_athlete = None
feedback_message = ""
pick_again_button = None
next_round_button = None
round_count = 1
total_rounds = 10
score = 0
incorrect = 0
time_limit = 30
start_time = time.time()
restart_button = None
show_final_screen = False
start_button = None
intro_button = None

while running:
    current_time = time.time()
    elapsed_time = current_time - start_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if not game_started and not show_intro_screen and start_button and start_button.collidepoint(mouse_pos):
                # Parādīt ievada ekrānu
                show_intro_screen = True
            elif show_intro_screen and intro_button and intro_button.collidepoint(mouse_pos):
                # Sākt spēli
                game_started = True
                show_intro_screen = False
                athletes = generate_athletes()
                right_player = determine_right_player(athletes)
                start_time = time.time()
            elif restart_button and restart_button.collidepoint(mouse_pos):
                # Restartēt spēli
                round_count = 1
                score = 0
                incorrect = 0
                athletes = generate_athletes()
                right_player = determine_right_player(athletes)
                selected_athlete = None
                feedback_message = ""
                pick_again_button = None
                next_round_button = None
                start_time = time.time()
                restart_button = None
                show_final_screen = False
            elif next_round_button and next_round_button.collidepoint(mouse_pos):
                if show_final_screen:
                    running = False
                else:
                    round_count += 1
                    if round_count > total_rounds:
                        show_final_screen = True
                    else:
                        athletes = generate_athletes()
                        right_player = determine_right_player(athletes)
                        selected_athlete = None
                        feedback_message = ""
                        pick_again_button = None
                        next_round_button = None
                        start_time = time.time()
            elif selected_athlete:
                if pick_again_button and pick_again_button.collidepoint(mouse_pos):
                    selected_athlete = None
                    feedback_message = ""
                    pick_again_button = None
                    next_round_button = None
                    start_time = time.time()
            else:
                buttons = display_athlete_choices()
                for i, button in enumerate(buttons):
                    if button.collidepoint(mouse_pos):
                        selected_athlete = athletes[i]
                        if selected_athlete == right_player:
                            feedback_message = "Tu izvēlējies pareizo sportistu!"
                            score += 1
                        else:
                            feedback_message = "Tu izvēlējies nepareizo sportistu."
                            incorrect += 1
                        next_round_button = pygame.Rect(screen.get_width() // 2 - 75, 550, 150, 50)

    # Attīrīt ekrānu
    screen.fill(BLACK)

    if not game_started and not show_intro_screen:
        start_button = display_start_screen()
    elif show_intro_screen:
        intro_button = display_intro_screen()
    elif show_final_screen:
        restart_button = display_final_result(score, incorrect)
    elif elapsed_time >= time_limit:
        feedback_message = "Laiks beidzies, uz nākamo lapu"
        next_round_button = display_next_round_screen(feedback_message)
        incorrect += 1
    else:
        if selected_athlete:
            # Attēlot izvēlētā sportista skautu ziņojumu
            display_scouting_report(selected_athlete, 250, 250)
            # Attēlot atgriezenisko saiti
            feedback_text = font.render(feedback_message, True, GREEN if feedback_message == "Tu izvēlējies pareizo sportistu!" else RED)
            screen.blit(feedback_text, (screen.get_width() // 2 - feedback_text.get_width() // 2, 500))
            # Attēlot atbilstošo pogu
            mouse_pos = pygame.mouse.get_pos()
            button_color = LIGHT_GREEN if next_round_button and next_round_button.collidepoint(mouse_pos) else HOVER_GREEN
            draw_rounded_rect(screen, button_color, next_round_button, 25)
            button_text = font.render("Nākamā lapa", True, WHITE)
            screen.blit(button_text, (next_round_button.x + (150 - button_text.get_width()) // 2, next_round_button.y + (50 - button_text.get_height()) // 2))
        else:
            # Attēlot sportistu izvēles ar pogām
            display_athlete_choices()
            # Attēlot laika atskaiti
            timer_color = RED if (time_limit - elapsed_time) <= 10 else WHITE
            timer_text = font.render(f"Laiks atlicis: {max(0, int(time_limit - elapsed_time))}", True, timer_color)
            screen.blit(timer_text, (10, 10))
        
        # Attēlot kārtas numuru augšpusē, ja netiek rādīts gala ekrāns
        round_text = font.render(f"Lapa: {round_count}/{total_rounds}", True, WHITE)
        screen.blit(round_text, (screen.get_width() // 2 - round_text.get_width() // 2, 10))

    pygame.display.flip()

pygame.quit()
