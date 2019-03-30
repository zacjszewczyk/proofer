Proofer
=======

## Introduction

Given a plain text file formatted in Markdown, Proofer will generate a live preview of the article as it will appear [on my blog](http://zacs.site/blog.html). Using a modified version of my blog's template, it includes statistics like word, sentence, and paragraph count; average words per paragraph; suggestions to replace overused, complex, or repetitious words; and statistics based on the Flesch–Kincaid readability tests and the Gunning fog index. Although I did my best to calculate accurate results for those algorithms, I have little expertise in natural language processing; I did enough to get close, and I plan to fine-tune my script later.

## Document Statistics

Specifically, Proofer provides the following document statistics:

* Word count
* Sentence count
* Paragraphs count
* Average number of words per paragraph
* Number of overused words and phrases - A metric Proofer calculates using a lengthy list of pre-defined overused words and phrases culled from [Plain English Campaign](http://www.plainenglish.co.uk/) and [Marked 2](http://marked2app.com/).
* Number of repeated words - The number of unique words repeated three or more times in the document.
* Number of words to avoid - A metric Proofer calculates using a list of words and phrases from [Plain English Campaign](http://www.plainenglish.co.uk/) and [Marked 2](http://marked2app.com/).
* Fog index - The Gunning Fog Index estimates the years of formal education needed to understand the text on a first reading.
* Reading ease - The Flesch–Kincaid reading metric uses higher scores to indicate material that is easier to read, and lower scores to indicate difficulty.
* Grade level - The Flesch–Kincaid grade level estimates the number of years of education generally required to understand this text.

In addition, Proofer highlights all occurrences of overused words and phrases in one color, all repeat words in another, and all words to avoid in a third. This makes visualizing weak areas easy. Hovering over an individual paragraph also reveals all words of three syllables or more, which in general indicates words of greater complexity. Once again, this makes visualizing weak areas easy. 

## Paragraph Statistics

For each individual paragraph, Proofer also provides the following statistics. These are, in general, culled from the more extensive document statistics above.

* Paragraph word count
* Paragraph sentence count
* Number of overused words and phrases - See above.
* Number of repeated words - See above.
* Number of words to avoid - See above.