#!/usr/local/bin/python3

from re import findall

# Method: syllables
# Purpose: Accept a word and return the number of syllables *efficiently*
# Parameters:
# - word: Word to be parsed. (String)
def syllables(word):
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

def test_method(wordlist, method):
    fd = open(f"./Syllables/Individual Syllable Lists/syllable_{wordlist}.txt", "r")

    disagree,agree,total = 0,0,0

    for i,line in enumerate(fd):
        line = line.strip()
        word,sylls = line.split(",")

        total += 1

        # Ignore words for which dictionary had no syllable count, for now
        if (sylls == "-1"):
            continue

        if (method == "old"):
            calced_sylls = str(syllables(word))
        elif (method == "new"):
            calced_sylls = str(new_syllables(word))
        elif (method == "other"):
            calced_sylls = str(nsyl(word))

        if (calced_sylls != sylls):
            disagree += 1
            print(f"{word} - Expected: {sylls}; returned: {calced_sylls}")
        else:
            agree += 1

    fd.close()

    skipped = total-(agree+disagree)

    return f"{total} words processed. {skipped} ({(skipped/total*100):.2f}%) skipped. Of the remainder, {agree} matched ({(agree/(total-skipped)*100):.2f}%), and {disagree} did not ({(disagree/(total-skipped)*100):.2f}%)"

def new_syllables(word):
    add,sub = 0,0

    word = word.lower()

    consonants = ['a','e','i','o','u']

    add = sum([word.count(x) for x in consonants])

    if (word[-1] == 'e'):
        sub += 1

    sub = sum([word.count(x) for x in ['au', 'oy', 'oo', 'iou']])

    if (word.endswith("le") and word[-3] not in consonants):
        add += 1
    elif (word.endswith("les") and word[-4] not in consonants):
        add += 1

    return add-sub

from nltk.corpus import cmudict
d = cmudict.dict()

def nsyl(word):
    try:
        return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]][0]
    except KeyError:
        #if word not found in cmudict
        return -1

if (__name__ == "__main__"):
    wordlist = "a"
    results = [f"Old: {test_method(wordlist,'old')}"]
    results.append(f"New: {test_method(wordlist,'new')}")
    results.append(f"Other: {test_method(wordlist,'other')}")

    print(results[0])
    print(results[1])
    print(results[2])