import pygame as pg
import pygamebg

(sirina, visina) = (700, 600)
prozor = pygamebg.open_window(sirina, visina, "Connect4")
prozor.fill(pg.Color("white"))

crvena = 1
zuta = 2

crveniCrta = True
igraGotova = False
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
    
    if igraGotova :
        crtajGotovaIgra()
    else:
        crtajKolone()
        crtajPolja()
        crtajAnimaciju()


def crtajGotovaIgra():
    global sirina, visina, igraGotova, animacijaPotez
    (boja, s,s,s) = animacijaPotez
    if igraGotova :
        prozor.fill(pg.Color("black"))

        font = pg.font.SysFont("Arial", 20)
        tekst = font.render("Igra gotova", True, pg.Color("white"))
        tekstRect = tekst.get_rect(center = (sirina // 2, visina // 2))
        prozor.blit(tekst, tekstRect)

        tekst = font.render("Zuti je pobedio" if boja == 2 else "Crveni je pobedio", True, pg.Color("white"))
        tekstRect = tekst.get_rect(center = (sirina // 2, visina // 2 + 25))
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
    global crveniCrta, mis_x, y, poslednjiPotez, animacijaPotez, r, polja, igraGotova

    if(dogadjaj.type == pg.MOUSEBUTTONDOWN):
        if(igraGotova):
            igraGotova = not igraGotova
            polja = matricaNula()
            crveniCrta = True
            return True

        (mis_x,y) = dogadjaj.pos
        (boja, kolona, mestoUKoloni, pomeraj) = animacijaPotez
        polja[mestoUKoloni][kolona] = boja
        igraGotova = proveriIgru()
        kolona = proveriKolonu()
        
        for i in range(5, -1, -1):
            if polja[i][kolona] == 0:
                # polja[i][kolona] = 1 if crveniCrta else 2
                animacijaPotez = (crvena if crveniCrta else zuta, kolona, i, r)
                pg.time.set_timer(pg.USEREVENT, 50)
                crveniCrta = not crveniCrta
                poslednjiPotez = (i, kolona)
                break
        
        return True
    # otkucaj tajmera
    if dogadjaj.type == pg.USEREVENT:
        (boja, kolona, mestoUKoloni, pomeraj) = animacijaPotez
        if(pomeraj == mestoUKoloni * 100 + r):
            pg.time.set_timer(pg.USEREVENT, 0)
            polja[mestoUKoloni][kolona] = boja
            igraGotova = proveriIgru()
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
    if boja == 0:
        return False
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
    if brojIstih >=4:
        return True

    # gore levo
    brojIstih = 1

    x = a - 1
    y = b - 1
    while ((not (x < 0 or y < 0)) and (polja[x][y] == boja)):
        brojIstih += 1
        x -= 1
        y -= 1
    if brojIstih >= 4:
        return True    

    # dole desno
    
    x = a + 1
    y = b + 1
    while ((not (x > 5 or y > 6)) and (polja[x][y] == boja)):
        brojIstih += 1
        x += 1
        y += 1
    if brojIstih >= 4:
        return True    

    return False    

# vraca index kolone na osnovu pozicije misa na ekranu
def proveriKolonu(): 
    global mis_x

    for i in range(7):
        if mis_x < (i+1) *  100:
            return i
    return False

pygamebg.event_loop(crtaj, obradiDogadjaj)