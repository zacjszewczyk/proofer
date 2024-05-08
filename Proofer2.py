#!/usr/bin/python3

# Imports
import sys # CLI arguments
import argparse # CLI argument parsing
from os.path import isfile # Basic bounds checks
from datetime import datetime # Runtime
from re import sub # Text processing
from html import unescape
sys.path.insert(0, '/Users/zjszewczyk/Dropbox/Code/firstcrack-private')
from Markdown import Markdown
from re import findall
from re import split as resplit

# Use the argparse library to specific input and ouput files via the CLI.
parser = argparse.ArgumentParser(description='Identify elements of weak writing.')
parser.add_argument('input_file', metavar='-i', type=str, nargs='?' ,help='Input file.')
parser.add_argument('output_file', metavar='-o', type=str, nargs='?' ,help='Output file.')

# Class: c(olors)
# Purpose: provide access to ANSI escape codes for styling output
class c():
    HEADER = '\033[95m' # Pink
    OKBLUE = '\033[94m' # Purple
    OKGREEN = '\033[92m' # Green
    WARNING = '\033[93m' # Yellow
    FAIL = '\033[91m' # Red
    ENDC = '\033[0m' # None
    BOLD = '\033[1m' # Blue
    UNDERLINE = '\033[4m' # Underline

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

