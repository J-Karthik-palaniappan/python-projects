import pygame,random,time
pygame.init()
from PIL import Image

tile_size=45
nlev=4
winw=900
pygame.display.set_caption("land")
clock=pygame.time.Clock()

class maingame():
    def __init__(self):
        self.choice=1
        self.score=0
        self.life=[1,1,1,1]
        self.die_sound=pygame.mixer.Sound('sounds/die_sound.wav')
        self.win_sound=pygame.mixer.Sound('sounds/win_sound.wav')
        self.final_sound=pygame.mixer.Sound('sounds/final_sound.wav')
        self.setup()
        self.run()
        
    def setup(self):
        mainmap=Image.open(f'maps/map{self.choice}.png','r')
        colormap=Image.open('maps/colormap.png','r')
        pix=list(mainmap.getdata())
        colors=list(colormap.getdata())
        self.land=['']
        c=row=0
        for i in pix:
            c+=1
            if i in colors:
                self.land[row]+=str(colors.index(i))
            else :self.land[row]+=' '
            if(c%mainmap.width==0):
                self.land.append('')
                row+=1
        del self.land[-1]
        self.win=pygame.display.set_mode((winw,tile_size*len(self.land)))

    def run(self):
        self.lvl=level(self.land,self.win,self.score,self.life,self.choice)
        img=pygame.transform.scale(pygame.image.load("maps/background.jpg").convert(),(winw,tile_size*len(self.land)))
        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    exit()
            self.win.blit(img,(0,0))
            self.lvl.run()
            pygame.display.update()
            self.nextlvl()
            clock.tick(60)

    def nextlvl(self):
        if self.lvl.wongame:
            if self.choice<nlev:
                self.choice+=1
                self.score=self.lvl.score
                self.life=self.lvl.life
                pygame.mixer.Sound.play(self.win_sound)
                self.setup()
                self.run()
            else:
                time.sleep(1)
                pygame.mixer.Sound.play(self.final_sound)
                time.sleep(6)
                pygame.quit()
                exit()
        
        elif self.lvl.lostgame:
            time.sleep(1)
            pygame.mixer.Sound.play(self.die_sound)
            time.sleep(3)
            pygame.quit()
            exit()

class life(pygame.sprite.Sprite):
    def __init__(self,x,count):
        pygame.sprite.Sprite.__init__(self)
        self.importing()
        self.count=count
        self.x=x
        self.anim_speed=0.08
        self.image=self.life[self.count]
        self.rect=self.image.get_rect(x=self.x,y=10)

    def importing(self):
        self.life={}
        for i in range(1,4):
            self.life[i]=pygame.transform.scale(pygame.image.load(f"tiles/life{i}.png").convert_alpha(),(tile_size,tile_size))

    def reduce_life(self):
        self.count+=self.anim_speed
        self.image=self.life[int(self.count)]

