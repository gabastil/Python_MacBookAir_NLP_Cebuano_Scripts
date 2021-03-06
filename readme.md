# Cebuano Study

  1. [Paths](#paths)
  2. [Filenames](#filenames)
  3. [Packages](#packages)
  4. Scripts
  5. [Tags](#tags)

### Paths <a id="paths"></a>
  * data
  * scripts
  * output

### Filenames <a id="filenames"></a>

`.ceb.` extension used for Cebuano files.

Must contain `#[cebuano_research]` to be read.

### Packages <a id="packages"></a>

`parse` contains code to parse and extracts specified terms from a text.

To load: `from Parse.[module] import [class]`

  * Extractor.py	extract context/concordances, pairs, or word lists. (see scripts)
  * Parse.py		parse text into sentences, phrases, or tokens. 		(see scripts)

### Scripts <a id="scripts"></a>

```Empty```

### Tags <a id="tags"></a>

Numerical ranges [0-9;A-Z]

Tag | POS | Description
--- | :-: | ---
0000 | punctuation |
0001 | punctuation | other
*A000* | *number*
A001 | date |
*1000* | *noun*
1001 | noun | name - person
1002 | noun | name - place
1003 | noun | name - thing
1004 | noun | name - event
1005 | noun | name - organization
1006 | noun | name - proper name
10J1 | noun | name - person - with 'nga' adjective
10J2 | noun | name - place - with 'nga' adjective
10J3 | noun | name - thing - with 'nga' adjective
10J4 | noun | name - event - with 'nga' adjective
10J5 | noun | name - organization - with 'nga' adjective
10J6 | noun | name - proper name - with 'nga' adjective
1010 | noun | singular
1020 | noun | plural
1030 | noun | collective
1040 | noun | dual
1100 | noun | nominative
1200 | noun | accusative
1300 | noun | dative
1400 | noun | genitive
1500 | noun | locative
1600 | noun | vocative
1700 | noun | instrumental
*2000* | *pronoun*
2010 | pronoun | singular
2020 | pronoun | plural
2030 | pronoun | collective
2040 | pronoun | dual
2050 | pronoun | impersonal
2001 | pronoun | inclusive
2002 | pronoun | exclusive
2003 | pronoun | person - first
2004 | pronoun | person - second
2005 | pronoun | person - third
2100 | pronoun | nominative
2200 | pronoun | accusative
2300 | pronoun | dative
2400 | pronoun | genitive
2500 | pronoun | locative
2600 | pronoun | vocative
2700 | pronoun | instrumental
2800 | pronoun |
2900 | pronoun |
*3000* | *verb*
3001 | verb | tense - present
3002 | verb | tense - past
3003 | verb | tense - future
3004 | verb | mood - imperative
3005 | verb | mood - indicative
3006 | verb | mood - subjunctive
3007 | verb | mood - conditional
3008 | verb | mood - realis
3009 | verb | mood - irrealis
3010 | verb | aspect - imperfect
3020 | verb | aspect - continual
3030 | verb | aspect - perfect
3100 | verb | participle - present - gerund
3200 | verb | participle - past
*4000* | *adverb*
4001 | adverb | affirmative
4002 | adverb | negative
4003 | adverb | manner
4004 | adverb | location
4005 | adverb | extent
4010 | adverb | time - past1
4020 | adverb | time - past2
4030 | adverb | time - past3
4040 | adverb | time - present1
4050 | adverb | time - present2
4060 | adverb | time - present3
4070 | adverb | time - future1
4080 | adverb | time - future2
4090 | adverb | time - future3
*5000* | *adjective*
5100 | adjective | participle - present - gerund
5200 | adjective | participle - past
5001 | adjective | color
5002 | adjective | quality
5003 | adjective | quantity
5004 | adjective | relationship (e.g., possession)
*6000* | *conjunction*
6001 | conjunction | and
6002 | conjunction | but
6003 | conjunction | or
6004 | conjunction | xor
6005 | conjunction | not
*7000* | *preposition*
*8000* | *interjection*
*9000* | *grammatical particle*
9001 | particle | tense - present
9002 | particle | tense - past
9003 | particle | tense - future
9004 | particle | mood - imperative
9005 | particle | mood - indicative
9006 | particle | mood - subjunctive
9007 | particle | mood - conditional
9008 | particle | mood - realis
9009 | particle | mood - irrealis
9010 | particle | pos - noun
9020 | particle | pos - pronoun
9030 | particle | pos - verb
9040 | particle | pos - adverb
9050 | particle | pos - adjective
9060 | particle | pos - conjunction
9070 | particle | pos - preposition
9080 | particle | pos - interjection
9090 | particle | pos - interrogative
9000 | particle | definiteness - definite
9100 | particle | definiteness - indefinite
9200 | particle | number - singular
9300 | particle | number - plural
9400 | particle | number - dual
9500 | particle | number - collective
9600 | particle | number - modifier
