from machine import UART, Pin #libraries for serial communication
import sdcard #libraries for sd card communication
import uos

import json #library for parsing dictionaries

import utime #library for sleep()

import hashlib #library for hashing master password

from FunctionRef import encrypt,decrypt,genPass,returnSearched #links all the external functions from another file
from ScreenRef import callHub,callLock,callNewName,callNewPass,callSearchPass,callSelectPass,callFavourites,callSetFav, callChangePass #links all the screen scripts from another file

def changePassInput(key):
    global changeName, newPass, passDict,activescreen
    if key == "A":
        passDict[changeName] = newPass
        callChangePass(changeName,"Completed") #updates the screen letting the user know the password was added and the sd card was updated without error.
        utime.sleep(1)
        activescreen = "Hub"
        callHub() #goes back to the main menu
    if key == "B":
        newPass = genPass()
        callChangePass(changeName,newPass)
    if key == "#":
        activescreen = "Hub"
        callHub()

def writePass():
    global favourites, passDict, password, hashOut
    with open("/sd/data.txt", "w") as file: #writes new data back to file
        file.write(hashOut+"\r\n")
        file.write(str(encrypt(json.dumps(favourites),password))+"\r\n")
        file.write(str(encrypt(json.dumps(passDict),password)))

def serialSend(text):
    uart.write(text) #sends the text to be entered to the computer over serial to a different microcontroller

def favInput(key):
    global favourites,activescreen
    if key in "1234": #validates input
        if favourites[key] != "": #checks that slot isn't empty
            serialSend(passDict[favourites[key]]) #sends password associated with username to computer
            activescreen = "Hub"
            callHub() #back to main menu
    if key == "#":
        activescreen = "Hub"
        callHub()

def setFavInput(key):
    global favourites,selectedPass,activescreen, favourites, passDict, password, hashOut
    if key in "1234": #validates input
        favourites[key] = selectedPass #sets the value of the dictionary to the name of the password
        writePass()
        activescreen = "Hub"
        callHub() #back to main menu

def searchPassInput(key):
    global floatingText, selectedPass, activescreen, changeName
    if key not in "ABC#": #checks if input is text entry
        Typing(key) 
        callSearchPass(floatingText,returnSearched(floatingText,passDict)) #calls the search algorithm and updates the screen with the results
    if key in "ABC":
        returned = returnSearched(floatingText,passDict) #gets search results
        if key == "A":
            if returned[0] != "":
                selectedPass = returned[0] #sets a variable to be equal to the result chosen
        if key == "B":
            if returned[1] != "":
                selectedPass = returned[1]
        if key == "C":
            if returned[2] != "":
                selectedPass = returned[2]
        activescreen = "SelectPass"
        changeName = selectedPass
        callSelectPass(selectedPass,passDict[selectedPass]) #changes screen to show options available with that chosen result
    if key == "#":
        activescreen = "Hub" #go back to main menu
        callHub()
        clearTyping()

def selectPassInput(key):
    global selectedPass, activescreen, newPass, changeName
    if key in "ABCD#":
        if key == "A":
            serialSend(passDict[selectedPass]) #sends the password over serial
            callSelectPass(selectedPass,"completed") #lets the user know the action was completed
            utime.sleep(1)
            activescreen = "Hub" #back to main menu
            callHub()
        elif key == "B":
            delAccount(selectedPass) #calls function to delete password
            callSelectPass(selectedPass,"completed") #lets the user know the action was completed
            utime.sleep(1)
            activescreen = "Hub" #back to main menu
            callHub()
        elif key == "#":
            print("Hash")
            activescreen = "Hub" #back to main menu
            callHub()
        elif key == "C":
            activescreen = "SetFav" #calls menu to choose the slot of the password
            callSetFav(selectedPass)
        elif key == "D":
            activescreen = "ChangePass"
            newPass = genPass()
            callChangePass(changeName,newPass)
            
            
def addNewAccount(username,givenPass):
    global passDict, favourites, password
    passDict[username] = givenPass #creates a key value pair with the name of the account as the key and the value as the password
    writePass()
        
