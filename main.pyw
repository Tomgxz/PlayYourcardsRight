"""

deal 8 cards to hiddendeck
show 1 card

set startfund=50

bet higherlower >=50
remove bet from hiddenbal

if win
bal += bet
hiddenbal=bal

else
bal=hiddenbal

\o/

when you get to three for the first time
bal += 200

on final bet, if bal >= 4000
can bet all for a car
else its the same

after final card, you get your winnings, inc car if bet for it

"""


from random import shuffle
from tkinter import Tk,Label,Frame,StringVar,Button,Toplevel
from tkinter.font import Font

import threading,time

threads={}

class Card():
    
    """ Card Class. Each individual card on the board is made from one of these """
    
    def __init__(self,suit,num,_id,wildcard=False):
        """ Default constructor. Defines all card attributes """
        self.suit=suit
        self.num=num
        self._id=_id

        self.tkCard=None

        if wildcard:
            self.wildCard=True
        else:
            self.wildCard=False
        
    def __repr__(self):
        """ Defines what is outputted on print( <Card object> ) """
        return f"<Card {self._id} {self.code()}>\n"
    
    def code(self):
        """ Returns the card code in the format <suit>:<number> """
        if self.wildCard:
            return f"X:00"

        num="0" if self.num > 9 else ""
        num=f"{num}{self.num}"

        return f"{self.suit}:{self.num}"

    def id(self):
        """ Returns the card id """
        return self._id

    def symbol(self):
        return {"S":"♠","C":"♣","H":"♥","D":"♦"}[self.suit]
        
    def defineTkCard(self,x):
        """ Links the tkinter card to the object."""
        self.tkCard=x

