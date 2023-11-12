import pygame
import pygame_gui

pygame.init()

# 화면 크기 설정
size = (800, 600)
screen = pygame.display.set_mode(size)

# GUI 매니저 생성
manager = pygame_gui.UIManager(size)

# 버튼 생성
quit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                           text='Quit',
                                           manager=manager)

# 메시지 박스 변수 초기화
confirm_dialog = None

# 메인 루프
running = True
while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # 정말 나가겠냐고 묻는 메시지 박스 생성
            confirm_dialog = pygame_gui.windows.UIConfirmationDialog(rect=pygame.Rect((250, 200), (300, 200)),
                                                                    manager=manager,
                                                                    window_title='Quit Confirmation',
                                                                    action_long_desc='Are you sure you want to quit?',
                                                                    action_short_name='Yes',
                                                                    blocking=True)

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == quit_button:
                    # 정말 나가겠냐고 묻는 메시지 박스 생성
                    confirm_dialog = pygame_gui.windows.UIConfirmationDialog(rect=pygame.Rect((250, 200), (300, 200)),
                                                                            manager=manager,
                                                                            window_title='Quit Confirmation',
                                                                            action_long_desc='Are you sure you want to quit?',
                                                                            action_short_name='Yes',
                                                                            blocking=True)
            elif event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                if event.ui_element == confirm_dialog:
                    running = False

        manager.process_events(event)

    manager.update(pygame.time.Clock().tick(60))

    screen.fill((0, 0, 0))
    manager.draw_ui(screen)

    pygame.display.update()

pygame.quit()
