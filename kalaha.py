# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 18:34:14 2021

@author: Ladon66
"""
#
#
#              KALAHA
#
#

from __future__ import annotations
from typing import List
from board import Piece, Move
from minmax import find_best_move
import copy
from enum import Enum


class KPiece(Piece, Enum):
    SPIELER = 1                      # X ist der erste Spieler, der Mensch
    COMPUTER = 0                      # = ist der zweite Spieler, der Computer

    def opposite(self) -> KPiece:
        if self == KPiece.SPIELER:
            return KPiece.COMPUTER
        elif self == KPiece.COMPUTER:
            return KPiece.SPIELER

    def __str__(self) -> str:
        return self.value


class KBoard():
    def __init__(self, n:int=6, m:int=4) -> None:
        self._n=n                            # Anzahl der Mulden pro Spieler, der Wert wird übergeben
        self._brett: List[int] = [0]*(self._n*2+2)  # Gesamtes Brett
        self._gMuldeSpieler:int = self._n+1  # Position der Mulde des Spielers
        self._gMuldeGegner:int  = 0          # Position der Mulde des Gegners
        self._turn:KPiece = KPiece.SPIELER          # Der Spieler startet immer
        for i1 in range (self._n*2+2):
            if i1 not in (self._gMuldeSpieler, self._gMuldeGegner):
                self._brett[i1]=m

    def turn(self) -> Piece:
        return self._turn

    def move(self, location: Move) -> KBoard:       # location ist die Startmulde
        temp_brett: KBoard = copy.deepcopy(self)
        # Welche Mulde ist die gegnerische Mulde?
        if self._turn==KPiece.SPIELER:
            zMulde:int = self._gMuldeGegner
        else:
            zMulde:int = self._gMuldeSpieler
        start_mulde:int = location
        #temp_brett._brett[location]=0              #Die Start-Mulde wird leer gemacht
        #print ("Tempbrett: ", temp_brett._brett)
        while temp_brett._brett[start_mulde]>0:
            location = (location+1)%(temp_brett._n*2+2)
            if location != zMulde:
                 temp_brett._brett[location] +=1
                 temp_brett._brett[start_mulde] -=1
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


    # Gib Ja zurück, wenn unentschieden
    @property
    def is_draw(self) -> bool:
        self._brett[self._gMuldeGegner]==self._brett[self._gMuldeSpieler]

    # Evaluate muss anzeigen, wie gut die Stellung ist!!
    # Zunächst ist der Evaluate-Wert gleich dem Unterschied in den Gewinnmulden
    # ohne das Spielende zu beurteilen
    def evaluate(self, player: Piece) -> float:
        diff:float = self._brett[self._gMuldeSpieler]-self._brett[self._gMuldeGegner]
        if self._turn == KPiece.SPIELER:
            return diff
        else:
            return diff * (-1)

    def naechster_spieler(self)->None:
       self._turn = KPiece.opposite(self._turn)

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
        str1 += " |\n" + str(self._brett[self._gMuldeGegner])  # Gewinnmulde Gegner
        str1 += " "*(5*self._n+8)                   # Viele Leerzeichen
        str1 += str(self._brett[self._gMuldeSpieler]) # Eigene Mulde
        str1 += "\n    "      # Ein paar Leerzeichen
        for z1 in range (1, self._n+1):        # Spielermulden
            str1 += " | %2d"% self._brett[z1]
        str1 += " |\n        "
        for z1 in range (1, self._n+1):        # Zahlen zur Hilfe
            str1 += str(z1)+"    "
        str1 += "\n"
        # Aufsummieren der Steine, manchmal gehen welche verloren:
        """z1=0
        for i in range (self._n*2+2):
            z1 += self._brett[i]
        str1 += "Anzahl Steine: "+str(z1)+"\n"""
        return str1



n=6       # Anzahl der Mulden pro Spieler
m=4
board: KBoard = KBoard(n,m)
print (board)

def get_player_move() -> Move:
    player_move: Move = Move(-1)
    while player_move not in board.legal_moves:
        if board._turn == KPiece.SPIELER:
            print("Spieler ist am Zug \n")
        else:
            print("Computer ist am Zug \n")
        play: int = int(input("Legales Feld eingeben (0-"+str(n)+"): "))
        player_move = Move(play)
    return player_move


if __name__ == "__main__":
    # Spiel-Hauptschleife
    while True:
        human_move: Move = get_player_move() # Der Move ist die Zahleingabe!
        board:KBoard = board.move(human_move)
        print(board)
        board.naechster_spieler()
        if board.legal_moves==[]:
            print("Spiel ist aus")
            break
        computer_move: Move = find_best_move(board)
        print(f"Zug des Computers ist {computer_move}")
        board = board.move(computer_move)
        print(board)
        board.naechster_spieler()
        if board.legal_moves==[]:
            print("Spiel ist aus")
            break
    board.auswertung()
