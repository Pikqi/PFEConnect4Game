import pygame as pg
import pygamebg

(sirina, visina) = (700, 600)
prozor = pygamebg.open_window(sirina, visina, "Connect4")
prozor.fill(pg.Color("white"))

polja = [[0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0]]

crveniCrta = True

x = -1
y = 0

poslednjiPotez = (0,0)
# boja, kolona, mesto u koloni, novo mesto
animacijaPotez = (0,0,0,0)

crtajX = 0
r = 50

def crtaj():
    global crveniCrta
    prozor.fill(pg.Color("white"))
    crtajPolja()
    crtajAnimaciju()

def crtajPolja():
    global polja, animacijaPotez
    for i in range(len(polja)):
        for j in range(len(polja[i])):
            if polja[i][j] == 1:
                # pg.draw.rect(prozor, pg.Color("red"), ((j+1)*100 - 100 , (i+1) * 100 - 100, 100,100))
                pg.draw.circle(prozor, pg.Color("red"), ((j+1)*100 - 100 + r,(i+1) * 100 - 100 + r), r)

            elif polja[i][j] == 2:
                # pg.draw.rect(prozor, pg.Color("yellow"), ((j+1)*100 - 100, (i+1)*100 - 100, 100,100))
                pg.draw.circle(prozor, pg.Color("yellow"), ((j+1)*100 - 100 + r,(i+1) * 100 - 100 + r), r)

def crtajAnimaciju():
    global animacijaPotez, r
    (boja, kolona, mestoUKoloni, pomeraj) = animacijaPotez
    if(boja == 1):
        pg.draw.circle(prozor, pg.Color("red"), ((kolona) * 100 + r, pomeraj), r)
    if(boja == 2):
        pg.draw.circle(prozor, pg.Color("yellow"), ((kolona) * 100 + r, pomeraj), r)


def obradiDogadjaj(dogadjaj):
    global crveniCrta, x, y, poslednjiPotez, animacijaPotez, r, polja
    if(dogadjaj.type == pg.MOUSEBUTTONDOWN):
        (x,y) = dogadjaj.pos
        (boja, kolona, mestoUKoloni, pomeraj) = animacijaPotez
        polja[mestoUKoloni][kolona] = boja
        kolona = proveriKolonu()
        
        for i in range(5, -1, -1):
            if polja[i][kolona] == 0:
                # polja[i][kolona] = 1 if crveniCrta else 2
                animacijaPotez = (1 if crveniCrta else 2, kolona, i, r)
                pg.time.set_timer(pg.USEREVENT, 50)
                crveniCrta = not crveniCrta
                poslednjiPotez = (i, kolona)
                break
        # print(str(proveriIgru()))
        return True
    # otkucaj tajmera
    if dogadjaj.type == pg.USEREVENT:
        (boja, kolona, mestoUKoloni, pomeraj) = animacijaPotez
        if(pomeraj == mestoUKoloni * 100 + r):
            pg.time.set_timer(pg.USEREVENT, 0)
            polja[mestoUKoloni][kolona] = boja
            boja = 0
            return True
        animacijaPotez = (boja, kolona, mestoUKoloni, pomeraj + 25)
        # crtajAnimaciju()
        
        return True
    

    return False    

def proveriIgru():
    global poslednjiPotez, polja

    (a, b) = poslednjiPotez
    boja = polja[a][b]
    # 4 vertikalna
    
    brojIstih = 0
    for i in range(a, 6):
        if polja[i][b] == boja:
            brojIstih += 1
            
        else:
            break
    if brojIstih >= 4:
        return True
    # 4 horizontalna
    # levo
    brojIstih = 0
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

    if brojIstih == 5:
        return True  

    # diagonalno 
    brojIstih = 0
    # gore desno
    x = a
    y = b

    
    while((not (x < 0 or y > 6)) and polja[x][y] == boja):
        brojIstih += 1
        x -= 1
        y += 1
        if brojIstih >= 4:
            return True

    x = a
    y = b        
    # dole levo

    while((not (x > 5 or y <0)) and polja[x][y] == boja):
        brojIstih += 1
        x += 1
        y -= 1
        # print("dole levo")
        if brojIstih >= 5:
            return True

    return False                   

def proveriKolonu(): 
    global x

    if(x < 100):
        return 0
    if(x < 200):
        return 1
    if(x < 300):
        return 2    
    if(x < 400):
        return 3
    if(x < 500):
        return 4
    if(x < 600):
        return 5
    if(x < 700):
        return 6 
    return False

pygamebg.event_loop(crtaj, obradiDogadjaj)