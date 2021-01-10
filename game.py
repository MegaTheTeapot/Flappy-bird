import pygame,time,os,random,neat,threading
from googleapiclient.discovery import build
key = "youtubeApi key"
service = build("youtube","v3",developerKey=key)

pygame.font.init()
WIN_WIDTH = 500
WIN_HEIGHT = 800
win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))]
bg_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))
pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
font = pygame.font.SysFont("comicsans",50)
class Bird:
    imgs = bird_images
    max_rotation = 25
    rot_vel = 20
    animation_time = 5

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.imgs[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        d = self.vel*self.tick_count + 1.5*self.tick_count**2

        if d >= 16:
            d = 16
        if d < 0:
            d -= 2
        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
                if self.tilt < self.max_rotation:
                    self.tilt = self.max_rotation
                else:
                    if self.tilt > -90:
                        self.tilt -= self.rot_vel
    def draw(self,win):
        self.img_count += 1
        if self.img_count < self.animation_time:
            self.img = self.imgs[0]
        elif self.img_count < self.animation_time*2:
            self.img = self.imgs[1]
        elif self.img_count < self.animation_time*3:
            self.img = self.imgs[2]
        elif self.img_count < self.animation_time*4:
            self.img = self.imgs[1]
        elif self.img_count < self.animation_time*5:
            self.img = self.imgs[0]
            self.img_count = 0
        if self.tilt <= -80:
            self.img = self.imgs[1]
            self.img_count = self.animation_time*2
        rotated_image = pygame.transform.rotate(self.img,self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x,self.y)).center)
        win.blit(rotated_image,new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
class Pipe:
    gap = 200

    def __init__(self,x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.pipe_top = pygame.transform.flip(pipe_img, False, True)
        self.pipe_bottom = pipe_img

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.pipe_top.get_height()
        self.bottom = self.height + self.gap
    def move(self,vel):
        self.x -= vel
    def draw(self,win):
        win.blit(self.pipe_top,(self.x,self.top))
        win.blit(self.pipe_bottom,(self.x,self.bottom))
    def collide(self,bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.pipe_top)
        bottom_mask = pygame.mask.from_surface(self.pipe_bottom)

        top_offset = (self.x - bird.x,self.top - round(bird.y))
        bottom_offset = (self.x - bird.x,self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask,bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        if t_point or b_point:
            return True
        else:
            return False

class Base:

    Width = base_img.get_width()
    img = base_img

    def __init__(self,y):
        self.y = y
        self.x1 = 0
        self.x2 = self.Width

    def move(self,vel):
        self.x1 -= vel
        self.x2 -= vel

        if self.x1 + self.Width < 0:
            self.x1 = self.x2 + self.Width
        if self.x2 + self.Width < 0:
            self.x2 = self.x1 + self.Width

    def draw(self,win):
        win.blit(self.img,(self.x1,self.y))
        win.blit(self.img,(self.x2,self.y))
def draw_window(win,birds,pipes,base,score,vel,likes):
    win.blit(bg_img,(0,0))
    for pipe in pipes:
        pipe.draw(win)
    text = font.render("Score:"+ str(score), True,(255,255,255))
    win.blit(text,(WIN_WIDTH - 10 - text.get_width(),10))
    speed = font.render("Speed:" + str(vel),True,(255,255,255))
    win.blit(speed,(WIN_WIDTH - 360 - speed.get_width(),10))
    likes_ = font.render("Likes:" + str(likes),True,(255,255,255))
    win.blit(likes_,(WIN_WIDTH - 360 - likes_.get_width(),50))
    base.draw(win)
    for bird in birds:
        bird.draw(win)
    pygame.display.update()

def main(genomes,config):
    ge = []
    nets = []
    birds = []





    for _,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        birds.append(Bird(230,350))
        g.fitness = 0
        ge.append(g)

    add_pipe = False

    base = Base(730)
    score = 0
    clock = pygame.time.Clock()
    pipes = [Pipe(700)]
    run = True
    timer = 400
    while run:
        clock.tick(30)
        if timer == 400:
            response = service.videos().list(id = stream id",part = "statistics").execute()
            timer = 0

        likes = response["items"][0]["statistics"]["likeCount"]
        likes_ : int = 3
        for i in range(int(likes)):
            likes_ += 1
        vel : int = int(likes_)
        if likes == 0:
            vel = 3
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit("Manual ovverride")
        timer += 1

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].pipe_top.get_width():
                pipe_ind = 1
        else:
            run = False
            break
        for x,bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            output = nets[x].activate((bird.y,abs(bird.y - pipes[pipe_ind].height),abs(bird.y - pipes[pipe_ind].bottom)))
            if output[0] > 0.5:
                bird.jump()

        rem = []
        for pipe in pipes:
            for x,bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                #print("collision")
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
            if pipe.x + pipe.pipe_top.get_width() < 0:
               rem.append(pipe)
            pipe.move(vel)

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(700))
            add_pipe = False
        for r in rem:
            pipes.remove(r)
        for x,bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)


        base.move(vel)
        draw_window(win,birds,pipes,base,score,vel,likes)



#main()


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,neat.DefaultStagnation,
                                config_path)
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(main)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config-feedforward.txt")
    run(config_path)
