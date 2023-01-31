import random

def encrypt(plaintext,cipher):
    if len(plaintext) > 16:
        plaintext = plaintext + " "*(16-len(plaintext)%16) #add spaces to the end of the string until it is a length that is divisible by 16
    if len(plaintext) < 16:
        plaintext = plaintext + " "*(16-len(plaintext))
    charlist = []
    for char in plaintext:
        charlist.append(char) #creates a list of characters in the string
    pointer = 0 #sets up the variables required for the device
    grid = []
    tmpgrid = []
    tmprow = []
    while pointer < len(charlist):
        for i in range(0,4):
            for j in range(0,4): #creates a 3d array of a series of 4x4 grids
                tmp = ord(charlist[pointer]) #converts the character into binary number
                tmprow.append(tmp^cipher)  #appends a character which has been xord with the password
                pointer = pointer + 1 #increments the pointer
            tmpgrid.append(tmprow)
            tmprow = [] #appends and resets the row
        grid.append(tmpgrid)
        tmpgrid = [] #appends and resets the grid
    return grid

def decrypt(decgrid,cipher):
    outstring = "" #create an empty string
    for decsubgrid in decgrid: #loops through grids, then rows, then characters
        for decline in decsubgrid:
            for decitem in decline:
                outstring = outstring + chr(decitem ^ cipher) #xors the character again with the cipher to turn it back into the original character
    return outstring.strip() #strip any spaces and returns the string

def genPass():
    # List of characters to choose from for the password
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%&()_+-=;:?/\\"
    password_length = 10
    password = ""
    while len(password) < password_length:
      password += random.choice(characters) #picks a random character from the string and adds it to the password
    return password

def returnSearched(query,accList): #takes 2 parameters, the list of account names and the search query
    results = []
    if len(query) > 0: #checks that the query isn't empty
        for item in accList.keys():
            if item.startswith(query) == True: #if any accounts start with the query, append them to possible results
                results.append(item)
        if len(results) == 0:
            for item in accList.keys():
                if len(query) > 1:
                    if item.startswith(query[:-1]) == True: #if no results were found, check if any items start with the last character of the query removed, as they might still be cycling through characters
                        results.append(item)
        if len(results) == 0 and len(query) > 2: #if at least 3 characters have been typed, and still no results have been found, check if the query appears anywhere in the account names
            for item in accList.keys():
                if query in item:
                    results.append(item)
    sortedRes = sorted(results, key=len) #sort the possible results by length
    if len(sortedRes) < 3:
        for i in range(0,3-len(sortedRes)): #if less than 3 results were found, pad the list with empty strings
            sortedRes.append("")
    print(sortedRes) 
    return sortedRes #return the list