class patch(pygame.sprite.Sprite):
    def __init__(self,x,y,state):
        pygame.sprite.Sprite.__init__(self)
        self.importing()
        self.state=state
        self.image=self.tiles[self.state]
        self.x=x
        self.y=y
        self.rect=self.image.get_rect(x=self.x,y=self.y)

    def importing(self):
        self.tiles={}
        for i in '0156':
            self.tiles[i]=pygame.transform.scale(pygame.image.load(f"tiles/{i}.png").convert_alpha(),(tile_size,tile_size))
        self.tiles['tree1']=pygame.transform.scale(pygame.image.load("tiles/tree1.png").convert_alpha(),(tile_size*3//2,tile_size*3//2))
        self.tiles['tree2']=pygame.transform.scale(pygame.image.load("tiles/tree2.png").convert_alpha(),(tile_size*4//3,tile_size*2))
        self.tiles['grass1']=pygame.transform.scale(pygame.image.load("tiles/grass1.png").convert_alpha(),(tile_size,tile_size//2))
        self.tiles['grass2']=pygame.transform.scale(pygame.image.load("tiles/grass2.png").convert_alpha(),(tile_size,tile_size//2))
        
    def update(self,vel):
        self.rect.x+=vel

class coin(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.x=x
        self.y=y
        self.image=pygame.transform.scale(pygame.image.load("tiles/2.png").convert_alpha(),(tile_size//3,tile_size//3))
        self.rect=self.image.get_rect(x=self.x,y=self.y)

    def update(self,vel):
        self.rect.x+=vel

class enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.importing()
        self.count=0
        self.anim_speed=0.08
        self.image=self.tiles[self.count]
        self.x=x
        self.y=y
        self.direction=pygame.math.Vector2(0,0)
        self.rect=self.image.get_rect(x=self.x,y=self.y)
        self.direction.x=random.choice([1,-1])
        self.vel=1
        self.dead=False

    def importing(self):
        self.tiles=[]
        for i in range(1,4):
            self.tiles.append(pygame.transform.scale(pygame.image.load(f"tiles/E{i}.png").convert_alpha(),(tile_size*4//5,tile_size*4//5)))

    def animate(self):
        self.count+=self.anim_speed
        anim=self.tiles
        if self.count>=len(anim):
            self.count=0
        if self.direction.x<0:
            self.image=anim[int(self.count)]
        else:
            self.image=pygame.transform.flip(anim[int(self.count)],True,False)

    def die(self):
        self.dead=True
        self.count=1
        self.anim_speed=0
        self.vel=0
            
    def update(self,vel):
        self.animate()
        self.rect.x+=vel

class player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.importing()
        self.count=0
        self.anim_speed=0.08
        self.state="idle"
        self.face="right"
        self.image=self.animations[self.state][self.count]
        self.x=x
        self.y=y
        self.direction=pygame.math.Vector2(0,0)
        self.rect=self.image.get_rect(x=self.x,y=self.y)
        self.vel=tile_size/13
        self.gravity=tile_size/128
        self.jump_speed=-tile_size/4.3
        self.jump_sound=pygame.mixer.Sound('sounds/jump_sound.wav')

    def importing(self):
        self.animations={}
        self.animations["idle"]=[pygame.transform.scale(pygame.image.load(f"idle/img{i}.png").convert_alpha(),(tile_size-5,tile_size+5))for i in range(1,3)]
        self.animations["walk"]=[pygame.transform.scale(pygame.image.load(f"walk/img{i}.png").convert_alpha(),(tile_size-5,tile_size+5))for i in range(1,3)]
        self.animations["fall"]=[pygame.transform.scale(pygame.image.load("jump/fall.png").convert_alpha(),(tile_size-5,tile_size+5))]
        self.animations["jump"]=[pygame.transform.scale(pygame.image.load("jump/jump.png").convert_alpha(),(tile_size-5,tile_size+5))]

    def animate(self):
        self.count+=self.anim_speed
        anim=self.animations[self.state]
        if self.count>=len(anim):
            self.count=0
        if self.face=="right":
            self.image=anim[int(self.count)]
        else:
            self.image=pygame.transform.flip(anim[int(self.count)],True,False)

    def state_find(self):
        if self.direction.y<0:
            self.state="jump"
        elif self.direction.y>1:
            self.state="fall"
        else:
            if self.direction.x!=0:
                self.state="walk"
            else:
                self.state="idle"
            
    def userinput(self):
        keys=pygame.key.get_pressed()
        self.direction.x=0
        if keys[pygame.K_LEFT] and self.rect.left>self.vel:
            self.direction.x=-1
            self.face="left"
        if keys[pygame.K_RIGHT] and self.rect.right<winw-self.vel:
            self.direction.x=1
            self.face="right"

    def gravity_motion(self):
        self.direction.y+=self.gravity
        self.rect.y+=self.direction.y

    def jump(self,enemy=False):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or enemy:
            pygame.mixer.Sound.play(self.jump_sound)
            self.direction.y=self.jump_speed
            
    def update(self):
        self.userinput()
        self.state_find()
        self.animate()
        


class level():
    def __init__(self,land,win,score,life,choice):
        self.win=win
        self.world_shift=0
        self.score=score
        self.life=life
        self.choice=choice
        self.hit_sound=pygame.mixer.Sound('sounds/hit_sound.wav')
        self.coin_sound=pygame.mixer.Sound('sounds/coin_sound.mp3')
        self.land=land
        self.setup(self.land)
        self.wongame=False
        self.lostgame=False

    def setup(self,land):
        self.land_grp=pygame.sprite.Group()
        self.player_grp=pygame.sprite.GroupSingle()
        self.coin_grp=pygame.sprite.Group()
        self.enemy_grp=pygame.sprite.Group()
        self.stop_grp=pygame.sprite.Group()
        self.health_grp=pygame.sprite.Group()
        self.background_grp=pygame.sprite.Group()
        for i in range(len(self.life)-1,-1,-1):
            self.health_grp.add(life(tile_size*i,self.life[i]))
        for i in range(len(land)):
            for j in range(len(land[i])):
                if land[i][j]=="4":
                    man=player(tile_size*j,tile_size*i)
                    self.player_grp.add(man)
                elif land[i][j]=='2':
                    c=coin(tile_size*j+tile_size//4,tile_size*i+tile_size//2)
                    self.coin_grp.add(c)
                elif land[i][j]=='3':
                    alien=enemy(tile_size*j,tile_size*i+tile_size//4)
                    self.enemy_grp.add(alien)
                elif land[i][j]=='5':
                    stp=patch(tile_size*j,tile_size*i,land[i][j])
                    self.stop_grp.add(stp)
                elif land[i][j]!=' ':
                    piece=patch(tile_size*j,tile_size*i,land[i][j])
                    self.land_grp.add(piece)
                    if land[i][j]=='1':
                        if random.randint(1,5)==3:
                            piece=patch(tile_size*j-15,tile_size*(i)-tile_size*3//2,'tree1')
                            self.background_grp.add(piece)
                        elif random.randint(1,5)==3:
                            piece=patch(tile_size*j-15,tile_size*(i)-tile_size*2,'tree2')
                            self.background_grp.add(piece)
                        if random.randint(1,3)==3:
                            piece=patch(tile_size*j,tile_size*(i)-tile_size//2,'grass1')
                            self.background_grp.add(piece)
                        elif random.randint(1,3)==3:
                            piece=patch(tile_size*j,tile_size*(i)-tile_size//2,'grass2')
                            self.background_grp.add(piece)

    def scroll(self):
        man=self.player_grp.sprite
        if man.rect.centerx<200 and man.direction.x<0:
            self.world_shift=5
            man.vel=0
            for spt in self.land_grp.sprites():
                if spt.rect.left<0:
                    break
            else:
                self.world_shift=0
                man.vel=5
        elif man.rect.centerx>winw-200 and man.direction.x>0:
            self.world_shift=-5
            man.vel=0
            for spt in self.land_grp.sprites():
                if spt.rect.right>winw:
                    break
            else:
                self.world_shift=0
                man.vel=5
        else:
            self.world_shift=0
            man.vel=5
            

    def horizontal_collision(self):
        man=self.player_grp.sprite
        man.rect.x+=man.direction.x*man.vel
        for spt in self.land_grp.sprites():
            if spt.rect.colliderect(man.rect):
                if man.direction.x>0:
                    man.rect.right=spt.rect.left
                elif man.direction.x<0:
                    man.rect.left=spt.rect.right
                if spt.state=='6':
                    self.wongame=True

    def vertical_collision(self):
        man=self.player_grp.sprite
        man.gravity_motion()
        for spt in self.land_grp.sprites():
            if spt.rect.colliderect(man.rect):
                if man.direction.y>0:
                    man.rect.bottom=spt.rect.top
                    man.direction.y=0
                    man.jump()
                elif man.direction.y<0:
                    man.rect.top=spt.rect.bottom
                    man.direction.y=0
                if spt.state=='6':
                    self.wongame=True

    def coin_collision(self):
        man=self.player_grp.sprite
        for spt in self.coin_grp.sprites():
            if spt.rect.colliderect(man.rect):
                self.coin_grp.remove(spt)
                pygame.mixer.Sound.play(self.coin_sound)
                self.score+=1

    def enemy_stop_collision(self):
        for alien in self.enemy_grp.sprites():
            for spt in self.stop_grp.sprites():
                if alien.rect.colliderect(spt.rect):
                    if alien.direction.x==1:
                        alien.direction.x=-1
                    elif alien.direction.x==-1:
                        alien.direction.x=1
            alien.rect.x+=alien.vel*alien.direction.x

    def player_enemy_collision(self):
        man=self.player_grp.sprite
        for alien in self.enemy_grp.sprites():
            if alien.dead==False and alien.rect.colliderect(man.rect):
                if man.direction.y>1:
                    alien.die()
                    man.jump(True)
                else:
                    for ind,spt in enumerate(self.health_grp.sprites()):
                        if spt.count<=3:
                            spt.reduce_life()
                            self.life[len(self.life)-ind-1]=int(spt.count)
                            pygame.mixer.Sound.play(self.hit_sound)
                            break
                    else:
                        self.lostgame=True

    def score_show(self):
        coin=pygame.transform.scale(pygame.image.load(f"tiles/2.png").convert_alpha(),(tile_size-10,tile_size-10))
        coin_rect=coin.get_rect(x=tile_size,y=tile_size+10)
        self.win.blit(coin,coin_rect)
        text=pygame.font.Font(None,40)
        score_surface=text.render(str(self.score),True,"black")
        score_rect=score_surface.get_rect(center=(coin_rect.centerx+tile_size,coin_rect.centery))
        self.win.blit(score_surface,score_rect)

    def show_text(self,txt):
        text=pygame.font.SysFont('Poor Richard',70)
        if txt=='won':
            surface1=text.render("You won",True,"green")
            if self.choice==nlev:surface2=text.render("well played!!",True,"orange")
            else: surface2=text.render("Moving to next level",True,"orange")
        elif txt=='lost':
            surface1=text.render("You lost",True,"red")
            surface2=text.render("Game over",True,"orange")
        self.win.blit(surface1,surface1.get_rect(center=(winw//2,100)))
        self.win.blit(surface2,surface2.get_rect(center=(winw//2,200)))

    def loose_check(self):
        if self.player_grp.sprite.rect.y>tile_size*len(self.land):
            self.lostgame=True
        
    def run(self):
        self.scroll()
        self.land_grp.update(self.world_shift)
        self.coin_grp.update(self.world_shift)
        self.stop_grp.update(self.world_shift)
        self.enemy_grp.update(self.world_shift)
        self.background_grp.update(self.world_shift)
        self.player_grp.update()
        self.horizontal_collision()
        self.vertical_collision()
        self.enemy_stop_collision()
        self.coin_collision()
        self.player_enemy_collision()
        self.background_grp.draw(self.win)
        self.land_grp.draw(self.win)
        self.enemy_grp.draw(self.win)
        self.coin_grp.draw(self.win)
        self.player_grp.draw(self.win)
        self.health_grp.draw(self.win)
        self.score_show()
        self.loose_check()
        if self.wongame: self.show_text('won')
        elif self.lostgame: self.show_text('lost')

main=maingame()
