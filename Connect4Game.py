import pygame as pg
import pygamebg
import random
import numpy as np
import math
(sirina, visina) = (700, 600)
prozor = pygamebg.open_window(sirina, visina, "Connect4")
prozor.fill(pg.Color("white"))

crvena = 1
zuta = 2

najboljiPotezIScore = 0
pobedioJe = 0
crveniCrta = True
igraGotova = False
animacijaUToku = False
nacinIgre = 2 # 0 = nije izabrano 1 = igrac protiv igraca 2 = igrac protiv racunara
mis_x = -1
y = 0
# poluprecnik kruga
r = 50

def matricaNula():
    return [([0]*7) for i in range(6)]


polja = matricaNula()

poslednjiPotez = (0,0)
# boja, kolona, mesto u koloni, novo mesto
animacijaPotez = (0,0,0,0)

def crtaj():
    prozor.fill(pg.Color("white"))

    # if nacinIgre == 0:
    #     crtajBirajMod()


   
    
    crtajKolone()
    crtajPolja()
    crtajAnimaciju()
    if igraGotova:
        crtajGotovaIgra()

def crtajBirajMod():
    global nacinIgre
    prozor.fill(pg.Color("white"))
    # pg.draw.rect(prozor, pg.Color("white"), ((sirina/2 -200, visina / 2 - 200), (400, 150))) #400 * 150

    font = pg.font.SysFont("Arial", 20)
    tekst = font.render("Igrac protiv igraca", True, pg.Color("black"))
    tekstRect = tekst.get_rect(center = ((sirina/2 -200, visina / 2 - 200)))

    # pg.draw.rect(prozor, pg.Color("white"), ((sirina/2 -200, visina / 2 ), (400, 150)))
    

