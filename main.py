import pygame, random

pygame.init()
gameScreen = pygame.display.set_mode((800,800))
pygame.display.set_caption("yahtzee")

#colours
button_colour = (139, 71, 93, 255)#(47, 79, 79, 255)
background_colour = (255, 192, 203, 255)#(69, 139, 116, 255)
sheet_colour = (240, 248, 255, 255)
text_colour = (0, 0, 0, 0)
gameScreen.fill(background_colour)
#text
font = pygame.font.Font("freesansbold.ttf", 18)

#button setup
button_position = (350, 700)
button_dimension = (100, 50)
button = pygame.Rect(button_position, button_dimension)

#dice setup
dice_dimension = (50,50)
dice_positions = [(225, 625), (300, 625), (375, 625), (450, 625), (525, 625)]
dice = [0, 0, 0, 0, 0]
for i in range(len(dice_positions)):
    dice[i] = pygame.Rect(dice_positions[i], dice_dimension)

#load dice faces
def load_images():
    images = {}
    numbers = ["one", "two", "three", "four", "five", "six"]
    for i,num in enumerate(numbers, start=1):
        images[i] = pygame.image.load("images/{}.png".format(num)).convert()
        images[i] = pygame.transform.scale(images[i],dice_dimension)
    return images

def load_grey():
    images = {}
    numbers = ["one", "two", "three", "four", "five", "six"]
    for i,num in enumerate(numbers, start=1):
        images[i] = pygame.image.load("images/g{}.png".format(num)).convert()
        images[i] = pygame.transform.scale(images[i],dice_dimension)
    return images

#score sheet
rect_dim = (40,25)
sheet = pygame.Rect((150,50),(500,500))
rects = [385, 425, 465, 505, 545, 585]
yrects = [100, 125, 150, 175, 200, 225, 325, 350, 375, 400, 425, 450, 475]
scoreblocks = []
scoreblocks.append(pygame.Rect((rects[0],100),rect_dim))
scoreblocks.append(pygame.Rect((rects[0],125),rect_dim))
scoreblocks.append(pygame.Rect((rects[0],150),rect_dim))
scoreblocks.append(pygame.Rect((rects[0],175),rect_dim))
scoreblocks.append(pygame.Rect((rects[0],200),rect_dim))
scoreblocks.append(pygame.Rect((rects[0],225),rect_dim))
scoreblocks.append(pygame.Rect((rects[0],325),rect_dim))
scoreblocks.append(pygame.Rect((rects[0],350),rect_dim))
scoreblocks.append(pygame.Rect((rects[0],375),rect_dim))
scoreblocks.append(pygame.Rect((rects[0],400),rect_dim))
scoreblocks.append(pygame.Rect((rects[0],425),rect_dim))
scoreblocks.append(pygame.Rect((rects[0],450),rect_dim))
scoreblocks.append(pygame.Rect((rects[0],475),rect_dim))
rollnumrect = pygame.Rect((185,635), (20, 20))

#GAME SETUP
#all dice can be rolled
rollable = [True, True, True, True, True]
dice_values = [1, 1, 1, 1, 1]

#INITIALIZE SCORES
scores = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
bonus = 0
ybonus = 0
possible = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
rollnum = 0
saveable = [True, True, True, True, True, True, True, True, True, True, True, True, True]
roundnum = 0

#FUNCTIONS
#update possible scores
def update(possible, values):
    counts = [values.count(1), values.count(2), values.count(3), values.count(4), values.count(5), values.count(6)]
    possible[0] = counts[0]
    possible[1] = (counts[1])*2
    possible[2] = (counts[2])*3
    possible[3] = (counts[3])*4
    possible[4] = (counts[4])*5
    possible[5] = (counts[5])*6
    if counts.count(3) == 1 or counts.count(4) == 1 or counts.count(5) == 1:
        possible[6] = sum(values) #3ofakind
    else:
        possible[6] = 0
    if counts.count(4) == 1 or counts.count(5) == 1: #4ofakind
        possible[7] = sum(values)
    else:
        possible[7] = 0
    if counts.count(3) == 1 and counts.count(2) == 1: #full house
        possible[8] = 25
    else: 
        possible[8] = 0
    #small straight
    if {1,2,3,4}.issubset(values) or {2,3,4,5}.issubset(values) or {3,4,5,6}.issubset(values):
        possible[9] = 30
    else: 
        possible[9] = 0
    #large straight
    if {1,2,3,4,5}.issubset(values) or {2,3,4,5,6}.issubset(values):
        possible[10] = 40
    else:
        possible[10] = 0

    if counts.count(5) == 1: #yahtzee
        possible[11] = 50
    else:
        possible[11] = 0
    possible[12] = sum(values) #chance
    return possible

