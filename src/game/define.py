import pygame # 게임 상수를 지정해 놓은 간단한 ? 파일

# 화면 및 칸 크기, 가로 세로 배열되는 크기를 지정
WIDTH = 800
HEIGHT = WIDTH + (WIDTH / 2)
ROWS, COLS = 8, 8
BLOCK_SIZE = WIDTH // COLS

# rgb
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)

# 체커에선 상대 보드 끝쪽에 도달하면 왕이 되는데, 왕을 표시하기 위해서는 왕의 사진(왕관)을 집어넣어줘야 한다.
# 여기에선 칸의 크기에 맞추어서 사진을 리솔루션 해주어야 한다.
# 이는 원래사진의 화질을 유지하면서, 덮을 수 있는 투명배경사진이어야 하는데, 다행히도 그런 사진은 구했고, 
CROWN = pygame.transform.scale(pygame.image.load('src/img/crown.png'), (44, 25))