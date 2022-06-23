import pygame, sys, random
pygame.display.set_caption('Snake Game')

screen_width = 600
screen_height = 600

# Karelerin Pixel Olarak Boyutu
gridsize = 20
# Karelerin Width ve Height Değerlerine Göre EKranda Kaç Adet Kare Olacağını Hesaplayan Kod
grid_width = int(screen_width / gridsize)
grid_height = int(screen_height / gridsize)

# Renkler
light_green = (0, 170, 140)
dark_green = (0, 140, 120)
food_color = (255, 200, 0)
snake_color = (34, 34, 34)

# Hareket İşlemleri
up = (0, -1)
down = (0, 1)
right = (1, 0)
left = (-1, 0)


# Yılan Objesi Oluşturmak İçin Class
class SNAKE:
    def __init__(self):
        self.positions = [((screen_width/2),(screen_height/2))]
        self.length = 1
        self.direction = random.choice([up, down, right, left])
        self.color = snake_color
        self.score = 0

    def draw(self, surface):
        for p in self.positions:
            rect = pygame.Rect((p[0], p[1]), (gridsize, gridsize))
            pygame.draw.rect(surface, self.color, rect)

    def move(self):
        current = self.positions[0]
        x, y = self.direction
        new = ((current[0] + (x * gridsize)), (current[1] + (y * gridsize)))

        if new[0] in range(0, screen_width) and new[1] in range(0, screen_height) and not new in self.positions[2:]:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
        else:
            self.reset()

    def reset(self):
        self.length = 1
        self.positions = [((screen_width/2),(screen_height/2))]
        self.direction = random.choice([up, down, right, left])
        self.score = 0

    def handle_keys(self):
        # Çıkış Yapılıp Yapılmadığını Kontrol Ettik
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)

    def turn(self, direction):
        if (direction[0] * -1, direction[1] * -1) == self.direction:
            return
        else:
            self. direction = direction


# Food Objesi Oluşturmak İçin Class
class FOOD:
    def __init__(self):
        self.position = (0, 0)
        self.color = food_color
        self.random_position()

    # Random Bir Yerde Çizilmesini Sağlayan Kod Satırı
    def random_position(self):
        self.position = (random.randint(0, grid_width-1)*gridsize, random.randint(0,grid_height-1)*gridsize)

    # PyGame İle Çizilmesini Sağlayan Kod Satırı
    def draw(self, surface):
        rect = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, self.color, rect)


def drawGrid(surface):
    # Ekranımızı Bir Açık Bir Koyu Renge Boyamak İçin For Dönügüsü Kullandık
    # pygame.draw methodu ile çizme işlemi gerçekleştirildi
    # pygame.Rect methodu ile objeler oluşturuluyor
    for x in range(0, int(grid_width)):
        for y in range(0, int(grid_height)):
            if(x + y) % 2 == 0:
                light = pygame.Rect((x * gridsize, y * gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, light_green, light)
            else:
                dark = pygame.Rect((x * gridsize, y * gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, dark_green, dark)


def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 25)
    surface = pygame.Surface(screen.get_size()) # pygame.Surface komutu ile bir yüzey oluşturduk
    surface = surface.convert()

    food = FOOD()
    snake = SNAKE()

    while True:

        # Güncelleme ve Çizilmesi Gereken Nesnelerin Çizilmesini Sağladık
        clock.tick(10)
        snake.handle_keys()
        snake.move()
        drawGrid(surface)
        if snake.positions[0] == food.position:
            snake.length += 1
            snake.score += 1
            food.random_position()
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        score_text = font.render("Score: {0}".format(snake.score), True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        pygame.display.update()


main()