import pygame
import sys
import random

# Các hằng số cho chế độ chơi
EASY_MODE = "easy"
MEDIUM_MODE = "medium"
HARD_MODE = "hard"

# Các biến cho chế độ chơi
pipe_speeds = {
    EASY_MODE: 2,
    MEDIUM_MODE: 5,
    HARD_MODE: 8
}

gravity_values = {
    EASY_MODE: 0.15,
    MEDIUM_MODE: 0.25,
    HARD_MODE: 0.35
}


# Các hàm và biến khác trong trò chơi

# Các hàm và biến cho trò chơi
def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos + 432, 650))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos - 700))
    return bottom_pipe, top_pipe


def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= pipe_speed
    return pipes


def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True


def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == "main game":
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)
    if game_state == "game_over":
        score_surface = game_font.render(f"Score: {int(score)}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f"High Score: {int(high_score)}", True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(216, 630))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


# Khởi tạo Pygame
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()

# Cấu hình màn hình
screen = pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()
game_font = pygame.font.Font("04B_19.ttf", 35)


# Tạo các biến cho trò chơi
bird_movement = 0
game_active = True
score = 0
high_score = 0

# Chèn background
bg = pygame.image.load("assests/background-night.png").convert()
bg = pygame.transform.scale2x(bg)

# Tạo màn hình lựa chọn chế độ chơi
def game_mode_selection():
    selected_mode = None

    while not selected_mode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_mode = EASY_MODE
                elif event.key == pygame.K_2:
                    selected_mode = MEDIUM_MODE
                elif event.key == pygame.K_3:
                    selected_mode = HARD_MODE

        screen.blit(bg, (0, 0))
        mode_text = game_font.render("Select Game Mode:", True, (255, 255, 255))
        mode_rect = mode_text.get_rect(center=(216, 200))
        screen.blit(mode_text, mode_rect)

        easy_text = game_font.render("1. Easy", True, (255, 255, 255))
        easy_rect = easy_text.get_rect(center=(216, 300))
        screen.blit(easy_text, easy_rect)

        medium_text = game_font.render("2. Medium", True, (255, 255, 255))
        medium_rect = medium_text.get_rect(center=(216, 350))
        screen.blit(medium_text, medium_rect)

        hard_text = game_font.render("3. Hard", True, (255, 255, 255))
        hard_rect = hard_text.get_rect(center=(216, 400))
        screen.blit(hard_text, hard_rect)

        pygame.display.update()
        clock.tick(60)

    return selected_mode


def reset_game():
    global bird_movement, game_active, score, pipe_list

    bird_movement = 0
    game_active = True
    score = 0
    pipe_list = []

    bird_rect.center = (100, 384)

    pygame.time.set_timer(spawnpipe, 1200)


# Chế độ chơi
game_mode = game_mode_selection()
pipe_speed = pipe_speeds[game_mode]
gravity = gravity_values[game_mode]

# Chèn sàn
floor = pygame.image.load("assests/floor.png").convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

# Tạo chim
bird_down = pygame.transform.scale2x(pygame.image.load("assests/yellowbird-downflap.png").convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load("assests/yellowbird-midflap.png").convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load("assests/yellowbird-upflap.png").convert_alpha())
bird_list = [bird_down, bird_mid, bird_up]  # 0 1 2
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center=(100, 384))

# Tạo timer cho bird
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 200)

# Tạo ống
pipe_surface = pygame.image.load("assests/pipe-green.png").convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

# Tạo timer
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)
pipe_height = [200, 300, 400]

# Tạo màn hình kết thúc
game_over_surface = pygame.transform.scale2x(pygame.image.load("assests/message.png").convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(216, 384))

# Chèn âm thanh
flap_sound = pygame.mixer.Sound("sound/sfx_wing.wav")
hit_sound = pygame.mixer.Sound("sound/sfx_hit.wav")
score_sound = pygame.mixer.Sound("sound/sfx_point.wav")
score_sound_countdown = 100

# Vòng lặp chính của trò chơi
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement = -5
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                reset_game()
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()

    screen.blit(bg, (0, 0))

    if game_active:
        # Chim
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Ống
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)

        score += 0.01
        score_display("main game")

        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display("game_over")

    # Sàn
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
