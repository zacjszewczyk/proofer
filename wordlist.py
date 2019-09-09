#!/usr/local/bin/python3

# Imports
from scraper import Scraper # Web scraper
from os.path import exists # File operations
from os import remove # Migrating files
from multiprocessing import Pool # Multiprocessing
from os import listdir # Finding files

# Method: BuildSyllableDictionary
# Purpose: Enrich wordlist with true syllables from a dictionary
# Parameters: none.
def BuildSyllableDictionary():
    # Create a new instance of the web scraper
    s = Scraper()

    # Open the wordlist
    s_fd = open("/usr/share/dict/words", "r")

    # Create the syllable dictionary file if it does not exist.
    if (not exists("./syllable_dictionary.txt")):
        open("./syllable_dictionary.txt", "w").close()
    
    # Open the syllable dictionary
    c_fd = open("./syllable_dictionary.txt", "r")

    # Clear and open a temporary output syllable dictionary, to write to.
    open("./syllable_dictionary.txt.bak", "w").close()
    d_fd = open("./syllable_dictionary.txt.bak", "a")
    
    # Enumerate the wordlist
    for i, word in enumerate(s_fd):
        # Convert wordlist word to lowercase and strip newline
        word = word.lower().strip()

        # Read a line from the syllable dictionary
        comp = c_fd.readline().split(",")[0].strip()

        # If the word in the wordlist has already been added to the syllable
        # dictionary, skip it.
        if (word == comp):
            continue

        # Query Google for the definition of the wordlist's word. Depending on
        # the user agent string, the number of syllables may be in a span or
        # div. If neither element is in the response, try another source.
        resp = s.scrape("https://google.com/search?q=define%20"+word)
        if ('<span data-dobid="hdw">' in resp):
            resp = resp.split('<span data-dobid="hdw">',1)[1].split("</span>",1)[0]
            print(word,",",resp.count("·")+1)
            d_fd.write(word+","+str(resp.count("·")+1)+'\n')
            continue
        elif ('<div data-hveid="20">' in resp):
            resp = resp.split('<div data-hveid="20">',1)[1].split(">",1)[1].split("<",1)[0]
            print(word,",",resp.count("·")+1)
            d_fd.write(word+","+str(resp.count("·")+1)+'\n')
            continue
        else:
            resp = ""

        # If Google does not have a syllable breakdown for the target word,
        # try HowManySyllables.com.
        if (resp == ""):
            resp = s.scrape("https://www.howmanysyllables.com/words/"+word)
        
        # If the response contains a certain paragraph, parse the number of
        # syllables. If not all has failed, so return -1 for the syllable count
        if ('<p id="SyllableContentContainer">' in resp and '<span class="Answer_Red">' in resp.split('<p id="SyllableContentContainer">',1)[1]):
            resp = resp.split('<p id="SyllableContentContainer">',1)[1].split('<span class="Answer_Red">',1)[1].split('</span>',1)[0]
            print(word,",",resp.count("-")+1)
            d_fd.write(word+","+str(resp.count("-")+1)+'\n')
        else:
            print(word,",",-1)
            d_fd.write(word+","+str(-1)+'\n')

    # Close all files
    s_fd.close()
    d_fd.close()
    c_fd.close()

    # Append the temporary syllable dictionary to the actual
    # syllable dictionary, then remove the temp file.
    s_fd = open("./syllable_dictionary.txt.bak", "r")
    d_fd = open("./syllable_dictionary.txt", "a")
    for i,line in enumerate(s_fd):
        d_fd.write(line)

    # Close files
    s_fd.close()
    d_fd.close()

    # Cleanup
    remove("./syllable_dictionary.txt.bak")
    del s


###############################################################################
########################## The old ^ meets the new ˅ ##########################
###############################################################################


# Method: SplitUpWordlist
# Purpose: Break wordlist into sub-wordlists by letter of alphabet
# Parameters: none.
def SplitUpWordlist():
    # Open the wordlist
    wordlist_fd = open("/usr/share/dict/words", "r")
    
    # Keep track of which letters have their own output file
    alphabet = []

    # Enumerate the wordlist. For each letter, create a new wordlist file in
    # the form {letter}.txt, that contains all letters starting with {letter}.
    for i,line in enumerate(wordlist_fd):
        # Transform the wordlist's word
        line = line.strip().lower()
        
        # If the script has not processed {letter} yet, create {letter}.txt
        # and write all words starting with {letter} to it.
        if (line[0] not in alphabet):
            try:
                d_fd.close()
            except:
                pass
            open("./"+line[0]+".txt", "w").close()
            d_fd = open("./"+line[0]+".txt", "a")
            d_fd.write(line+'\n')
        else:
            d_fd.write(line+'\n')

    # Close the file
    wordlist_fd.close()

