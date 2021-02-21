# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 18:34:14 2021

@author: Ladon66
"""
#
#
#                         KALAHA
#
#
#       Regeln siehe https://de.wikipedia.org/wiki/Kalaha
#
#  Hinweise:
#  Die Button-Technik funktioniert sehr schlecht
#   Darstellung von Farben, aufblinken lassen etc. klappt nicht
#  Möglicherweise arbeitet auch die Bewertungs-Funktion nicht richtig 
#   (bezüglich Fangen und Extrarunde)

from __future__ import annotations
from typing import List, NewType, Dict
import copy
from enum import Enum
import pygame, time
from typing import Dict, List
from pygame import Surface, Rect, Color
pygame.init()

# Farben sind von hier: https://www.colorcombos.com/color-schemes/203/ColorCombo203.html
COLOR1:Color = pygame.Color( 27,  97, 155) # matisse / Inactive Color
COLOR2:Color = pygame.Color(172, 203, 224) # regent st blue / Active Color beim drüber-hovern
COLOR3:Color = pygame.Color(211, 224, 234) # botticelli  / Hintergrund
COLOR4:Color = pygame.Color(248, 242, 229) # yellow orange
COLOR5:Color = pygame.Color(154, 154, 155) # manatee   / Farbe der Schrift
COLOR6:Color = pygame.Color(215, 90, 32) # hot cinnamon
FONT = pygame.font.Font(None, 30)

n=10 # N ist zwischen 3 und 10
kList:List[Dict] =[]
screen:Surface = pygame.display.set_mode((1000, 460))
screen.fill(COLOR3)
clock = pygame.time.Clock()
Move = NewType('Move', int)


def tunix()->None:
    pass 

def whatMove(i)->None:
    global kList
    l1:int=len(kList)-1
    button:Dict=kList[l1]
    button['text']= FONT.render(str(i), True, COLOR5)
    draw_button(button, screen)



def quit_game()->None:  # A callback function for the button.
    pygame.quit()

def draw_button(button:Dict, screen)->None:
    """Draw the button rect and the text surface."""
    pygame.draw.rect(screen, button['color'], button['rect'])
    screen.blit(button['text'], button['text rect'])


def create_button(x, y, w, h, text, callback, bNummer):
    """A button is a dictionary that contains the relevant data.
    Consists of a rect, text surface and text rect, color and a
    callback function.
    """
    # The button is a dictionary consisting of the rect, text,
    # text rect, color and the callback function.
    text_surf:Surface = FONT.render(text, True, COLOR5)
    button_rect:Rect = pygame.Rect(x, y, w, h)
    text_rect:Rect = text_surf.get_rect(center=button_rect.center)
    button:Dict = {
        'rect': button_rect,
        'text': text_surf,
        'text rect': text_rect,
        'color': COLOR1,
        'callback': callback,
        'bNummer':bNummer
        }
    return button




class KPiece(Enum):
    SPIELER = 1                      # X ist der erste Spieler, der Mensch
    COMPUTER = 0                      # = ist der zweite Spieler, der Computer

    def opposite(self) -> KPiece:
        if self == KPiece.SPIELER:
            return KPiece.COMPUTER
        elif self == KPiece.COMPUTER:
            return KPiece.SPIELER

    def __str__(self) -> str:
        if self == KPiece.SPIELER:
            return "Spieler"
        elif self == KPiece.COMPUTER:
            return "Computer"


class KBoard():
    def __init__(self) -> None:
        self._n=n                            # Anzahl der Mulden pro Spieler, der Wert wird übergeben
        self._brett: List[int] = [0]*(self._n*2+2)  # Gesamtes Brett
        self._gMuldeSpieler:int = self._n+1  # Position der Mulde des Spielers
        self._gMuldeGegner:int  = 0          # Position der Mulde des Gegners
        self._turn:KPiece = startspieler     # Der startende Spieler
        self._message:str ="init"                # Die Info die dem Spieler angezeigt werden soll.
        for i1 in range (self._n*2+2):
            if i1 not in (self._gMuldeSpieler, self._gMuldeGegner):
                self._brett[i1]=m

    def turn(self) -> KPiece:
        return self._turn

    def eigene_Felder(self)->List[Move]:
        if self._turn == KPiece.SPIELER:
           return [Move(l) for l in range(1, self._n+1)]
        else:
           return [Move(l) for l in range(self._n+2,self._n*2+2)]

    def eigene_Mulde(self)->int:
        if self._turn==KPiece.SPIELER:
            return self._n+1
        else:
            return 0

    def gegner_Mulde(self)->int:
        if self._turn==KPiece.COMPUTER:
            return self._n+1
        else:
            return 0

    def move(self, location: Move, verbose:bool) -> KBoard:       # location ist die Startmulde
        temp_brett: KBoard = copy.deepcopy(self)
        temp_brett._message='...'                           # erstmal die Rückmeldung auf Leer setzen.
        start_mulde:int = location
        zz1 = temp_brett._brett[start_mulde]
        temp_brett._brett[start_mulde]=0
        while zz1>0:
            location = (location+1)%(temp_brett._n*2+2)
            if location != self.gegner_Mulde():
                 zz1 -=1
                 temp_brett._brett[location] +=1
        # Wenn der letzte Stein in einer leeren Spielmulde des aktiven Spielers landet und 
        # direkt gegenüber in der gegnerischen Mulde ein oder mehrere Steine liegen, sind 
        # sowohl der letzte Stein als auch die gegenüberliegenden Steine gefangen und werden 
        # zu den eigenen Steinen in die Gewinnmulde gelegt.
        if regel_Fangen:
            #print ("wegen Fangen: location: {}, startmulde: {} turn: ".format(location, start_mulde)+ str(self._turn)) 
            if temp_brett._brett[location]==1 and location in self.eigene_Felder():
                if verbose:
                    temp_brett._message='Fangen' 
                    print ("Fangen für ", self._turn)
                # z1 ist die gegenüberliegende Mulde
                z1=(temp_brett._n*2+2)-location
                # if self._turn == KPiece.SPIELER:
                #     print ("Fangen: location: {}, gegenüber: {} Eigene Felder: ".format(location, z1), self.eigene_Felder())
                temp_brett._brett[location]=0
                temp_brett._brett[self.eigene_Mulde()] +=1
                temp_brett._brett[self.eigene_Mulde()] += temp_brett._brett[z1]
                temp_brett._brett[z1]=0
        if not (regel_Extrarunde) or location != self.eigene_Mulde():
            temp_brett._turn = KPiece.opposite(self._turn)
        else:
            if verbose:
                temp_brett._message='Extrarunde für ' + str(self.turn())
                print ("Extrarunde für ", self._turn)
        return temp_brett

    @property
    def legal_moves(self) -> List[Move]:
        if self._turn == KPiece.SPIELER:
           return [Move(l) for l in range(1, self._n+1) if self._brett[l] != 0]
        else:
           return [Move(l) for l in range(self._n+2,self._n*2+2) if self._brett[l] != 0]

    @property
    def is_win(self) -> bool:
        # Wenn in der eigenen Gewinnmulde mehr Steine liegen als in der des Gegners
        return  self._brett[self._gMuldeGegner]>self._brett[self._gMuldeSpieler]

    def auswertung(self) -> None:
        # übrige Steine in die Mulden räumen:
        # eigener Spieler:
        for i in range (1, self._n+1):
            self._brett[self._gMuldeSpieler] += self._brett[i]
            self._brett[i]=0
        for i in range(self._n+2,self._n*2+2):
            self._brett[self._gMuldeGegner] += self._brett[i]
            self._brett[i]=0
        print ("Endstand:")
        print (self)
        if self._brett[self._gMuldeGegner]>self._brett[self._gMuldeSpieler]:
            print ("Computer hat gewonnen ", end="")
        elif self._brett[self._gMuldeGegner]<self._brett[self._gMuldeSpieler]:
            print ("Spieler hat gewonnen ", end="")
        else:
            print ("Unentschieden ", end="")
        print (str(self._brett[self._gMuldeGegner])+ ":"+ str(self._brett[self._gMuldeSpieler]))
        return

    # Evaluate muss anzeigen, wie gut die Stellung ist!!
    # Zunächst ist der Evaluate-Wert gleich dem Unterschied in den Gewinnmulden
    # ohne das Spielende zu beurteilen
    def evaluate(self, player: KPiece) -> float:
        diff:float = self._brett[self._gMuldeSpieler]-self._brett[self._gMuldeGegner]
        if self._turn == KPiece.SPIELER:
            return diff
        else:
            return diff * (-1)

    def wert_feld(self, i)->int:
        return self._brett[i]

    def belege_werte(self, button_list:List[Dict]):
        # Belegung der button_list mit den Werten aus board:
        # print ("belege Werte: ", self._message)
        i=0
        for button in button_list:
            if button['bNummer']!=99: # 99er sind andere Buttons
                wert:int=self.wert_feld(i)
                button['text']= FONT.render(str(wert), True, COLOR5)
                draw_button(button, screen)
                i += 1
        # Jetzt die Message schreiben.
        button = button_list[2]
        print ("belege Werte: ",self._message )
        button['text']=FONT.render(self._message, True, COLOR5)
        button['color']=COLOR1
        draw_button(button, screen)
        time.sleep(1)
        button['color']=COLOR1

    
    def show_message(self, button_list:List[Dict], msg:str, i:int):
        button=button_list[2]
        print ("show_Message: ",button)
        button['text']=FONT.render(msg, True, COLOR6)
        draw_button(button, screen)
        time.sleep(i)

    def get_message (self)->str:
        return self._message


    # Hier zeichnen wir das Brett
    def __repr__(self) -> str:
        str1 =""
        """if self._turn == KPiece.SPIELER:
            str1 += "Spieler ist am Zug \n"
        else:
            str1 += "Computer ist am Zug \n"""
        str1 += "    "     # Ein paar Leerzeichen, dann die Gegnermulden
        for z1 in range (self._n*2+1, self._n+1, -1):     # Gegnermulden
            str1 += " | %2d"% self._brett[z1]
        str1 += " |\n"
        str1 += str(self._brett[self._gMuldeGegner])  # Gewinnmulde Gegner
        str1 += " "*(5*self._n+8)                   # Viele Leerzeichen
        str1 += str(self._brett[self._gMuldeSpieler]) # Eigene Mulde
        str1 += "\n    "      # Ein paar Leerzeichen
        for z1 in range (1, self._n+1):        # Spielermulden
            str1 += " | %2d"% self._brett[z1]
        str1 += " |\n        "
        for z1 in range (1, self._n+1):        # Zahlen zur Hilfe
            str1 += str(z1)+"    "
        # Aufsummieren der Steine, manchmal gehen welche verloren:
        z1=0
        for i in range (self._n*2+2):
            z1 += self._brett[i]
        if z1 != n*m*2:
            str1 += " ABWEICHUNG: "+str(z1)
        str1 += "\n"
        return str1


