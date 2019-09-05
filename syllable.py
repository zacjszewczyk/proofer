#!/usr/local/bin/python3

# Imports
from re import findall # Vowel count

# Method: OldSyllableCount
# Purpose: Accept a word and return the number of syllables
# Parameters: word: Word to be parsed. (String)
# H/t: https://github.com/eaydin/sylco
def OldSyllableCount(word):
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
# Purpose: Accept a word and return the number of syllables efficiently
# Parameters: word: Word to be parsed. (String)
def NewSyllableCount(word):
    # Count the number of vowels (A, E, I, O, U) in the word.
      # Add 1 every time the letter 'y' makes the sound of a vowel (A, E, I, O, U).
      # Subtract 1 for each silent vowel (like the silent 'e' at the end of a word).
    # Subtract 1 for each diphthong or triphthong in the word.
      # Diphthong: when 2 vowels make only 1 sound (au, oy, oo)
      # Triphthong: when 3 vowels make only 1 sound (iou)
    # Does the word end with "le" or "les?" Add 1 only if the letter before the "le" is a consonant.
    # The number you get is the number of syllables in your word.

# Method: FindConflicts
# Purpose: Find syllable conflicts between dictionary and algorithm
# Parameters:
# - syllable_dictionary: Wordlist with syllables (List)
def FindConflicts(syllable_dictionary):
    # for word, syllable in syllable_dictionary:
    #     predicted_syllable = NewSyllableCount(word)
    #     if (syllable != predicted_syllable):
    #         print(word,"-","Actual:",syllable,"/ Predicted",predicted_syllable)

# Method: BuildSyllableDictionary
# Purpose: Enrich wordlist with true syllables from a dictionary
# Parameters: none.
def BuildSyllableDictionary():
    # Use a wordlist or command line dictionary (i.e. https://github.com/Mckinsey666/vocabs) for input
    # Get true syllables for each word
    # Save in the format [word, syllables]
    # Append to syllable_dictionary
    # return syllable_dictionary
