#javid husseynly, rupen patel
#june 12 2019
#  'Bird Hunt'


#imports
import pygame
import time
import random
pygame.init()

#our main window
window = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Bird Hunt")


#loading sprites, images
runR = [pygame.image.load('runR1.v1.png'), pygame.image.load('runR2.v1.png'),pygame.image.load('runR3.v1.png'), pygame.image.load('runR4.v1.png'), pygame.image.load('runR5.v1.png'), pygame.image.load('runR6.v1.png')]
runL = [pygame.image.load('runL1.v1.png'), pygame.image.load('runL2.v1.png'), pygame.image.load('runL3.v1.png'), pygame.image.load('runL4.v1.png'), pygame.image.load('runL5.v1.png'), pygame.image.load('runL6.v1.png')]
background = pygame.image.load('background.png')
char = pygame.image.load('idle.v1.png')
shootR = pygame.image.load('shootR.v1.png')
shootL = pygame.image.load('shootL.v1.png')
shootU = pygame.image.load('shootU.v1.png')
idleL = pygame.image.load('idleL.v1.png')
idleR = pygame.image.load('idleR.v1.png')
bird1L = pygame.image.load('bird1L.png')
bird2L = pygame.image.load('bird2L.png')
bird3L = pygame.image.load('bird3L.png')
bird1R = pygame.image.load('bird1R.png')
bird2R = pygame.image.load('bird2R.png')
bird3R = pygame.image.load('bird3R.png')
clock = pygame.time.Clock()

#loading sounds
gunshot = pygame.mixer.Sound('gunshot.wav')
birdHit = pygame.mixer.Sound('bird hit.wav')
birdDeath = pygame.mixer.Sound('bird death.wav')
playerDeath = pygame.mixer.Sound('death.wav')

#loading music, playing on loop
music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

#initializing some global variables
score = 0
level = 1
run = True

#initializing some button colours
clickColour = (255, 226, 198)
orange2 = (249, 121, 6)
black = (0,0,0)