class Game():
    
    """ Main game class. Contains all tkinter code"""
    
    def __init__(self):
        """ Default constructor. Creates all attributes and runs the game """

        self.objects=[]
        
        self.cards=self.getStartingDeck()
        shuffle(self.cards)

        self.selected=None

        self.STARTINGBAL=50
        self.bal=self.STARTINGBAL
        self.betAmt=50

        self.money="💰"
        
        self.cards=self.cards[0:8]
        self.currentCard=0
        
        self.initializeTk()
        self.gameScreen()

        self.dlg=None
        
        self.root.mainloop()

        exit()

    def resetGame(self):
        self.objects=[]
        
        self.cards=self.getStartingDeck()
        shuffle(self.cards)

        self.selected=None

        self.bal=self.STARTINGBAL
        self.betAmt=50

        self.money="💰"
        
        self.cards=self.cards[0:8]
        self.currentCard=0
        
        self.gameScreen()

        self.dlg=None
        
        self.root.mainloop()

        exit()
        
    
    def initializeTk(self):
        """ Creates all tkinter variables including fonts and colors. Defines window attributes """
        self.root=Tk()

        self.fontPrimary="Lexend"
        self.fontSecondary="Roboto"

        self.titleFont=Font(
            family=self.fontPrimary,
            size="36",
            weight="bold"
        )

        self.headerFont=Font(
            family=self.fontPrimary,
            size="26",
        )

        self.headerFontBold=Font(
            family=self.fontPrimary,
            size="26",
            weight="bold"
        )

        self.captionFont=Font(
            family=self.fontPrimary,
            size="20",
            weight="bold"
        )

        self.bodyFont=Font(
            family=self.fontPrimary,
            size="12"
        )

        self.colors = {
            "dark":"#111111",
            "light":"#fdfdfd",

            "danger":"#EA5D5C",
            "warning":"#ffc107",
            "success":"#4dbd74",

            "primary": {
                "light": "#384461",
                "accent": "#2F3951",
                "normal": "#252D40",
                "dark": "#131720"
            },

            "secondary": {
                "light": "#FEC87C",
                "accent": "#FDBD63",
                "normal": "#FDB34B",
                "dark": "#FC9D17"
            },

            "accent1": {
                "light": "#83D7BB",
                "accent": "#70D1B1",
                "normal": "#5DCBA6",
                "dark": "#3BB98F"
            },

            "accent2": {
                "light": "#EF8476",
                "accent": "#EC7060",
                "normal": "#E95A47",
                "dark": "#E4331B"
            },

            "gray": {
                "50": "#f2f2f7",
                "100":"#cfcfd7",
                "200":"#c2cfd6",
                "300":"#c1c1cf",
                "400":"#9f9fab",
                "500":"#6d6d83",
                "600":"#5c6970",
                "700":"#454f54",
                "800":"#2e3538",
                "900":"#2e3538"
            }
        }
        
        self.bgcolor=self.colors["light"]

        self.root.title("Play Your Cards Right")
        self.root.iconbitmap('icon.ico')
        self.w=self.root.winfo_screenwidth()
        self.h=self.root.winfo_screenheight()
        self.root.geometry(f"{self.w}x{self.h}")
        self.root.minsize(self.w,self.h)
        self.root.state("zoomed")

        self.root.grid_columnconfigure(0, weight=1)

        self.root.configure(bg=self.bgcolor)

    def gameScreen(self):
        """ Creates screen shown when game is being played """
        title=self.createTitle()
        
        self.board=Frame(self.root,bg=self.bgcolor,pady=64)
        self.board.grid(row=1,column=0)
        self.board.grid_propagate(1)

        self.objects.append(self.board)

        self.deck=Frame(self.board,bg=self.bgcolor)
        self.deck.grid(row=0,column=0,pady=10,columnspan=2)
        self.deck.columnconfigure(8, weight=1)

        self.objects.append(self.deck)

        # create spaces

        for i in range(8):
            l=self.createPiecePlaceholder(self.deck)
            l.grid(row=1,column=i,padx=2)

        card=self.cards[0]
        l=self.createShownPiece(self.deck,card)
        card.defineTkCard(l)
        l.grid(row=1,column=0,padx=2)
    
        i=1
        for card in self.cards[1:]:
            l=self.createHiddenPiece(self.deck,card)
            card.defineTkCard(l)
            l.grid(row=1,column=i,padx=2)
            i+=1


        self.createBalanceBoard(col=i)



































        self.options=Frame(self.board,bg=self.bgcolor,pady=128)
        self.options.grid(row=1,column=0,columnspan=100)

        self.objects.append(self.options)

        self.betArea=Frame(self.options,width=500,height=50,bg=self.bgcolor)
        self.betArea.grid(row=1,column=1,padx=22,pady=32,columnspan=i+1)

        self.objects.append(self.betArea)

        _=Label(self.betArea,text="Select Betting Amount:", font=self.headerFont,fg=self.colors["dark"], bg=self.bgcolor,)
        _.grid(row=0,column=0,columnspan=3)

        self.objects.append(_)

        def onHover(e):
            """ Handles a card being hovered over """
            e.widget.config(bg=self.colors["accent1"]["accent"])

        def onHoverExit(e):
            """ Handles a card stopped being hovered over """
            e.widget.config(bg=self.colors["accent1"]["normal"])

        self.betDisplayVar=StringVar(self.betArea,f"{self.money} {self.betAmt}")
        
        self.betDisplay=Label(
            self.betArea,
            font=self.bodyFont,
            textvariable=self.betDisplayVar,
            bg=self.colors["accent1"]["normal"],
            width=10,
            height=2,
            bd=5,
            relief="groove",
            fg=self.colors["dark"]
        )

        self.objects.append(self.betDisplay)

        self.betDisplay.bind("<Enter>", onHover)
        self.betDisplay.bind("<Leave>", onHoverExit)

        self.betChangeBtns=Frame(self.betArea,bg=self.bgcolor,)

        self.objects.append(self.betChangeBtns)

        def resetColorThreadUp(self):
            time.sleep(1)
            self.betValUp.configure(fg=self.colors["dark"])

        def resetColorThreadDown(self):
            time.sleep(1)
            self.betValDown.configure(fg=self.colors["dark"])

        def incr(e,self):
            if self.betAmt >= self.bal:
                self.betValUp.configure(fg=self.colors["danger"])
                
                t = threading.Thread(target=resetColorThreadUp, args=[self])
                t.start()
                
                return
            
            self.betAmt+=50
            self.onBetChange()

        def decr(e,self):
            if self.betAmt <= 50:
                self.betValDown.configure(fg=self.colors["danger"])
                
                t = threading.Thread(target=resetColorThreadDown, args=[self])
                t.start()
                
                return
            
            self.betAmt-=50
            self.onBetChange()

        btnFont=Font(size=16)

        self.betValUp=Label(
            self.betChangeBtns,
            bd=0,
            fg=self.colors["dark"],
            text="⬆",
            font=btnFont,
            bg=self.bgcolor,
        )

        self.objects.append(self.betValUp)
    
        self.betValDown=Label(
            self.betChangeBtns,
            bd=0,
            fg=self.colors["dark"],
            text="⬇",
            font=btnFont,
            bg=self.bgcolor,
        )

        self.objects.append(self.betValDown)

        self.betValUp.bind("<Button-1>", lambda event, self=self: incr(event,self))
        self.betValDown.bind("<Button-1>", lambda event, self=self: decr(event,self))

        def max_(e,self):           
            self.betAmt=self.bal
            self.onBetChange()

        def min_(e,self):
            self.betAmt=50
            self.onBetChange()

        self.betValMax=Label(
            self.betChangeBtns,
            bd=0,
            fg=self.colors["dark"],
            text="Max",
            font=btnFont,
            bg=self.bgcolor,
        )

        self.objects.append(self.betValMax)
    
        self.betValMin=Label(
            self.betChangeBtns,
            bd=0,
            fg=self.colors["dark"],
            text="Min",
            font=btnFont,
            bg=self.bgcolor,
        )

        self.objects.append(self.betValMin)

    
        self.betValMax.bind("<Button-1>", lambda event, self=self: max_(event,self))
        self.betValMin.bind("<Button-1>", lambda event, self=self: min_(event,self))

        self.betDisplay.grid(row=1,column=0,sticky="e")
        self.betChangeBtns.grid(row=1,column=1, sticky="e")
        
        self.betValUp.grid(row=0,column=0, sticky="w",padx=16)
        self.betValDown.grid(row=1,column=0, sticky="w",padx=16)

        self.betValMax.grid(row=0,column=1, sticky="w",padx=16)
        self.betValMin.grid(row=1,column=1, sticky="w",padx=16)






























        def onHover(e,isHigh):
            """ Handles a piece being hovered over """
            
            if isHigh:
                if self.selected==True:
                    return
            else:
                if self.selected==False:
                    return
                
            e.widget.config(fg=self.colors["gray"]["800"])

        def onHoverExit(e,isHigh):
            """ Handles a piece stopped being hovered over """
            
            if isHigh:
                if self.selected==True:
                    return
            else:
                if self.selected==False:
                    return
                
            e.widget.config(fg=self.colors["dark"])

        def onClick(e,self,isHigh):
            if isHigh:
                if self.selected==False or self.selected==None:
                    self.selected=True
                    
                    self.high.config(fg=self.colors["accent1"]["dark"])
                    self.low.config(fg=self.colors["dark"])

                    self.activateBtn()

            if not isHigh:
                if self.selected==True or self.selected==None:
                    self.selected=False
                    
                    self.high.config(fg=self.colors["dark"])
                    self.low.config(fg=self.colors["accent1"]["dark"])

                    self.activateBtn()
                    
        self.higherOrLowerFrame=Frame(self.options,width=50,height=50,bg=self.bgcolor,)
        self.higherOrLowerFrame.grid(row=1,column=0,padx=22,pady=32)

        self.objects.append(self.higherOrLowerFrame)

        self.high=Label(self.higherOrLowerFrame,text="Higher", font=self.headerFontBold,fg=self.colors["dark"],bg=self.bgcolor,)
        self.high.grid(row=0,column=0,padx=32)

        self.objects.append(self.high)

        self.low=Label(self.higherOrLowerFrame,text="Lower", font=self.headerFontBold,fg=self.colors["dark"],bg=self.bgcolor,)
        self.low.grid(row=0,column=1,padx=32)

        self.objects.append(self.low)

        self.high.bind("<Button-1>", lambda event, self=self, isHigh=True: onClick(event,self,isHigh))
        self.high.bind("<Enter>", lambda event, isHigh=True: onHover(event,isHigh))
        self.high.bind("<Leave>", lambda event, isHigh=True: onHoverExit(event,isHigh))

        self.low.bind("<Button-1>", lambda event, self=self, isHigh=False: onClick(event,self,isHigh))
        self.low.bind("<Enter>", lambda event, isHigh=False: onHover(event,isHigh))
        self.low.bind("<Leave>", lambda event, isHigh=False: onHoverExit(event,isHigh))



        self.goBtn=Button(
            self.options,
            text="Place Bet!",
            font=self.headerFont,
            fg=self.colors["dark"],
            bg=self.colors["gray"]["400"],
            activebackground=self.colors["accent2"]["normal"],
            bd=5,
            relief="groove",
            state="disabled",
            command=self.takeTurn,
        )

        self.objects.append(self.goBtn)
        
        self.goBtn.grid(row=2,column=0,pady=64,columnspan=999)


    def takeTurn(self):
        self.currentCard+=1
        try:
            card=self.cards[self.currentCard]
        except IndexError:
            raise Exception("All cards area already displayed")
        
        l=self.createShownPiece(self.deck,card)
        card.defineTkCard(l)
        l.grid(row=1,column=self.currentCard,padx=2)

        card=self.cards[self.currentCard]
        pcard=self.cards[self.currentCard-1]

        fail=False

        if self.selected:
            if pcard.num >= card.num:
                fail=True
        else:
            if pcard.num <= card.num:
                fail=True

        if fail:
            self.bal-=self.betAmt
            self.onBalChange()
        else:
            self.bal+=self.betAmt
            self.onBalChange()
            

        if self.currentCard == 3:
            self.bal+=200
            self.onBalChange()


        if self.bal < 50:
            self.loseScreen()
        elif self.currentCard == 7:
            self.winScreen()


    def loseScreen(self):
        if self.dlg is not None:
            self.dlg.destroy()
        self.dlg=LoseScreen(self.root,self)

    def winScreen(self):
        if self.dlg is not None:
            self.dlg.destroy()
        self.dlg=WinScreen(self.root,self)
        
    def activateBtn(self):
        if self.selected is not None:
            self.goBtn.configure(fg=self.colors["dark"],bg=self.colors["accent2"]["normal"],state="active")
        
    def onBetChange(self):
        self.betDisplayVar.set(f"{self.money} {self.betAmt}")

    def onBalChange(self):
        self.balanceVar.set(f"Your Balance:\n{self.money} {self.bal}")
        self.betDisplayVar.set(f"{self.money} 50")
        self.betAmt=50

    def createTitle(self):
        """ Creates and returns the title text object """
        title=Label(self.root,text="Play Your Cards Right", font=self.titleFont,fg=self.colors["dark"],bg=self.bgcolor)
        title.grid(row=0,column=0)
        self.objects.append(title)
        return title
       
    def createPiecePlaceholder(self,root):
        """ Creates and returns a widget containing nothing. In context, used to define the size of the grid, and all the positions in it """
        label=Label(
            root,
            font=self.captionFont,
            text="",
            bg=self.bgcolor,
            width=3,
            height=2,
            bd=5,
            #relief="groove",
        )

        self.objects.append(label)

        return label

    def createBalanceBoard(self,col=9):
        """ Creates a widget showing the balance """

        def onHover(e):
            """ Handles a card being hovered over """
            e.widget.config(bg=self.colors["accent1"]["accent"])

        def onHoverExit(e):
            """ Handles a card stopped being hovered over """
            e.widget.config(bg=self.colors["accent1"]["normal"])
       
        self.balanceVar=StringVar(self.board,f"Your Balance:\n{self.money} {self.bal}")
        
        self.balance=Label(
            self.board,
            font=self.captionFont,
            textvariable=self.balanceVar,
            bg=self.colors["accent1"]["normal"],
            width=12,
            height=2,
            bd=5,
            relief="groove",
            fg=self.colors["dark"]
        )

        self.balance.grid(row=0,column=col,padx=22)

        self.balance.bind("<Enter>", onHover)
        self.balance.bind("<Leave>", onHoverExit)

        self.objects.append(self.balance)
        
    def createShownPiece(self,root,card):
        """ Creates and returns a card on the board. Contains commands that handle card selection and movement. Calls a command to check all cards for invalid positions """

        def onHover(e):
            """ Handles a card being hovered over """
            e.widget.config(bg=self.colors["gray"]["200"])

        def onHoverExit(e):
            """ Handles a card stopped being hovered over """
            e.widget.config(bg=self.colors["gray"]["100"])
       
        if card.suit in ["C","S"]:
            cardsuit=self.colors["primary"]["light"]
        elif card.suit in ["H","D"]:
             cardsuit=self.colors["accent2"]["dark"]
        
        label=Label(
            root,
            font=self.captionFont,
            text=f"{card.num}\n{card.symbol()}",
            bg=self.colors["gray"]["100"],
            cursor="plus",
            width=3,
            height=2,
            relief="groove",
            bd=5,
            fg=cardsuit,
        )

        label.bind("<Enter>", onHover)
        label.bind("<Leave>", onHoverExit)

        self.objects.append(label)

        return label

    def createHiddenPiece(self,root,card):
        """ Creates and returns a card on the board. Contains commands that handle card selection and movement. Calls a command to check all cards for invalid positions """

        def onHover(e):
            """ Handles a card being hovered over """
            e.widget.config(bg=self.colors["secondary"]["dark"])

        def onHoverExit(e):
            """ Handles a card stopped being hovered over """
            e.widget.config(bg=self.colors["secondary"]["normal"])
    
        
        label=Label(
            root,
            font=self.captionFont,
            text="",
            bg=self.colors["secondary"]["normal"],
            width=3,
            height=2,
            relief="groove",
            bd=5,
        )

        label.bind("<Enter>", onHover)
        label.bind("<Leave>", onHoverExit)

        self.objects.append(label)

        return label

    def destroyWindow(self):
        for obj in self.objects[::-1]:
            obj.destroy()
        #self.root.destroy()
        
    def getStartingDeck(self):
        colors=["S","C","H","D"]
        deck=[]
        colorInt=0
        step=1
        id_=0

        color=colors[colorInt]

        for i in range(52):
            deck.append(Card(color,step,id_))
            step+=1
            id_+=1

            if i==51:
                continue

            if step>13:
                colorInt+=1
                step=1
                color=colors[colorInt]
                    
        colorInt=0
        step=1
        
        return deck  