# Store the Plain English Campaign's list of alternative words to common complex
# ones (http://www.plainenglish.co.uk/the-a-z-of-alternative-words.html), plus 
# my additions.
pec = {"an absence of":"no, none","absence of":"no, none","abundance":"enough, plenty, a lot (or say how many)","accede to":"allow, agree to","accelerate":"speed up","accentuate":"stress","accommodation":"where you live, home","accompanying":"with","accomplish":"do, finish","according to our records":"our records show","accordingly":"in line with this, so","acknowledge":"thank you for","acquaint yourself with":"find out about, read","acquiesce":"agree","acquire":"buy, get","additional":"extra, more","adjacent":"next to","adjustment":"change, alteration","admissible":"allowed, acceptable","advantageous":"useful, helpful","advise":"tell, say (unless you are giving advice)","affix":"add, write, fasten, stick on, fix to","afford an opportunity":"let, allow","afforded":"given","aforesaid":"this, earlier in this document","aggregate":"total","aligned":"lined up, in line","alleviate":"ease, reduce","allocate":"divide, share, give","along the lines of":"like, as in","alternative":"(a) choice, (the) other","alternatively":"or, on the other hand","ameliorate":"improve, help","amendment":"change","anticipate":"expect","apparent":"clear, plain, obvious, seeming","applicant (the)":"you","application":"use","appreciable":"large, great","apprise":"inform, tell","appropriate":"proper, right, suitable","appropriate to":"suitable for","approximately":"about, roughly","as a consequence of":"because","as of the date of":"from","as regards":"about, on the subject of","ascertain":"find out","assemble":"build, gather, put together","assistance":"help","at an early date":"soon (or say when)","at its discretion":"can, may (or edit out)","at the moment":"now (or edit out)","at the present time":"now (or edit out)","attempt":"try","attend":"come to, go to, be at","attributable to":"due to, because of","authorize":"allow, let","authority":"right, power, may (as in 'have the authority to')","axiomatic":"obvious, goes without saying","belated":"late","beneficial":"helpful, useful","bestow":"give, award","breach":"break","by means of":"by","calculate":"work out, decide","cease":"finish, stop, end","circumvent":"get round, avoid, skirt, circle","clarification":"explanation, help","combine":"mix","combined":"together","commence":"start, begin","communicate":"talk, write, telephone (be specific)","competent":"able, can","compile":"make, collect","complete":"fill in, finish","completion":"end","comply with":"keep to, meet","component":"part","comprises":"is made up of, includes","(it is) compulsory":"(you) must","conceal":"hide","concerning":"about, on","conclusion":"end","concur":"agree","condition":"rule","consequently":"so","considerable":"great, important","constitutes":"makes up, forms, is","construe":"interpret","consult":"talk to, meet, ask","consumption":"amount used","contemplate":"think about","contrary to":"against, despite","correct":"put right","correspond":"write","costs the sum of":"costs","counter":"against","courteous":"polite","cumulative":"added up, added together","currently":"now (or edit out)","customary":"usual, normal","deduct":"take off, take away","deem to be":"treat as","defer":"put off, delay","deficiency":"lack of","delete":"cross out","demonstrate":"show, prove","denote":"show","depict":"show","designate":"point out, show, name","desire":"wish, want","dispatch":"send, post","despite the fact that":"though, although","determine":"decide, work out, set, end","detrimental":"harmful, damaging","difficulties":"problems","diminish":"lessen, reduce","disburse":"pay, pay out","discharge":"carry out","disclose":"tell, show","disconnect":"cut off, unplug","discontinue":"stop, end","discrete":"separate","discuss":"talk about","disseminate":"spread","documentation":"papers, documents","domiciled in":"living in","dominant":"main","due to the fact that":"because, as","duration":"time, life","during which time":"while","dwelling":"home","economical":"cheap, good value","eligible":"allowed, qualified","elucidate":"explain, make clear","emphasize":"stress","empower":"allow, let","enable":"allow","enclosed":"inside, with","(please find) enclosed":"I enclose","encounter":"meet","endeavor":"try","inquire":"ask","inquiry":"question","ensure":"make sure","entitlement":"right","envisage":"expect, imagine","equivalent":"equal, the same","erroneous":"wrong","establish":"show, find out, set up","evaluate":"test, check","evince":"show, prove","ex officio":"because of his or her position","exceptionally":"only when, in this case","excessive":"too many, too much","exclude":"leave out","excluding":"apart from, except","exclusively":"only","exempt from":"free from","expedite":"hurry, speed up","expeditiously":"as soon as possible, quickly","expenditure":"spending","expire":"run out","extant":"current, in force","extremity":"limit","fabricate":"make, make up","facilitate":"help, make possible","factor":"reason","failure to":"if you do not","finalize":"end, finish","following":"after","for the duration of":"during, while","for the purpose of":"to, for","for the reason that":"because","formulate":"plan, devise","forthwith":"now, at once","forward":"send","frequently":"often","furnish":"give","further to":"after, following","furthermore":"then, also, and","generate":"produce, give, make","give consideration to":"consider, think about","grant":"give","henceforth":"from now on, from today","hereby":"now, by this (or edit out)","herein":"here (or edit out)","hereinafter":"after this (or edit out)","hereof":"of this","hereto":"to this","heretofore":"until now, previously","hereunder":"below","herewith":"with this (or edit out)","hitherto":"until now","hold in abeyance":"wait, postpone","hope and trust":"hope, trust (but not both)","if and when":"if, when (but not both)","illustrate":"show, explain","immediately":"at once, now","implement":"carry out, do","imply":"suggest, hint at","in a number of cases":"some (or say how many)","in accordance with":"as under, in line with, because of","in addition (to)":"and, as well as, also","in advance":"before","in case of":"if","in conjunction with":"and, with","in connection with":"for, about","in consequence":"because, as a result","in excess of":"more than","in lieu of":"instead of","in order that":"so that","in receipt of":"get, have, receive","in relation to":"about","in respect of":"about, for","in the absence of":"without","in the course of":"while, during","in the event of/that":"if","in the majority of instances":"most, mostly","in the near future":"soon","in the neighborhood of":"about, around","in view of the fact that":"as, because","inappropriate":"wrong, unsuitable","inception":"start, beginning","incorporating":"which includes","incur":"have to pay, owe","indicate":"show, suggest","inform":"tell","initially":"at first","initiate":"begin, start","insert":"put in","instances":"cases","intend to":"will","intimate":"say, hint","irrespective of":"despite, even if","is of the opinion":"thinks","issue":"give, send","it is known that":"I/we know that","jeopardies":"risk, threaten","(a) large number of":"many, most (or say how many)","locality":"place, area","locate":"find, put","magnitude":"size","(it is) mandatory":"(you) must","manner":"way","manufacture":"make","marginal":"small, slight","material":"relevant","materialize":"happen, occur","may in the future":"may, might, could","merchandise":"goods","mislay":"lose","modification":"change","moreover":"and, also, as well","negligible":"very small","nevertheless":"but, however, even so","notify":"tell, let us (or you) know","notwithstanding":"even if, despite, still, yet","numerous":"many (or say how many)","objective":"aim, goal","(it is) obligatory":"(you) must","obtain":"get, receive","occasioned by":"caused by, because of","on behalf of":"for","on numerous occasions":"often","on request":"if you ask","on the grounds that":"because","on the occasion that":"when, if","operate":"work, run","optimum":"best, ideal","option":"choice","ordinarily":"normally, usually","otherwise":"or","outstanding":"unpaid","owing to":"because of","partially":"partly","participate":"join in, take part","particulars":"details, facts","per annum":"a year","perform":"do","permissible":"allowed","permit":"let, allow","personnel":"people, staff","persons":"people, anyone","peruse":"read, read carefully, look at","place":"put","possess":"have, own","possessions":"belongings","practically":"almost, nearly","predominant":"main","prescribe":"set, fix","preserve":"keep, protect","previous":"earlier, before, last","principal":"main","prior to":"before","proceed":"go ahead","procure":"get, obtain, arrange","profusion of":"plenty, too many (or say how many)","prohibit":"ban, stop","projected":"estimated","prolonged":"long","promptly":"quickly, at once","promulgate":"advertise, announce","proportion":"part","provide":"give","provided that":"if, as long as","provisions":"rules, terms","proximity":"closeness, nearness","purchase":"buy","pursuant to":"under, because of, in line with","reconsider":"think again about, look again at","reduce":"cut","reduction":"cut","referred to as":"called","refers to":"talks about, mentions","(have) regard to":"take into account","regarding":"about, on","regulation":"rule","reimburse":"repay, pay back","reiterate":"repeat, restate","relating to":"about","remain":"stay","remainder":"the rest, what is left","remittance":"payment","remuneration":"pay, wages, salary","render":"make, give, send","report":"tell","represents":"shows, stands for, is","request":"ask, question","require":"need, want, force","requirements":"needs, rules","reside":"live","residence":"home, where you live","restriction":"limit","retain":"keep","review":"look at (again)","revised":"new, changed","said/such/same":"the, this, that","scrutinize":"read (look at) carefully","select":"choose","settle":"pay","similarly":"also, in the same way","solely":"only","specified":"given, written, set","state":"say, tell us, write down","statutory":"legal, by law","subject to":"depending on, under, keeping to","submit":"send, give","subsequent to/upon":"after","subsequently":"later","substantial":"large, great, a lot of","substantially":"more or less","sufficient":"enough","supplement":"go with, add to","supplementary":"extra, more","supply":"give, sell, deliver","(the) tenant":"you","terminate":"stop, end","that being the case":"if so","the question as to whether":"whether","thereafter":"then, afterwards","thereby":"by that, because of that","therein":"in that, there","thereof":"of that","thereto":"to that","thus":"so, therefore","to date":"so far, up to now","to the extent that":"if, when","transfer":"change, move","transmit":"send","ultimately":"in the end, finally","unavailability":"lack of","undernoted":"the following","undersigned":"I, we","undertake":"agree, promise, do","uniform":"same, similar","unilateral":"one-sided, one-way","unoccupied":"empty","until such time":"until","utilization":"use","utilize":"use","variation":"change","virtually":"almost (or edit out)","visualize":"see, predict","ways and means":"ways","we have pleasure in":"we are glad to","whatsoever":"whatever, what, any","whensoever":"when","whereas":"but","whether or not":"whether","with a view to":"to, so that","with effect from":"from","with reference to":"about","with regard to":"about, for","with respect to":"about, for","with the minimum of delay":"quickly (or say when)","you are requested":"please","your attention is drawn to":"please see, please note","zone":"area, region","before too long":"soon"}

