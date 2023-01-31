from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000) #set up i2c object
oled = SSD1306_I2C(128, 64, i2c) #set up screen object

def callHub():
    oled.fill(0) #clears the screen
    oled.text("Password Manager",0,0) #writes text at those coordinates
    oled.text("A-Search",30,10)
    oled.text("B-Create",30,20)
    oled.text("C-Favourites",15,30)
    oled.show() #displays the buffered screen
    
def callLock(text):
    oled.fill(0)
    oled.text("Enter Password:",0,0)
    oled.text(text,0,20)
    oled.text("A-Enter",30,50)
    oled.show()
    
def callNewName(currName):
    oled.fill(0)
    oled.text("Enter Name:",0,0)
    oled.text(currName,0,15)
    oled.text("A-Accept",30,30)
    oled.text("#-Back",35,40)
    oled.show()
    
def callNewPass(accName,genPass):
    oled.fill(0)
    oled.text("Do you want",20,0)
    oled.text(accName,((128-(len(accName)*8))//2),10) #centres text
    oled.text("to have password",0,20)
    oled.text(genPass,20,30)
    oled.text("A-Accept #-Back",0,40)
    oled.text("B-Regenerate",0,50)
    oled.show()
    
def callSearchPass(search,results):
    oled.fill(0)
    oled.text("Enter Search:",0,0)
    oled.text(search,0,10)
    oled.text("A-"+results[0],0,20)
    oled.text("B-"+results[1],0,30)
    oled.text("C-"+results[2],0,40)
    oled.text("#-Back",0,50)
    oled.show()
    
def callSelectPass(selected,password):
    oled.fill(0)
    oled.text(selected,0,0)
    oled.text(password,0,12)
    oled.text("A-Type  D-Regen",0,24)
    oled.text("B-Delete",20,34)
    oled.text("C-Favourite",10,44)
    oled.text("#-Back",20,54)
    oled.show()

def callFavourites(favDict):
    oled.fill(0)
    oled.text("Favourites",0,0)
    oled.text("1-"+favDict["1"],0,10)
    oled.text("2-"+favDict["2"],0,20)
    oled.text("3-"+favDict["3"],0,30)
    oled.text("4-"+favDict["4"],0,40)
    oled.text("#-Back",0,50)
    oled.show()
    
def callSetFav(favName):
    oled.fill(0)
    oled.text("Set Location For",0,0)
    oled.text(favName,((128-(len(favName)*8))//2),20) #centres text
    oled.text("1-4",50,40)
    oled.show()

def callChangePass(accName,genPass):
    oled.fill(0)
    oled.text("Change password:",0,0)
    oled.text(accName,((128-(len(accName)*8))//2),10) #centres text
    oled.text("to",55,20)
    oled.text(genPass,((128-(len(genPass)*8))//2),30)
    oled.text("A-Accept B-Regen",0,40)
    oled.text("#-Cancel",30,50)
    oled.show()