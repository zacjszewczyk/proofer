#!/usr/local/bin/python3

# Import modules
import sys
import os
from time import sleep
import datetime
import re
from re import findall
sys.path.insert(0, '/Users/zjszewczyk/Dropbox/Code/Standalone')
from Markdown import Markdown

####
## "pec_overused" is a list of overused words from Plain English Campaign (http://www.plainenglish.co.uk/the-a-z-of-alternative-words.html)
## pec_overused    = ["an absence of", "absence of", "abundance", "accede to", "accelerate", "accentuate", "accommodation", "accompanying", "accomplish", "according to our records", "accordingly", "acknowledge", "acquaint yourself with", "acquiesce", "acquire", "additional", "adjacent", "adjustment", "admissible", "advantageous", "advise", "affix", "afford an opportunity", "afforded", "aforesaid", "aggregate", "aligned", "alleviate", "allocate", "along the lines of", "alternative", "alternatively", "ameliorate", "amendment", "anticipate", "apparent", "applicant", "application use", "appreciable", "apprise", "appropriate", "appropriate to", "approximately", "as a consequence of", "as of the date of", "as regards", "ascertain", "assemble", "assistance", "at an early date", "at its discretion", "at the moment", "at the present time", "attempt try", "attend", "attributable to", "authorise", "authority", "axiomatic", "beneficial", "bestow", "breach", "by means of", "cease", "circumvent", "clarification", "combine", "combined", "commence", "communicate", "competent", "compile", "complete", "completion", "comply with", "component", "comprises", "compulsory", "conceal", "concerning", "conclusion", "concur", "condition", "consequently", "considerable", "constitutes", "construe", "consult", "consumption", "contemplate", "contrary to", "correct", "correspond", "costs the sum of", "counter", "courteous", "cumulative", "currently", "customary", "deem to be", "defer", "deficiency", "delete", "demonstrate", "denote", "depict", "designate", "desire", "despatch", "dispatch", "despite the fact that", "determine", "detrimental", "difficulties", "diminish", "disburse", "discharge", "disclose", "disconnect", "discontinue", "discrete", "discuss", "disseminate", "documentation", "domiciled in", "dominant", "due to the fact that", "duration", "during which time", "dwelling", "eligible", "elucidate", "emphasise", "empower", "enable", "enclosed", "enclosed", "encounter", "endeavour", "enquire", "enquiry", "ensure", "entitlement", "envisage", "equivalent", "erroneous", "establish", "evaluate", "evince", "ex officio", "exceptionally", "excessive", "exclude", "excluding", "exclusively", "exempt from", "expedite", "expeditiously", "expenditure", "expire", "extant", "extremity", "facilitate", "factor", "failure to", "finalise", "following", "for the duration of ", "for the purpose of", "for the reason that", "formulate", "forthwith", "forward", "frequently", "furnish give", "further to", "furthermore", "give consideration to", "grant", "hereby", "herein", "hereinafter", "hereof", "hereto", "heretofore", "hereunder", "herewith", "hitherto", "hold in abeyance", "hope and trust", "illustrate", "immediately", "implement", "imply", "in a number of cases", "in accordance with", "in addition to", "in advance", "in case of", "in conjunction with", "in connection with", "in consequence", "in excess of", "in lieu of", "in order that", "in receipt of", "in relation to", "in respect of", "in the absence of", "in the course of", "in the event of/that", "in the majority of instances", "in the near future", "in the neighbourhood of", "in view of the fact that", "inappropriate", "inception", "incorporating", "incur", "indicate", "inform", "initially", "initiate", "insert", "instances", "intend to", "intimate", "irrespective of", "is of the opinion", "issue", "it is known that", "locality", "locate", "mandatory", "manner", "manufacture", "marginal", "material", "materialise", "may in the future", "merchandise", "mislay", "modification", "moreover", "nevertheless", "notify", "notwithstanding", "numerous", "obligatory", "obtain", "occasioned by", "on behalf of", "on numerous occasions", "on request", "on the grounds that because", "on the occasion that", "operate", "optimum", "option", "ordinarily", "otherwise", "outstanding", "owing to", "participate", "particulars", "per annum", "perform", "permissible", "permit", "personnel", "persons", "peruse", "place", "possess", "possessions", "practically", "predominant", "prescribe", "preserve", "previous", "principal", "prior to", "proceed", "procure", "profusion of", "prohibit", "projected", "prolonged", "promptly", "promulgate", "proportion", "provide", "provided that", "provisions", "proximity", "purchase", "pursuant to", "reduce", "reduction", "referred to as", "refers to", "regard to", "regarding", "regulation", "reimburse", "reiterate", "relating to about", "remain", "remainder", "remittance", "remuneration", "render", "report", "represents", "request", "require", "requirements", "reside", "residence", "restriction", "retain", "review", "revised", "scrutinise", "select", "settle", "similarly", "solely", "specified", "state", "statutory", "subject to", "submit", "subsequent to", "subsequent upon", "subsequently", "substantial", "substantially", "sufficient", "supplement", "supplementary", "supply", "terminate", "that being the case if so", "the question as to whether", "thereafter", "thereby", "therein", "thereof", "thereto", "thus", "to date", "to the extent that", "transfer", "transmit", "unavailability", "undernoted", "undersigned", "undertake", "uniform", "unilateral", "unoccupied", "until such time until", "utilisation", "utilise", "virtually", "visualise", "we have pleasure in", "whatsoever", "whensoever", "whereas", "whether or not", "with a view to", "with effect from", "with reference to", "with regard to", "with respect to", "with the minimum of delay", "your attention is drawn to", "zone"]
#
## "marked_overused" is a list of overused words from the Marked 2 app
## marked_overused = ["a total of", "absolutely", "abundantly", "actually", "all things being equal", "as a matter of fact", "as far as I am concerned", "at the end of the day", "at this moment in time", "basically", "current", "currently", "during the period from", "each and every one", "existing", "extremely", "I am of the opinion that", "I would like to say", "I would like to take this opportunity to", "in due course", "in the end", "in the final analysis", "in this connection", "in total", "in view of the fact that", "it should be understood", "last but not least", "obviously", "of course", "other things being equal", "pretty much", "quite", "really", "really quite", "regarding the", "the fact of the matter is", "the month of", "the months of", "to all intents and purposes", "to one's own mind", "very", "a large number of", "a number of", "absence of", "abundance", "accede to", "accelerate", "accentuate", "accommodation", "accompany", "accompanying", "accomplish", "accorded", "according to our records", "accordingly", "accrue", "acknowledge", "acquaint yourself with", "acquiesce", "acquire", "additional", "adjacent", "adjacent to", "adjustment", "admissible", "advantageous", "adversely impact", "advise", "affix", "afford an opportunity", "afforded", "aforementioned", "aforesaid", "aggregate", "aircraft", "aligned", "all of", "alleviate", "allocate", "along the lines of", "already existing", "alternative", "alternatively", "ameliorate", "amendment", "anticipate", "apparent", "applicant", "application", "appreciable", "apprise", "appropriate", "appropriate to", "approximately", "as a consequence of", "as a means of", "as of the date of", "as of yet", "as regards", "as to", "as yet", "ascertain", "assemble assistance", "assistance", "at an early date", "at its discretion", "at the moment", "at the present time", "at this time", "attain", "attempt", "attend", "attributable to", "authorise", "authority to", "authorize", "axiomatic", "because of the fact that", "belated", "beneficial", "benefit from", "bestow", "breach", "by means of", "by virtue of", "calculate", "cease", "circumvent", "clarification", "close proximity", "combine", "combined", "commence", "communicate", "competent", "compile", "complete", "completion", "comply with", "component", "comprise", "compulsory", "conceal", "concerning", "conclusion", "concur", "condition", "consequently", "considerable", "consolidate", "constitute", "constitutes", "construe", "consult", "consumption", "contemplate", "contrary to", "correct", "correspond", "costs the sum of", "counter", "courteous", "cumulative", "currently", "customary", "deduct", "deem to be", "defer", "deficiency", "delete", "demonstrate", "denote", "depart", "depict", "designate", "desire", "despatch", "despite the fact that", "determine", "detrimental", "difficulties", "diminish", "disburse", "discharge", "disclose", "disconnect", "discontinue", "discrete", "discuss", "dispatch", "disseminate", "documentation", "domiciled in", "dominant", "due to the fact of", "due to the fact that", "duration", "during which time", "dwelling", "each and every", "economical", "eligible", "eliminate", "elucidate", "emphasise", "employ", "empower", "enable", "enclosed", "encounter", "endeavor", "endeavour", "enquire", "enquiry", "ensure", "entitlement", "enumerate", "envisage", "equitable", "equivalent", "erroneous", "establish", "evaluate", "evidenced", "evince", "ex officio", "exceptionally", "excessive", "exclude", "excluding", "exclusively", "exempt from", "expedite", "expeditiously", "expend", "expenditure", "expiration", "expire", "extant", "extremity", "fabricate", "facilitate", "factor", "factual evidence", "failure to", "feasible", "finalise", "finalize", "first and foremost", "following", "for the duration of", "for the purpose of", "for the reason that", "forfeit", "formulate", "forthwith", "forward", "frequently", "furnish", "further to", "furthermore", "generate", "give consideration to", "grant", "henceforth", "hereby", "herein", "hereinafter", "hereof", "hereto", "heretofore", "hereunder", "herewith", "hitherto", "hold in abeyance", "honest truth", "hope and trust", "however", "if and when", "illustrate", "immediately", "impacted", "implement", "imply", "in a number of cases", "in a timely manner", "in accordance with", "in addition to", "in addition", "in advance", "in all likelihood", "in an effort to", "in between", "in case of", "in conjunction with", "in connection with", "in consequence", "in excess of", "in lieu of", "in light of the fact that", "in many cases", "in order that", "in order to", "in receipt of", "in regard to", "in relation to", "in respect of", "in some instances", "in terms of", "in the absence of", "in the course of", "in the event of", "in the event that", "in the majority of instances", "in the near future", "in the neighbourhood of", "in the process of", "in view of the fact that", "inappropriate", "inception", "incorporating", "incumbent upon", "incurred", "indicate", "indication", "inform", "initially", "initiate", "insert", "instances", "intend to", "intimate", "irrespective of", "is applicable to", "is authorized to", "is in accordance with", "is of the opinion", "is responsible for", "issue", "it is essential", "it is known that", "jeopardise", "liaise with", "locality", "locate", "magnitude", "mandatory", "manner", "manufacture", "marginal", "material", "materialise", "maximum", "may in the future", "merchandise", "methodology", "minimize", "minimum", "mislay", "modification", "modify", "monitor", "moreover", "multiple", "necessitate", "negligible", "nevertheless", "not certain", "not many", "not often", "not unless", "not unlike", "notify", "notwithstanding", "null and void", "numerous", "objective", "obligate", "obligatory", "obtain", "occasioned by", "on behalf of", "on numerous occasions", "on receipt of", "on request", "on the contrary", "on the grounds that", "on the occasion that", "on the other hand", "one particular", "operate", "optimum", "option", "ordinarily", "otherwise", "outstanding", "overall", "owing to", "owing to the fact that", "partially", "participate", "particulars", "pass away", "per annum", "percentage of", "perform", "permissible", "permit", "personnel", "persons", "pertaining to", "peruse", "place", "please find enclosed", "point in time", "portion", "possess", "possessions", "practically", "preclude", "predominant", "prescribe", "preserve", "previous", "previously", "principal", "prior to", "prioritize", "proceed", "procure", "proficiency", "profusion of", "progress something", "prohibit", "projected", "prolonged", "promptly", "promulgate", "proportion", "provide", "provided that", "provisions", "proximity", "purchase", "pursuant to", "put simply", "qualify for", "readily apparent", "reconsider", "reduce", "reduction", "refer back", "refer to", "referred to as", "regard to", "regarding", "regulation", "reimburse", "reiterate", "relating to", "relocate", "remain", "remainder", "remittance", "remuneration", "render", "represent", "request", "require", "requirement", "requirements", "reside", "residence", "restriction", "retain", "review", "revised", "satisfy", "scrutinise", "select", "settle", "shall", "should you wish", "similar to", "similarly", "solely", "solicit", "span across", "specified", "state", "statutory", "strategize", "subject to", "submit", "subsequent", "subsequent to", "subsequent upon", "subsequently", "substantial", "substantially", "successfully complete", "sufficient", "supplement", "supplementary", "supply", "take pleasure in", "tenant", "terminate", "that being the case", "the month of", "the question as to whether", "thereafter", "thereby", "therefore", "therein", "thereof", "thereto", "thus", "time period", "to date", "to the extent that", "took advantage of", "transfer", "transmit", "transpire", "ultimately", "unavailability", "undernoted", "undersigned", "undertake", "uniform", "unilateral", "unoccupied", "until such time", "until such time as", "utilisation", "utilise", "utilization", "utilize", "validate", "variation", "various different", "very", "virtually", "visualise", "ways and means", "we have pleasure in", "whatsoever", "whensoever", "whereas", "whether or not", "whilst", "with a view to", "with effect from", "with reference to", "with regard to", "with respect to", "with the exception of", "with the minimum of delay", "witnessed", "you are requested", "your attention is drawn"]
#
## "overlap" is a join of the two lists. This is the list used in this program.
overlap         = ['an absence of', 'absence of', 'abundance', 'accede to', 'accelerate', 'accentuate', 'accommodation', 'accompanying', 'accomplish', 'according to our records', 'accordingly', 'acknowledge', 'acquaint yourself with', 'acquiesce', 'acquire', 'additional', 'adjacent', 'adjustment', 'admissible', 'advantageous', 'advise', 'affix', 'afford an opportunity', 'afforded', 'aforesaid', 'aggregate', 'aligned', 'alleviate', 'allocate', 'along the lines of', 'alternative', 'alternatively', 'ameliorate', 'amendment', 'anticipate', 'apparent', 'applicant', 'application use', 'appreciable', 'apprise', 'appropriate', 'appropriate to', 'approximately', 'as a consequence of', 'as of the date of', 'as regards', 'ascertain', 'assemble', 'assistance', 'at an early date', 'at its discretion', 'at the moment', 'at the present time', 'attempt try', 'attend', 'attributable to', 'authorise', 'authority', 'axiomatic', 'beneficial', 'bestow', 'breach', 'by means of', 'cease', 'circumvent', 'clarification', 'combine', 'combined', 'commence', 'communicate', 'competent', 'compile', 'complete', 'completion', 'comply with', 'component', 'comprises', 'compulsory', 'conceal', 'concerning', 'conclusion', 'concur', 'condition', 'consequently', 'considerable', 'constitutes', 'construe', 'consult', 'consumption', 'contemplate', 'contrary to', 'correct', 'correspond', 'costs the sum of', 'counter', 'courteous', 'cumulative', 'currently', 'customary', 'deem to be', 'defer', 'deficiency', 'delete', 'demonstrate', 'denote', 'depict', 'designate', 'desire', 'despatch', 'dispatch', 'despite the fact that', 'determine', 'detrimental', 'difficulties', 'diminish', 'disburse', 'discharge', 'disclose', 'disconnect', 'discontinue', 'discrete', 'discuss', 'disseminate', 'documentation', 'domiciled in', 'dominant', 'due to the fact that', 'duration', 'during which time', 'dwelling', 'eligible', 'elucidate', 'emphasise', 'empower', 'enable', 'enclosed', 'enclosed', 'encounter', 'endeavour', 'enquire', 'enquiry', 'ensure', 'entitlement', 'envisage', 'equivalent', 'erroneous', 'establish', 'evaluate', 'evince', 'ex officio', 'exceptionally', 'excessive', 'exclude', 'excluding', 'exclusively', 'exempt from', 'expedite', 'expeditiously', 'expenditure', 'expire', 'extant', 'extremity', 'facilitate', 'factor', 'failure to', 'finalise', 'following', 'for the duration of ', 'for the purpose of', 'for the reason that', 'formulate', 'forthwith', 'forward', 'frequently', 'furnish give', 'further to', 'furthermore', 'give consideration to', 'grant', 'hereby', 'herein', 'hereinafter', 'hereof', 'hereto', 'heretofore', 'hereunder', 'herewith', 'hitherto', 'hold in abeyance', 'hope and trust', 'illustrate', 'immediately', 'implement', 'imply', 'in a number of cases', 'in accordance with', 'in addition to', 'in advance', 'in case of', 'in conjunction with', 'in connection with', 'in consequence', 'in excess of', 'in lieu of', 'in order that', 'in receipt of', 'in relation to', 'in respect of', 'in the absence of', 'in the course of', 'in the event of/that', 'in the majority of instances', 'in the near future', 'in the neighbourhood of', 'in view of the fact that', 'inappropriate', 'inception', 'incorporating', 'incur', 'indicate', 'inform', 'initially', 'initiate', 'insert', 'instances', 'intend to', 'intimate', 'irrespective of', 'is of the opinion', 'issue', 'it is known that', 'locality', 'locate', 'mandatory', 'manner', 'manufacture', 'marginal', 'material', 'materialise', 'may in the future', 'merchandise', 'mislay', 'modification', 'moreover', 'nevertheless', 'notify', 'notwithstanding', 'numerous', 'obligatory', 'obtain', 'occasioned by', 'on behalf of', 'on numerous occasions', 'on request', 'on the grounds that because', 'on the occasion that', 'operate', 'optimum', 'option', 'ordinarily', 'otherwise', 'outstanding', 'owing to', 'participate', 'particulars', 'per annum', 'perform', 'permissible', 'permit', 'personnel', 'persons', 'peruse', 'place', 'possess', 'possessions', 'practically', 'predominant', 'prescribe', 'preserve', 'previous', 'principal', 'prior to', 'proceed', 'procure', 'profusion of', 'prohibit', 'projected', 'prolonged', 'promptly', 'promulgate', 'proportion', 'provide', 'provided that', 'provisions', 'proximity', 'purchase', 'pursuant to', 'reduce', 'reduction', 'referred to as', 'refers to', 'regard to', 'regarding', 'regulation', 'reimburse', 'reiterate', 'relating to about', 'remain', 'remainder', 'remittance', 'remuneration', 'render', 'report', 'represents', 'request', 'require', 'requirements', 'reside', 'residence', 'restriction', 'retain', 'review', 'revised', 'scrutinise', 'select', 'settle', 'similarly', 'solely', 'specified', 'state', 'statutory', 'subject to', 'submit', 'subsequent to', 'subsequent upon', 'subsequently', 'substantial', 'substantially', 'sufficient', 'supplement', 'supplementary', 'supply', 'terminate', 'that being the case if so', 'the question as to whether', 'thereafter', 'thereby', 'therein', 'thereof', 'thereto', 'thus', 'to date', 'to the extent that', 'transfer', 'transmit', 'unavailability', 'undernoted', 'undersigned', 'undertake', 'uniform', 'unilateral', 'unoccupied', 'until such time until', 'utilisation', 'utilise', 'virtually', 'visualise', 'we have pleasure in', 'whatsoever', 'whensoever', 'whereas', 'whether or not', 'with a view to', 'with effect from', 'with reference to', 'with regard to', 'with respect to', 'with the minimum of delay', 'your attention is drawn to', 'zone', 'a total of', 'absolutely', 'abundantly', 'actually', 'all things being equal', 'as a matter of fact', 'as far as I am concerned', 'at the end of the day', 'at this moment in time', 'basically', 'current', 'during the period from', 'each and every one', 'existing', 'extremely', 'I am of the opinion that', 'I would like to say', 'I would like to take this opportunity to', 'in due course', 'in the end', 'in the final analysis', 'in this connection', 'in total', 'it should be understood', 'last but not least', 'obviously', 'of course', 'other things being equal', 'pretty much', 'quite', 'really', 'really quite', 'regarding the', 'the fact of the matter is', 'the month of', 'the months of', 'to all intents and purposes', "to one's own mind", 'very', 'a large number of', 'a number of', 'accompany', 'accorded', 'accrue', 'adjacent to', 'adversely impact', 'aforementioned', 'aircraft', 'all of', 'already existing', 'application', 'as a means of', 'as of yet', 'as to', 'as yet', 'assemble assistance', 'at this time', 'attain', 'attempt', 'authority to', 'authorize', 'because of the fact that', 'belated', 'benefit from', 'by virtue of', 'calculate', 'close proximity', 'comprise', 'consolidate', 'constitute', 'deduct', 'depart', 'due to the fact of', 'each and every', 'economical', 'eliminate', 'employ', 'endeavor', 'enumerate', 'equitable', 'evidenced', 'expend', 'expiration', 'fabricate', 'factual evidence', 'feasible', 'finalize', 'first and foremost', 'for the duration of', 'forfeit', 'furnish', 'generate', 'henceforth', 'honest truth', 'however', 'if and when', 'impacted', 'in a timely manner', 'in addition', 'in all likelihood', 'in an effort to', 'in between', 'in light of the fact that', 'in many cases', 'in order to', 'in regard to', 'in some instances', 'in terms of', 'in the event of', 'in the event that', 'in the process of', 'incumbent upon', 'incurred', 'indication', 'is applicable to', 'is authorized to', 'is in accordance with', 'is responsible for', 'it is essential', 'jeopardise', 'liaise with', 'magnitude', 'maximum', 'methodology', 'minimize', 'minimum', 'modify', 'monitor', 'multiple', 'necessitate', 'negligible', 'not certain', 'not many', 'not often', 'not unless', 'not unlike', 'null and void', 'objective', 'obligate', 'on receipt of', 'on the contrary', 'on the grounds that', 'on the other hand', 'one particular', 'overall', 'owing to the fact that', 'partially', 'pass away', 'percentage of', 'pertaining to', 'please find enclosed', 'point in time', 'portion', 'preclude', 'previously', 'prioritize', 'proficiency', 'progress something', 'put simply', 'qualify for', 'readily apparent', 'reconsider', 'refer back', 'refer to', 'relating to', 'relocate', 'represent', 'requirement', 'satisfy', 'shall', 'should you wish', 'similar to', 'solicit', 'span across', 'strategize', 'subsequent', 'successfully complete', 'take pleasure in', 'tenant', 'that being the case', 'therefore', 'time period', 'took advantage of', 'transpire', 'ultimately', 'until such time', 'until such time as', 'utilization', 'utilize', 'validate', 'variation', 'various different', 'ways and means', 'whilst', 'with the exception of', 'witnessed', 'you are requested', 'your attention is drawn']
####