# Method: BuildSyllableDictionaryWithMultiprocessing
# Purpose: Enrich wordlist with syllables from dictionary, with multiprocessing
# Parameters: none.
def BuildSyllableDictionaryWithMultiprocessing():
    # Find all source files of the form {letter}.txt
    files = [x for x in listdir("./") if len(x) == 5]
    
    # Use multithreading to speed up capturing syllables for entire dictionary
    with Pool() as pool:
        pool.map(BuildDictionary, files)

# Method: BuildDictionary
# Purpose: Capture syllables for all words in a wordlist
# Parameters:
# - tgt: Source wordlist (String)
def BuildDictionary(tgt):
    # Clear an interim output file, then open for appending
    open("./interim_" + tgt, "w").close()
    d_fd = open("./interim_" + tgt, "a")

    # Open the source wordlist
    s_fd = open("./" + tgt, "r")

    # Open the existing syllable dictionary
    c_fd = open("./syllable_" + tgt, "r")

    # Enumerate the wordlist. 
    for i,word in enumerate(s_fd):
        # Convert wordlist word to lowercase and strip newline
        word = word.lower().strip()

        # Read a line from the syllable dictionary
        comp = c_fd.readline().split(",")[0].lower().strip()
        
        # If the word in the wordlist has already been added to the syllable
        # dictionary, skip it.
        if (comp == word):
            continue

        # If the word has not been added to the syllable dictionary, capture
        # the syllable count and append the word and that number to the dict.
        d_fd.write(line + "," + str(DownloadSyllable(line)) + '\n')        


    # Close all files
    d_fd.close()
    s_fd.close()
    c_fd.close()

    # Append the temporary syllable dictionary to the actual
    # syllable dictionary, then remove the temp file.
    s_fd = open("./interim_" + tgt, "r")
    d_fd = open("./" + tgt, "a")
    for i,line in enumerate(s_fd):
        d_fd.write(line)

    # Close files
    d_fd.close()
    s_fd.close()

    # Delete temp file
    remove("./interim_"+tgt)

# Method: DownloadSyllable
# Purpose: Capture syllables for single word
# Parameters:
# - word: Target word (String)
def DownloadSyllable(word):
    # Create a new instance of the Scraper class. This is necessary since these
    # queries will be split up among multiple processors with dissimilar memory
    s = Scraper()
    
    # Query Google for the definition of the wordlist's word. Depending on
    # the user agent string, the number of syllables may be in a span or
    # div. If neither element is in the response, try another source.
    resp = scrape("https://google.com/search?q=define%20"+word)
    if ('<span data-dobid="hdw">' in resp):
        resp = resp.split('<span data-dobid="hdw">',1)[1].split("</span>",1)[0]
        print(word,",",resp.count("·")+1)
        return resp.count("·")+1
    elif ('<div data-hveid="20">' in resp):
        resp = resp.split('<div data-hveid="20">',1)[1].split(">",1)[1].split("<",1)[0]
        print(word,",",resp.count("·")+1)
        return resp.count("·")+1
    else:
        resp = ""

    # If Google does not have a syllable breakdown for the target word,
    # try HowManySyllables.com.
    if (resp == ""):
        resp = scrape("https://www.howmanysyllables.com/words/"+word)
    
    # If the response contains a certain paragraph, parse the number of
    # syllables. If not all has failed, so return -1 for the syllable count
    if ('<p id="SyllableContentContainer">' in resp and '<span class="Answer_Red">' in resp.split('<p id="SyllableContentContainer">',1)[1]):
        resp = resp.split('<p id="SyllableContentContainer">',1)[1].split('<span class="Answer_Red">',1)[1].split('</span>',1)[0]
        print(word,",",resp.count("-")+1)
        return resp.count("-")+1
    else:
        print(word,",",-1)
        return -1
    
    # Cleanup
    del s

# Method: RecoverFromError
# Purpose: Append contents of partial temp files to syllable dictionaries.
# Parameters: none.
def RecoverFromError():
    # Find all temp source files
    files = [x for x in listdir("./") if ".txt" in x and "interim" in x]
    
    # Append cotnents of partial temp files to syllable dictionary
    for tgt in files:
        # Open the files
        s_fd = open("./"+tgt, "r")
        d_fd = open("./"+tgt.replace("interim", "syllable"), "a+")

        # Do the copying
        for i,line in enumerate(s_fd):
            d_fd.write(line)

        # Close the files
        d_fd.close()
        s_fd.close()

