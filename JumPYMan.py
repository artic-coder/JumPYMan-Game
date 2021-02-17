"""JumpyMan in python3 with py framework
Written by Artic Coder
Platform : MacOS using Sublime 3
Features : 
~*Multiple Levels with multiple enemies.*~
~*Shows infromation such as speed,score and live status.*~
~*Speed and lives management on higher levels.*~
~*Player can shoot bi-directionally.*~
~*Random respawing of enemies and lives.*~
~*Collision detection with hitbox mechanism.*~
~*Improved Graphics and sounds*~
"""

#Import all modules.
import pygame as py
import random   

#Game related constants (**EDIT ON OWN RISK**).
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 480
RED = (0xFF,0,0)
GREEN = (0,0x7F,0)
BLUE = (0,0,0xFF)
BLACK = (0,0,0)
WHITE = (0xFF,0xFF,0xFF)
PLAYER_FRAME_LIMIT = 27
ENEMY_FRAME_LIMIT = 33
BULLETS_LIMIT = 5
BULLETS_COLOR = BLACK
JUMP_LIMIT = 8
ENEMY_HEALTH = 10
PLAYER_SPEED = 5
ENEMY_SPEED = 3
SPRITE_SIZE = 64
LIFE_TIMER = 600
GAME_FONT = 'optimattc'

#Game related variables.
score = 0
hiscore = 0
lives = 5
level = 1
speed = 3
player_dead = False
life_visible = True
life_x = 150
life_y = 280
life_wait_timer = 1
life_hitbox = (life_x+2,life_y+2,24,24)
life_taken = False
pause = False

#Initialize game section.
py.init()
game_screen = py.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
py.display.set_caption("JumpyMan by HaseeB")
clock = py.time.Clock()

#Sprites section.
player_walk_right = [py.image.load('resources/R1.png'), py.image.load('resources/R2.png'), py.image.load('resources/R3.png'), py.image.load('resources/R4.png'), py.image.load('resources/R5.png'), py.image.load('resources/R6.png'), py.image.load('resources/R7.png'), py.image.load('resources/R8.png'), py.image.load('resources/R9.png')]
player_walk_left = [py.image.load('resources/L1.png'), py.image.load('resources/L2.png'), py.image.load('resources/L3.png'), py.image.load('resources/L4.png'), py.image.load('resources/L5.png'), py.image.load('resources/L6.png'), py.image.load('resources/L7.png'), py.image.load('resources/L8.png'), py.image.load('resources/L9.png')]
enemy_walk_right = [py.image.load('resources/R1E.png'), py.image.load('resources/R2E.png'), py.image.load('resources/R3E.png'), py.image.load('resources/R4E.png'), py.image.load('resources/R5E.png'), py.image.load('resources/R6E.png'), py.image.load('resources/R7E.png'), py.image.load('resources/R8E.png'), py.image.load('resources/R9E.png'), py.image.load('resources/R10E.png'), py.image.load('resources/R11E.png')]
enemy_walk_left = [py.image.load('resources/L1E.png'), py.image.load('resources/L2E.png'), py.image.load('resources/L3E.png'), py.image.load('resources/L4E.png'), py.image.load('resources/L5E.png'), py.image.load('resources/L6E.png'), py.image.load('resources/L7E.png'), py.image.load('resources/L8E.png'), py.image.load('resources/L9E.png'), py.image.load('resources/L10E.png'), py.image.load('resources/L11E.png')]
background_platform = py.image.load('resources/back_platform.jpg')
player_life = py.image.load('resources/life.png')

