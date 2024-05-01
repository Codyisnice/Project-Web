import pygame, sys
from pygame.locals import *
import time
from button import Button as Button
import subprocess

# Initialize Pygame
pygame.init()
screen_width, screen_height = 1792, 1024
screen = pygame.display.set_mode((screen_width, screen_height))
SCREEN = pygame.display.set_mode((1792, 1024))
pygame.display.set_caption("Forest Adventure Game")
clock = pygame.time.Clock()
finalboss_music = pygame.mixer.Sound("assets/final_boss_music.ogg")
BG = pygame.image.load("assets/boss_BG.png")
Click_sound = pygame.mixer.Sound("assets/clicking_sound.wav")
pDmg_sound = pygame.mixer.Sound("assets/playerdmg.mp3")     # player damage
mDmg_sound = pygame.mixer.Sound("assets/monsterdmg.mp3")        # monster damage
pImg = pygame.image.load("assets/sword.png").convert()      #player image
mImg = pygame.image.load("assets/Final Boss-Static.png").convert()   # monster image
start_mission_image = pygame.image.load("assets/finalboss_entry.png")
lose_music = pygame.mixer.Sound("assets/lose_music.wav")
win_music = pygame.mixer.Sound("assets/win_music.ogg")

#-------Data---------------

questions = ["5 ? 5 = 25", "5 + ? = 11", "3 + 7 = ?", "5 ? 3 = 8", "12 + ? = 18", "7 + 5 = ?", "10 ? 3 = 7", "17 - ? = 13", "9 ? 3 = 3", "14 + 3 = ?", "2 + 9 = ?", "7 x ? = 14"]
answers = ["*", "6", "10", "+", "6", "12", "-", "4", "/", "17", "11", "2"]

def display_start_screen():
    screen.blit(start_mission_image, (0, 0))  # Assuming the image size matches the screen size
    pygame.display.flip()
    finalboss_music.play(-1)
    finalboss_music.set_volume(0.5)
    time.sleep(1)  # Display the image for 3 seconds
   
# Call the function to display the start mission screen
display_start_screen()
time.sleep(1)
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/ThaleahFat.ttf", size)

