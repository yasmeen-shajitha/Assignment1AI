import time
from random import randint
from collections import deque
from size_and_color import *
import pygame


def distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


class Monkey:
    def __init__(self):
        self.position = (0, 0)
        self.have_chair, self.have_stick, self.have_banana = False, False, False

    def move(self, pos):
        if self.position[0] < pos[0]:
            for _ in range(pos[0] - self.position[0]):
                y_monkey += ONE_STEP
                print('Down')
        else:
            for _ in range(self.position[0] - pos[0]):
                y_monkey -= ONE_STEP
                print('Up')

        if self.position[1] < pos[1]:
            for _ in range(pos[1] - self.position[1]):
                x_monkey += ONE_STEP
                print('Right')
        else:
            for _ in range(self.position[1] - pos[1]):
                x_monkey -= ONE_STEP
                print('Left')
        self.position = pos

    def pick_chair(self, map):
        if map.chair == self.position:
            self.have_chair = True
            print('Have chair')

    def pick_stick(self, map):
        if map.stick == self.position:
            self.have_stick = True
            print('Have stick')

    def take_banana(self, map):
        if map.banana == self.position and self.have_stick and self.have_chair:
            print('Have banana')


class Main:

    def __init__(self) -> None:
        self.grid = [[0 for _ in range(ROW)] for _ in range(COLUMN)]
        self.visited = set()
        self.monkey, self.chair, self.stick, self.banana =(0, 0), (0, 0), (0, 0), (0, 0)

    def set_location_object(self):
        # set the chair as number 1, stick as number 2 and bananas as number 3
        visited = set()
        yet_created, is_created_chair, is_created_stick, is_created_banana = False, False, False, False
        while not yet_created:
            temp_row, temp_column = randint(0, ROW - 1), randint(0, COLUMN - 1)
            if (temp_row, temp_column) in visited:
                continue
            visited.add((temp_row, temp_column))

            if not is_created_chair:
                self.grid[temp_row][temp_column] = 1
                is_created_chair = True

            elif not is_created_stick:
                self.grid[temp_row][temp_column] = 2
                is_created_stick = True
            else:
                self.grid[temp_row][temp_column] = 3
                is_created_banana = True

            if is_created_chair and is_created_stick and is_created_banana:
                yet_created = True

    def get_all_object(self):
        return self.chair != (0, 0) and self.stick != (0, 0) and self.banana != (0, 0)

    def find_location_object(self, rows, columns):
        queue = deque()
        self.visited.add((rows, columns))
        queue.append((rows, columns))
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        while queue:
            temp_row, temp_column = queue.popleft()
            if self.get_all_object():
                break
            for direct_row, direct_column in directions:
                r, c = temp_row + direct_row, temp_column + direct_column
                if (r not in range(ROW)
                        or c not in range(COLUMN)):
                    continue

                if (self.grid[r][c] == 0
                        and (r, c) not in self.visited):
                    queue.append((r, c))
                    self.visited.add((r, c))

                if self.get_all_object():
                    break
                if self.grid[r][c] == 1:
                    self.chair = (r, c)
                if self.grid[r][c] == 2:
                    self.stick = (r, c)
                if self.grid[r][c] == 3:
                    self.banana = (r, c)

    def pick_chair_first(self):
        return distance(self.monkey, self.chair) + distance(self.chair, self.stick) + distance(self.stick, self.banana)

    def pick_stick_first(self):
        return distance(self.monkey, self.stick) + distance(self.stick, self.chair) + distance(self.chair, self.banana)

    def movement(self, player):
        if self.pick_chair_first() < self.pick_stick_first():
            player.move(self.chair)
            player.pick_chair(self)
            player.move(self.stick)
            player.pick_stick(self)
        else:
            player.move(self.stick)
            player.pick_stick(self)
            player.move(self.chair)
            player.pick_chair(self)

        player.move(self.banana)
        player.take_banana(self)


pygame.init()

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Monkey and Banana')

clock = pygame.time.Clock()