#enemy class, bird
class Bird:

    #our list of sprite images for animation (bird going to the left, going to the right)
    walkL = [bird1L, bird2L, bird3L]
    walkR = [bird1R, bird2R, bird3R]

    #initializing variables
    def __init__(self,x,y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x, self.y, 125, 115)
        self.health = 10

    #drawing bird onto screen
    def draw(self,window):

        #run move function
        self.move()

        #walkCount is like an animation cycle
        #there are three frames per animation cycle for the bird
        #we let walkCount go up to 18 and then integer divide by 6 so we cycle through the three frames
        #we do this integer division to slow down the animation cycle
        if self.walkCount + 1 >= 18:
            self.walkCount = 0

        #if velocity is positive, bird goes to the right
        if self.vel > 0:

            #walkCount // 6 gives us the index for our animation cycle list
            window.blit(self.walkR[self.walkCount // 6], (self.x, self.y))
            self.walkCount += 1

        #if velocity is negative, bird goes to the left
        else:
            window.blit(self.walkL[self.walkCount // 6], (self.x, self.y))
            self.walkCount += 1

        #health bars for the birds
        #there is a red bar behind a green bar, the green bar goes down everytime the bird is hit
        pygame.draw.rect(window, (255, 0, 0), (self.hitbox[0] + 20, self.hitbox[1] - 20, 100, 5))
        pygame.draw.rect(window, (0, 255, 0), (self.hitbox[0] + 20, self.hitbox[1] - 20, 100 - ((100/10) * (10 - self.health)), 5))

        #hitbox for the bird updates after movement
        self.hitbox = (self.x, self.y + 10, 125, 115)


        
    #movement of bird
    def move(self):

        #if velocity is positive, moves to the right
        if self.vel > 0:

            #checks to make sure bird is within boundaries, if so, the bird moves to the right
            if self.x + self.vel + self.width < self.path[1]:
                self.x += self.vel

            #if it reaches boundary, it turns around                
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

        #same thing as above, but to the left        
        else:
            if self.x - self.vel > 0:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0      

    #function for if bird is hit
    def hit(self):

        #if it has health remaining, it goes down by 1 and the 'hit' sound plays
        if self.health > 1:
            self.health -= 1
            birdHit.play()

        #if it has no health remaining, the death sound plays, and the bird gets removed from the list    
        else:
            birdDeath.play()
            birds.pop(birds.index(self))

        


#user-controlled player class        
class Character:

    #initializing variables
    def __init__(self, x, y, width, height, vel, isJump, jumpCount, left, right, walkCount, shootR, shootL, shootU, standing):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.isJump = isJump
        self.jumpCount = jumpCount
        self.left = left
        self.right = right
        self.walkCount = walkCount
        self.shootR = shootR
        self.shootL = shootL
        self.shootU = shootU
        self.standing = standing
        self.hitbox = (self.x + 25, self.y, 65, 125)
        self.health = 3
        
        
        
    #getters, setters
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height
    def getVel(self):
        return self.vel
    def getIsJump(self):
        return self.isJump
    def getJumpCount(self):
        return self.jumpCount
    def getLeft(self):
        return self.left
    def getRight(self):
        return self.right
    def getWalkCount(self):
        return self.walkCount
    def getShootR(self):
        return self.shootR
    def getShootL(self):
        return self.shootL
    def getShootU(self):
        return self.shootU

    

    def setX(self, x):
        self.x = x
    def setY(self, Y):
        self.y = y
    def setWidth(self, width):
        self.width = width
    def setHeight(self, height):
        self.height = height
    def setVel(self, vel):
        self.vel = vel
    def setIsJump(self, isJump):
        self.isJump = isJump
    def setJumpCount(self, jumpCount):
        self.jumpCount = jumpCount
    def setLeft(self, left):
        self.left = left
    def setRight(self, right):
        self.right= right
    def setWalkCount(self, walkCount):
        self.walkCount = walkCount
    def setShootR(self, shootR):
        self.shootR = shootR
    def setShootL(self, shootL):
        self.shootL = shootL
    def setShootU(self, shootU):
        self.shootU = shootU

        

    #function for if player is hit
    def hit(self):
        
        global score
        global level
        global birds
        global bullets
        global poops

        #initializing some fonts
        font2 = pygame.font.SysFont('arial', 200)
        font3 = pygame.font.SysFont('comicsans', 40)

        #if player has health remaining, it goes down by 1
        if player1.health > 1:
            player1.health -= 1

            #displays 'HIT!' on the screen, pauses game for 2 seconds
            text1 = font2.render("HIT!", 1, (255, 0, 0))
            window.blit(text1, (1280/2 - (text1.get_width()/2), 200))
            pygame.display.update()
            time.sleep(2)

            #gets rid of poop bombs and bullets on screen and moves the character to the left of the screen
            poops = []
            bullets = []
            player1.x = 50

        #if player has no health remaining, they die   
        else:

            #death sound is played
            playerDeath.play()

            #displaying end of game screen, showing score
            pygame.draw.rect(window, (0, 0, 0,), (215,125,850,210))
            text3 = font3.render(("GAME OVER!"), 1, (250, 0, 0))
            window.blit(text3, (1280/2 - (text3.get_width()/2), 150))
            text6 = font3.render(("Your score: " + str(score)), 1, (250, 0, 0))
            window.blit(text6, (1280/2 - (text6.get_width()/2), 210))
            text5 = font3.render(("Game will restart in 4 seconds."), 1, (250, 0, 0))
            window.blit(text5, (1280/2 - (text5.get_width()/2), 270))
            pygame.display.update()
            time.sleep(4)

            
            #resets game to beginning
            score = 0
            level = 1
            birds = []
            birds.append(Bird(100, 100, 146, 200, 1280))
            player1.health = 3
            player1.x = 1280/2
            bullets = []
            poops = []

                       

    #drawing character to screen
    def draw(self,window):

        #shootL, shootR, shootU are variables that keep track of whether the character is shooting
        #if they are shooting, it displays the character image where he is shooting a gun
        if self.getShootL():
            window.blit(shootL, (self.getX(), self.getY()))

        elif self.getShootR():
            window.blit(shootR, (self.getX(), self.getY()))

        elif self.getShootU():
            window.blit(shootU, (self.getX(), self.getY()))

        #if they are not shooting and not standing idle, they are running
        elif not (self.standing):

            #running to the left
            if self.getLeft():

                #similar to bird animation, walkCount stores our index to cycle through the animation cycle (runL, runR)
                window.blit(runL[self.getWalkCount()//3], (self.getX(), self.getY()))
                self.walkCount += 1
                if self. walkCount >= 18:
                    self.walkCount = 0

            #running to the right
            elif self.getRight():
                window.blit(runR[self.getWalkCount()//3], (self.getX(), self.getY()))
                self.walkCount += 1
                if self.walkCount >= 18:
                    self.walkCount = 0

        #if they are standing idle, we check to see if the player was last running right or left
        #this way we can display the correct idle image for the character
        #for example, if i was running right and i stop, my character should be idle but still facing right
        else:
            if self.getRight():
                window.blit(idleR, (self.x, self.y))
            else:
                window.blit(idleL, (self.x, self.y))

                
        #update the character's hitbox after movement
        self.hitbox = (self.x + 25, self.y , 65, 125)




#these are the 'poop bombs' that the birds drop
class Poop():

    #initializing variables
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10
        self.colour = (181, 101, 29)
        self.vel = 8

    #drawing the bomb onto the screen    
    def draw(self, window):
        pygame.draw.circle(window, self.colour, (self.x,self.y), self.radius)




#these are the bullets the character's gun shoots
class projectile():

    #initializing variables
    def __init__(self, x, y, radius, colour, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.facing = facing
        self.vel = 10 

    #drawing bullets    
    def draw(self, window):
        pygame.draw.circle(window, self.colour, (self.x,self.y), self.radius)

        

#redrawing everything in the main game loop   
def redrawGameWindow():
 
    #displaying background
    window.blit(background, (0,0))

    
    #text displaying score, level, health on top right of screen
    font8 = pygame.font.SysFont('arial', 15, True)
    text8 = font8.render("Press X on the top right to go back to the menu", 1, (0,0,0))
    window.blit(text8, (950, 12))
    
    text = font1.render("Your Score: " + str(score), 1, (0,0,0))
    window.blit(text, (1000, 30))

    text2 = font1.render("Health: " + str(player1.health), 1, (0,0,0))
    window.blit(text2, (1000, 60))

    text4 = font1.render("Level: " + str(level), 1, (0,0,0))
    window.blit(text4, (1000, 90))

    #player1 is our instance of class Character, our user-controlled player (he is initialized later)
    player1.draw(window)


    #drawing birds, bullets, and poop bombs
    for bird in birds:
        bird.draw(window)
    for bullet in bullets:
        bullet.draw(window)
    for poop in poops:
        poop.draw(window)

    #updating screen
    pygame.display.update()




#function to reset all variables to restart game
def restartGame():
        global score
        global bullets
        global birds
        global level
        global poops
        global run


        run = True
        score = 0
        level = 1
        birds = []
        birds.append(Bird(100, 100, 146, 200, 1280))
        player1.health = 3
        player1.x = 1280/2
        bullets = []
        poops = []

        #run main game loop
        game()



#initializing our user-controlled character
player1 = Character(100, 500, 113, 125, 10, False, 8, False, False, 0, False, False, False, True)

#initializing a font
font1 = pygame.font.SysFont('arial', 30, True)

#initializing lists and adding our first bird
bullets = []
poops = []
birds = []
birds.append(Bird(100, 100, 146, 200, 1280))



#out main game loop
def game():
    global score
    global bullets
    global birds
    global level
    global poops
    global run

    while run == True:

        #if all the birds have died, increase the level
        if len(birds) == 0:
            level += 1

            #add birds equivalent to the level (eg, add 5 birds on level 5), place them at random locations in the sky
            for x in range(level):
                a = random.randint(100, 1100)
                b = random.randint(90, 111)
                birds.append(Bird(a, b, 146, 200, 1280))

                #half the birds start moving left, the other have start moving right
                if a % 2 == 0:
                    birds[-1].vel = birds[-1].vel * -1

        #our framerate        
        clock.tick(60)

        
        #getting keyboard events
        for event in pygame.event.get():

            #if you press the X button on top right of window, quit main game loop
            if event.type == pygame.QUIT:
                run = False
            

        #checking if bullet hits bird
        for bullet in bullets:

            #used is a variable to keep track of when a bullet hit a bird, to combat an error received when
            #a bullet simaltaneously enters the hitboxes of two birds
            
            used = False
            for bird in birds:

                if used == False:

                    #checking to see if it hits a birds hitbox
                    if bullet.y - bullet.radius < bird.hitbox[1] + bird.hitbox[3] and bullet.y + bullet.radius > bird.hitbox[1]:
                        if bullet.x + bullet.radius > bird.hitbox[0] and bullet.x - bullet.radius < bird.hitbox[0] + bird.hitbox[2]:

                            #bird hit function runs to decrease health
                            bird.hit()

                            #increase score
                            score += 1

                            #get rid of bullet and set it as used
                            bullets.pop(bullets.index(bullet))
                            used = True

                            

            #moving the bullet through the screen   
            if bullet.x < 1280 and bullet.x > 0 and bullet.y > 0:

                #if we shoot top left
                if bullet.facing == 0:
                    bullet.x -= bullet.vel
                    bullet.y -= bullet.vel

                #if we shoot the bullet straight up
                elif bullet.facing == 1:
                    bullet.y -= bullet.vel

                #if we shoot the bullet top right
                else:
                    bullet.x += bullet.vel
                    bullet.y -= bullet.vel

            #if bullet goes out of boundaries, remove it 
            else:
                bullets.pop(bullets.index(bullet))

                


        #every frame, a bird as a 1 in 50 chance of dropping a poop bomb
        for bird in birds:
            a = random.randint(1,50)
            if a == 1:
                poops.append(Poop((bird.x + (bird.width // 2)), bird.y + 45))

                

        #checking to see if a poop bomb hits the player
        for poop in poops:
            if poop.y - poop.radius < player1.hitbox[1] + player1.hitbox[3] and poop.y + poop.radius > player1.hitbox[1]:
                if poop.x + poop.radius > player1.hitbox[0] and poop.x - poop.radius < player1.hitbox[0] + player1.hitbox[2]:

                    #get rid of the poop bomb, run player hit() method to decrease health
                    poops.pop(poops.index(poop))   # <-- isnt this the greatest line of code ever written
                    player1.hit()

            #if poop bomb is still in range, move it down the screen       
            if poop.y < 650:
                poop.y += poop.vel

            #once it is out of boundaries, delete the poop bomb
            else:
                poops.pop(poops.index(poop))


                

        #get keys pressed
        keys = pygame.key.get_pressed()

        #if i is pressed
        if keys[pygame.K_i]:

            #set shootL to true so the correct image is displayed for the character
            player1.setShootL(True)
            player1.setShootR(False)
            player1.setShootU(False)

            #set walkCount to 0 so animation cycle resets
            player1.setWalkCount(0)

            #there can be no more than 8 bullets on the screen on the time to reduce spamming
            if len(bullets) <8:

                #play gunshot sound, create bullet
                gunshot.play()
                bullets.append(projectile(round(player1.getX() + player1.getWidth() // 2 - 60), round(player1.getY() + player1.getHeight() // 2 - 70), 6, (0,0,0), 0))


                
        #repeated for shooting up    
        elif keys[pygame.K_o]:
            player1.setShootL(False)
            player1.setShootR(False)
            player1.setShootU(True)
            player1.setWalkCount(0)
            if len(bullets) <8:
                gunshot.play()
                bullets.append(projectile(round(player1.getX() + player1.getWidth() // 2 + 18), round(player1.getY() + player1.getHeight() // 2 - 70), 6, (0,0,0), 1))

                
        #repeated for shooting top right
        elif keys[pygame.K_p]:
            player1.setShootL(False)
            player1.setShootR(True)
            player1.setShootU(False)
            player1.setWalkCount(0)
            if len(bullets) <8:
                gunshot.play()
                bullets.append(projectile(round(player1.getX() + player1.getWidth() // 2 + 60), round(player1.getY() + player1.getHeight() // 2 - 70), 6, (0,0,0), 2))


        #moving to the left if they are within the boundaries
        elif keys[pygame.K_a] and player1.getX() > player1.getVel(): 
            player1.setShootL(False)
            player1.setShootR(False)
            player1.setShootU(False)
            player1.x -= player1.getVel()
            player1.setLeft(True)
            player1.setRight(False)
            player1.standing = False


        #moving to the right if they are within the boundaries        
        elif keys[pygame.K_d] and player1.getX() < (1280 - player1.getWidth() - player1.getVel()):
            player1.setShootL(False)
            player1.setShootR(False)
            player1.setShootU(False)
            player1.x += player1.getVel()
            player1.setRight(True)
            player1.setLeft(False)
            player1.standing = False


        #if they are not running left or right, they are standing idle      
        else:
            player1.standing = True
            player1.setShootL(False)
            player1.setShootR(False)
            player1.setShootU(False)
            player1.setWalkCount(0)

            
        #jumping   
        if not player1.getIsJump():    #if the player is not already in the air (isJump = False), pressing w causes them to jump
            
            if keys[pygame.K_w]:
                player1.setShootL(False)
                player1.setShootR(False)
                player1.setShootU(False)
                player1.setIsJump(True)
                player1.setLeft(False)
                player1.setRight(False)
                player1.setWalkCount(0)


        #if isJump = True, they are in the air, and a parabola is formed to mimic gravity
        else:

            #player demonstrates the parabola y = x^2 / 2, such that -8 < y < 8 in the set of integers
            if player1.getJumpCount() >= -8:
                neg = 1
                if player1.getJumpCount() < 0:
                    neg = -1
                player1.y -= (player1.getJumpCount() ** 2) /2 * neg
                player1.jumpCount -= 1
                
            #once the parabola reaches completion, isJump is set to False and jumpCount is reset to 8
            else:
                player1.setIsJump(False)
                player1.setJumpCount(8)


        #run the draw function
        redrawGameWindow()
        
        
    
        