def gameloop():
    # initial variables
    qNum = 0
    ans = "" 
    plrcurrhp = 100     # player hp
    moncurrhp = 200     # monster hp
    while True:
        GAME_MOUSE_POS = pygame.mouse.get_pos()
       
        if plrcurrhp < 1:
            gameover()
        if moncurrhp < 1:
            gamewin()
        else:
            SCREEN.fill("Black")
            SCREEN.blit(BG, (0, 0))
            updatehp(plrcurrhp, moncurrhp)
        numsym0 = Button(image=pygame.image.load("assets/Numbers204.png"), pos=(1192, 918), 
                                    text_input="0", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        numsym1 = Button(image=pygame.image.load("assets/Numbers204.png"), pos=(1192, 714), 
                                    text_input="1", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        numsym2 = Button(image=pygame.image.load("assets/Numbers204.png"), pos=(1192, 510), 
                                    text_input="2", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        numsym3 = Button(image=pygame.image.load("assets/Numbers204.png"), pos=(1192, 306), 
                                    text_input="3", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        numsym4 = Button(image=pygame.image.load("assets/Numbers204.png"), pos=(1192, 102), 
                                    text_input="4", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        numsym5 = Button(image=pygame.image.load("assets/Numbers204.png"), pos=(1432, 918), 
                                    text_input="5", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        numsym6 = Button(image=pygame.image.load("assets/Numbers204.png"), pos=(1432, 714), 
                                    text_input="6", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        numsym7 = Button(image=pygame.image.load("assets/Numbers204.png"), pos=(1432, 510), 
                                    text_input="7", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        numsym8 = Button(image=pygame.image.load("assets/Numbers204.png"), pos=(1432, 306), 
                                    text_input="8", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        numsym9 = Button(image=pygame.image.load("assets/Numbers204.png"), pos=(1432, 102), 
                                    text_input="9", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        calsym1 = Button(image=pygame.image.load("assets/Numbers204.png"), pos=(1672, 102), 
                                    text_input="+", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        calsym2 = Button(image=pygame.image.load("assets/Numbers204.png"), pos=(1672, 306), 
                                    text_input="-", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        calsym3 = Button(image=pygame.image.load("assets/Numbers204.png"), pos=(1672, 510), 
                                    text_input="x", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        calsym4 = Button(image=pygame.image.load("assets/Numbers204.png"), pos=(1672, 714), 
                                    text_input="/", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        calsym5 = Button(image=pygame.image.load("assets/Numbers204.png"), pos=(1672, 918), 
                                    text_input="ENTER", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        for button in [numsym0, numsym1, numsym2, numsym3, numsym4, numsym5, numsym6, numsym7, numsym8, numsym9, calsym1, calsym2, calsym3, calsym4, calsym5]:
                    button.changeColor(GAME_MOUSE_POS)
                    button.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if numsym0.checkForInput(GAME_MOUSE_POS):
                    Click_sound.play()
                    time.sleep(0.3)
                    ans += "0"
                if numsym1.checkForInput(GAME_MOUSE_POS):
                    Click_sound.play()
                    time.sleep(0.3)
                    ans += "1"
                if numsym2.checkForInput(GAME_MOUSE_POS):
                    Click_sound.play()
                    time.sleep(0.3)
                    ans += "2"
                if numsym3.checkForInput(GAME_MOUSE_POS):
                    Click_sound.play()
                    time.sleep(0.3)
                    ans += "3"
                if numsym4.checkForInput(GAME_MOUSE_POS):
                    Click_sound.play()
                    time.sleep(0.3)
                    ans += "4"
                if numsym5.checkForInput(GAME_MOUSE_POS):
                    Click_sound.play()
                    time.sleep(0.3)
                    ans += "5"
                if numsym6.checkForInput(GAME_MOUSE_POS):
                    Click_sound.play()
                    time.sleep(0.3)
                    ans += "6"
                if numsym7.checkForInput(GAME_MOUSE_POS):
                    Click_sound.play()
                    time.sleep(0.3)
                    ans += "7"
                if numsym8.checkForInput(GAME_MOUSE_POS):
                    Click_sound.play()
                    time.sleep(0.3)
                    ans += "8"
                if numsym9.checkForInput(GAME_MOUSE_POS):
                    Click_sound.play()
                    time.sleep(0.3)
                    ans += "9"
                if calsym1.checkForInput(GAME_MOUSE_POS):
                    Click_sound.play()
                    time.sleep(0.3)
                    ans += "+"
                if calsym2.checkForInput(GAME_MOUSE_POS):
                    Click_sound.play()
                    time.sleep(0.3)
                    ans += "-"
                if calsym3.checkForInput(GAME_MOUSE_POS):
                    Click_sound.play()
                    time.sleep(0.3)
                    ans += "*"
                if calsym4.checkForInput(GAME_MOUSE_POS):
                    Click_sound.play()
                    time.sleep(0.3)
                    ans += "/"
                if calsym5.checkForInput(GAME_MOUSE_POS):
                    Click_sound.play()
                    time.sleep(0.3)
                    check = checkans(qNum, ans) 
                    if check == True:
                        moncurrhp -= 25
                        qNum += 1
                        pDmg_sound.play()
                        ans = ""
                        break
                    else:
                        plrcurrhp -= 25
                        qNum += 1
                        mDmg_sound.play()
                        ans = ""
                        break
                        
        for i in range(12):
            SCREEN.blit(pImg, (50, 550))       # NEEED to set
            SCREEN.blit(mImg, (670, 100))      # NEED to set
            QUESTION_TEXT1 = get_font(75).render("What is :", True, "White")
            QUESTION_RECT1 = QUESTION_TEXT1.get_rect(center=(268, 350))
            SCREEN.blit(QUESTION_TEXT1, QUESTION_RECT1)

            question = questions[qNum]
            QUESTION_TEXT2 = get_font(75).render(question, True, "White")
            QUESTION_RECT2 = QUESTION_TEXT2.get_rect(center=(268, 400))
            SCREEN.blit(QUESTION_TEXT2, QUESTION_RECT2)
                        
        pygame.display.update()   
            

def gameover():
    finalboss_music.stop()
    lose_music.play()
    while True:
        
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(75).render("GAMEOVER", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(896, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)
        MENU_BACK = Button(image=None, pos=(896, 600), 
                            text_input="MAIN MENU", font=get_font(75), base_color="White", hovering_color="Green")

        MENU_BACK.changeColor(PLAY_MOUSE_POS)
        MENU_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MENU_BACK.checkForInput(PLAY_MOUSE_POS):
                    subprocess.run(['python', 'menu.py'])

        pygame.display.update()  
    
def gamewin():
    finalboss_music.stop()
    win_music.play()
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(75).render("YOU WIN!!!", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(896, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)
        MENU_BACK = Button(image=None, pos=(896, 600), 
                            text_input="MAIN MENU", font=get_font(75), base_color="White", hovering_color="Green")

        MENU_BACK.changeColor(PLAY_MOUSE_POS)
        MENU_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MENU_BACK.checkForInput(PLAY_MOUSE_POS):
                    subprocess.run(['python', 'menu.py'])

        pygame.display.update()         

def checkans(qNum, ans):
    if ans == answers[qNum]:
        return True
    else:
        return False

def updatehp(plr, mon):
    # update player hp
    plrhp = str(plr)
    plrhp = f"Player HP: {plrhp}/100"
    PLAYHP_TEXT = get_font(45).render(plrhp, True, "White")
    PLAYHP_RECT = PLAYHP_TEXT.get_rect(center=(804, 922))
    SCREEN.blit(PLAYHP_TEXT, PLAYHP_RECT)

    # update monster hp
    monhp = str(mon)
    monhp = f"Monster HP: {monhp}/200"
    MONHP_TEXT = get_font(45).render(monhp, True, "White")
    MONHP_RECT = MONHP_TEXT.get_rect(center=(268, 102))
    SCREEN.blit(MONHP_TEXT, MONHP_RECT)


    

gameloop()