# A list of be verbs to avoid
be_verbs        = ["am", "is", "are", "was", "were", "be", "being", "been", "you're", "they're"]
# A list of words to exclude from word repetition highlighting
exclude         = be_verbs+["the", "a", "or", "my", "and", "to", "we", "I", "for", "i", "what", "of", "that", "he", "she", "it", "you", "your", "have", "which", "in", "on", "with", "would", "as", "had"]

# Method: SyllableCount
# Purpose: Accept a word and return the number of syllables
# Parameters: word: Word to be parsed. (String)
# H/t: https://github.com/eaydin/sylco
def SyllableCount(word):
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

# Method: GenFile
# Purpose: Generate an HTML file for proofing
# Parameters:
# - iname: Name of content file. (String)
def GenFile(iname):
    # Instantiate document statistics
    #   fk_wc is a special word count for the Flesch-Kincaid readability test
    #   word_count is a by-paragraph word count
    #   total_sentences is a count of all sentences in document
    #   total_word_count is the word count for the entire document
    #   total_overused_words is the count of overused words
    #   total_repeated_words is the count of unique repeated words in the document,
    #       not including the individual repeats
    #   total_avoid_words is the ocunt of words to avoid in the document
    #   complex_words is a running count of words with over three syllables
    #   syllable_count is a running cound of syllables in the document
    fk_wc = 0
    word_count = []
    total_sentences = 0
    total_word_count = 0
    total_overused_words = 0
    total_repeated_words = 0
    total_avoid_words = 0
    complex_words = 0
    syllable_count = 0

    # Open th template file, read its contents, and split them for easy access later
    template_fd = open("template.html", "r")
    template = template_fd.read().split("<!--Divider-->")
    template_fd.close()

    # Clear the output file, then write the opening HTML tags
    o_fd = open("index.html", "w").close()
    o_fd = open("index.html", "a")
    o_fd.write(template[0])

    # Open the source file
    fd = open(iname, "r")
    
    # Read the title from the source file
    title = fd.readline().strip()
    if (title[0] == "#"):
        title = title.split("](")
        title = "<h2 class='linkpost'><a href=\""+title[1][:-3]+"\">"+title[0][3:]+"</a></h2>"
    else:
        title = "<h2 class='original'>"+title+"</h2>\n"
    
    # Get rid of the title separator (=) and the following blank line
    fd.readline()

    # Write the opening <article> tag and article title
    o_fd.write("<article>\n")
    o_fd.write(title)

    block = False
    # Iterate over each line in the file
    for line in iter(fd.readline, ""):
        fk_wc += line.count(" ")+1

        # Save a "backup" of the line, for searching a sanitized version of it
        backup = line
        
        # If we're looking at an empty line, just skip over it; else continue
        if (len(line.strip()) == 0):
            continue

        # Do not collect stats on code snippets. Write them to the file and
        # move on.
        if (line[0:4] == "<pre" or block == True):
            if (line.find("</pre>") == -1):
                block = True
            else:
                block = False
        
        # Do not collect stats on images. Write them to the file and move on.
        if (line[0:2] == "![" or line[0:4] == "<pre"):
            o_fd.write(Markdown(line, "https://zacs.site/")+"\n")
            continue
        
        # Instantiate paragraph-specific statistics
        wc = 0 # Word count for current paragraph
        overused_words = 0 # Number of overused words
        repeated_words = 0 # Number of repeated words
        avoid_words = 0 # Number of words to avoid
        dict_count = {} # A dictionary that will count occurences of each word

        # For each word in the list of overused words to avoid, search the
        # paragraph case insensitively. If a match is found, increment the count
        # of overused words in the paragraph and document, then highlight it.
        for word in overlap:
            m = re.search("[^\w]"+word+"[^\w]", line, re.IGNORECASE)
            if (m):
                overused_words += line.lower().count(word)
                total_overused_words += overused_words

                # The first replace will capture matches with uppercase letters
                # that start a sentence, or regular lowercase words; if the first
                # replace targeted matches with uppercase letters that start a
                # sentence, the second replace will capture all other occurences of
                # that word that may exist throughout the document.
                line = line.replace(m.group(0), " <span class='replace'>"+m.group(0)+"</span> ")
                if (m.group(0) != m.group(0).lower()):
                    line = line.replace(m.group(0).lower(), " <span class='replace'>"+m.group(0).lower().strip()+"</span> ")

        # For each word in the sentence, count repetitions. If there are three or more
        # of the same word in a sentnece, highlight all occurences. Also check for be
        # verbs as well, and highlight them accordingly.
        # for word in backup.split(" "):
        for word in re.split("(\s|--)", backup):

            if ("](" in word):
                word = word.split("](")[0]

            # This strips any special characters from the word, such as punctuation.
            stripped = re.sub(r"^[\W]+", "", word.strip())
            stripped = re.sub(r"[\W]+$", "", stripped)

            if (len(stripped) == 0):
                continue

            wc += 1

            # First check if we have decided to exclude the word, as in the case of "the",
            # "of", "a", "for", or similar words. If true, skip the word; else, proceed.
            if (stripped.lower() not in exclude):
                # If the word already exists in the dictionary, increment its count; else
                # instantiate it to 1
                if (stripped.lower() in dict_count):
                    dict_count[stripped.lower()] += 1
                else:
                    dict_count[stripped.lower()] = 1

                # Once there are at least three occurences of a word in the paragraph,
                # highlight it as a repeat word and incrememnt the number of unique words
                # repeated in the document.
                if (dict_count[stripped.lower()] == 3):
                    line = re.sub(r"([^\w])"+stripped+r"([^\w])", r"\1<span class='repeat "+stripped+"'>"+stripped+r"</span>\2", line)
                    repeated_words += 1
                    total_repeated_words += 1

            # Check for be verbs, "ly" words in the document. If found, highlight
            # them and increment the be verb count.
            if (stripped.lower() in be_verbs) or (stripped.lower()[-2:] == "ly"):
                line = re.sub(r"([^\w])"+stripped+r"([^\w])", r"\1<span class='avoid'>"+stripped+r"</span>\2", line)
                avoid_words += 1
                total_avoid_words += 1

            # To calculate the number of complex words, first exclude proper nouns. Next,
            # exclude compound words, then strip -es, -ed, and -ing endings. Finally, if
            # the number of syllables in the remaining word is >= 3, found a complex word.
            if (not (re.search("^[A-Z]", stripped))):
                if ("-" not in stripped):
                    if (SyllableCount(stripped.lower()) >= 3):
                        start = line.find(word)
                        length = len(word)
                        end = start+length

                        # print("Searched: '%s'" % line[start:end])
                        # print("With ends: '%s'" % line[start-1:end+1])
                        # print("Preceeding character: '%s'" % line[start-1])
                        # print("After character: '%s'" % line[end])
                        # print(re.match("[\>\w]", line[start-1]))
                        # print(re.match("[\<\w]", line[end]))
                        # print(line)
                        # print
                        if not ("http" in stripped or re.match("[\>\w]", line[start-1]) or re.match("[\<\w]", line[end])):
                            line = line.replace(stripped, "<span class='complex_word'>"+stripped+"</span>")
                        # line = re.sub((r"[^\>\w]")+stripped+(r"[^\<\w]"), "\1<span class='complex_word'>"+stripped+"</span>\2", line)
                        complex_words += 1
                        # sleep(1)

            syllable_count += SyllableCount(stripped.lower())

        word_count.append(wc)

        # Count sentences in paragraph, and add that number to the running sentence total
        sentences = (len(re.findall("\.[^\w]",line))+len(re.findall("[?!]",line))) or 1
        total_sentences += sentences

        if (line[0:1] != "* " and line[0] != "#" and line[0:3] != "<pre" and block == False and line[-7:].strip() != "</pre>"):
            # Write the paragraph stats div to the output file, then the parsed line.
            o_fd.write("<div class='floating_stats'><div>Words: %d. Sentences: %d</div><div>Overused phrase: %d</div><div>Repeated: %d; Avoid: %d</div></div>\n" % (word_count[-1], sentences, overused_words, repeated_words, avoid_words))
        o_fd.write(Markdown(line, "https://zacs.site/")+"\n")

    # Close the source file
    fd.close()

    # Write closing <article> tag
    o_fd.write("</article>")
    
    # Sum the paragraph word counts into a single count, for document stats
    for num in word_count:
        total_word_count += int(num)

    # Get a timestamp for the document stats
    d = datetime.datetime.now()
    utime = "%d-%d-%d %d:%d:%d" % (d.year,d.month,d.day,d.hour,d.minute,d.second)

    # Calculate Gunning Fog Index
    # estimates the years of formal education needed to understand the text on a first reading.
    gfi = 0.4*(float(total_word_count)/float(total_sentences) + 100.0*float(complex_words)/float(total_word_count))

    # Calculate Flesch-Kincaid Readability Test
    # higher scores indicate material that is easier to read; lower numbers indicate difficulty.
    fkr = 206.835 - 1.015*(float(fk_wc)/float(total_sentences)) - 84.6*(float(syllable_count)/float(fk_wc))
    print(type(fkr))

    if (fkr <= 30.0):
        fkr = "<span class='extreme'>%3.2f</span>" % (fkr)
    elif (fkr <= 50.0):
        fkr = "<span class='hard'>%3.2f</span>" % (fkr)
    elif (fkr <= 60.0):
        fkr = "<span class='tough'>%3.2f</span>" % (fkr)
    elif (fkr <= 70.0):
        fkr = "<span class='plain'>%3.2f</span>" % (fkr)
    elif (fkr <= 80.0):
        fkr = "<span class='fair'>%3.2f</span>" % (fkr)
    elif (fkr <= 90.0):
        fkr = "<span class='easy'>%3.2f</span>" % (fkr)
    elif (fkr <= 100.00):
        fkr = "<span class='simple'>%3.2f</span>" % (fkr)

    # Calculate the Flesch-Kincaid Grade level:
    # the number of years of education generally required to understand this text.
    fgl = 0.39 * float(total_word_count)/float(total_sentences) + 11.8 * float(syllable_count)/float(total_word_count) - 15.59

    # Write the closing HTML to the output file, with document stats. Close it.
    o_fd.write(template[1] % (utime, utime, total_word_count, str(total_word_count/200.0)+" mins", total_sentences, len(word_count), total_word_count/len(word_count), total_overused_words, total_repeated_words, total_avoid_words, gfi, fkr, fgl))
    o_fd.close()

if (__name__ == "__main__"):
    t1 = datetime.datetime.now()

    if (len(sys.argv) <= 1):
        print("Provide text file.")
        sys.exit(1)

    f = sys.argv[1]

    if (not os.path.isfile(f)):
        print("Provide valid file.")
        sys.exit(1)

    if (len(sys.argv) != 3):
        f_s = []

        while True:
            n_s = os.stat(f)
            n_s = [n_s.st_mtime, n_s.st_ctime]

            if (f_s == n_s):
                sleep(2)
                continue
            
            # File has changed
            d = datetime.datetime.now()
            utime = "%d-%d-%d %d:%d:%d" % (d.year,d.month,d.day,d.hour,d.minute,d.second)
            print("Building: ", utime)
            GenFile(f)

            f_s = n_s
    else:
        print("Building '%s'" % f)
        GenFile(f)

        t2 = datetime.datetime.now()

        print(("Execution time: %s" % (t2-t1)))