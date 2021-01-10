import pygame,time,os,random,neat
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
    vel = 5
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
    def move(self):
        self.x -= self.vel
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
    vel = 5
    Width = base_img.get_width()
    img = base_img

    def __init__(self,y):
        self.y = y
        self.x1 = 0
        self.x2 = self.Width

    def move(self):
        self.x1 -= self.vel
        self.x2 -= self.vel

        if self.x1 + self.Width < 0:
            self.x1 = self.x2 + self.Width
        if self.x2 + self.Width < 0:
            self.x2 = self.x1 + self.Width

    def draw(self,win):
        win.blit(self.img,(self.x1,self.y))
        win.blit(self.img,(self.x2,self.y))
def draw_window(win,bird,pipes,base,score):
    win.blit(bg_img,(0,0))
    for pipe in pipes:
        pipe.draw(win)
    text = font.render("Score "+ str(score), True,(255,255,255))
    win.blit(text,(WIN_WIDTH - 10 - text.get_width(),10))
    base.draw(win)
    bird.draw(win)
    pygame.display.update()

def main():
    add_pipe = False
    bird = Bird(230,350)
    base = Base(730)
    score = 0
    clock = pygame.time.Clock()
    pipes = [Pipe(700)]
    run = True
    while run:
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        #bird.move()
        rem = []
        for pipe in pipes:
            if pipe.collide(bird):
                pass

                #print("collision")
            if pipe.x + pipe.pipe_top.get_width() < 0:
               rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(700))
            add_pipe = False
        for r in rem:
            pipes.remove(r)
        if bird.y + bird.img.get_height() >= 730:
            pass


        base.move()
        draw_window(win,bird,pipes,base,score)
    pygame.quit()
    quit("Manual ovverride")


main()
