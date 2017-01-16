#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Elliot
#
# Created:     02/08/2015
# Copyright:   (c) Elliot 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from Tkinter import *
import time, random

Master = Tk()


class Game1():

    def __init__(self, xcoord1=380, ycoord1=550, xcoord2=400, ycoord2=570):
        self.Master = Master
        self.Master.geometry("800x600+0+0")
        self.xcoord1 = xcoord1
        self.xcoord2 = xcoord2
        self.ycoord1 = ycoord1
        self.ycoord2 = ycoord2
        self.Lasers = []
        self.Direction = [[-1, 0], [0, 1], [1, 0], [0, 1]]
        self.DirectionCounter = 0
        self.LifeMultiplier = 1
        self.BossCount = 0
        self.RememberColourChange = 0
        Game1Canvas = Canvas(self.Master, bg="black", height=600, width=800)
        Game1Canvas.place(x=0, y=0)
        self.Canvas = Game1Canvas
        self.Master.bind("<Left>", self.MoveLeft)
        self.Master.bind("<Right>", self.MoveRight)
        self.Canvas.bind("<Button-1>", self.Shoot)
        self.Ship = self.Canvas.create_rectangle(self.xcoord1, self.ycoord1, self.xcoord2, self.ycoord2, fill = "red")
        self.Level = 1
        self.Lives = 3
        self.LifeText = self.Canvas.create_text(750, 550, text = "LIVES: " + str(self.Lives), fill="green", font=1000)
        self.LevelPlay()

    def GameOver(self):
        for i in range(0, 20):
            time.sleep(0.1)
            self.GameOverText = self.Canvas.create_text(390, 300, text = "GAME OVER", fill="red", font=1000)
            Master.update()
            time.sleep(0.1)
            self.Canvas.delete(self.GameOverText)
            Master.update()
        self.Canvas.destroy()
        self.__init__()

    def MoveLeft(self, event):
        (x0,y0,x1,y1) = self.Canvas.bbox(self.Ship)
        if x0 > 0:
            self.Canvas.move(self.Ship, -10, 0)

    def MoveRight(self, event):
        (x0,y0,x1,y1) = self.Canvas.bbox(self.Ship)
        if x1 < self.Canvas.winfo_width():
            self.Canvas.move(self.Ship, 10, 0)

    def Shoot(self, event):
        if len(self.Lasers) < 20:
            (x0,y0,x1,y1) = self.Canvas.bbox(self.Ship)
            Laser = self.Canvas.create_rectangle(x0 + 2, y0 - 30, x1 - 2, y1 - 30, fill = "pink")
            self.Lasers.append(Laser)

    def Boss(self):
        self.BossCount += 1
        for i in range(0, 20):
            time.sleep(0.1)
            self.LevelText = self.Canvas.create_text(390, 300, text = "WARNING, BOSS LEVEL!!!", fill="red", font=1000)
            Master.update()
            time.sleep(0.1)
            self.Canvas.delete(self.LevelText)
            Master.update()
        self.Enemy = self.Canvas.create_rectangle(300, 0, 500, 200, fill="green", tags="Enemy")
        Count = self.Canvas.find_all()[len(self.Canvas.find_all()) - 1]
        self.Enemy_Data = {"EnemyID": Count, "EnemyColour": "Green", "EnemyHealth": 10 * self.BossCount,  "ShootDelay": 9999}
        self.EnemyList.append(self.Enemy_Data)

    def do_animation(self):
        if self.DirectionCounter == 35:
            self.DirectionCounter = 0
        else:
            self.DirectionCounter += 1
        Lasers = self.Lasers[:]
        if self.RememberColourChange != 0:
            self.Canvas.itemconfig(self.RememberColourChange, fill = "green")
            self.RememberColourChange = 0
        for i in range(0, len(self.EnemyList)):
            if self.EnemyList[i]["ShootDelay"] == 0:
                (x0,y0,x1,y1) = self.Canvas.bbox(self.EnemyList[i]["EnemyID"])
                EnemyLaser = self.Canvas.create_rectangle(x0 + 2, y0 + 30, x1 - 2, y1 + 30, fill = "purple")
                self.Lasers.append("E" + str(EnemyLaser))
                self.EnemyList[i]["ShootDelay"] = random.choice([240, 270, 300, 330, 360, 390, 420, 450])
            else:
                self.EnemyList[i]["ShootDelay"] -= 1
        for Laser in Lasers:
            if str(Lasers[Lasers.index(Laser)])[0] == "E":
                (x0,y0,x1,y1) = self.Canvas.bbox(Laser[1:len(Lasers[Lasers.index(Laser)])])
                if self.Canvas.find_overlapping(x0, y0, x1, y1) > 0:
                    for i in range(0, len(self.Canvas.find_overlapping(x0, y0, x1, y1))):
                        if self.Canvas.find_overlapping(x0, y0, x1, y1)[i] == self.Ship:
                            self.Lives -= 1
                            self.Canvas.delete(Laser[1:len(Lasers[Lasers.index(Laser)])])
                            self.Lasers.remove(Laser)
                            self.Canvas.itemconfig(self.LifeText, text="LIVES: " + str(self.Lives))
                            break
                if y1 < self.Canvas.winfo_height():
                    self.Canvas.move(Laser[1:len(Lasers[Lasers.index(Laser)])], 0, 10)
                else:
                    self.Canvas.delete(Laser[1:len(Lasers[Lasers.index(Laser)])])
                    self.Lasers.remove(Laser)
            else:
                (x0,y0,x1,y1) = self.Canvas.bbox(Laser)
                if y1 > 0:
                    self.Canvas.move(Laser, 0, -10)
                else:
                    self.Canvas.delete(Laser)
                    self.Lasers.remove(Laser)
            if len(self.Canvas.find_overlapping(x0, y0, x1, y1)) > 1:
                for i in range(0, len(self.EnemyList)):
                    if self.EnemyList[i - 1]["EnemyID"] == self.Canvas.find_overlapping(x0, y0, x1, y1)[0] and str(Laser)[0] != "E":
                        if self.EnemyList[i - 1]["EnemyHealth"] == 1:
                            self.EnemyList.pop(i - 1)
                            self.Canvas.delete(self.Canvas.find_overlapping(x0, y0, x1, y1)[0])
                            self.Canvas.delete(Laser)
                            self.Lasers.remove(Laser)
                            break
                        else:
                            self.EnemyList[i - 1]["EnemyHealth"] -= 1
                            self.RememberColourChange = self.EnemyList[i - 1]["EnemyID"]
                            self.Canvas.itemconfig(self.EnemyList[i - 1]["EnemyID"], fill = "red")
                            self.Canvas.delete(Laser)
                            self.Lasers.remove(Laser)
                            break
        if len(self.Canvas.find_overlapping(0, self.Canvas.winfo_height(), self.Canvas.winfo_width(), self.Canvas.winfo_height() + 10)) > 0:
            for i in range(0, len(self.Canvas.find_overlapping(0, self.Canvas.winfo_height(), self.Canvas.winfo_width(), self.Canvas.winfo_height() + 10))):
                for s in range(0, len(self.EnemyList)):
                    if self.EnemyList[s - 1]["EnemyID"] == self.Canvas.find_overlapping(0, self.Canvas.winfo_height(), self.Canvas.winfo_width(), self.Canvas.winfo_height() + 10)[0]:
                        self.Lives -= 1
                        self.Canvas.itemconfig(self.LifeText, text="LIVES: " + str(self.Lives))
                        self.EnemyList.pop(0)
                        self.Canvas.delete(self.Canvas.find_overlapping(0, self.Canvas.winfo_height(), self.Canvas.winfo_width(), self.Canvas.winfo_height() + 10)[0])
        for i in range(0, 1): #+ (self.Level * 1)):
            self.Canvas.move("Enemy", self.Direction[self.DirectionCounter / 9][0], self.Direction[self.DirectionCounter / 9][1])
        if self.Lives < 0:
            self.GameOver()
        else:
            if len(self.EnemyList) < 1:
                self.Level += 1
                self.LevelPlay()
            else:
                Master.after(30, self.do_animation)

    def LevelPlay(self):
        self.EnemyList = []
        self.EnemyListColours = ["green", "green", "blue", "green", "yellow", "blue", "green"]
        for i in range(0, 20):
            time.sleep(0.1)
            self.LevelText = self.Canvas.create_text(390, 300, text = "LEVEL " + str(self.Level), fill="red", font=1000)
            Master.update()
            time.sleep(0.1)
            self.Canvas.delete(self.LevelText)
            Master.update()
        if self.Level % 4 == 0:
            self.Boss()
            self.LifeMultiplier += 1
        else:
            for s in range(0, self.Level):
                self.Enemy_Locations = [[100, 0 - ((s) * 100), 120, 20 - ((s) * 100)], [200, 0 - ((s) * 100), 220, 20 - ((s) * 100)], [300, 0 - ((s) * 100), 320, 20 - ((s) * 100)], [400, 0 - ((s) * 100), 420, 20 - ((s) * 100)], [500, 0 - ((s) * 100), 520, 20 - ((s) * 100)], [600, 0 - ((s) * 100), 620, 20 - ((s) * 100)], [700, 0 - ((s) * 100), 720, 20 - ((s) * 100)]]
                for i in range(0, 7):
                    TempColour = random.choice(self.EnemyListColours)
                    self.Enemy = self.Canvas.create_rectangle(self.Enemy_Locations[i][0], self.Enemy_Locations[i][1], self.Enemy_Locations[i][2], self.Enemy_Locations[i][3], fill=TempColour, tag="Enemy")
                    Count = self.Canvas.find_all()[len(self.Canvas.find_all()) - 1]
                    self.Enemy_Data = {"EnemyID": Count, "EnemyColour": TempColour, "EnemyHealth": 1 * self.LifeMultiplier, "ShootDelay": random.choice([0, 30, 60, 90, 120, 150, 180, 210, 240, 240, 270, 300, 330, 360, 390, 420, 450])}
                    self.EnemyList.append(self.Enemy_Data)
        self.do_animation()

Game1()

Master.mainloop()

