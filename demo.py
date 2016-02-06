import sys
import pygame
import time
import calendar
from datetime import date

from pygame.locals import *

FPS=30
fpsClock=pygame.time.Clock()

#opciones del grafico
ancho=240
alto=320
numFilas=7
numColumnas=4
borde=2
posActualSelector=0
sumaValor=0

#colores
NEGRO=(0,0,0)
BLANCO=(255,255,255)
AZUL=(0,0,255)
TEXTO=(255,255,255)
FONDO=(0,0,0)
CUADROS=(0,0,0)
RESALTADO=(0,255,0)

tituloX=ancho*2

arrNumeros=[]
num=0

#mensajes
arrMensajesTop=[]
arrMensajesTop.append("Weekday")
arrMensajesTop.append("Christmas Day")
arrMensajesTop.append("Easter")
arrMensajesTop.append("Thanksgiving")
arrMensajesTop.append("Mother's day")
arrMensajesTop.append("Father's day")
mensajeTopActual=0


for fila in range(numFilas):
        arrCol=[]
        for columna in range(numColumnas):
                arrCol.append(0)
                num+=1
                if (num>9):
                        num=0	
        arrNumeros.append(arrCol)

pygame.init()
#pygame.font.init()


fontObj=pygame.font.Font('DS-DIGIT.TTF',24)
fontObj1=pygame.font.Font('DS-DIGIT.TTF',18)

DISPLAYSURF=pygame.display.set_mode((ancho,alto))
pygame.display.set_caption("Demo")


def dibujaEncabezado():
    global mensajeTopActual
    global posActualSelector
    global sumaValor
    
    my_date = date.today()
    #cambiamos el mensaje
    if (posActualSelector==-1):
        print "Cambiando Top: "
        print str(sumaValor)
        numMensajesTop=len(arrMensajesTop)
        if (sumaValor!=0):
            mensajeTopActual+=sumaValor
            sumaValor=0
        if (mensajeTopActual<0):
            mensajeTopActual=numMensajesTop-1
        if (mensajeTopActual>(numMensajesTop-1)):
            mensajeTopActual=0
                
    if (mensajeTopActual==0):
        today = calendar.day_name[my_date.weekday()]
    else:
        today = arrMensajesTop[mensajeTopActual]
    fecha=time.strftime("%Y/%m/%d")
    textSurfaceObj=fontObj1.render(fecha,True, BLANCO, FONDO)
    textRectObj=textSurfaceObj.get_rect()
    textRectObj.center=((ancho/2),48)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
    textSurfaceObj=fontObj.render(today,True, BLANCO, FONDO)
    textRectObj=textSurfaceObj.get_rect()
    textRectObj.center=(tituloX,16)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
        
def dibujaCuadros():
        global sumaValor
        offsetX=130
        anchoCuadro=22 #ancho/numColumnas
        altoCuadro=(alto-64)/numFilas
        cuadroActual=0
        for y in range(numFilas):
                arrNums=arrNumeros[y]
                for x in range(numColumnas):
                        if (cuadroActual==posActualSelector):
                                COLOR=RESALTADO
                                #actualizamos el valor
                                if (sumaValor!=0):	
                                        arrNumeros[y][x]=arrNumeros[y][x]+sumaValor
                                        if (arrNumeros[y][x]>9):
                                                arrNumeros[y][x]=0
                                        if (arrNumeros[y][x]<0):
                                                arrNumeros[y][x]=9
                                        sumaValor=0

                        else:
                                COLOR=CUADROS
                        pygame.draw.rect(DISPLAYSURF, COLOR, ( offsetX+x*anchoCuadro ,64+(y*altoCuadro), (anchoCuadro-borde), (altoCuadro-borde)))
                        #dibujamos el numero actual
                        textSurfaceObj=fontObj.render(str(arrNums[x]),True, BLANCO, COLOR)
                        textRectObj=textSurfaceObj.get_rect()
                        textRectObj.center=(offsetX+(anchoCuadro/2)+x*(anchoCuadro),(64+altoCuadro/2)+y*(altoCuadro))
                        DISPLAYSURF.blit(textSurfaceObj, textRectObj)			


                        cuadroActual+=1

while True:
        DISPLAYSURF.fill(FONDO)
        dibujaEncabezado()
        dibujaCuadros()
        tituloX -= 1
        if (tituloX<=(-ancho*2)):
                tituloX=ancho*2
        for event in pygame.event.get():
                if event.type==QUIT:
                        pygame.quit()
                        sys,exit()
                elif event.type==KEYUP:		
                        if event.key==K_RIGHT:
                                posActualSelector+=1
                                if (posActualSelector>(numFilas*numColumnas-1)):
                                        posActualSelector=-1
                                #print posActualSelector
                        elif event.key==K_LEFT:
                                posActualSelector-=1
                                if (posActualSelector<-1):
                                        posActualSelector=(numFilas*numColumnas-1)
                                #print posActualSelector
                        elif event.key==K_UP:
                                sumaValor=1
                        elif event.key==K_DOWN:
                                sumaValor=-1
        pygame.display.update()
        fpsClock.tick(FPS)
