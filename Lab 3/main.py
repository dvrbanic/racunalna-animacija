import math
import random
import time
import pygame

color_black = (0, 0, 0)
color_table = (70, 160, 126)
color_white = (255, 255, 255)
color_red = (255, 0, 0)
color_yellow = (255, 255, 0)
color_green = (0, 255, 0)
color_blue = (0, 0, 255)
color_light_sky_blue = (135, 206, 250)
color_navy = (0, 0, 128)
color_slate_blue = (106, 90, 205)
color_medium_slate_blue = (123, 104, 238)


class Ball:
    def __init__(self, ):
        self.x = width / 2
        self.y = 80 + (height - 80) / 2
        self.size = 10
        self.color = color_white
        self.speed = 2
        side = random.randint(0, 1)
        if side == 0:
            angle_deg = random.randint(45, 135)
        else:
            angle_deg = -random.randint(45, 135)
        self.angle = math.radians(angle_deg)

    def display(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

    def move(self):
        self.x += math.sin(self.angle) * self.speed
        self.y += math.cos(self.angle) * self.speed

    def bounce(self):
        if self.y > (height - 5 - self.size):
            self.angle = math.pi - self.angle
            return 1
        elif self.y < (80 + self.size):
            self.angle = math.pi - self.angle
            return 1
        elif self.x > width - 5:
            player.score += 1
            if player.score == 7:
                return 0
            return -1
        elif self.x < 5:
            cpu.score += 1
            if cpu.score == 7:
                return 0
            return -1


class Player:
    def __init__(self):
        self.x = 15
        self.y = height / 2
        self.width = 10
        self.height = 90
        self.score = 0

    def display(self):
        pygame.draw.rect(screen, color_white, pygame.Rect(self.x, self.y, self.width, self.height))

    def move(self):
        (mouse_x, mouse_y) = pygame.mouse.get_pos()
        if 80 < mouse_y - self.height / 2 < height - self.height - 5:
            self.y = mouse_y - self.height / 2
        elif mouse_y - self.height / 2 <= 80:
            self.y = 80
        elif mouse_y >= height - self.height - 5:
            self.y = height - self.height - 5

    def collide_with_ball(self):
        if self.x + ball.size < ball.x < self.x + self.width + ball.size:
            if self.y - ball.size <= ball.y < self.y + self.height * 0.15 + ball.size:
                ball.angle = math.radians(random.randint(125, 145))
                ball.x = self.x + self.width + ball.size + 1
                if ball.speed == 1:
                    ball.speed = 1.5
                elif ball.speed == 1.5:
                    ball.speed = 2
                elif ball.speed == 2:
                    ball.speed = 2.5
                elif ball.speed == 2.5:
                    ball.speed = 3
            elif self.y + self.height * 0.15 + ball.size <= ball.y < self.y + self.height * 0.4 + ball.size:
                ball.angle = math.radians(random.randint(105, 120))
                ball.x = self.x + self.width + ball.size + 1
            elif self.y + self.height * 0.4 + ball.size <= ball.y < self.y + self.height * 0.5 + ball.size:
                ball.angle = math.radians(random.randint(90, 100))
                ball.x = self.x + self.width + ball.size + 1
            elif self.y + self.height * 0.5 + ball.size <= ball.y < self.y + self.height * 0.6 + ball.size:
                ball.angle = math.radians(random.randint(80, 90))
                ball.x = self.x + self.width + ball.size + 1
            elif self.y + self.height * 0.6 + ball.size <= ball.y < self.y + self.height * 0.85 + ball.size:
                ball.angle = math.radians(random.randint(60, 75))
                ball.x = self.x + self.width + ball.size + 1
            elif self.y + self.height * 0.85 + ball.size <= ball.y < self.y + self.height * 1.0 + ball.size:
                ball.angle = math.radians(random.randint(35, 55))
                ball.x = self.x + self.width + ball.size + 1
                if ball.speed == 1:
                    ball.speed = 1.5
                elif ball.speed == 1.5:
                    ball.speed = 2
                elif ball.speed == 2:
                    ball.speed = 2.5
                elif ball.speed == 2.5:
                    ball.speed = 3


class CPU:
    def __init__(self):
        self.x = width - 25
        self.y = height / 2
        self.width = 10
        self.height = 90
        self.score = 0

    def display(self):
        pygame.draw.rect(screen, color_white, pygame.Rect(self.x, self.y, self.width, self.height))

    def move(self, moving_speed):
        if math.radians(1) < ball.angle < math.radians(180):
            if self.y > ball.y - ball.size and self.y > 81.5:
                self.y -= moving_speed
            elif self.y + self.height < ball.y + ball.size and self.y + self.height < height - 6.5:
                self.y += moving_speed

    def collide_with_ball(self):
        if self.x - ball.size < ball.x < self.x and self.y - ball.size < ball.y < self.y + self.height + ball.size:
            ball.angle = - ball.angle
            ball.x = self.x - self.width - ball.size - 1


class Booster:
    def __init__(self):
        self.size = 25
        self.x = random.randint(250, 1030)
        self.y = random.randint(120, 660)
        powers = ["Bigger paddle", "Smaller paddle", "Faster ball", "Slower ball"]
        self.power = powers[random.randint(0, 3)]
        self.collided = False


class Booster_list:
    def __init__(self):
        self.boosters = []

    def display(self):
        for bstr in self.boosters:
            if bstr.power == "Bigger paddle":
                pygame.draw.circle(screen, color_yellow, (bstr.x, bstr.y), bstr.size)
                # font = pygame.font.Font('freesansbold.ttf', 10)
                # text = font.render('+ paddle', True, color_black)
                # text_rect = text.get_rect()
                # text_rect.center = (bstr.x, bstr.y)
                # screen.blit(text, text_rect)
            elif bstr.power == "Smaller paddle":
                pygame.draw.circle(screen, color_green, (bstr.x, bstr.y), bstr.size)
                # font = pygame.font.Font('freesansbold.ttf', 10)
                # text = font.render('- paddle', True, color_black)
                # text_rect = text.get_rect()
                # text_rect.center = (bstr.x, bstr.y)
                # screen.blit(text, text_rect)
            elif bstr.power == "Faster ball":
                pygame.draw.circle(screen, color_red, (bstr.x, bstr.y), bstr.size)
                # font = pygame.font.Font('freesansbold.ttf', 10)
                # text = font.render('+ speed', True, color_black)
                # text_rect = text.get_rect()
                # text_rect.center = (bstr.x, bstr.y)
                # screen.blit(text, text_rect)
            elif bstr.power == "Slower ball":
                pygame.draw.circle(screen, color_blue, (bstr.x, bstr.y), bstr.size)
                # font = pygame.font.Font('freesansbold.ttf', 10)
                # text = font.render('- speed', True, color_black)
                # text_rect = text.get_rect()
                # text_rect.center = (bstr.x, bstr.y)
                # screen.blit(text, text_rect)

    def collided(self):
        for bstr in self.boosters:
            dx = bstr.x - ball.x
            dy = bstr.y - ball.y
            distance = math.hypot(dx, dy)

            if distance < bstr.size + ball.size :
                bstr.collided = True
                if bstr.power == "Faster ball":
                    if ball.speed == 1:
                        ball.speed = 1.5
                    elif ball.speed == 1.5:
                        ball.speed = 2
                    elif ball.speed == 2:
                        ball.speed = 2.5
                    elif ball.speed == 2.5:
                        ball.speed = 3
                elif bstr.power == "Slower ball":
                    if ball.speed == 3:
                        ball.speed = 2.5
                    elif ball.speed == 2.5:
                        ball.speed = 2
                    elif ball.speed == 2:
                        ball.speed = 1.5
                    elif ball.speed == 1.5:
                        ball.speed = 1
                elif bstr.power == "Bigger paddle":
                    if player.height == 70:
                        player.height = 90
                    if player.height == 90:
                        player.height = 110
                elif bstr.power == "Smaller paddle":
                    if cpu.height == 110:
                        cpu.height = 90
                    if cpu.height == 90:
                        cpu.height = 70

    def create(self):
        self.boosters.append(Booster())

    def delete(self):
        if self.boosters:
            boosters_new = [bstr for bstr in self.boosters if bstr.collided is False]
            self.boosters = boosters_new


def set_header(player, cpu):
    font = pygame.font.Font('freesansbold.ttf', 28)
    text = font.render(f'Player score: {player.score}     CPU score: {cpu.score}', True, color_green)
    text_rect = text.get_rect()
    text_rect.center = (width * 0.33, 40)
    screen.blit(text, text_rect)

    font_bstr = pygame.font.Font('freesansbold.ttf', 10)

    pygame.draw.circle(screen, color_yellow, (960, 40), 25)
    text1 = font_bstr.render('+ paddle', True, color_black)
    text_rect1 = text1.get_rect()
    text_rect1.center = (960, 40)
    screen.blit(text1, text_rect1)

    pygame.draw.circle(screen, color_green, (1030, 40), 25)
    text2 = font_bstr.render('- paddle', True, color_black)
    text_rect2 = text2.get_rect()
    text_rect2.center = (1030, 40)
    screen.blit(text2, text_rect2)

    pygame.draw.circle(screen, color_red, (1100, 40), 25)
    text3 = font_bstr.render('+ speed', True, color_black)
    text_rect3 = text3.get_rect()
    text_rect3.center = (1100, 40)
    screen.blit(text3, text_rect3)

    pygame.draw.circle(screen, color_blue, (1170, 40), 25)
    text4 = font_bstr.render('- speed', True, color_black)
    text_rect4 = text4.get_rect()
    text_rect4.center = (1170, 40)
    screen.blit(text4, text_rect4)


def set_screen():
    global screen
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pong")
    screen.fill(color_black)
    pygame.draw.rect(screen, color_table, pygame.Rect(5, 80, width - 10, height - 85))


def set_screen_lobby():
    global screen
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pong")
    screen.fill(color_light_sky_blue)
    font = pygame.font.Font('freesansbold.ttf', 40)

    text = font.render('Select difficulty', True, color_navy)
    text_rect = text.get_rect()
    text_rect.center = (width / 2, 150)
    screen.blit(text, text_rect)


def select_difficulty():
    global running_game
    is_selecting = True

    while is_selecting:

        set_screen_lobby()
        font = pygame.font.Font('freesansbold.ttf', 40)

        (mouse_x, mouse_y) = pygame.mouse.get_pos()

        if (width / 2) - 100 <= mouse_x <= (width / 2) + 100 and 260 <= mouse_y <= 340:
            pygame.draw.rect(screen, color_medium_slate_blue, pygame.Rect((width / 2) - 100, 260, 200, 80))
        else:
            pygame.draw.rect(screen, color_slate_blue, pygame.Rect((width / 2) - 100, 260, 200, 80))

        if (width / 2) - 100 <= mouse_x <= (width / 2) + 100 and 360 <= mouse_y <= 440:
            pygame.draw.rect(screen, color_medium_slate_blue, pygame.Rect((width / 2) - 100, 360, 200, 80))
        else:
            pygame.draw.rect(screen, color_slate_blue, pygame.Rect((width / 2) - 100, 360, 200, 80))

        if (width / 2) - 100 <= mouse_x <= (width / 2) + 100 and 460 <= mouse_y <= 540:
            pygame.draw.rect(screen, color_medium_slate_blue, pygame.Rect((width / 2) - 100, 460, 200, 80))
        else:
            pygame.draw.rect(screen, color_slate_blue, pygame.Rect((width / 2) - 100, 460, 200, 80))

        text1 = font.render('Easy', True, color_navy)
        text_rect1 = text1.get_rect()
        text_rect1.center = (width / 2, 300)
        screen.blit(text1, text_rect1)

        text2 = font.render('Medium', True, color_navy)
        text_rect2 = text2.get_rect()
        text_rect2.center = (width / 2, 400)
        screen.blit(text2, text_rect2)

        text3 = font.render('Hard', True, color_navy)
        text_rect3 = text3.get_rect()
        text_rect3.center = (width / 2, 500)
        screen.blit(text3, text_rect3)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game = False
                is_selecting = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if (width / 2) - 100 <= mouse_x <= (width / 2) + 100 and 260 <= mouse_y <= 340:
                    return 1
                if (width / 2) - 100 <= mouse_x <= (width / 2) + 100 and 360 <= mouse_y <= 440:
                    return 1.5
                if (width / 2) - 100 <= mouse_x <= (width / 2) + 100 and 460 <= mouse_y <= 540:
                    return 3


if __name__ == "__main__":
    old_time = time.time()
    running_game = True
    bounce_ret = -1
    width, height = 1280, 720

    pygame.init()

    player = Player()
    cpu = CPU()
    ball = Ball()
    boosters = Booster_list()

    difficulty = select_difficulty()

    while running_game:
        set_screen()
        set_header(player, cpu)

        if bounce_ret == -1:
            ball = Ball()
            bounce_ret = 1
        elif bounce_ret == 0:
            running_game = False

        if time.time() - old_time > random.randint(10, 20) and len(boosters.boosters) < 3:
            boosters.create()
            old_time = time.time()

        boosters.collided()
        boosters.delete()
        boosters.display()

        ball.move()
        bounce_ret = ball.bounce()
        ball.display()

        player.move()
        player.display()
        player.collide_with_ball()

        cpu.move(difficulty)
        cpu.display()
        cpu.collide_with_ball()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game = False
