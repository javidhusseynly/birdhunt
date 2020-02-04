#javid husseynly, rupen patel
#june 12 2019

#importing pygame
import pygame

#initializing pygame
pygame.init()

#define colours
black = (0, 0, 0)
clickColour = (255, 226, 198)
yellow = (255, 255, 0)
yellow2 = (248, 188, 7)
orange2 = (249, 121, 6)
red = (248, 68, 7)
clickColour = (255, 226, 198)

# set size of screen
size = [1280, 720]
screen = pygame.display.set_mode(size)

#loading in images
background = pygame.image.load("background.png").convert()
logo = pygame.image.load("logo.png")
screen1 = pygame.image.load("how to play.png")
credits1 = pygame.image.load("credits.png")

#loading in caption
pygame.display.set_caption("Bird Hunt")


clock=pygame.time.Clock()

#function that runs the menu
def menu():

    pygame.init()
    
    done = False    

    while done==False:
    #for loop that ends while loop when close button is clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                quitNow()

            #displays images
            screen.blit(background, [0,0])
            screen.blit(logo, (475,50))

            #button instances
            button("Play", 490, 318, 300, 80, clickColour, yellow)
            button("How to Play", 490, 418, 300, 80, clickColour, yellow2)
            button("Credits", 490, 518, 300, 80, clickColour, orange2)
            button("Quit", 490, 618, 300, 80, clickColour, red)

            
            pygame.display.flip()

            #plays 15 frames per second
            clock.tick(60)



#function that creates new surface with text rendered on it
def text_objects(text,font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

#function that creates buttons
def button(text, x, y, wth, hgt, activeColour, inactiveColour):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    #if mouse position is located on the button, then button lights up
    if x+wth > mouse[0] > x and y+hgt > mouse[1] > y:
        pygame.draw.rect(screen, activeColour, (x, y, wth, hgt))
        

        if click[0] == 1 and y==318:
            restartGame()

        elif click[0] == 1 and y==418:
            howToPlay()

        elif click[0] == 1 and y==518:
            credits()
            
        elif click[0] == 1 and y==618:
            quitNow()

        elif click[0] == 1 and x==10:
            menu()

        elif click[0] and x==1060:
            restartGame()

        
           
    #else, button remains inactive       
    else:
        pygame.draw.rect(screen, inactiveColour, (x, y, wth, hgt))

    #places text on center of button
    pygame.font.init()
    buttonText = pygame.font.Font("freesansbold.ttf", 40)
    textSurf, textRect = text_objects (text, buttonText)
    textRect.center = ((x + (wth/2)), (y+(hgt/2)))
    screen.blit(textSurf, textRect)

#function that quits game
def quitNow():
    pygame.quit()
    quit()

#function that runs how to play menu
def howToPlay():
    run = True

    #for loop that ends while loop when close button is clicked
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quitNow()

        # places how to play menu and buttons on screen     
        screen.blit(screen1, [0,0])
        button("Back", 10, 40, 200, 80, clickColour, orange2)
        button("Play", 1060, 40, 200, 80, clickColour, orange2)
        pygame.display.update()
        clock.tick(60)

#function that shows credits screen 
def credits():
    run = True

    #for loop that ends while loop when close button is clicked
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quitNow()

        #places credits screen and buttons on screen 
    
        screen.blit(credits1, [0,0])
        button("Back", 10, 40, 200, 80, clickColour, orange2)
        pygame.display.update()
        clock.tick(60)

#functions that calls restart function from gameEngine.py
        
def restartGame():
   import gameEngine
   gameEngine.restartGame() 

#run menu
menu()
#closes the window and quits
quitNow()