# Method: FinalCheck
# Purpose: Compare wordlists to syllable dictionaries
# Parameters: none.
def FinalCheck():
    # Find all source wordlists of the form {letter}.txt
    files = sorted([x for x in listdir("./") if ".txt" in x and len(x) == 5])
    
    # Compare each wordlist to its syllable dictionary, to make sure syllable
    # dictionary has all words from the source wordlist.
    for tgt in files:
        # Open the source wordlist and attempt to open syllable dictionary.
        # If the dictionary does not yet exist, notify the user.
        source_fd = open("./"+tgt, "r")
        if (not exists("./syllable_"+tgt)):
            print("File '%s' does not exist." % ("./syllable_"+tgt))
            continue

        # Open the syllable dictionary
        sylls_fd = open("./syllable_"+tgt, "r")
        
        # Instantiate boolean to track similarity
        notTheSame = False
        
        # Enumerate the wordlist.
        for i,source_line in enumerate(source_fd):
            # Read a line from the source wordlist and the syllable dictionary
            source_line = source_line.strip().lower()
            sylls_line = sylls_fd.readline().split(",")[0].strip().lower()
            
            # If the lines do not match, notify the user and set the boolean.
            if (source_line != sylls_line):
                print("Source line %d, '%s', and syllable dictionary line, '%s', do not match." % (i, source_line, sylls_line))
                notTheSame = True
        
        # Close all files
        source_fd.close()
        sylls_fd.close()
        
        # Tell the user whether the syllable dictionary has all the words from
        # the wordlist or if they diverge.
        if (notTheSame):
            print(tgt,"and","./syllable_"+tgt+" are not the same.")
        else:
            print(tgt,"and","./syllable_"+tgt+" ARE the same.")

# Method: CombineWordlists
# Purpose: Combine disparate sub-wordlists into a single wordlist.
# Parameters:
# - name: Filename for the monolithic wordlist (String)
def CombineWordlists(name):
    # Find all sub-wordlists like syllable_{letter}.txt. Sort alphabetically.
    files = sorted([x for x in listdir("./") if "syllable_" in x and ".txt" in x])
    
    # Clear the master wordlist, then open for appending sub-wordlists
    open("./"+name, "w").close()
    master_fd = open("./"+name, "a")
    
    # Open each wordlist and write its contents to the master wordlist.
    for sub_wordlist in files:
        sub_fd = open("./"+sub_wordlist, "r")
        for i,line in enumerate(sub_fd):
            master_fd.write(line)
        # Close file
        sub_fd.close()
    # Close file
    master_fd.close()

# Method: CompareWordlists
# Purpose: Compare master wordlist with syllable dictionary.
# Parameters:
# - master: File path for the master wordlist (String)
# - syl: File path for the syllable dictionary (String)
def CompareWordlists(master, syl):
    # Open the wordlists
    master_fd = open(master, "r")
    syl_fd = open(syl, "r")

    # Enumerate the master wordlist
    for i,master_line in enumerate(master_fd):
        # Read a line from the syllable dictionary
        syl_line = syl_fd.readline()

        # Transform the lines for comparison
        master_line = master_line.lower().strip()
        syl_line = syl_line.split(",")[0].strip()

        # Compare the two lines
        if (master_line != syl_line):
            # Print the line number and the different words
            print("Line %d: master '%s' vs syllable dictionary '%s'" % (i, master_line, syl_line))
            # Exit so we can fix this line, then re-run
            break

    # Close files
    master_fd.close()
    syl_fd.close()

if (__name__ == "__main__"):
    # Build the syllable dictionary.
    # BuildSyllableDictionary()

    ###########################################################################
    ######################## The old ^ meets the new ˅ ########################
    ###########################################################################

    # That was super slow! So let's split up the wordlist so we can give
    # sub-wordlists to each processor.
    # SplitUpWordlist()
    # BuildSyllableDictionaryWithMultiprocessing()

    # Oh no! We ran into some errors. Recover the contents of partial
    # temp files.
    # RecoverFromError()

    # Now that it looks like we have full syllable dictionaries, confirm this.
    # For each word in each sub-wordlist, make sure the syllable dictionaries
    # have an entry for each word.
    # FinalCheck()

    # Now that we know the syllable wordlists are good to go, combine them into
    # a single file. Since the source was "web2", we'll call ours "webS".
    # CombineWordlists("webS")

    # Oh no! The original wordlist has 235,886 entries, but the syllable
    # dictionary only has 235,883. Let's find those 3 differences.
    # CompareWordlists("/usr/share/dict/words", "./webS")

    # It turns out, most wordlist groups started with a capital letter and then
    # the lowercase version, i.e. line 1: A; line 2: a. Since I transformed 
    # these lines to ignore capitalization and then had to recover temp files
    # a few times, the sub-wordlists were missing a "b", "c", and "w" that the
    # Recover function did not write to the syllable dictionary, because it saw
    # them already there. A quick fix and voila, a syllable-enriched wordlist.

    fd = open("./webS", "r")

    for i,line in enumerate(fd):
        word,sylls = [x.strip() for x in line.split(",")]
        print(word)
        print(sylls)

    fd.close()