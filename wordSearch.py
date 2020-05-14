import string
import random
import tkinter as tk

# tkinter set-up
root = tk.Tk()
frame = tk.Frame(root)
frame.pack()

root2 = tk.Tk()
words = tk.Frame(root2)
words.pack()

wordList = ['PROGRAMMING','CODE','ENCRYPTION','ALGORITHM','BOOLEAN','STRING','INTEGER','ARRAY','INTERNET','CIPHER','CAESAR','VARIABLES','DEBUGGING','FUNCTION','COMPRESSION','FILES','BINARY','BYTES','DATA','COMPRESSION','ENCODING','PACKETS','ROUTERS','INTERNET','ASYMMETRIC','SYMMETRIC','VIGENERE','DECRYPTING','CRACKING','LOOPS','PYTHON','JAVA','JAVASCRIPT','RUBY','BASIC','ASSEMBLY','LANGUAGE','COMPUTER','SOFTWARE','PROGRAMS','LIST','DATABASE','CLASS','OBJECT','MATRIX','THEORY','IMAGE','PACKETS','WHILELOOPS','ASCII','COMMAND','COMPILER','FLEMMING','EMULATOR','WINDOWS','DOS','SCRIPT','LINUX','MAC','FREEBSD', 'UBUNTU', 'ARCH', 'MINT', 'DEBIAN']



size = 25
numWords = 25

# String to hold current letters which are pressed in series
pressedWord = ''

prev = [0,0]
route = [0,0]

arr = [[0 for x in range(size)]for y in range(size)]
button = [[0 for x in range(size)]for y in range(size)]
check = [0 for numWords in range(size)]
dictionary = [0 for createWordSet in range(numWords)]

#  3 2 1
#   \|/
# 4--+--0
#   /|\
#  5 6 7
#All 8 possible directions (Number above corresponding to array index)
directionArr = [[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1]]


class square:
    status = False      # true = has been pressed
    char = ''           # character at location x, y
    filled = False      # does a character fill this space (f = no, t = yes) 


# Puts word on board location (Called by wordPlace) after valid location is found
def fill(x, y, word, direction):
    for i in range(len(word)):
        arr[x + direction[0]*i][ y + direction[1]*i].char = word[i]
        arr[x + direction[0]*i][ y + direction[1]*i].filled = True

# Picks random word from wordList list, and picks random location and direction. If it fails, it will contiune until a valid location is found        
def wordPlace(j, dictionary):    
    word = random.choice(wordList)
    direction = directionArr[random.randrange(0,7)]

    x = random.randrange(0, size-1)
    y = random.randrange(0, size-1)

    if(x + len(word)*direction[0] > size-1 or x + len(word)*direction[0] < 0
       or  y + len(word)*direction[1] > size-1) or y + len(word)*direction[1] < 0:
        wordPlace(j, dictionary)
        return
    
    for i in range(len(word)):
        if(arr[x + direction[0]*i][y+ direction[1]*i].filled == True):
            if(arr[x + direction[0]*i][y+ direction[1]*i].char != word[i]):
                wordPlace(j, dictionary)
                return
    dictionary[j] = word

    check[j] = tk.Label(words, text = word,height = 1, width = 15, font=('None %d ' %(10)), anchor = 'c')
    check[j].grid()
    
    fill(x, y, word, direction)
    return dictionary
    

# Colours area appropirate colour, depending if word was valid or not
def colourWord(pressedWord, valid):
    route[0] *= -1
    route[1] *= -1
    for i in range(len(pressedWord)):
        if valid == True or arr[prev[0]+i*route[0]][prev[1]+i*route[1]].status == True:
            button[prev[0]+i*route[0]][prev[1]+i*route[1]].config(bg='lime green')
            arr[prev[0]+i*route[0]][prev[1]+i*route[1]].status = True       
        elif(arr[prev[0]+i*route[0]][prev[1]+i*route[1]].status == False):
            button[prev[0]+i*route[0]][prev[1]+i*route[1]].config(bg= '#F0F0F0')

#Checks to see if word is a valid word on lits
def checkWord():
    global pressedWord

    if pressedWord in dictionary:
        check[int(dictionary.index(pressedWord))].configure(font=('None %d overstrike' %(10)))
        check[int(dictionary.index(pressedWord))].grid()
        dictionary[dictionary.index(pressedWord)] = ''  #For cases when same word appears multiple times

        colourWord(pressedWord, True)
    else:
        colourWord(pressedWord, False)
    pressedWord = ''
    prev = [0,0]
    
# Makes sure direction being clicked is consistent, also handles highlighting button clicked yellow  
def buttonPress (x, y):
    global pressedWord, prev, route
    newPressed = [x, y]
    
	#Allows first click to be anywhere on board
    if(len(pressedWord) == 0):
        prev = newPressed
        print(prev)
        pressedWord = arr[x][y].char
        button[x][y].configure(bg='yellow')

	# Second click needs to be one of the 8 surrounding  the initial click (Less for when first press is along wall boarder)
    elif(len(pressedWord) == 1 and (x - prev[0])**2 <= 1 and (y - prev[1])**2 <= 1 and newPressed != prev):
        pressedWord += arr[x][y].char
        button[x][y].configure(bg='yellow')
        
        route = [x-prev[0], y-prev[1]]
        prev = [x, y]

	# Uses direction defined by the second click to only allow presses to contiune in the direction that was initally clicked    
    elif(len(pressedWord) > 1 and x - prev[0] == route[0] and y - prev[1] == route[1]):
        pressedWord += arr[x][y].char
        button[x][y].configure(bg='yellow')
        prev = [x,y]

#Creates physcial (size x size) grid of buttons
for x in range(size):
    for y in range(size):
        arr[x][y] = square()

#Puts all words on word search
for i in range(numWords):
    wordPlace(i, dictionary)
 
#Fills in remaining space with random letters, and creates tkinter windows
for y in range(size):
    for x in range(size):
        
		# Fills empty locations (only locations listed as empty after word placed)
        if(arr[x][y].filled == False):
           #arr[x][y].char = ' ' # Used for debugging (does not fill in random letters, making it easier to find valid words
            arr[x][y].char = random.choice(string.ascii_uppercase)

        button[x][y] = tk.Button(frame, text = arr[x][y].char, bg= '#F0F0F0', width=2, height=1, command=lambda x=x, y=y: buttonPress(x, y))
        button[x][y].grid(row=x, column=y)

checkW = tk.Button(words, text = "check Word", height = 1, width = 15, anchor = 'c', command = checkWord)
checkW.grid()

root.title("Word Search Board")
root2.title("Word List")

root.mainloop()
root2.mainloop()
