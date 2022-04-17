import pygame,random
pygame.init()

win=pygame.display.set_mode((800,500))
pygame.display.set_caption("Rocket game")
clock=pygame.time.Clock()

surface=pygame.image.load("sky.png").convert()
rocket=pygame.image.load("rocket.png").convert_alpha()
rocket_rect=rocket.get_rect(midtop=(400,350))
bullet=pygame.image.load("bullet img.png").convert_alpha()
alien=pygame.image.load("alien.png").convert_alpha()
text=pygame.font.Font(None,60)
text2=pygame.font.Font(None,40)
bullet_sound=pygame.mixer.Sound('bullet.mp3')
blast_sound=pygame.mixer.Sound('blast.mp3')
explosion=[pygame.image.load(f"exp{i}.png")for i in range(1,6)]

class blast:
    def __init__(self,explosion,x,y,count):
        self.explosion=explosion
        self.x=x
        self.y=y
        self.count=count
        self.exp_rect=self.explosion[count].get_rect(center=(x,y))
    def draw(self,win):
        win.blit(self.explosion[int(self.count)],self.exp_rect)
                 
class spaceship:
    def __init__(self,alien,neg,hit):
        self.alien=alien
        self.neg=neg
        self.hit=hit
        self.alien_rect=self.alien.get_rect(center=(random.randint(150,650),0))
    def draw(self,win):
        win.blit(self.alien,self.alien_rect)        

class shoot:
    def __init__(self,x,bullet):
        self.bullet=bullet
        self.x=x
        self.bullet_rect=self.bullet.get_rect(midbottom=(self.x,350))
    def draw(self,win):
        win.blit(self.bullet,self.bullet_rect)

time=0
score=0
life=3
bullets=[]
aliens=[]
blasting=[]
active=True
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
        if active==False and event.type==pygame.MOUSEBUTTONDOWN:
            active=True
            time=0
            score=0
            life=3
            bullets=[]
            aliens=[]
            
    if active:
        if time%15==0:
            bullets.append(shoot(rocket_rect.midtop[0],bullet))
        for i in bullets:
            if i.bullet_rect.y>0:
                i.bullet_rect.y-=2
            else:
                bullets.remove(i)

        k=pygame.key.get_pressed()
        if k[pygame.K_LEFT] and rocket_rect.left>0:
            rocket_rect.x-=3
        if k[pygame.K_RIGHT] and rocket_rect.right<800:
            rocket_rect.x+=3
            
        if time%120==0:
            aliens.append(spaceship(alien,1,0))
            for i in aliens:
                i.neg=random.choice([-1,1])
        for i in aliens:
            if i.alien_rect.y<=500:
                i.alien_rect.y+=1
                i.alien_rect.x+=i.neg
                if i.alien_rect.left<0 : i.alien_rect.left=0
                elif i.alien_rect.right>800 : i.alien_rect.right=800
            else:
                aliens.remove(i)

        time_surface=text.render("time:"+str(int(time/60)),True,"grey")
        score_surface=text.render("score:"+str(score),True,"orange")
        life_surface=text.render("life:"+str(life),True,"red")
        
        win.blit(surface,(0,0))
        win.blit(time_surface,(25,450))
        win.blit(score_surface,(600,450))
        win.blit(life_surface,(25,25))
        win.blit(rocket,rocket_rect)

        for i in bullets:
            i.draw(win)
            for j in aliens:
                if j.alien_rect.colliderect(i.bullet_rect):
                    pygame.mixer.Sound.play(bullet_sound)
                    bullets.remove(i)
                    j.hit+=1
                    if j.hit==4:
                        aliens.remove(j)
                        blasting+=[blast(explosion,j.alien_rect.centerx,j.alien_rect.centery,0)]
                        pygame.mixer.Sound.play(blast_sound)
                        score+=1
        for i in aliens:
            i.draw(win)
            if i.alien_rect.y==500:
                life-=1
        if life==0:
            active=False
        time+=1
        for i in blasting:
            i.draw(win)
            i.count+=0.1
            if i.count>=5:
                blasting.remove(i)
    else:
        win.fill("light yellow")
        out=text.render("GAME OVER!!",True,"red")
        click=text2.render("tap on screen to play again",True,"dark green")
        time_surface=text2.render("time:"+str(int(time/60)),True,"grey")
        score_surface=text2.render("score:"+str(score),True,"orange")
        out_rect=out.get_rect(center=(400,100))
        time_rect=time_surface.get_rect(center=(400,150))
        score_rect=score_surface.get_rect(center=(400,200))
        click_rect=click.get_rect(center=(400,300))
        pygame.draw.rect(win,"black",out_rect)
        win.blit(out,out_rect)
        win.blit(time_surface,time_rect)
        win.blit(score_surface,score_rect)
        win.blit(click,click_rect)
    pygame.display.update()
    clock.tick(60)