monkey = pygame.image.load('monkey.png')
chair = pygame.image.load('chair.png')
stick = pygame.image.load('stick.png')
banana = pygame.image.load('banana.png')
floor = pygame.image.load('floor.jpg')
icon = pygame.image.load('monkeyIcon.png')
up = pygame.image.load('up.png')
down = pygame.image.load('down.png')
right = pygame.image.load('right.png')
left = pygame.image.load('left.png')

pygame.display.set_icon(icon)


def quitgame():
    pygame.quit()
    quit()


def show_image(x, y, image):
    gameDisplay.blit(image, (x, y))


def text_object(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()


def button(msg, x, y, w, h, ic, ac, size, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))

    smallText = pygame.font.SysFont('Times New Roman', size)
    TextSurf, TextRect = text_object(msg, smallText)
    TextRect.center = (x + w/2, y + h/2)
    gameDisplay.blit(TextSurf, TextRect)


def finish():

    Finish = True

    while Finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
        largeText = pygame.font.SysFont('Times New Roman', 40)
        TextSurf, TextRect = text_object('CONGRATULATION! YOU WIN THE GAME', largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(TextSurf, TextRect)

        button('MENU', 150, 600, 100, 50, GREEN, BRIGHT_GREEN, 20, game_intro)

        button('QUIT', 550, 600, 100, 50, RED, BRIGHT_RED, 20, quitgame)

        pygame.display.update()
        clock.tick(30)


def game_intro():
    time.sleep(0.1)
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
        gameDisplay.fill(WHITE)
        largeText = pygame.font.SysFont('Times New Roman', 70)
        TextSurf, TextRect = text_object('MOKEY AND BANANA', largeText)
        TextRect.center = ((display_width/2), (display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        button('PLAY', 150, 600, 100, 50, GREEN, BRIGHT_GREEN, 20, game_loop)

        button('AUTO PLAY', 350, 600, 120, 50, GREEN, BRIGHT_GREEN, 20, autoplay)

        button('QUIT', 550, 600, 100, 50, RED, BRIGHT_RED, 20, quitgame)

        pygame.display.update()
        clock.tick(30)


def autoplay():
    game_loop(True)


def game_loop(auto_play=False):
    play = Main()
    player = Monkey()
    play.set_location_object()
    for i in play.grid: print(i)
    play.find_location_object(0, 0)
    print(play.chair, play.stick, play.banana)
    pos_chair = play.chair
    pos_stick = play.stick
    pos_banana = play.banana
    hint = False

    x_monkey, y_monkey = 0, 0
    x_chair, y_chair = pos_chair[1] * 100, pos_chair[0] * 100
    x_stick, y_stick = pos_stick[1] * 100, pos_stick[0] * 100
    x_banana, y_banana = pos_banana[1] * 100, pos_banana[0] * 100
    left_hint, right_hint, down_hint, up_hint = False, False, False, False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if auto_play:
                continue

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_LEFT and x_monkey >= MIN_LENGTH:
                x_monkey -= ONE_STEP
            elif event.key == pygame.K_RIGHT and x_monkey < MAX_LENGTH:
                x_monkey += ONE_STEP
            elif event.key == pygame.K_UP and y_monkey >= MIN_LENGTH:
                y_monkey -= ONE_STEP
            elif event.key == pygame.K_DOWN and y_monkey < MAX_LENGTH:
                y_monkey += ONE_STEP
            elif event.key == pygame.K_h:
                hint = True
                play.monkey = (x_monkey // 100, y_monkey // 100)
                print(play.pick_stick_first(), play.pick_chair_first())
                if not player.have_chair and not player.have_stick:
                    if play.pick_stick_first() < play.pick_chair_first():

                        #Pick stick
                        if x_monkey == x_stick:
                            if y_monkey < y_stick:
                                down_hint = True
                            elif y_monkey > y_stick:
                                up_hint = True
                        elif x_monkey < x_stick:
                            right_hint = True
                        else:
                            left_hint = True

                    else:
                        # Pick chair
                        if x_monkey == x_chair:
                            if y_monkey < y_chair:
                                down_hint = True
                            elif y_monkey > y_chair:
                                up_hint = True
                        elif x_monkey < x_chair:
                            right_hint = True
                        else:
                            left_hint = True

                elif player.have_stick and not player.have_chair:
                    # Pick chair
                    if x_monkey == x_chair:
                        if y_monkey < y_chair:
                            down_hint = True
                        elif y_monkey > y_chair:
                            up_hint = True
                    elif x_monkey < x_chair:
                        right_hint = True
                    else:
                        left_hint = True

                elif player.have_chair and not player.have_stick:
                    # Pick stick
                    if x_monkey == x_stick:
                        if y_monkey < y_stick:
                            down_hint = True
                        elif y_monkey > y_stick:
                            up_hint = True
                    elif x_monkey < x_stick:
                        right_hint = True
                    else:
                        left_hint = True

                else:
                    #Pick banana
                    if x_monkey == x_banana:
                        if y_monkey < y_banana:
                            down_hint = True
                        elif y_monkey > y_banana:
                            up_hint = True
                    elif x_monkey < x_banana:
                        right_hint = True
                    else:
                        left_hint = True

            # print(down_hint, right_hint, left_hint, up_hint)

        gameDisplay.blit(floor, (0, 0))

        if x_monkey == x_stick and y_monkey == y_stick:
            player.have_stick = True

        if x_monkey == x_chair and y_monkey == y_chair:
            player.have_chair = True

        if x_monkey == x_banana and y_monkey == y_banana and player.have_chair and player.have_stick:
            player.have_banana = True

        if not player.have_stick:
            show_image(x_stick, y_stick, stick)
        if not player.have_chair:
            show_image(x_chair, y_chair, chair)
        show_image(x_monkey, y_monkey, monkey)
        if not player.have_banana:
            show_image(x_banana, y_banana, banana)
        else:
            finish()

        if auto_play:
            if play.pick_stick_first() < play.pick_chair_first():
                if not player.have_stick:
                    if x_monkey != x_stick:
                        x_monkey += ONE_STEP
                        time.sleep(0.5)
                    elif y_monkey != y_stick:
                        y_monkey += ONE_STEP
                        time.sleep(0.5)
                elif not player.have_chair:
                    if x_monkey == x_chair:
                        if y_monkey < y_chair:
                            y_monkey += ONE_STEP
                        else:
                            y_monkey -= ONE_STEP
                    elif x_monkey < x_chair:
                        x_monkey += ONE_STEP
                    else:
                        x_monkey -= ONE_STEP
                    time.sleep(0.5)
            elif not player.have_chair:
                if x_monkey != x_chair:
                    x_monkey += ONE_STEP
                    time.sleep(0.5)
                elif y_monkey != y_chair:
                    y_monkey += ONE_STEP
                    time.sleep(0.5)
            elif not player.have_stick:
                if x_monkey == x_stick:
                    if y_monkey < y_stick:
                        y_monkey += ONE_STEP
                    else:
                        y_monkey -= ONE_STEP
                elif x_monkey < x_stick:
                    x_monkey += ONE_STEP
                else:
                    x_monkey -= ONE_STEP
                time.sleep(0.5)
            if player.have_stick and player.have_chair:
                if x_monkey != x_banana:
                    if x_monkey < x_banana:
                        x_monkey += ONE_STEP
                    else:
                        x_monkey -= ONE_STEP
                    time.sleep(0.5)
                elif y_monkey < y_banana:
                    y_monkey += ONE_STEP
                else:
                    y_monkey -= ONE_STEP
                time.sleep(0.5)

        if up_hint:
            show_image(x_monkey, y_monkey - ONE_STEP, up)
            up_hint = False
        elif down_hint:
            show_image(x_monkey, y_monkey + ONE_STEP, down)
            down_hint = False
        elif left_hint:
            show_image(x_monkey - ONE_STEP, y_monkey, left)
            left_hint = False
        elif right_hint:
            show_image(x_monkey + ONE_STEP, y_monkey, right)
            right_hint = False

        pygame.display.update()
        if hint:
            time.sleep(1)
            hint = False
        clock.tick(60)


if __name__ == "__main__":
    game_intro()