# Store Marked 2's keyword highlighting lists.
# Commented are the originals. Used are the unique elements not contained in pec
# marked_avoid = ["a total of","absolutely","abundantly","actually","all things being equal","as a matter of fact","as far as I am concerned","at the end of the day","at this moment in time","basically","current","currently","during the period from","each and every one","existing","extremely","I am of the opinion that","I would like to say","I would like to take this opportunity to","in due course","in the end","in the final analysis","in this connection","in total","in view of the fact that","it should be understood","last but not least","obviously","of course","other things being equal","pretty much","quite","really","really quite","regarding the","the fact of the matter is","the month of","the months of","to all intents and purposes","to one's own mind","very"]
# marked_alternate = ["a large number of","a number of","absence of","abundance","accede to","accelerate","accentuate","accommodation","accompany","accompanying","accomplish","accorded","according to our records","accordingly","accrue","acknowledge","acquaint yourself with","acquiesce","acquire","additional","adjacent","adjacent to","adjustment","admissible","advantageous","adversely impact","advise","affix","afford an opportunity","afforded","aforementioned","aforesaid","aggregate","aircraft","aligned","all of","alleviate","allocate","along the lines of","already existing","alternative","alternatively","ameliorate","amendment","anticipate","apparent","applicant","application","appreciable","apprise","appropriate","appropriate to","approximately","as a consequence of","as a means of","as of the date of","as of yet","as regards","as to","as yet","ascertain","assemble assistance","assistance","at an early date","at its discretion","at the moment","at the present time","at this time","attain","attempt","attend","attributable to","authorize","authority to","authorize","axiomatic","because of the fact that","belated","beneficial","benefit from","bestow","breach","by means of","by virtue of","calculate","cease","circumvent","clarification","close proximity","combine","combined","commence","communicate","competent","compile","complete","completion","comply with","component","comprise","compulsory","conceal","concerning","conclusion","concur","condition","consequently","considerable","consolidate","constitute","constitutes","construe","consult","consumption","contemplate","contrary to","correct","correspond","costs the sum of","counter","courteous","cumulative","currently","customary","deduct","deem to be","defer","deficiency","delete","demonstrate","denote","depart","depict","designate","desire","dispatch","despite the fact that","determine","detrimental","difficulties","diminish","disburse","discharge","disclose","disconnect","discontinue","discrete","discuss","dispatch","disseminate","documentation","domiciled in","dominant","due to the fact of","due to the fact that","duration","during which time","dwelling","each and every","economical","eligible","eliminate","elucidate","emphasize","employ","empower","enable","enclosed","encounter","endeavor","endeavor","inquire","inquiry","ensure","entitlement","enumerate","envisage","equitable","equivalent","erroneous","establish","evaluate","evidenced","evince","ex officio","exceptionally","excessive","exclude","excluding","exclusively","exempt from","expedite","expeditiously","expend","expenditure","expiration","expire","extant","extremity","fabricate","facilitate","factor","factual evidence","failure to","feasible","finalize","finalize","first and foremost","following","for the duration of","for the purpose of","for the reason that","forfeit","formulate","forthwith","forward","frequently","furnish","further to","furthermore","generate","give consideration to","grant","henceforth","hereby","herein","hereinafter","hereof","hereto","heretofore","hereunder","herewith","hitherto","hold in abeyance","honest truth","hope and trust","however","if and when","illustrate","immediately","impacted","implement","imply","in a number of cases","in a timely manner","in accordance with","in addition to","in addition","in advance","in all likelihood","in an effort to","in between","in case of","in conjunction with","in connection with","in consequence","in excess of","in lieu of","in light of the fact that","in many cases","in order that","in order to","in receipt of","in regard to","in relation to","in respect of","in some instances","in terms of","in the absence of","in the course of","in the event of","in the event that","in the majority of instances","in the near future","in the neighborhood of","in the process of","in view of the fact that","inappropriate","inception","incorporating","incumbent upon","incurred","indicate","indication","inform","initially","initiate","insert","instances","intend to","intimate","irrespective of","is applicable to","is authorized to","is in accordance with","is of the opinion","is responsible for","issue","it is essential","it is known that","jeopardize","liaise with","locality","locate","magnitude","mandatory","manner","manufacture","marginal","material","materialize","maximum","may in the future","merchandise","methodology","minimize","minimum","mislay","modification","modify","monitor","moreover","multiple","necessitate","negligible","nevertheless","not certain","not many","not often","not unless","not unlike","notify","notwithstanding","null and void","numerous","objective","obligate","obligatory","obtain","occasioned by","on behalf of","on numerous occasions","on receipt of","on request","on the contrary","on the grounds that","on the occasion that","on the other hand","one particular","operate","optimum","option","ordinarily","otherwise","outstanding","overall","owing to","owing to the fact that","partially","participate","particulars","pass away","per annum","percentage of","perform","permissible","permit","personnel","persons","pertaining to","peruse","place","please find enclosed","point in time","portion","possess","possessions","practically","preclude","predominant","prescribe","preserve","previous","previously","principal","prior to","prioritize","proceed","procure","proficiency","profusion of","progress something","prohibit","projected","prolonged","promptly","promulgate","proportion","provide","provided that","provisions","proximity","purchase","pursuant to","put simply","qualify for","readily apparent","reconsider","reduce","reduction","refer back","refer to","referred to as","regard to","regarding","regulation","reimburse","reiterate","relating to","relocate","remain","remainder","remittance","remuneration","render","represent","request","require","requirement","requirements","reside","residence","restriction","retain","review","revised","satisfy","scrutinize","select","settle","shall","should you wish","similar to","similarly","solely","solicit","span across","specified","state","statutory","strategize","subject to","submit","subsequent","subsequent to","subsequent upon","subsequently","substantial","substantially","successfully complete","sufficient","supplement","supplementary","supply","take pleasure in","tenant","terminate","that being the case","the month of","the question as to whether","thereafter","thereby","therefore","therein","thereof","thereto","thus","time period","to date","to the extent that","took advantage of","transfer","transmit","transpire","ultimately","unavailability","undernoted","undersigned","undertake","uniform","unilateral","unoccupied","until such time","until such time as","utilization","utilize","utilization","utilize","validate","variation","various different","very","virtually","visualize","ways and means","we have pleasure in","whatsoever","whensoever","whereas","whether or not","whilst","with a view to","with effect from","with reference to","with regard to","with respect to","with the exception of","with the minimum of delay","witnessed","you are requested","your attention is drawn"]

