Proofer
=======

## Introduction

Given a plain text file formatted in Markdown, Proofer will generate a live preview of the article as it will appear [on my blog](http://zacs.site/blog). Using a modified version of my blog's template, it includes statistics like word, sentence, and paragraph count; average words per paragraph; suggestions to replace overused, complex, or repetitious words; and statistics based on the Flesch–Kincaid readability tests and the Gunning fog index. Although I did my best to calculate accurate results for those algorithms, I have little expertise in natural language processing; I did enough to get close, and I plan to fine-tune my script later.

## Document Statistics

Specifically, Proofer provides the following document statistics:

* Word count
* Sentence count
* Paragraphs count
* Avgerage number of words per paragraph
* Number of overused words and phrases - A metric Proofer calculates using a lengthy list of pre-defined overused words and phrases culled from [Plain English Campaign](http://www.plainenglish.co.uk/) and [Marked 2](http://marked2app.com/).
* Repeated words - The number of unique words repeated three or more times in the document.
* Words to avoid - A metric Proofer calculates using a list of words and phrases from [Plain English Campaign](http://www.plainenglish.co.uk/) and [Marked 2](http://marked2app.com/).