def crtajGotovaIgra():
    global sirina, visina, igraGotova, animacijaPotez
    (boja, s,s,s) = animacijaPotez
    if igraGotova :
        # prozor.fill(pg.Color("black"))

        font = pg.font.SysFont("Arial", 40)
        tekst = font.render("Igra gotova", True, pg.Color("blue"))
        tekstRect = tekst.get_rect(center = (sirina // 2, visina // 2))
        prozor.blit(tekst, tekstRect)

        tekst = font.render("Zuti je pobedio" if pobedioJe == 2 else "Crveni je pobedio", True, pg.Color("blue"))
        tekstRect = tekst.get_rect(center = (sirina // 2, visina // 2 + 50))
        prozor.blit(tekst, tekstRect)
        
        animacijaPotez = (0,0,0,0)

def crtajKolone():
    for i in range(1, 7):
        pg.draw.line(prozor, pg.Color("black"), (i * 100, 0), (i * 100, visina), 3)

# crtanje svih polja iz matrice polja
def crtajPolja():
    global polja, animacijaPotez

    for i in range(len(polja)):
        for j in range(len(polja[i])):
            if polja[i][j] == 1:
                pg.draw.circle(prozor, pg.Color("red"), ((j+1)*100 - 100 + r,(i+1) * 100 - 100 + r), r)
            elif polja[i][j] == 2:
                pg.draw.circle(prozor, pg.Color("yellow"), ((j+1)*100 - 100 + r,(i+1) * 100 - 100 + r), r)


# crtanje trenutnog padajuceg kruga
def crtajAnimaciju():
    global animacijaPotez, r
    (boja, kolona, mestoUKoloni, pomeraj) = animacijaPotez
    if(boja == crvena):
        pg.draw.circle(prozor, pg.Color("red"), ((kolona) * 100 + r, pomeraj), r)
        return
    if(boja == zuta):
        pg.draw.circle(prozor, pg.Color("yellow"), ((kolona) * 100 + r, pomeraj), r)


def obradiDogadjaj(dogadjaj):
    global crveniCrta, mis_x, y, poslednjiPotez, animacijaPotez, r, polja, igraGotova, animacijaUToku

    if(dogadjaj.type == pg.MOUSEBUTTONDOWN and not animacijaUToku):
        if(igraGotova):
            igraGotova = not igraGotova
            polja = matricaNula()
            crveniCrta = True
            return True

        (mis_x,y) = dogadjaj.pos
        (boja, kolona, mestoUKoloni, pomeraj) = animacijaPotez
        polja[mestoUKoloni][kolona] = boja
        igraGotova = nadjiScore(poslednjiPotez, polja) >= 4
        kolona = proveriKolonu()
        
        for i in range(5, -1, -1):
            if polja[i][kolona] == 0:
                # polja[i][kolona] = 1 if crveniCrta else 2
                animacijaPotez = (crvena if crveniCrta else zuta, kolona, i, r)
                pg.time.set_timer(pg.USEREVENT, 50)
                animacijaUToku = True
                # crveniCrta = not crveniCrta
                poslednjiPotez = (i, kolona)
                break
        
        return True
    # otkucaj tajmera
    if dogadjaj.type == pg.USEREVENT:
        (boja, kolona, mestoUKoloni, pomeraj) = animacijaPotez
        if(pomeraj == mestoUKoloni * 100 + r):
            pg.time.set_timer(pg.USEREVENT, 0)
            animacijaUToku = False
            polja[mestoUKoloni][kolona] = boja
            boja = 0
            if nadjiScore(poslednjiPotez, polja) >= 4:
                igraGotova = True
                return True
            igrajSledeciPotez()
            igraGotova = nadjiScore(poslednjiPotez, polja) >= 4
            return True
        animacijaPotez = (boja, kolona, mestoUKoloni, pomeraj + 25)
        # crtajAnimaciju()
        
        return True
    
    return False    

def igrajSledeciPotez():
    global polja, poslednjiPotez
    
    # while True:
    #     mesto = random.randint(0, 6)
    #     y = nadjiSlobodnoY(mesto, polja)

    #     if y < 6:
    #         break
        
    # polja[y][mesto] = zuta
    # poslednjiPotez = (y, mesto)

    noviPotez =  minimax(polja, 2, True, poslednjiPotez)[1]

    (a, b) = noviPotez

    polja[a][b] = zuta
    poslednjiPotez = (a, b)
    
    
def minimax(polja1, depth, isMaximizing, poslednjiPotez1):
    global najboljiPotezIScore
    if depth == 0 or nadjiScore(poslednjiPotez1, polja1) >= 4:
        return [nadjiScore(poslednjiPotez1, polja1), poslednjiPotez1]

    if isMaximizing:
        najboljiPotez = (0,0)
        score = -math.inf
        for i in range(0, 7):
            y = nadjiSlobodnoY(i, polja1)
            if y >=6:
                continue
            else:
                polja2 = np.copy(polja1)
                polja2[y][i] = zuta
                poslednjiPotez1 = (y, i)
                newScore = minimax(polja2, depth-1, not isMaximizing, poslednjiPotez1)[0] 
                if newScore > score:
                    najboljiPotez = (y, i)
                    score = newScore
                # score = max(score, minimax(polja2, depth - 1, not isMaximizing, poslednjiPotez1)[0])

        return [score, najboljiPotez]
    if not isMaximizing:
        najboljiPotez = (0,0)
        score = math.inf
        for i in range(0, 7):
            y = nadjiSlobodnoY(i, polja1)
            if y >=6:
                continue
            else:
                polja2 = np.copy(polja1)
                polja2[y][i] = crvena 
                poslednjiPotez1 = (y, i)
                newScore = minimax(polja2, depth-1, not isMaximizing, poslednjiPotez1)[0] 
                if newScore < score:
                    najboljiPotez = (y, i)
                    score = newScore            
        return [score, poslednjiPotez1]
def nadjiScore(poslednjiPotez, polja):
    # global poslednjiPotez, polja, pobedioJe
    global pobedioJe
    score = -math.inf

    pobedioJe = 0
    (a, b) = poslednjiPotez
    boja = polja[a][b]
    if boja == 0:
        return False
    # 4 vertikalna
    
    brojIstih = 0
    for i in range(a, 6):
        if polja[i][b] == boja:
            brojIstih += 1
            
        else:
            break
    # if brojIstih >= 4:
    #     pobedioJe = boja
    #     # return True
    score = max(score, brojIstih)    

    # 4 horizontalna
    # levo
    brojIstih = -1
    for i in range(b, -1, -1):
        if polja[a][i] == boja:
            brojIstih += 1
        
        else:
            break
    # desno
    for i in range(b, 7):
        if polja[a][i] == boja:
            brojIstih += 1
        else:
            break

    # if brojIstih >= 5:
    #     pobedioJe = boja
    #     return True  

    score = max(score, brojIstih)

    # diagonalno 
    brojIstih = 1
    # gore desno
    x = a-1
    y = b+1

    while((not (x < 0 or y > 6)) and polja[x][y] == boja):
        brojIstih += 1
        x -= 1
        y += 1

    x = a+1
    y = b-1        
    # dole levo

    while((not (x > 5 or y < 0)) and polja[x][y] == boja):
        brojIstih += 1
        x += 1
        y -= 1
        # print("dole levo")
    # if brojIstih >=4:
        #  pobedioJe = boja
    #     return True
    score = max(score, brojIstih)
    # gore levo
    brojIstih = 1

    x = a - 1
    y = b - 1
    while ((not (x < 0 or y < 0)) and (polja[x][y] == boja)):
        brojIstih += 1
        x -= 1
        y -= 1
    # if brojIstih >= 4:
    #     pobedioJe = boja
    #     return True    
    score = max(score, brojIstih)
    # dole desno
    
    x = a + 1
    y = b + 1
    while ((not (x > 5 or y > 6)) and (polja[x][y] == boja)):
        brojIstih += 1
        x += 1
        y += 1
    # if brojIstih >= 4:
    #     pobedioJe = boja
    #     return True    
    score = max(score, brojIstih)
    if score >= 4:
        pobedioJe = boja
    return score    

# vraca index kolone na osnovu pozicije misa na ekranu
def proveriKolonu(): 
    global mis_x

    for i in range(7):
        if mis_x < (i+1) *  100:
            return i
    return False

def nadjiSlobodnoY (x, polja):
    for i in range(5, 0, -1):
        if polja[i][x] == 0:
            return i
    return 6
    
pygamebg.event_loop(crtaj, obradiDogadjaj)