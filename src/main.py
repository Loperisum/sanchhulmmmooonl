import pygame
import game.define
import os
import random
import time

# pygame 초기화
pygame.init()

FPS = 60
# Frames Per Sec

pygame.display.set_caption('즐겁고 신나는 체커 게임\(￣︶￣*\))')

def main():
    # processing = 1
    processing = True
    clock = pygame.time.Clock()
    # 화면 크기 설정
    screen_width = 1000
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    background_image = pygame.image.load('src/bg/bg.jpg')
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    # 이미지 파일이 있는 폴더 경로 설정
    image_folder = "src/images/"

    # 폴더에서 모든 이미지 파일을 가져와 리스트에 저장
    image_list = []
    for filename in os.listdir(image_folder):
        if filename.endswith(".jpg"):  # 확장자에 따라 조절
            image = pygame.image.load(os.path.join(image_folder, filename))
            image_list.append(image)

    # 현재 이미지 선택
    if image_list:
        current_image = random.choice(image_list)
        current_image = pygame.transform.smoothscale(current_image, (600, 600))
    else:
        # 이미지 리스트가 비어있는 경우에 대한 처리
        current_image = pygame.Surface((100, 100))  # 임의의 빈 이미지를 생성하거나 다른 대체 방법 사용
    image_rect = current_image.get_rect()
    image_rect.centerx = screen_width // 2
    image_rect.centery = screen_height // 2

    # 초기 속도 및 회전 속도 설정
    speed_x = random.randint(5, 10)
    speed_y = random.randint(5, 10)
    rotation_speed = random.randint(1, 5)

    # 음악 로드 및 재생
    pygame.mixer.music.load('src/intro.mp3')
    pygame.mixer.music.play(0)  # 음악 1회 재생

    while processing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                processing = False

        # 음악이 재생 중일 때만 이미지 동작
        if pygame.mixer.music.get_busy():
            # 이미지 위치 업데이트
            image_rect.x += speed_x
            image_rect.y += speed_y

            # 화면 경계에 닿으면 방향 변경 및 이미지 교체
            if image_rect.left < 0 or image_rect.right > screen_width:
                speed_x = -speed_x
                current_image = random.choice(image_list)
                current_image.set_alpha(80)
            if image_rect.top < 0 or image_rect.bottom > screen_height:
                speed_y = -speed_y
                current_image = random.choice(image_list)
                current_image.set_alpha(80)

            # 이미지 회전 업데이트
            current_image = pygame.transform.rotate(current_image, rotation_speed)

        # 화면 초기화 및 이미지 그리기
        screen.fill((255, 255, 255))
        screen.blit(background_image, (0, 0))
        screen.blit(current_image, image_rect)

        pygame.display.flip()
        clock.tick(60)

    # 음악 종료 후 1초 대기
    pygame.mixer.music.stop()
    time.sleep(1)

    pygame.quit()
    
main()