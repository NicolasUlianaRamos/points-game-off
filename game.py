import pygame
import sys
import time

# Inicializa o pygame
pygame.init()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Dimensões da janela
WIDTH, HEIGHT = 600, 650  # Aumentei a altura para espaço da pontuação
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dots and Boxes")

# Variáveis do jogo
GRID_SIZE = 5  # Tamanho da grade (5x5 pontos)
DOT_RADIUS = 10
MARGIN = 50  # Margem entre os pontos e as bordas
CELL_SIZE = (WIDTH - 2 * MARGIN) // (GRID_SIZE - 1)
LINE_WIDTH = 5

# Inicializando as linhas e caixas
horizontal_lines = [[False] * (GRID_SIZE - 1) for _ in range(GRID_SIZE)]
vertical_lines = [[False] * (GRID_SIZE) for _ in range(GRID_SIZE - 1)]
boxes = [[None] * (GRID_SIZE - 1) for _ in range(GRID_SIZE - 1)]

# Pontuação e turno
player_turn = 1  # Alterna entre 1 e 2
scores = [0, 0]  # Índice 0 = Jogador 1, Índice 1 = Jogador 2

# Fonte para a pontuação
font = pygame.font.SysFont(None, 40)

# Desenha o tabuleiro
def draw_board():
    screen.fill(WHITE)

    # Desenha pontuação
    score_text = f"Player 1: {scores[0]} pontos  |  Player 2: {scores[1]} pontos"
    text = font.render(score_text, True, BLACK)
    screen.blit(text, (MARGIN, 10))  # Mostra a pontuação na parte superior da tela

    # Desenha pontos
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            pygame.draw.circle(screen, BLACK, (MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE + 50), DOT_RADIUS)

    # Desenha linhas horizontais
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE - 1):
            if horizontal_lines[row][col]:
                if horizontal_lines[row][col] == 1:
                    color = RED
                else:
                    color = BLUE
                pygame.draw.line(screen, color, 
                                 (MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE + 50), 
                                 (MARGIN + (col + 1) * CELL_SIZE, MARGIN + row * CELL_SIZE + 50), LINE_WIDTH)

    # Desenha linhas verticais
    for row in range(GRID_SIZE - 1):
        for col in range(GRID_SIZE):
            if vertical_lines[row][col]:
                if vertical_lines[row][col] == 1:
                    color = RED
                else:
                    color = BLUE
                pygame.draw.line(screen, color, 
                                 (MARGIN + col * CELL_SIZE, MARGIN + row * CELL_SIZE + 50), 
                                 (MARGIN + col * CELL_SIZE, MARGIN + (row + 1) * CELL_SIZE + 50), LINE_WIDTH)

    # Desenha caixas preenchidas
    for row in range(GRID_SIZE - 1):
        for col in range(GRID_SIZE - 1):
            if boxes[row][col] is not None:
                if boxes[row][col] == 1:
                    color = RED
                else:
                    color = BLUE
                pygame.draw.rect(screen, color, 
                                 (MARGIN + col * CELL_SIZE + LINE_WIDTH, MARGIN + row * CELL_SIZE + LINE_WIDTH + 50, 
                                  CELL_SIZE - LINE_WIDTH * 2, CELL_SIZE - LINE_WIDTH * 2))

    pygame.display.flip()

# Checa se uma linha foi clicada
def get_clicked_line(pos):
    x, y = pos
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE - 1):
            line_x1 = MARGIN + col * CELL_SIZE
            line_x2 = MARGIN + (col + 1) * CELL_SIZE
            line_y = MARGIN + row * CELL_SIZE + 50
            if line_x1 <= x <= line_x2 and abs(line_y - y) <= LINE_WIDTH // 2 and not horizontal_lines[row][col]:
                return ('horizontal', row, col)

    for row in range(GRID_SIZE - 1):
        for col in range(GRID_SIZE):
            line_y1 = MARGIN + row * CELL_SIZE + 50
            line_y2 = MARGIN + (row + 1) * CELL_SIZE + 50
            line_x = MARGIN + col * CELL_SIZE
            if line_y1 <= y <= line_y2 and abs(line_x - x) <= LINE_WIDTH // 2 and not vertical_lines[row][col]:
                return ('vertical', row, col)

    return None

# Checa se uma caixa foi completada
def check_for_box():
    completed_box = False
    for row in range(GRID_SIZE - 1):
        for col in range(GRID_SIZE - 1):
            if boxes[row][col] is None:
                if horizontal_lines[row][col] and horizontal_lines[row + 1][col] and \
                   vertical_lines[row][col] and vertical_lines[row][col + 1]:
                    boxes[row][col] = player_turn
                    scores[player_turn - 1] += 1
                    completed_box = True
    return completed_box

# Verifica se o jogo acabou
def is_game_over():
    for row in boxes:
        if None in row:
            return False
    return True

# Tela final com o vencedor
def show_winner():
    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 72)

    if scores[0] > scores[1]:
        text = font.render("Player 1 Wins!", True, RED)
    elif scores[1] > scores[0]:
        text = font.render("Player 2 Wins!", True, BLUE)
    else:
        text = font.render("It's a Tie!", True, GRAY)

    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

    # Aguarda 5 segundos e fecha o jogo
    time.sleep(5)
    pygame.quit()
    sys.exit()

# Lógica principal do jogo
def game_loop():
    global player_turn

    while True:
        draw_board()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked_line = get_clicked_line(pos)

                if clicked_line:
                    line_type, row, col = clicked_line

                    if line_type == 'horizontal':
                        horizontal_lines[row][col] = player_turn
                    elif line_type == 'vertical':
                        vertical_lines[row][col] = player_turn

                    if not check_for_box():
                        player_turn = 3 - player_turn  # Alterna entre 1 e 2

        # Checa se o jogo acabou
        if is_game_over():
            show_winner()

        pygame.display.flip()

game_loop()
