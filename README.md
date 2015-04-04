# anki-note-maker
This Anki Note Maker gets a single text (.txt or no extension) file and makes the corresponding .csv files for basic, reversible, and cloze deletion cards, without requiring segregation into diffferent files beforehand. Makes converting typewritten notes faster!

The front and back part of the card is determined by the '?' everything before the '?' is the question or front portion, everything after is the answer or back portion.

Segregation into different types of cards is based on the first character of the line.
- no special character for [basic] cards
- ! or (shift + 1) for [reversible] cards
- \# or (shift + 2) for [cloze deletion] cards
- $ or (shift + 3) for step-by-step events cards (special card types I made; explained later, not yet implemented)
- % or (shift + 4) for residue cards (incomplete cards without an answer yet; you don't want to add those to your decks!)

-----

This is how basic card text looks like before running the program:
> What is the capital of X? Y 

This is what the card looks like after
- (front) What is the capital of X?
-- (back) Y
    
-----

This is how reversible card text looks like before running the program:

> !What is the capital of X country? capital: Y

This is what the 2 cards looks like after
 - (front) What is the capital of X country?
 -- (back) capital: Y
 
 * (front) capital: Y
 ** (back) What is the capital of X country?

-----

This is how cloze deletion card text looks like before running the program:
> @What are the cities found in X? A, B, C

This is what the 3 cards looks like after
- (front) What are the cities found in X? _, B, C
-- (back) What are the cities found in X? A, B, C

* (front) What are the cities found in X? A, _, C
** (back) What are the cities found in X? A, B, C

- (front) What are the cities found in X? A, B, _
-- (back) What are the cities found in X? A, B, C
 
-----

This is how step-by-step card text looks like before running the program:
> $stage of Event X? (1) ABC, (2) one-two-three, (3) do-re-mi, (4) you-and-me

This is what the 3 cards looks like after
- (front) What is the first or #1 stage of Event X that comes before do-re-mi?
-- (back) ABC

* (front) What is the #2 stage of Event X that comes after (1) ABC and before (3) do-re-mi?
** (back) one-two-three

- (front) What is the #3 stage of Event X that comes after (2) one-two-three and before (4) you-and-me?
-- (back) do-re-mi

* (front) What is the last or #4 stage of Event X that comes after (3) do-re-mi?
** (back) you-and-me

### Version
1.0.0

### Installation

As long as you have [Python], you should be good to go.

### Development

Contributions are welcome!


### Todo's

 - make in runnable in Terminal in one line with file as argument
 - GUI
 - Add Code Comments

License
----

GNU GPL


**Free Software, Hell Yeah!**

Used [dillinger.io]() to generate this Markdown document.

[basic]: http://ankisrs.net/docs/manual.html#the-basics
[reversible]: http://ankisrs.net/docs/manual.html#reverse-cards
[cloze deletion]: http://ankisrs.net/docs/manual.html#cloze
[Python]: https://www.python.org/downloads/

