import tkinter as t
from tkinter import *
import random
from tkinter import messagebox

tk=Tk()
tk.title("X-O")
class game:
    def __init__(self):
        self.xwin=0
        self.owin=0
        self.tie=0
        self.start(None)
        
    def start(self,txt):
        if txt=='X':self.xwin+=1
        elif txt=='O':self.owin+=1
        elif txt=='tie':self.tie+=1
        self.l=[['','',''],['','',''],['','','']]
        self.btns=[['','',''],['','',''],['','','']]
        self.mov=1
        for i in range(3):
            for j in range(3):
                self.btns[i][j]=btn(i,j)
                self.btns[i][j].print()
        l1=Label(tk,text="'X'wins:"+str(self.xwin),height=2,font=("COMIC SANS MS",20,"bold")).grid(row=3,column=0)
        l2=Label(tk,text="'O'wins:"+str(self.owin),height=2,font=("COMIC SANS MS",20,"bold")).grid(row=3,column=1)
        l3=Label(tk,text="Tie:"+str(self.tie),height=2,font=("COMIC SANS MS",20,"bold")).grid(row=3,column=2)

    def wincheck(self,txt):
        for i in range(3):
            if (self.l[i][0]==self.l[i][1]==self.l[i][2]==txt) or (self.l[0][i]==self.l[1][i]==self.l[2][i]==txt):
                messagebox.showinfo("game message",txt+" won")
                self.start(txt)
        if (self.l[1][1]==self.l[2][2]==self.l[0][0]==txt) or (self.l[2][0]==self.l[1][1]==self.l[0][2]==txt):
            messagebox.showinfo("game message",txt+" won")
            self.start(txt)
        elif ('' not in self.l[0]) and ('' not in self.l[1]) and ('' not in self.l[2]):
            messagebox.showinfo("game message","Tie !!\n awesome game :)")
            self.start('tie')

    def ai(self):
        if self.mov==2:
            if self.l[1][1]=='X':
                self.aiclick(0,0)
            else:
                self.aiclick(1,1)
        elif self.mov>2:
            if (self.aidefence('O')):pass
            elif (self.aidefence('X')):pass
            elif (self.mov==4 and self.doubleattack()):pass
            else:
                for i in self.l:
                    if '' in i:
                        self.ai_randfill()
                        break
        self.wincheck('O')

    def aidefence(self,var):
        for i in range(3):
            num=-1
            if self.l[i][0]==self.l[i][1]==var:num=2
            elif self.l[i][0]==self.l[i][2]==var:num=1
            elif self.l[i][1]==self.l[i][2]==var:num=0
            if num!=-1 and self.l[i][num]=='':
                self.aiclick(i,num)
                return True

        for i in range(3):
            num=-1
            if self.l[0][i]==self.l[1][i]==var:num=2
            elif self.l[0][i]==self.l[2][i]==var:num=1
            elif self.l[1][i]==self.l[2][i]==var:num=0
            if num!=-1 and self.l[num][i]=='':
                self.aiclick(num,i)
                return True
            
        if self.l[0][0]==self.l[1][1]==var and self.l[2][2]=='':
            self.aiclick(2,2)
            return True
        elif self.l[0][0]==self.l[2][2]==var and self.l[1][1]=='':
            self.aiclick(1,1)
            return True
        elif self.l[2][2]==self.l[1][1]==var and self.l[0][0]=='':
            self.aiclick(0,0)
            return True
        
        if self.l[0][2]==self.l[1][1]==var and self.l[2][0]=='':
            self.aiclick(2,0)
            return True
        elif self.l[0][2]==self.l[2][0]==var and self.l[1][1]=='':
            self.aiclick(1,1)
            return True
        elif self.l[2][0]==self.l[1][1]==var and self.l[0][2]=='':
            self.aiclick(0,2)
            return True
        return False

    def ai_randfill(self):
        a=random.randint(0,2)
        b=random.randint(0,2)
        if(self.l[a][b]==''):
            self.aiclick(a,b)
            return
        self.ai_randfill()

    def aiclick(self,row,col):
        self.l[row][col]='O'
        self.btns[row][col].but.config(text='O',state=t.DISABLED,disabledforeground="green")
        self.mov+=1

    def doubleattack(self):
        if self.l[0][1]==self.l[1][0]=='X' or self.l[0][2]==self.l[1][0]=='X' or self.l[0][1]==self.l[2][0]=='X':
            self.aiclick(0,0)
            return True
        elif self.l[2][1]==self.l[1][2]=='X' or self.l[2][0]==self.l[1][2]=='X' or self.l[0][2]==self.l[2][1]=='X':
            self.aiclick(2,2)
            return True
        elif self.l[0][1]==self.l[1][2]=='X' or self.l[0][1]==self.l[2][2]=='X' or self.l[0][0]==self.l[1][2]=='X':
            self.aiclick(0,2)
            return True
        elif self.l[1][0]==self.l[2][1]=='X' or self.l[1][0]==self.l[2][2]=='X' or self.l[0][0]==self.l[2][1]=='X':
            self.aiclick(2,0)
            return True
        elif self.l[2][0]==self.l[0][2]=='X' or self.l[0][0]==self.l[2][2]=='X':
            self.aiclick(0,1)
            return True
        elif self.l[1][1]==self.l[2][2]=='X':
            self.aiclick(0,2)
            return True
        return False
        
class btn:
    def __init__(self,row,column):
        self.row=row
        self.column=column
        
    def print(self):
        self.but=Button(tk,bg="papaya whip",width=3,text=" ",bd=15,font=('arial',60,'bold'),relief=SUNKEN,command=self.clicked)
        self.but.grid(row=self.row,column=self.column)

    def clicked(self):
        maingame.mov+=1
        maingame.l[self.row][self.column]='X'
        self.but.config(text='X',state=t.DISABLED,disabledforeground="blue")
        maingame.wincheck('X')
        maingame.ai()
maingame=game()
messagebox.showinfo("Challenge","I challege you\n 'X' will never increase from 0")
tk.mainloop()