marked_avoid = ['a total of','absolutely','abundantly','actually','all things being equal','as a matter of fact','as far as I am concerned','at the end of the day','at this moment in time','basically','current','during the period from','each and every one','existing','extremely','I am of the opinion that','I would like to say','I would like to take this opportunity to','in due course','in the end','in the final analysis','in this connection','in total','it should be understood','last but not least','obviously','of course','other things being equal','pretty much','quite','really','really quite','regarding the','the fact of the matter is','the month of','the months of','to all intents and purposes',"to one's own mind",'very']
marked_alternate = ['a large number of','a number of','accompany','accorded','accrue','adjacent to','adversely impact','aforementioned','aircraft','all of','already existing','applicant','as a means of','as of yet','as to','as yet','assemble assistance','at this time','attain','authority to','because of the fact that','benefit from','by virtue of','close proximity','comprise','compulsory','consolidate','constitute','depart','due to the fact of','each and every','eliminate','employ','enumerate','equitable','evidenced','expend','expiration','factual evidence','feasible','first and foremost','forfeit','honest truth','however','impacted','in a timely manner','in addition to','in addition','in all likelihood','in an effort to','in between','in light of the fact that','in many cases','in order to','in regard to','in some instances','in terms of','in the event of','in the event that','in the process of','incumbent upon','incurred','indication','is applicable to','is authorized to','is in accordance with','is responsible for','it is essential','jeopardize','liaise with','mandatory','maximum','methodology','minimize','minimum','modify','monitor','multiple','necessitate','not certain','not many','not often','not unless','not unlike','null and void','obligate','obligatory','on receipt of','on the contrary','on the other hand','one particular','overall','owing to the fact that','pass away','percentage of','pertaining to','please find enclosed','point in time','portion','preclude','previously','prioritize','proficiency','progress something','put simply','qualify for','readily apparent','refer back','refer to','regard to','relocate','represent','requirement','satisfy','shall','should you wish','similar to','solicit','span across','strategize','subsequent','subsequent to','subsequent upon','successfully complete','take pleasure in','tenant','the month of','therefore','time period','took advantage of','transpire','until such time as','validate','various different','very','whilst','with the exception of','witnessed','your attention is drawn']