def delAccount(username):
    global passDict, favourites, password
    del passDict[username] #deletes key value pair from the main dictionary
    if username in favourites.values(): #if password was a favourite, replace it with an empty string
        for item in favourites:
            if favourites[item] == username:
                favourites[item] = ""
    writePass()

def newPassInput(key):
    global activescreen,newName,newPass
    if key == "A":
        addNewAccount(newName,newPass)
        callNewPass(newName,"Completed") #updates the screen letting the user know the password was added and the sd card was updated without error.
        utime.sleep(1)
        activescreen = "Hub"
        callHub() #goes back to the main menu
    elif key == "#":
        activescreen = "NewName"
        callNewName("")
    elif key == "B":
        newPass = genPass() #regenerates the password
        callNewPass(newName,newPass)

def newNameInput(key):
    global activescreen,floatingText,newName,newPass
    if key not in "A#": #checks if input should be handled as text entry
        Typing(key)
        callNewName(floatingText) #calls the typing algorithm with the pressed key and updates the screen with the new output
    elif key == "A":
        newName = floatingText #sets the name of the new password
        clearTyping()
        activescreen = "NewPass"
        newPass = genPass()
        callNewPass(newName,newPass) #moves on to the new password screen with a randomly generated password
    elif key == "#":
        clearTyping()
        activescreen = "Hub"
        callHub() #deletes all text entered and goes back to the hub
        
def hubInput(key):
    global activescreen
    if key == "B":
        activescreen = "NewName" #calls screen to create new name
        callNewName("")
    if key == "A":
        activescreen = "SearchPass"
        clearTyping()
        callSearchPass("",["","",""]) #calls the search screen with no text entered and no results shown
    if key == "C":
        activescreen = "Favourites" #calls favourites menu
        callFavourites(favourites)
    
def lockInput(key):
    global currentPassword, activescreen,dictDump, passDict, password, favDump, favourites
    if key not in "ABCD*#": #checks if input is valid
        currentPassword = currentPassword + key #adds the number pressed to string and updates the screen
        callLock(currentPassword)
    elif key == "*":
        currentPassword = currentPassword[:-1] #deletes the last character in the string
        callLock(currentPassword)
    elif key == "A":
        if str(hashlib.sha256(currentPassword).digest()) == hashOut: #hashes entered password with sha256, checks password against hash stored on SD card
            password = int(currentPassword)
            #print(dictDump)
            #print(password)
            #print(decrypt(dictDump,password))
            #print(type(decrypt(dictDump,password)))
            passDict = json.loads(decrypt(dictDump,password)) #Decrypts contents of SD card
            favourites = json.loads(decrypt(favDump,password)) #Decrypts contents of favourites menu
            #print(favourites)
            activescreen = "Hub" #changes screen
            callHub()
        else:
            callLock("wrong") #tells the user the entered password is wrong
            utime.sleep(1)
            currentPassword = ""
            callLock(currentPassword)

def Keypad4x4Read(cols,rows):
  for r in rows:
    r.value(0) #sets the current pin low
    result=[cols[0].value(),cols[1].value(),cols[2].value(),cols[3].value()] #creates an array to store the current pin states
    if min(result)==0: #if any pins are low
      key=key_map[int(rows.index(r))][int(result.index(0))] #finds the key based on the keymap and the current row and column that are low
      r.value(1) #sets the pin high
      return(key)#returns the key
    r.value(1)

floatingText = "" #sets up global variables required for typing
fixedText = ""
letterMap = {"1":["","1"],"2":["a","b","c","2"],"3":["d","e","f","3"],"4":["g","h","i","4"],"5":["j","k","l","5"],"6":["m","n","o","6"],"7":["p","q","r","s","7"],"8":["t","u","v","8"],"9":["w","x","y","z","9"],"0":[" ","0"]}
floatingInput = ""
floatingChar = ""
floatingReps = 0