def alphabeta(board: KBoard, maximizing: bool, original_player: KPiece, max_depth: int = 8, alpha: float = float("-inf"), beta: float = float("inf")) -> float:
    #Wenn keine Züge mehr möglich sind oder die Suchtiefe erreicht ist: Bewerte die Stellung
    if board.legal_moves==[] or max_depth == 0:
        return board.evaluate(original_player)

    if maximizing: # die eigenen Gewinne maximieren
        for move in board.legal_moves:
            result: float = alphabeta(board.move(move, False), False, original_player, max_depth - 1, alpha, beta)
            alpha = max(result, alpha)
            if beta <= alpha:
                break
        return alpha
    else:  # Die Gewinne des Gegners Minimieren
        for move in board.legal_moves:
            result = alphabeta(board.move(move, False), True, original_player, max_depth - 1, alpha, beta)
            beta = min(result, beta)
            if beta <= alpha:
                break
        return beta

button_list:List[Dict]=[]

# Den besten möglichen Zug an der aktuellen Position finden
# und bis zu max_depth vorausschauen
def find_best_move(board: KBoard, max_depth) -> Move:
    best_eval: float = float("-inf")
    best_move: Move = Move(-1)
    print ("Legal Moves:", board.legal_moves)
    for move in board.legal_moves:
        result: float = alphabeta(board.move(move, False), False, board.turn, max_depth)
        #print ("result: {0}, best_eval: {1}".format(result, best_eval))
        if result > best_eval:
            best_eval = result
            best_move = move
    return best_move




