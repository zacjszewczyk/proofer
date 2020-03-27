#!/usr/local/bin/python3

# Imports
from re import findall # Vowel count
from scraper import Scraper # Web scraper
from os.path import exists # File operations
from os import remove # Migrating files
from datetime import datetime # Runtime
from multiprocessing import Pool # Multiprocessing
from os import listdir

# Method: sylco
# Purpose: Accept a word and return the number of syllables
# Parameters:
# - word: Word to be parsed. (String)
# Source: https://github.com/eaydin/sylco/blob/master/sylco.py
def sylco(word) :

    word = word.lower()

    # exception_add are words that need extra syllables
    # exception_del are words that need less syllables
    
    exception_add = ['serious','crucial']
    exception_del = ['fortunately','unfortunately']
    
    co_one = ['cool','coach','coat','coal','count','coin','coarse','coup','coif','cook','coign','coiffe','coof','court']
    co_two = ['coapt','coed','coinci']
    
    pre_one = ['preach']
    

    syls = 0 #added syllable number
    disc = 0 #discarded syllable number

    #1) if letters < 3 : return 1
    if len(word) <= 3 :
        syls = 1
        return syls
    
    #2) if doesn't end with "ted" or "tes" or "ses" or "ied" or "ies", discard "es" and "ed" at the end.
    # if it has only 1 vowel or 1 set of consecutive vowels, discard. (like "speed", "fled" etc.)

    if word[-2:] == "es" or word[-2:] == "ed" :
        doubleAndtripple_1 = len(findall(r'[eaoui][eaoui]',word))
        if doubleAndtripple_1 > 1 or len(findall(r'[eaoui][^eaoui]',word)) > 1 :
            if word[-3:] == "ted" or word[-3:] == "tes" or word[-3:] == "ses" or word[-3:] == "ied" or word[-3:] == "ies" :
                pass
            else :
                disc+=1
    
    #3) discard trailing "e", except where ending is "le"  
   
    le_except = ['whole','mobile','pole','male','female','hale','pale','tale','sale','aisle','whale','while']
    
    if word[-1:] == "e" :
        if word[-2:] == "le" and word not in le_except :
            pass
        
        else :
            disc+=1
    
    #4) check if consecutive vowels exists, triplets or pairs, count them as one.

    doubleAndtripple = len(findall(r'[eaoui][eaoui]',word))
    tripple = len(findall(r'[eaoui][eaoui][eaoui]',word))
    disc+=doubleAndtripple + tripple
    
    #5) count remaining vowels in word.
    numVowels = len(findall(r'[eaoui]',word))

    #6) add one if starts with "mc"
    if word[:2] == "mc" :
        syls+=1
        
    #7) add one if ends with "y" but is not surrouned by vowel
    if word[-1:] == "y" and word[-2] not in "aeoui" :
        syls +=1
        
    #8) add one if "y" is surrounded by non-vowels and is not in the last word.
    
    for i,j in enumerate(word) :
        if j == "y" :
            if (i != 0) and (i != len(word)-1) :
                if word[i-1] not in "aeoui" and word[i+1] not in "aeoui" :
                    syls+=1
    
    
    #9) if starts with "tri-" or "bi-" and is followed by a vowel, add one.
    
    if word[:3] == "tri" and word[3] in "aeoui" :
        syls+=1
    
    if word[:2] == "bi" and word[2] in "aeoui" :
        syls+=1
    
    #10) if ends with "-ian", should be counted as two syllables, except for "-tian" and "-cian"
    
    if word[-3:] == "ian" : 
    #and (word[-4:] != "cian" or word[-4:] != "tian") :
        if word[-4:] == "cian" or word[-4:] == "tian" :
            pass
        else :
            syls+=1
    
    #11) if starts with "co-" and is followed by a vowel, check if exists in the double syllable dictionary, if not, check if in single dictionary and act accordingly.
    
    if word[:2] == "co" and word[2] in 'eaoui' :
    
        if word[:4] in co_two or word[:5] in co_two or word[:6] in co_two :
            syls+=1
        elif word[:4] in co_one or word[:5] in co_one or word[:6] in co_one :
            pass
        else :
            syls+=1

    #12) if starts with "pre-" and is followed by a vowel, check if exists in the double syllable dictionary, if not, check if in single dictionary and act accordingly.

    if word[:3] == "pre" and word[3] in 'eaoui' :
        if word[:6] in pre_one :
            pass
        else :
            syls+=1

    #13) check for "-n't" and cross match with dictionary to add syllable.
    
    negative = ["doesn't", "isn't", "shouldn't", "couldn't","wouldn't"]
    
    if word[-3:] == "n't" :
        if word in negative :
            syls+=1
        else :
            pass   

    #14) Handling the exceptional words.
   
    if word in exception_del :
        disc+=1
        
    if word in exception_add :
        syls+=1     
    
        
    # calculate the output
    return numVowels - disc + syls