def clearTyping(): #function to reset the value of all variable associated with typing
    global fixedText, floatingText, letterMap, floatingInput, floatingChar, floatingReps
    floatingInput = ""
    floatingChar = ""
    floatingReps = 0
    fixedText = ""
    floatingText = ""

def Typing(key):
    global fixedText, floatingText, letterMap, floatingInput, floatingChar, floatingReps
    if key == "*": #backspace key
        if floatingInput == "":
            fixedText = fixedText[:-1] #either clears the floating text, or removes the last letter of fixed text 
        floatingInput = "" #resets variables
        floatingChar = ""
        floatingReps = 0
        floatingText = fixedText #updates output text
    else:
        if key == floatingChar:
            floatingReps = floatingReps + 1 #if the key is the same as the one last pressed, incremement a counter
        else:
            fixedText = fixedText + floatingInput #otherwise, make the floating character permanent and reset reps and the floating character
            floatingInput = ""
            floatingChar = key
            floatingReps = 0
        try:
            floatingIndex = len(letterMap[key]) #allows cycling through the letters multiple times
            floatingInput = letterMap[key][floatingReps%floatingIndex] #find the floating character by accessing an index position of a list which is stored as the value in a dictionary where the button is the key
            floatingText = fixedText + floatingInput #output text is the fixed text and the new floating character
        except:
            print("Out of range, probably, something else could've gone wrong, but this is an except statement so it clearly isn't that bad so like just firm it and keep going.")

CS = machine.Pin(9, machine.Pin.OUT) #Sets up pins associated with the SD card and creates an instance of the SD object
spi = machine.SPI(1,baudrate=1000000,polarity=0,phase=0,bits=8,firstbit=machine.SPI.MSB,sck=machine.Pin(10),mosi=machine.Pin(11),miso=machine.Pin(12))
sd = sdcard.SDCard(spi,CS)
vfs = uos.VfsFat(sd) #mounts sd card so it can be accessed
uos.mount(vfs, "/sd")

col_list=[16,17,18,19] #sets pins associated with keypad
row_list=[20,21,22,26]

currentPassword = "" #variables associated with the master password 
exOutput = ""
password = 0

newName = "" #global variables used when creating a new password 
newPass = ""

selectedPass = "" #stores the name of the selected account

activescreen = "Lock" #sets the first screen to be viewed
callLock(currentPassword) #calls the screen

passDict = [] #data structure to store password dictionary

favourites = {} #structure to store favourites dictionary

uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5)) #set up uart object

changeName = ""

with open("/sd/data.txt", "r") as file:
    hashOut = file.readline().strip('\r\n') #dumps contents of SD card into a variable
    favDump = json.loads(file.readline().strip('\r\n'))
    dictDump = json.loads(file.readline()) #converts strings into lists that can be decrypted

for x in range(0,4):
    row_list[x]=Pin(row_list[x], Pin.OUT) #sets row pins to output pins
    row_list[x].value(1)

for x in range(0,4):
    col_list[x] = Pin(col_list[x], Pin.IN, Pin.PULL_UP) #sets column pins to input pins

#create a keypad I can later reference as coordinates
key_map=[["1","4","7","*"],\
         ["A","B","C","D"],\
         ["3","6","9","#"],\
         ["2","5","8","0"]]

while True: #the main loop of the program
    key=Keypad4x4Read(col_list, row_list) #reads the key from the keypad
    if key != None: #if a key is pressed, call the input function of the currently active screen
        if activescreen == "Lock":
            lockInput(key)
        elif activescreen == "Hub":
            hubInput(key)
        elif activescreen == "NewName":
            newNameInput(key)
        elif activescreen == "NewPass":
            newPassInput(key)
        elif activescreen == "SearchPass":
            searchPassInput(key)
        elif activescreen == "SelectPass":
            selectPassInput(key)
        elif activescreen == "Favourites":
            favInput(key)
        elif activescreen == "SetFav":
            setFavInput(key)
        elif activescreen == "ChangePass":
            changePassInput(key)
    utime.sleep(0.2) #sleep to stop inputs being called multiple times