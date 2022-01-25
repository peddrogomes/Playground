# Hangman game
#

# -----------------------------------

import random
import string

WORDLIST_FILENAME = "words.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    arq=open(WORDLIST_FILENAME,'r')
    
    print('Loading word list from file...')
    wordlist=[]    
    for word in arq:
        wordlist.append(word)
        
    wordlist=wordlist[0].split()
    
    print('\t{} words loaded.'.format(len(wordlist)))
    arq.close()
    return wordlist

def chooseWord(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    
    return random.choice(wordlist)

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = loadWords()

def isWordGuessed(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: boolean, True if all the letters of secretWord are in lettersGuessed;
      False otherwise
    '''
    if(set(secretWord)==set(lettersGuessed)):
        bol=True
    else:
        bol=False
    return bol



def getGuessedWord(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters and underscores that represents
      what letters in secretWord have been guessed so far.
    '''
    wordprint=''
    aux=False
    for i in secretWord:
        for j in lettersGuessed:
            if(i==j):
                wordprint+=i
                aux=True
        if(aux==True):
            aux=False
        else:
            wordprint+='_ '
        
    
    return wordprint



def getAvailableLetters(lettersGuessed):
    '''
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters that represents what letters have not
      yet been guessed.
    '''
    LisAvaiLet= list(string.ascii_lowercase)
	
    
    letterslist=''
    aux=False
    for i in LisAvaiLet:
        for j in lettersGuessed:
            if i==j:
                aux=True
        if aux==True:
            aux=False
        else:
            letterslist+=i
            
    return letterslist

def letterispartofword(letter, secretWord):
    
    bol=False
    
    for i in secretWord:
        if i==letter[0]:
            bol=True
    
    return bol


def hangman(secretWord):
    '''
    secretWord: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many 
      letters the secretWord contains.

    * Ask the user to supply one guess (i.e. letter) per round.

    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computers word.

    * After each round, you should also display to the user the 
      partially guessed word so far, as well as letters that the 
      user has not yet guessed.

    '''
    print('Welcome to the game, Hangman!')
    
    print('I am thinking of a word that is {} letters long.'.format(len(secretWord)))
    
    lettersGuessed=''
    attempts=0
    while(not(isWordGuessed(secretWord, lettersGuessed))):
            
        print('--------------------------------')
        print('You have {} guesses left'.format(8-attempts))
        print('Available letters: {}'.format(getAvailableLetters(lettersGuessed)))
        
        letter=input('Please guess a letter:')
        
        
        if letterispartofword(letter, lettersGuessed):
           print('This letter has gone guessed.') 
           print('Keep trying {}.'.format(getGuessedWord(secretWord, lettersGuessed)))
        else:
            
            lettersGuessed+=letter
            
            if(letterispartofword(letter, secretWord)):
                
                print('Good guess: {}'.format(getGuessedWord(secretWord, lettersGuessed)))
                
            else:
                
                print('Oops! That letter is not in my word: {}'.format(getGuessedWord(secretWord, lettersGuessed)))
                attempts=attempts+1
            
        if(attempts==8):
            
            print('--------------------------------')
            print('You lose!')
            print('The word is {}.'.format(secretWord))
            break
        
    if(isWordGuessed(secretWord, lettersGuessed)):
        print('--------------------------------')
        print('Congratulations, you won!')
    return


# When you've completed your hangman function, uncomment these two lines
# and run this file to test! (hint: you might want to pick your own
# secretWord while you're testing)

secretWord = chooseWord(wordlist).lower()
hangman(secretWord)