#Player class with all attributes related to player.
class Player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = PLAYER_SPEED
        self.is_jump = False
        self.left = False
        self.right = False
        self.walk_count = 0
        self.jump_limit = JUMP_LIMIT
        self.standing = True
        self.hitbox = (self.x+17,self.y+11,29,52)

    def draw(self,game_screen):
        if self.walk_count + 1 >= PLAYER_FRAME_LIMIT:
            self.walk_count = 0
        if not(self.standing):
            if self.left:
                game_screen.blit(player_walk_left[self.walk_count//3],(self.x,self.y))                                
                self.walk_count += 1
            elif self.right:
                game_screen.blit(player_walk_right[self.walk_count//3],(self.x,self.y))                                
                self.walk_count += 1        
        else:
            if self.right:
                game_screen.blit(player_walk_right[0],(self.x,self.y))
            else:
                game_screen.blit(player_walk_left[0],(self.x,self.y))
        self.hitbox = (self.x+17,self.y+11,29,52)       

    def hit(self):
            self.is_jump = False
            self.jump_limit = JUMP_LIMIT
            self.x = random.randint(0,SCREEN_WIDTH-50) 
            self.y = 370
            self.walk_count = 0        


#Enemy class with all attributes related to enemy.
class Enemy(object):
    def __init__(self,x,y,width,height,end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.walk_count = 0
        self.path = [self.x,self.end]
        self.speed = ENEMY_SPEED
        self.hitbox = (self.x+17,self.y+2,31,57)
        self.health = ENEMY_HEALTH
        self.visible = True
    
    def draw(self,game_screen):
        if self.visible:
            self.move()
            if self.walk_count + 1 >= ENEMY_FRAME_LIMIT:
                self.walk_count = 0
            
            if self.speed > 0:
                game_screen.blit(enemy_walk_right[self.walk_count//3],(self.x,self.y))
                self.walk_count += 1
            else:
                game_screen.blit(enemy_walk_left[self.walk_count//3],(self.x,self.y))
                self.walk_count += 1
            
            py.draw.rect(game_screen,RED,(self.hitbox[0],self.hitbox[1] - 20,50,10))
            py.draw.rect(game_screen,GREEN,(self.hitbox[0],self.hitbox[1] - 20,50 - ((50/ENEMY_HEALTH) * (ENEMY_HEALTH - self.health)),10))
            self.hitbox = (self.x+17,self.y+2,31,57)                                                

    def move(self):
        if self.speed > 0:
            if self.x + self.speed < self.path[1]:
                self.x += self.speed
            else:
                self.speed = self.speed * -1
                self.walk_count = 0
        else:
            if self.x - self.speed > self.path[0]:
                self.x += self.speed
            else:
                self.speed = self.speed * -1
                self.walk_count = 0

    def hit(self,level):
        if self.health > 0:
            self.health -= 1 if level < 5 else 2
        else:
            self.visible = False                                     
                            
#Projectile class for bullets.
class Projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.speed = 8 * facing

    def draw(self,game_screen):
        py.draw.circle(game_screen,self.color,(self.x,self.y),self.radius)
                                
#Method to render sprites.
def renderSprites():
    global life_wait_timer,life_taken,life_x,life_y,life_hitbox,life_visible

    game_screen.blit(background_platform, (0,0))

    logo_font = py.font.SysFont(GAME_FONT,30,True,True)

    logo_text = logo_font.render('JumpyMan V 1.0',0,BLUE)
    game_screen.blit(logo_text,(SCREEN_WIDTH/4,30))

    font = py.font.SysFont(GAME_FONT,20,True,True)

    info_text_1 = font.render('SPACE - Shoot.            UP - Jump             LEFT/RIGHT - Move',1,BLACK)
    game_screen.blit(info_text_1,(0,70))

    lives_text = font.render('Lives ' + str(lives),1,RED)
    game_screen.blit(lives_text,(0,0))
    
    level_text = font.render('level ' + str(level),1,GREEN)
    game_screen.blit(level_text,(120,0))

    hiscore_text = font.render('Speed ' + str(speed),1,GREEN)
    game_screen.blit(hiscore_text,(240,0))

    score_text = font.render('Score ' + str(score),1,BLUE)
    game_screen.blit(score_text,(360,0))

    hiscore_text = font.render('Hiscore ' + str(hiscore),1,BLUE)
    game_screen.blit(hiscore_text,(480,0))

    #Draw player/enemies/bullets on every frame.
    player.draw(game_screen)

    if level < 5:
        enemy_1.draw(game_screen)
    elif level >= 5 and level < 10:
        enemies = [enemy_1,enemy_2]
        for enemy in enemies:
            enemy.draw(game_screen)
    elif level >= 10:
        enemies = [enemy_1,enemy_2,enemy_3]
        for enemy in enemies:
            enemy.draw(game_screen) 
    
    for bullet in bullets:
        bullet.draw(game_screen)

    #Get new positon for life if taken.    
    if life_taken:
        life_x = random.randint(0,SCREEN_WIDTH-50)
        life_y = random.randint(280,SCREEN_HEIGHT-70)
        life_taken = False
        life_visible = False
    else:
        life_wait_timer += 1   

    #Wait till life wait timer loop ends after draw new life.    
    if not life_taken and life_wait_timer % LIFE_TIMER == 0:
        life_visible = True

    if life_visible:        
        game_screen.blit(player_life,(life_x,life_y))            
    
    life_hitbox = (life_x+2,life_y+2,24,24)        
    py.display.update()

#Method to detect collision between enemy/player/bullet/life.
def  spriteCollisionDetection(enemy,bullets):
    global score,lives,level,life_taken

    #Player and enemy collision detection.    
    if player.hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3] and player.hitbox[1] + player.hitbox[3] > enemy.hitbox[1]:
        if player.hitbox[0] + player.hitbox[2] > enemy.hitbox[0] and player.hitbox[0] < enemy.hitbox[0] + enemy.hitbox[2]:
            if enemy.visible:
                player.hit()
                score -= 5
                score = 0 if score < 0 else score
                lives -= 1
                py.mixer.music.load('resources/player_dead.mp3')
                py.mixer.music.play(1)
                py.time.delay(1000)

    #Player and life collision detection.    
    if player.hitbox[1] < life_hitbox[1] + life_hitbox[3] and player.hitbox[1] + player.hitbox[3] > life_hitbox[1]:
        if player.hitbox[0] + player.hitbox[2] > life_hitbox[0] and player.hitbox[0] < life_hitbox[0] + life_hitbox[2]:
                if life_visible:
                    lives += 1
                    life_taken = True 
                    py.mixer.music.load('resources/life_up.wav')
                    py.mixer.music.play(1)  

    #Enemy and bullet collision detection.            
    for bullet in bullets:
        if bullet.y - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3] and bullet.y + bullet.radius > enemy.hitbox[1]:
            if bullet.x + bullet.radius > enemy.hitbox[0] and bullet.x - bullet.radius < enemy.hitbox[0] + enemy.hitbox[2]:
                if enemy.visible:
                    py.mixer.music.load('resources/enemy_bullet_hit.mp3')
                    py.mixer.music.play(1)
                    enemy.hit(level)
                    score += 1
                    bullets.remove(bullet)
                
        #Remove bullets from screen.           
        if bullet.x < SCREEN_WIDTH and bullet.x > 0:
            bullet.x += bullet.speed
        
        else:
            bullets.remove(bullet)

#Method to respawn enemies.
def respawnEnemy(enemy):
    enemy_collided = False
    py.mixer.music.load('resources/enemy_dead.wav')
    py.mixer.music.play(1)
    py.time.delay(1000)
    enemy.health = ENEMY_HEALTH
    enemy.visible = True
    enemy.x = random.randint(0,SCREEN_WIDTH-50)


#Main method for game.
if __name__ == '__main__':

    #Creating player and enemies instances.
    player = Player(300,370,SPRITE_SIZE,SPRITE_SIZE)
    enemy_1 = Enemy(0,380,SPRITE_SIZE,SPRITE_SIZE,SCREEN_WIDTH-50)
    enemy_2 = Enemy(100,380,SPRITE_SIZE,SPRITE_SIZE,SCREEN_WIDTH-50)
    enemy_3 = Enemy(200,380,SPRITE_SIZE,SPRITE_SIZE,SCREEN_WIDTH-50)
    bullets = []
    shoot_loop = 0
    reset_speed = True
    run = True
    pause_freq = 0

    #Main game loop.
    while run:
        clock.tick(PLAYER_FRAME_LIMIT)

        #Game over section - reset all variables and constants.
        if lives <= 0:
            #Reset variables.
            hiscore = (score + 5) if score > hiscore else hiscore
            lives = 5
            score = 0
            level = 1
            speed = 3
            BULLETS_LIMIT = 5
            LIFE_TIMER = 600
            enemy_1.health = ENEMY_HEALTH
            enemy_1.speed = ENEMY_SPEED
            player.speed = PLAYER_SPEED
            enemy_1.visible = True

            #Print game over text and load music.
            game_over_font = py.font.SysFont('arial',40,True,True)
            game_over_text = game_over_font.render('Game Over (Press ENTER Key)',1,RED)
            game_screen.blit(game_over_text,(150,150))
            py.mixer.music.load('resources/game_over.mp3')
            py.mixer.music.play(1)

            #Remove bullets from screen.            
            for bullet in bullets:           
                bullets.remove(bullet)

            #Update display and delay.        
            py.display.update()
            pause = True   

        #Application quit event.    
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                    
        #Shooting limit range.    
        if shoot_loop > 0:
            shoot_loop += 1
        if shoot_loop > 3:
            shoot_loop = 0        

        #Respawn new enemy and check collision.        
        if level < 5:
            if not enemy_1.visible and enemy_1.health == 0:
                respawnEnemy(enemy_1)
                enemy_1.speed = abs(enemy_1.speed) + 1
                level += 1
                speed = abs(enemy_1.speed)
            spriteCollisionDetection(enemy_1,bullets)
        elif level >= 5 and level < 10:
            enemies = [enemy_1,enemy_2]
            if level == 5 and reset_speed:
                enemy_1.speed = enemy_2.speed = speed = ENEMY_SPEED
                BULLETS_LIMIT = 7
                LIFE_TIMER = 400
                player.speed += 2
                reset_speed = False
            if level == 9: 
                reset_speed = True

            if not enemy_1.visible and not enemy_2.visible and enemy_1.health == 0 and enemy_2.health == 0:
                for enemy in enemies:
                    respawnEnemy(enemy)
                    enemy.speed = abs(enemy.speed) + 1
                    speed = abs(enemy.speed)
                level += 1

            for enemy in enemies:    
                spriteCollisionDetection(enemy,bullets)

            #Bug fix for life taken because of multiple detection. 
            #PERMANENT-FIX-TO-DO : Move Player-Life Detection code here.
            if life_taken:
                lives -= 1

        elif level >= 10:
            enemies = [enemy_1,enemy_2,enemy_3]
            if level == 10 and reset_speed:
                enemy_1.speed = enemy_2.speed = enemy_3.speed = speed = ENEMY_SPEED
                player.speed += 3
                BULLETS_LIMIT = 10
                LIFE_TIMER = 200
                reset_speed = False
            if not enemy_1.visible and not enemy_2.visible and not enemy_3.visible and enemy_1.health == 0 and enemy_2.health == 0 and enemy_3.health == 0:
                
                for enemy in enemies:    
                    respawnEnemy(enemy)
                    enemy.speed = abs(enemy.speed) + 1
                    speed = abs(enemy.speed)
                level += 1

            for enemy in enemies:    
                spriteCollisionDetection(enemy,bullets)

            if life_taken:    
                lives -= 2     

        #Get the key pressed        
        keys = py.key.get_pressed()

        #Bullet spawn section.
        if keys[py.K_SPACE] and shoot_loop == 0:
            py.mixer.music.load('resources/bullet.mp3')
            py.mixer.music.play(1)
            facing = -1 if player.left else 1    
            projectile = Projectile((player.x + player.width //2),round(player.y + player.height//2),6,BULLETS_COLOR,facing)        
            
            if len(bullets) < BULLETS_LIMIT:
                bullets.append(projectile)
            shoot_loop = 1

        if keys[py.K_RETURN]:
            pause = not pause
            py.mixer.music.load('resources/pause_on.mp3')
            py.mixer.music.play(1)
            pause_freq += 1

        if pause_freq % 2 == 0 and pause_freq > 0:    
            py.mixer.music.load('resources/pause_off.mp3')
            py.mixer.music.play(1)
            pause_freq = 1
                       

        #Moving section of player.    
        if keys[py.K_LEFT] and player.x > player.speed:
            player.x -= player.speed
            player.left = True
            player.right = False
            player.standing = False
        elif keys[py.K_RIGHT] and player.x < SCREEN_WIDTH - player.width - player.speed:
            player.x += player.speed
            player.right = True
            player.left = False
            player.standing = False
        else:
            player.standing = True
            player.walk_count = 0
        
        #Jump section of player.    
        if not(player.is_jump):
            if keys[py.K_UP]:
                py.mixer.music.load('resources/player_jump.wav')
                py.mixer.music.play(1)
                player.is_jump = True
                player.right = False
                player.left = False
                player.walk_count = 0
        else:
            if player.jump_limit >= -JUMP_LIMIT:
                player.y -= (player.jump_limit*abs(player.jump_limit)) / 2
                player.jump_limit -= 1
            else:
                player.is_jump = False
                player.jump_limit = JUMP_LIMIT

        if not pause:        
            #Render sprites on every frame.        
            renderSprites()

    py.quit()