#draw button 
def setup():
    pygame.draw.rect(gameScreen, button_colour, button) 
    pygame.draw.rect(gameScreen, sheet_colour, sheet)

    #draw outline of sheet
    pygame.draw.lines(gameScreen, button_colour, True, [(150,50), (650,50), (650, 550), (150, 550)], 1) #outline
    pygame.draw.lines(gameScreen, button_colour, False, [(175,100),(625,100),(625,125),(175,125),(175,150),(625,150),(625,175),(175,175),(175,200),(625,200),(625,225),(175,225),(175,250),(625,250),(625,275),(175,275)])
    pygame.draw.lines(gameScreen,button_colour,False,[(175,325),(625,325),(625,350),(175,350),(175,375),(625,375),(625,400),(175,400),(175,425),(625,425),(625,450),(175,450),(175,475),(625,475),(625,500),(175,500),(175,525),(625,525)])
    pygame.draw.lines(gameScreen,button_colour,True,[(175,75),(625,75),(625,525),(175,525)],2)
    pygame.draw.lines(gameScreen,button_colour,False,[(385,75),(385,525),(425,525),(425,75),(465,75),(465,525),(505,525),(505,75),(545,75),(545,525),(585,525),(585,75)])
    pygame.draw.rect(gameScreen, sheet_colour, pygame.Rect((386, 251), (239, 24)))

    #text

    gameScreen.blit(font.render("UPPER SECTION", True, text_colour), pygame.Rect((180,80),rect_dim))
    gameScreen.blit(font.render("ones", True, text_colour), pygame.Rect((180,100),rect_dim))
    gameScreen.blit(font.render("twos", True, text_colour), pygame.Rect((180,125),rect_dim))
    gameScreen.blit(font.render("threes", True, text_colour), pygame.Rect((180,150),rect_dim))
    gameScreen.blit(font.render("fours", True, text_colour), pygame.Rect((180,175),rect_dim))
    gameScreen.blit(font.render("fives", True, text_colour), pygame.Rect((180,200),rect_dim))
    gameScreen.blit(font.render("sixes", True, text_colour), pygame.Rect((180,225),rect_dim))
    gameScreen.blit(font.render("bonus", True, text_colour), pygame.Rect((180,250),rect_dim))
    gameScreen.blit(font.render("LOWER SECTION", True, text_colour), pygame.Rect((180,300),rect_dim))
    gameScreen.blit(font.render("3 of a kind", True, text_colour), pygame.Rect((180,325),rect_dim))
    gameScreen.blit(font.render("4 of a kind", True, text_colour), pygame.Rect((180,350),rect_dim))
    gameScreen.blit(font.render("full house", True, text_colour), pygame.Rect((180,375),rect_dim))
    gameScreen.blit(font.render("small straight", True, text_colour), pygame.Rect((180,400),rect_dim))
    gameScreen.blit(font.render("large straight", True, text_colour), pygame.Rect((180,425),rect_dim))
    gameScreen.blit(font.render("yahtzee", True, text_colour), pygame.Rect((180,450),rect_dim))
    gameScreen.blit(font.render("chance", True, text_colour), pygame.Rect((180,475),rect_dim))
    gameScreen.blit(font.render("yahtzee bonus", True, text_colour), pygame.Rect((180,500),rect_dim))
    gameScreen.blit(font.render("ROLL", True, sheet_colour), pygame.Rect((377, 715), (50,20)))


def roll():
    num = random.randint(1,6)
    return (num)
     


#game setup
setup()
faces = load_images()
gfaces = load_grey()

#dice
for i in range(len(rollable)):
    gameScreen.blit(faces[1], dice_positions[i])