# Method: MySyllableCount
# Purpose: Accept a word and return the number of syllables. Modded for speed.
# Parameters: 
# - word: Word to be parsed. (String)
# H/t: https://github.com/eaydin/sylco
def MySyllableCount(word):
    word = word.lower()

    syls = 0 # Number of added syllables
    disc = 0 # Number of discarded syllables

    #1) If three or less letters, one syllable
    if len(word) <= 3 :
        return 1

    #2) If doesn't end with "ted" or "tes" or "ses" or "ied" or "ies", discard "es" and "ed" at the end.
    # if it has only 1 vowel or 1 set of consecutive vowels, discard. (like "speed", "fled" etc.)
    double_vowel = len(findall(r'[eaoui][eaoui]',word))

    if word[-2:] in ["es", "ed"]:
        if double_vowel > 1 or len(findall(r'[eaoui][^eaoui]',word)) > 1 :
            if word[-3:] in ["ted", "tes", "ses", "ied", "ies"]:
                pass
            else:
                disc+=1

    #3) discard trailing "e", except where ending is "le"  
    if word[-1:] == "e" :
        if word[-2:] == "le" and word not in ['whole','mobile','pole','male','female','hale','pale','tale','sale','aisle','whale','while']:
            pass
        else :
            disc+=1

    #4) check if consecutive vowels exists, triplets or pairs, count them as one.
    disc += double_vowel + len(findall(r'[eaoui][eaoui][eaoui]',word))

    #5) count remaining vowels in word.
    numVowels = len(findall(r'[eaoui]',word))

    #6) add one if starts with "mc"
    if word[:2] == "mc" :
        syls+=1

    #7) add one if ends with "y" but is not surrouned by vowel
    if word[-1:] == "y" and word[-2] not in "aeoui" :
        syls +=1

    #8) add one if "y" is surrounded by non-vowels and is not in the last word.
    for i,j in enumerate(word) :
        if j == "y" :
            if (i != 0) and (i != len(word)-1) :
                if word[i-1] not in "aeoui" and word[i+1] not in "aeoui" :
                    syls+=1

    #9) if starts with "tri-" or "bi-" and is followed by a vowel, add one.
    if word[:3] == "tri" and word[3] in "aeoui" :
        syls+=1

    if word[:2] == "bi" and word[2] in "aeoui" :
        syls+=1

    #10) if ends with "-ian", should be counted as two syllables, except for "-tian" and "-cian"
    if word[-3:] == "ian" : 
        if word[-4:] in ["cian", "tian"]:
            pass
        else :
            syls+=1

    #11) if starts with "co-" and is followed by a vowel, check if exists in the double syllable dictionary, if not, check if in single dictionary and act accordingly.
    if word[:2] == "co" and word[2] in 'eaoui' :
        if (set(['coapt','coed','coinci']).intersection([word[:4], word[:5], word[:6]])):
            syls+=1
        elif (set(['cool','coach','coat','coal','count','coin','coarse','coup','coif','cook','coign','coiffe','coof','court']).intersection([word[:4], word[:5], word[:6]])):
            pass
        else :
            syls+=1

    #12) if starts with "pre-" and is followed by a vowel, check if exists in the double syllable dictionary, if not, check if in single dictionary and act accordingly.
    if word[:3] == "pre" and word[3] in 'eaoui' :
        if word[:6] in ['preach']:
            pass
        else :
            syls+=1

    #13) check for "-n't" and cross match with dictionary to add syllable.
    if word[-3:] == "n't" :
        if word in ["doesn't", "isn't", "shouldn't", "couldn't","wouldn't"]:
            syls+=1
        else:
            pass

    #14) Handling the exceptional words.
    # exception_del are words that need less syllables
    if word in ['fortunately','unfortunately']:
        disc+=1
    # exception_add are words that need extra syllables
    if word in ['serious','crucial']:
        syls+=1     

    # calculate the output
    return numVowels - disc + syls

