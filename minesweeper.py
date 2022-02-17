import tkinter as t
from tkinter import *
import random
from tkinter import messagebox

width=int(input("enter number of rows:"))
height=int(input("enter number of columns:"))
bombs=int(input("enter number of bombs:"))

tk=Tk()
tk.title("game")
bomblist=[]
l=[]
# buttons functions
class btn:
    def __init__(self,row,column,num,color):
        self.row=row
        self.column=column
        self.num=num
        self.color=color
        
    def print(self):
        self.but=Button(tk,width=4,height=2,command=self.clicked)#definig button
        self.but.grid(row=self.row,column=self.column)

    #to make the button look sunken and checking if bomb is clicked    
    def clicked(self):
        l.remove(self)#removing clicked button from list
        if self.num==0:
            self.but.config(relief=SUNKEN,bg=self.color,state=t.DISABLED)
            self.showzero()
        else:
            self.but.config(relief=SUNKEN,bg=self.color,text=self.num,state=t.DISABLED)
            if self.num=='bomb':
                self.showbomb()
        self.wincheck()
 
    def showbomb(self):
        for i in l:
            if i.num=='bomb':#printing all the bombs
                i.but.config(relief=SUNKEN,bg=i.color,text=i.num,state=t.DISABLED)
        messagebox.showinfo("game message","YOU LOST")
        tk.destroy()

    def wincheck(self):
        for i in l: #if only bombs are not clicked, player won
            if i.num!='bomb':
                break
        else:
            messagebox.showinfo("game message","YOU WON")
            tk.destroy()
        
    def showzero(self):
        for i in l:
            for j in [self.row-1,self.row,self.row+1]:
                for k in [self.column-1,self.column,self.column+1]:
                    if i.row==j and i.column==k:#printing all the cells surrounding 0
                        i.clicked()#if 0 is present in surrounding, this function runs again

#main game
while bombs:#creating bomblist without repetition
    x=random.randint(0,width-1)
    y=random.randint(0,height-1)
    if (x,y) not in bomblist:
        bomblist=bomblist+[(x,y)]
        bombs=bombs-1
        
for i in range(width):
    for j in range(height):
        if (i,j) in bomblist:#setting number and color
            num='bomb'
            color='red'
        else:
            num=0
            color='light yellow'
            for a in [i-1,i,i+1]:
                for b in [j-1,j,j+1]:#checking for surrounding 8 cells
                    if (a,b) in bomblist:
                        num=num+1
        s=btn(i,j,num,color)#creating object
        s.print()
        l=l+[s]#adding objects to a list
tk.mainloop()