# Store the list of be verbs to avoid.
be_verbs = ["am", "is", "are", "was", "were", "be", "being", "been", "you're", "they're"]

# Store a list of words to exclude from repetition highlighting.
exclude = ["the", "a", "or", "my", "and", "to", "we", "an", "at", "I", "for", "i", "what", "of", "that", "he", "she", "it", "you", "your", "have", "which", "in", "on", "with", "would", "as", "had", "s"]

# If run, not imported:
if (__name__ == "__main__"):
    # Parse CLI arguments.
    args = parser.parse_args(sys.argv[1:])
    
    # Error if user does not specify an input file
    if (args.input_file == None):
        parser.print_help()
        sys.exit(1)

    # Make sure file exists
    if (not isfile(args.input_file)):
        print(f"{c.FAIL}Error:{c.ENDC} Input file does not exist.")
        sys.exit(1)

    # Record start time
    t1 = datetime.now()

    # Otherwise, process the input file
    print(f"Processing {c.UNDERLINE}{args.input_file}{c.ENDC} ... ")

    # Set document variables
    word_count, sentence_count, paragraph_count, overused_phrase_count, repeated_word_count, avoid_word_count, complex_words, syllable_count, fog_index, reading_ease, grade_level = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

    # Instantiate Markdown parser
    md = Markdown()

    # Read the template
    fd = open("./assets/template.html", "r")
    template = fd.read().split("<!-- DIVIDER -->")
    fd.close()

    # Open the output file
    if (args.output_file == None):
        args.output_file = "./index.html"
    open(args.output_file, "w").close()
    outfile = open(args.output_file, "a")

    # Process file
    infile = open(args.input_file, "r")
    
    for i,line in enumerate(infile):
        line = line.strip()

        if (i == 0): # Extract title
            if (line[:5] == "Type:"): # Handle files with a metadata header
                # Extract the title from the next line
                title = next(infile)[7:]
                # Skip three metadata lines and the blank line separator
                next(infile); next(infile); next(infile); next(infile)
            elif (line[0] == "#"): # Handle linkposts
                title = line.split("](")[0][2:]
            else: # Handle original articles
                title = line
                next(infile)

            # Write opening HTML tags and title to output file
            outfile.write(f"{template[0]}\n<article>\n<h2>{title}</h2>\n")
            continue
        
        # Parse Markdown line into HTML
        html_line = md.html(line)

        # Strip out all HTML tags from line, to leave only content.
        text_line = unescape(sub(r"(\<[^\>]+\>)", "", html_line))
        
        # Increase the paragraph count
        if (len(line) != 0): 
            if (line[0] != "#"):
                paragraph_count += 1

        # Tokenize paragraph by splitting into individual words.
        tokens = resplit(r"\W",text_line)

        # Extract unique words in sentence.
        tokens_set = frozenset(tokens)

        # Calculate total syllables present in document, and number of complex
        # words (words with >= 3 syllables). Also count words.
        long_words = []
        for word in tokens:
            if not (word.isalpha()): continue
            sylls = syllables(word)
            syllable_count += sylls
            if (sylls >= 3): 
                complex_words += 1
                if (word not in long_words):
                    html_line = html_line.replace(word, f"<span class='long'>{word}</span>")
                    long_words.append(word)
            word_count += 1

        # Find duplicate words, and highlight them.
        for word in (tokens_set - set(exclude+be_verbs)):
            if (len(word) != 0):
                if (tokens.count(word) > 2):
                    html_line = html_line.replace(word, f"<span class='dup'>{word}</span>")

        # Count sentences in paragraph, as defined by the number of '.', ';', 
        # '!', or '?' present.
        sentence_count += sum([text_line.count(x) for x in ['.',';','!','?']])

        # Highlight be verbs, words the Plain English Campaign lists as complex,
        # words Marked suggests avoiding, and words Marked suggests finding an
        # alternative for.
        for each in tokens_set:
            # Ignore non-word tokens and tokens that are in the exclude list
            if not (each.isalpha()): continue
            if (each in exclude): continue

            if (each in be_verbs): # Handle be verbs
                avoid_word_count += 1
                html_line = sub(f"(\W){each}(\W)", "\1<span class='avoid'>"+each+"</span>\2", html_line)
            elif (each in pec.keys()): # Handle Plain English Campaign's list
                overused_phrase_count += 1
                html_line = html_line.replace(each, f"<span class='trite tooltip'>{each}<span class='tooltiptext'>Consider replacing with: {pec[each]}</span></span>")
            elif (each in marked_avoid): # Handle Marked's Avoid word list
                avoid_word_count += 1
                html_line = html_line.replace(each, f"<span class='avoid'>{each}</span>")
            elif (each in marked_alternate): # Handle Marked's Alternate list
                overused_phrase_count += 1
                html_line = html_line.replace(each, f"<span class='alternate'>{each}</span>")

        # Write the processed line to the HTML file.
        outfile.write(f"{html_line}\n")
    # At the end of the input file, write closing HTML tags and close all files.
    else:
        # Calculate Gunning Fog Index, which estimates the years of formal
        # education needed to understand the text on a first reading.
        fog_index = 0.4*(float(word_count)/float(sentence_count) + 100.0*float(complex_words)/float(word_count))

        # Calculate Flesch-Kincaid Readability Test. Higher scores indicate
        # material that is easier to read; lower numbers indicate difficulty.
        reading_ease = 206.835 - 1.015*(float(word_count)/float(sentence_count)) - 84.6*(float(syllable_count)/float(word_count))
        if (reading_ease <= 30.0): reading_ease = "<span class='extreme'>%3.2f</span>" % (reading_ease)
        elif (reading_ease <= 50.0): reading_ease = "<span class='hard'>%3.2f</span>" % (reading_ease)
        elif (reading_ease <= 60.0): reading_ease = "<span class='tough'>%3.2f</span>" % (reading_ease)
        elif (reading_ease <= 70.0): reading_ease = "<span class='plain'>%3.2f</span>" % (reading_ease)
        elif (reading_ease <= 80.0): reading_ease = "<span class='fair'>%3.2f</span>" % (reading_ease)
        elif (reading_ease <= 90.0): reading_ease = "<span class='easy'>%3.2f</span>" % (reading_ease)
        elif (reading_ease <= 100.00): reading_ease = "<span class='simple'>%3.2f</span>" % (reading_ease)

        # Calculate the Flesch-Kincaid Grade level, which estimates the number
        # of years of education generally required to understand this text.
        grade_level = 0.39 * float(word_count)/float(sentence_count) + 11.8 * float(syllable_count)/float(word_count) - 15.59
        
        # Write the closing HTML tags, and fill in document statistics
        outfile.write(f"</article>\n{template[1].format(DTG=t1, WORDS=word_count, READING_TIME=(word_count/200), SENTENCES=sentence_count, PARAGRAPHS=paragraph_count, AVGWP=(word_count/paragraph_count), AVGWS=(word_count/sentence_count), AVGSS=(syllable_count/sentence_count), AVGS=(syllable_count/word_count), OVERUSED_PHRASES=overused_phrase_count, REPEATED_WORDS=repeated_word_count, WORDS_TO_AVOID=avoid_word_count, FOG_INDEX=fog_index, READING_EASE=reading_ease, GRADE_LEVEL=grade_level)}\n")
        
        # Close files.
        infile.close()
        outfile.close()

    # Record end time, and report execution time
    t2 = datetime.now()
    print(f"Execution time: {c.BOLD}{(t2-t1).total_seconds()}s{c.ENDC}")