# Method: NewSyllableCount
# Purpose: Accept a word and return the number of syllables *efficiently*
# Parameters:
# - word: Word to be parsed. (String)
def NewSyllableCount(word):
    add = 0
    dele = 0

    # Count the number of vowels (A, E, I, O, U) in the word.
    add = len(findall("[aeoiu]", word))
    # Add 1 every time the letter 'y' makes the sound of a vowel (A, E, I, O, U).
    if (add == 0 and 'y' in word):
        add += 1
    elif(word[-1] == 'y'):
        add += 1
    for i,c in enumerate(word):
        if (c == 'y'):
            if (i != 0 and i != (len(word)-1)):
                if (word[i-1] not in "aeiou" and word[i+1] not in "aeiou"):
                    add += 1
    # Subtract 1 for each silent vowel (like the silent 'e' at the end of a word).
    if (word[-1] in 'e'):
        dele += 1
    # Subtract 1 for each diphthong or triphthong in the word.
    # - Diphthong: when 2 vowels make only 1 sound (au, oy, oo)
    for match in findall("[aeiouy][aeiouy]",word):
        if (match not in ["ia", "ua"]):
            dele += 1
    # - Triphthong: when 3 vowels make only 1 sound (iou)
    dele += len(findall("[aeiouy][aeiouy][aeiouy]",word))
    # Does the word end with "le" or "les?" Add 1 only if the letter before the "le" is a consonant.
    if (word[-2:] == "le" and word[-3] not in "aeiouy"):
        add += 1
    elif (word[-3:] == "les" and word[-4] not in "aeiouy"):
        add += 1
    if ("n't" in word):
        add += 1
    return add - dele

# Method: FindConflicts
# Purpose: Find syllable conflicts between dictionary and target algorithm
# Parameters:
# - syllable_dictionary: Wordlist with syllables (List)
def FindConflicts(tgt):
    t1 = datetime.now()
    
    fd = open("./syllable_dictionary.txt", "r")
    for i, line in enumerate(fd):
        word, dsyl = line.split(",")
        dsyl = dsyl.strip()
        
        # Ignore words for which no dictionary syllable count exists
        if (dsyl == "-1"):
            continue

        if (tgt == "sylco"):
            predicted_syllable = sylco(word)
        elif (tgt == "MySyllableCount"):
            predicted_syllable = MySyllableCount(word)
        elif (tgt == "NewSyllableCount"):
            predicted_syllable = NewSyllableCount(word)
        else:
            print("Error: Invalid algorithm.")
            break

        if (int(dsyl) != int(predicted_syllable)):
            print("Word: %s. Syllables: %s. Predicted (%s): %s" % (word, dsyl, tgt, predicted_syllable))
    fd.close()

    t2 = datetime.now()
    print("Runtime: "+str(t2-t1))