#GAME
running = True
while running:
    pygame.display.update()

    if saveable == [False, False, False, False, False, False, False, False, False, False, False, False, False]:
        if (scores[0]+scores[1]+scores[2]+scores[3]+scores[4]+scores[5])>= 63:
            bonus += 35
        gameScreen.blit(font.render(str((sum(scores)+bonus+ybonus)), True, text_colour), pygame.Rect((rects[roundnum],528),rect_dim))

        #if game over
        if roundnum == 5:
            rollable = [False, False, False, False, False]
            saveable = [0]
        else: #reset & prepare for next round
            pygame.draw.rect(gameScreen, sheet_colour, pygame.Rect((386, 251), (239, 24)))
            roundnum += 1
            rollable = [True, True, True, True, True]
            dice_values = [1, 1, 1, 1, 1]
            scores = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            bonus = 0
            ybonus = 0
            possible = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            rollnum = 0
            scoreblocks = []
            scoreblocks.append(pygame.Rect((rects[roundnum],100),rect_dim))
            scoreblocks.append(pygame.Rect((rects[roundnum],125),rect_dim))
            scoreblocks.append(pygame.Rect((rects[roundnum],150),rect_dim))
            scoreblocks.append(pygame.Rect((rects[roundnum],175),rect_dim))
            scoreblocks.append(pygame.Rect((rects[roundnum],200),rect_dim))
            scoreblocks.append(pygame.Rect((rects[roundnum],225),rect_dim))
            scoreblocks.append(pygame.Rect((rects[roundnum],325),rect_dim))
            scoreblocks.append(pygame.Rect((rects[roundnum],350),rect_dim))
            scoreblocks.append(pygame.Rect((rects[roundnum],375),rect_dim))
            scoreblocks.append(pygame.Rect((rects[roundnum],400),rect_dim))
            scoreblocks.append(pygame.Rect((rects[roundnum],425),rect_dim))
            scoreblocks.append(pygame.Rect((rects[roundnum],450),rect_dim))
            scoreblocks.append(pygame.Rect((rects[roundnum],475),rect_dim))
            saveable = [True, True, True, True, True, True, True, True, True, True, True, True, True]



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            #if roll button clicked
            #check how many rolls done
            if rollnum < 3:
                if button.collidepoint(x, y):
                    for i in range(len(rollable)):
                        if rollable[i] == True:
                            dice_values[i] = roll();
                            gameScreen.blit(faces[dice_values[i]], dice_positions[i])

                    rollnum += 1
                    pygame.draw.rect(gameScreen, background_colour, rollnumrect)
                    gameScreen.blit(font.render(str(rollnum), True, button_colour), rollnumrect)
                    possible = update(possible, dice_values)

            #if dice clicked
            for i in range(len(dice)):
                if dice[i].collidepoint(x,y):
                    rollable[i] = not rollable[i]
                    if rollable [i] == False:
                        gameScreen.blit(gfaces[dice_values[i]], dice_positions[i])
                    else:

                        gameScreen.blit(faces[dice_values[i]], dice_positions[i])
            
            for i in range(len(scoreblocks)):
                if saveable[i] == True:
                    if scoreblocks[i].collidepoint(x,y):
                        #double yahtzee check 
                        if scores[11] == 50 and possible[11] == 50:
                            ybonus += 100
                            pygame.draw.rect(gameScreen, sheet_colour, pygame.Rect((rects[roundnum]+1, 501), (39,24)))
                            gameScreen.blit(font.render(str(ybonus), True, text_colour), pygame.Rect((rects[roundnum]+5,505),rect_dim))

                        #update scores
                        scores[i] = possible[i]
                        saveable[i] = False
                        text = font.render(str(possible[i]), True, text_colour)
                        gameScreen.blit(text, pygame.Rect((rects[roundnum]+10,yrects[i]+5),rect_dim))
                        #reset dice
                        for i in range(len(rollable)):
                            gameScreen.blit(faces[1], dice_positions[i])


                        #bonus progress bar
                        upper = sum(scores[0:6])
                        if upper > 63: #don't draw further than box
                            pygame.draw.rect(gameScreen, button_colour, pygame.Rect((385,250), (240,25)))
                        else: 
                            pygame.draw.rect(gameScreen, button_colour, pygame.Rect((385,250), (int(240 * upper / 63),25)))
                        
                        #reset rolls
                        pygame.draw.rect(gameScreen, background_colour, rollnumrect)
                        rollnum = 0
                        rollable = [True, True, True, True, True]
                        dice_values = [0, 0, 0, 0, 0]


pygame.quit()