class DialogBox(Toplevel):
    def __init__(self,parent,inheritedself):
        
        self.inherit=inheritedself

        Toplevel.__init__(self,parent)

        self.w=int(self.inherit.root.winfo_screenwidth()//3)
        self.h=int(self.inherit.root.winfo_screenheight()//3.5)

        self.geometry(f"{self.w}x{self.h}")
        self.minsize(self.w,self.h)
        self.maxsize(self.w,self.h)

        self.configure(bg=self.inherit.bgcolor)

        self.grid_columnconfigure(0, weight=1)

        self.container=Frame(self,bg=self.inherit.bgcolor)


        btns=Frame(self,bg=self.inherit.bgcolor)
        
        btn1=Button(
            btns,
            text="Retry",
            font=self.inherit.headerFont,
            fg=self.inherit.colors["dark"],
            bg=self.inherit.colors["accent1"]["normal"],
            activebackground=self.inherit.colors["accent1"]["normal"],
            bd=5,
            relief="groove",
            width=7,
            command=self.reset,
        )

        btn2=Button(
            btns,
            text="Exit",
            font=self.inherit.headerFont,
            fg=self.inherit.colors["dark"],
            bg=self.inherit.colors["accent2"]["normal"],
            activebackground=self.inherit.colors["accent2"]["normal"],
            bd=5,
            relief="groove",
            width=7,
            command=self.destroyStuff
        )

        self.container.grid(row=0,column=0,pady=16)
        btns.grid(row=1,column=0,pady=48)
        btn1.grid(row=0,column=0,padx=32)
        btn2.grid(row=0,column=1,padx=32)

    def destroyStuff(self):
        raise SystemExit

    def reset(self):
        self.destroy()
        self.inherit.resetGame()

class LoseScreen(DialogBox):
    def __init__(self,parent,inheritedself):

        DialogBox.__init__(self,parent,inheritedself)
        self.title("You Lost! - Play Your Cards Right")

        txt=Label(self.container,text="You Went Bust!", font=self.inherit.titleFont,fg=self.inherit.colors["dark"],bg=self.inherit.bgcolor)
        txt.grid(row=0,column=0,padx=32)

class WinScreen(DialogBox):
    def __init__(self,parent,inheritedself):

        DialogBox.__init__(self,parent,inheritedself)
        self.title("You Won! - Play Your Cards Right")

        sv=StringVar(self.container,f"You Won {self.inherit.money} {self.inherit.bal}!")

        if self.inherit.bal >= 4000:
            sv.set(f"You Won a Car!")

        txt=Label(self.container,textvariable=sv, font=self.inherit.titleFont,fg=self.inherit.colors["dark"],bg=self.inherit.bgcolor)
        txt.grid(row=0,column=0,padx=32)
            
        

if __name__ == "__main__":
    Game()
