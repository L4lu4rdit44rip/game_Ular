import pygame
import sys
import random

# Inisialisasi Pygame
pygame.init()

# Ukuran layar
WIDTH, HEIGHT = 400, 400

# Warna
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Ukuran ular dan makanan
CELL_SIZE = 20

# Inisialisasi layar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Ular")

# Menggambar ular
snake = [(100, 50), (90, 50), (80, 50)]

# Inisialisasi arah awal ular
direction = 'RIGHT'

# Skor awal
score = 0

# Sejarah skor (5 skor terakhir)
score_history = []

# Fungsi untuk menggambar ular
def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, BLACK, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))

# Fungsi untuk menggambar makanan
def draw_food(food):
    pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], CELL_SIZE, CELL_SIZE))

# Fungsi untuk mengecek tabrakan dengan dinding atau diri sendiri
def check_collision(snake):
    head = snake[0]
    if head[0] >= WIDTH or head[0] < 0 or head[1] >= HEIGHT or head[1] < 0:
        return True
    for segment in snake[1:]:
        if head == segment:
            return True
    return False

# Fungsi untuk menghasilkan makanan baru di lokasi yang tidak bertabrakan dengan ular
def generate_food(snake):
    while True:
        food = (random.randrange(1, (WIDTH//CELL_SIZE)) * CELL_SIZE, random.randrange(1, (HEIGHT//CELL_SIZE)) * CELL_SIZE)
        if food not in snake:
            return food

# Membuat makanan pertama
food = generate_food(snake)

# Inisialisasi variabel panjang tambahan ular
panjang_tambahan = 0

# Inisialisasi font
font = pygame.font.Font(None, 36)

# Perulangan utama
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and direction != 'DOWN':
                direction = 'UP'
            elif event.key == pygame.K_s and direction != 'UP':
                direction = 'DOWN'
            elif event.key == pygame.K_a and direction != 'RIGHT':
                direction = 'LEFT'
            elif event.key == pygame.K_d and direction != 'LEFT':
                direction = 'RIGHT'

    # Gerakan ular
    new_head = ()
    if direction == 'UP':
        new_head = (snake[0][0], snake[0][1] - CELL_SIZE)
    elif direction == 'DOWN':
        new_head = (snake[0][0], snake[0][1] + CELL_SIZE)
    elif direction == 'LEFT':
        new_head = (snake[0][0] - CELL_SIZE, snake[0][1])
    elif direction == 'RIGHT':
        new_head = (snake[0][0] + CELL_SIZE, snake[0][1])

    snake.insert(0, new_head)

    # Cek tabrakan dengan dinding atau diri sendiri
    if check_collision(snake):
        pygame.quit()
        sys.exit()

    # Cek apakah ular memakan makanan
    if snake[0] == food:
        score += 10
        food = generate_food(snake)
        panjang_tambahan += 10

        # Menambahkan skor ke dalam sejarah skor
        score_history.append(score)

        # Membatasi sejarah skor menjadi 5 skor terakhir
        if len(score_history) > 5:
            score_history.pop(0)

    # Menghapus bagian ekstra ular jika panjang tambahan melebihi 0
    if panjang_tambahan > 0:
        panjang_tambahan -= 1
    else:
        snake.pop()

    # Tampilan game
    screen.fill(WHITE)
    draw_snake(snake)
    draw_food(food)
    
    # Tampilkan skor yang diperbarui
    text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(text, (10, 10))

    # Tampilkan sejarah skor
    for i, hist_score in enumerate(score_history):
        text = font.render(f"Score {i+1}: {hist_score}", True, BLACK)
        screen.blit(text, (10, 50 + i * 30))

    pygame.display.flip()
    pygame.time.Clock().tick(10)