n:int=4                               # Anzahl der Mulden pro Spieler
m:int=5                               # Anzahl der Steine pro Mulde
level:int=6                           # Schwierigkeitsgrad
startspieler:KPiece = KPiece.SPIELER  # Startspieler
#startspieler:KPiece = KPiece.COMPUTER  # Startspieler
# Wenn der letzte Stein in der eigenen Gewinnmulde landet, gewinnt der aktive Spieler 
# eine Extra-Runde (oder: Bonus-Zug). Dies kann der Spieler auch mehrmals wiederholen 
# und darf dann jeweils weiterspielen.
regel_Extrarunde: bool = True
# Wenn der letzte Stein in einer leeren Spielmulde des aktiven Spielers landet und 
# direkt gegenüber in der gegnerischen Mulde ein oder mehrere Steine liegen, sind 
# sowohl der letzte Stein als auch die gegenüberliegenden Steine gefangen und werden 
# zu den eigenen Steinen in die Gewinnmulde gelegt.
regel_Fangen: bool = False


def main():

    # Buttons mit 99er Nummern sind keine Mulden sondern haben andere Aufgaben.
    button1:Dict = create_button(380, 380, 100, 50, 'Settings', tunix,99)
    button2:Dict = create_button(530, 380, 100, 50, 'Quit', quit_game,99)
    # Das wird der Nachrichten - Button!!!!
    button3:Dict = create_button(330, 300, 350, 50, '...', tunix,99)
    # Zeigt eine Nachricht an für eine bestimmte Zeit in Sekunden

    schritt_Weite = 80      # Die Felder sind 60 breit und der Zwischenraum ist 20
    gesamt_Breite = (n+2)*schritt_Weite-20   # Einen Zwischenraum abziehen
    xstart_Links   = (1000-gesamt_Breite)/2
    #Gewinnmulde Gegner
    kList.append(create_button(xstart_Links, 110, 60, 100, '0', tunix,0))
    # Untere Reihe für Spielermulden
    for i in range (1,n+1):
        xstart_Links += schritt_Weite
        kList.append(create_button(xstart_Links, 200, 60, 60, str(m), whatMove,i))
    #Gewinnmulde Spieler
    kList.append(create_button(xstart_Links+schritt_Weite, 110, 60, 100, '0', tunix,0))
        # Obere Reihe für Spielermulden
    for i in range (n+2,2*n+2):
        kList.append(create_button(xstart_Links,  80, 60, 60, str(m), tunix,0))
        xstart_Links -= 80


    # A list that contains all buttons.
    button_list = [button1, button2, button3] +kList
    board: KBoard = KBoard()

    board.belege_werte(button_list)
    board.show_message(button_list, 'Start',1)

    while True:
        for event in pygame.event.get():
            # This block is executed once for each MOUSEBUTTONDOWN event.
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 1 is the left mouse button, 2 is middle, 3 is right.
                if event.button == 1:
                    for button in button_list:
                        # `event.pos` is the mouse position.
                        if button['rect'].collidepoint(event.pos):
                            # Increment the number by calling the callback
                            # function in the button list.
                            # 99er Button: Aufruf ohne Parameter
                            if button['bNummer']==99:
                                button['callback']()
                            elif button['bNummer']>0:
                                board:KBoard = board.move(button['bNummer'], True)
                                print (board)
                                board.belege_werte(button_list)
                                if board.legal_moves==[]:
                                    print("Spiel ist aus")
                                    board.auswertung()
                                    break
                                while board.turn()==KPiece.COMPUTER:
                                    print("C ist dran: ", board.turn())
                                    computer_move: Move = find_best_move(board, level)
                                    print(f"Zug des Computers ist {computer_move}")
                                    board = board.move(computer_move, True)
                                    print (board)
                                    board.belege_werte(button_list)
                                if board.legal_moves==[]:
                                    print("Spiel ist aus")
                                    board.auswertung()
                                    break
            elif event.type == pygame.MOUSEMOTION:
                # When the mouse gets moved, change the color of the
                # buttons if they collide with the mouse.
                # Wenn callback = tunix ist das ein nicht aufrufbares Feld und 
                # wird anders gerendert.
                for button in button_list:
                    if button['rect'].collidepoint(event.pos) and button['callback']!=tunix:
                        button['color'] = COLOR2
                    else:
                        button['color'] = COLOR1

        #screen.fill(WHITE)
        for button in button_list:
            draw_button(button, screen)
        pygame.display.update()
        clock.tick(30)


main()
pygame.quit()