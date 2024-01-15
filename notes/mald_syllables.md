# MALD  lexcial decision dataset (real words)
26,793 real words

## syllable segmentation is based on Celex and prosodic
words in Celex 2,4458, ~ 7,000 had different number of phonemes, syllable  
were estimated by matching phoneme strings with needleman wunch  
Subsequently the syllable index of a given Celex phoneme position was  
mapped to the textgrid phoneme set (automatic transcription of words,  
part of MALD dataset)  

The remaining 2,335 words not in Celex where syllabified with prosodic  
a python module to generate syllable boundaries and stress patterns
700 words could not be syllabified with prosodic
600 words had a different number of phonemes compared to the textgrid
1,000 words could be syllabified with prosodic. 

In total 25,426 words were syllabified (based on celex or prosodic)



### general
||types|tokes|
|-|----|-----|
|words|25,426|25,428|
|syllables|7,483|62,771|

25,426 out 62,771 syllables are stressed  
4,477 of the stressed syllables are from 1 syllable words (there are 4,477 syllable words)  
3,711 syllables types occur only once in the baldey dataset (2,911 are stressed)

### word counts with n syllables
|# syllables|word count|
|-----------|-----|
2|10,130|
3|6,642|
4|3,007|
1|4,447|
5|967|
6|167|
7|27|

### syllable duration
||mean|median|std|min|max|
|-|---|------|---|---|---|
|all|212|190|112|3|785|
|stressed|239|202|121|3|785|
|unstressed|195|180|102|30|616|

Density plot of syllable duration (stressed vs unstressed)

![Screenshot 2023-10-02 at 10 47 39](https://github.com/martijnbentum/E2ELD-cautious-fiesta/assets/19554953/bc433824-f35a-45f7-baf2-54fbef579a92)

## Duration differences in stressed vs unstressed vowels

Distribution duration differences between stressed and the mean duration of unstressed vowels in the same word. (median 0.010 | mean 0.012 | 56% of stressed vowels is longer than unstressed vowels)
(duration stressed - mean(duration unstressed vowels))

<img width="621" alt="Screenshot 2024-01-04 at 14 03 07" src="https://github.com/martijnbentum/E2ELD-cautious-fiesta/assets/19554953/fee07987-38c8-473e-80ff-c49d6b1e9b2e">

Distribution duration differences between stressed and  the duration of an unstressed vowel in the same word.
(median 0.01 | mean 0.012 | 61 % of stressed vowels is longer than unstressed vowels)
(duration stressed - duration unstressed vowel (same word))

![Screenshot 2024-01-08 at 16 51 35](https://github.com/martijnbentum/E2ELD-cautious-fiesta/assets/19554953/de3c3ff7-2e50-4688-8ec6-5c1d01af7d6b)

## Duration differences in stressed vs unstressed syllables

Distribution duration differences between stressed and the mean duration of unstressed syllables in the same word. (median 0.07 | mean 0.11 | 42% of stressed syllables is longer than unstressed syllables)
(duration stressed - mean(duration unstressed syllables))

![Screenshot 2024-01-15 at 15 25 29](https://github.com/martijnbentum/E2ELD-cautious-fiesta/assets/19554953/9f064da8-14bf-4b6e-b519-32667473b7f8)

Distribution duration differences between stressed and unstressed syllable in the same word. (median 0.08 | mean 0.11 | 48% of stressed syllables is longer than unstressed syllables)
(duration stressed - mean(duration unstressed syllables))

![Screenshot 2024-01-15 at 15 30 16](https://github.com/martijnbentum/E2ELD-cautious-fiesta/assets/19554953/6690f4e2-9702-46c6-99f0-27e63b554b80)

### top 20 syllable types with highest token counts
|syllable|count|stressed|unstressed|word|word ipa|
|--------|-----|--------|----------|----|--------|
|ʌ|981|23|958|a|ʌ|
|l i|963|60|903|abnormally|æ b n ɔ ɹ m ʌ l i|
|ɪ n|790|118|672|bedouin|b ɛ d u ɪ n|
|ʃ ʌ n|715|2|713|abduction|ʌ b d ʌ k ʃ ʌ n|
|d ɪ|680|115|565|accredited|ʌ k ɹ ɛ d ɪ t ɪ d|
|ɹ i|651|39|612|actuary|æ k tʃ u ɛ ɹ i|
|s ʌ|497|57|440|absolute|æ b s ʌ l u t|
|t ɝ|485|66|419|accelerator|æ k s ɛ l ɝ eɪ t ɝ|
|ʌ n|479|20|459|aberration|æ b ɝ eɪ ʃ ʌ n|
|m ʌ|455|48|407|abdominal|ʌ b d ɑ m ʌ n ʌ l|
|t ʌ|449|12|437|acceptable|ʌ k s ɛ p t ʌ b ʌ l|
|l ʌ|433|12|421|abilities|ʌ b ɪ l ʌ t i z|
|t i|425|39|386|ability|ʌ b ɪ l ʌ t i|
|k ʌ n|412|15|397|african|æ f ɹ ʌ k ʌ n|
|ɪ|400|61|339|absenteeism|æ b s ʌ n t i ɪ z ʌ m|
|ɹ ʌ|399|29|370|adorable|ʌ d ɔ ɹ ʌ b ʌ l|
|t ɪ ŋ|391|4|387|abstracting|æ b s t ɹ æ k t ɪ ŋ|
|k ʌ|366|67|299|abracadabra|æ b ɹ ʌ k ʌ d æ b ɹ ʌ|
|n ʌ|364|14|350|abominable|ʌ b ɑ m ʌ n ʌ b ʌ l|
|ɹ ɪ|354|53|301|airily|ɛ ɹ ɪ l i|

### syllable with variable stress descriptive_statistics.stress_variability()
35 syllable types with atleast 50 tokens with percentage stressed between .4 & .6

```python
{'l ɪ': {'stressed': 158,
  'unstressed': 137,
  'syllables': [Syl| l ɪ      | 0.12 | primary   | i: 2 | abolition | celex ul,
   Syl| l ɪ      | 0.12 | primary   | i: 2 | abolitionist | celex,
   Syl| l ɪ      | 0.15 | primary   | i: 2 | abolitionists | celex ul,
   Syl| l ɪ      | 0.14 | no stress | i: 4 | accessibility | celex,
   Syl| l ɪ      | 0.14 | no stress | i: 2 | acknowledges | celex],
  'perc_stressed': 0.54},
 's ɪ': {'stressed': 152,
  'unstressed': 125,
  'syllables': [Syl| s ɪ      | 0.21 | primary   | i: 1 | acidic | celex,
   Syl| s ɪ      | 0.16 | primary   | i: 1 | acidity | celex,
   Syl| s ɪ      | 0.15 | no stress | i: 2 | adversity | celex,
   Syl| s ɪ      | 0.16 | no stress | i: 2 | anglicism | celex,
   Syl| s ɪ      | 0.17 | no stress | i: 3 | asceticism | celex],
  'perc_stressed': 0.55},
 't ɪ': {'stressed': 113,
  'unstressed': 139,
  'syllables': [Syl| t ɪ      | 0.11 | no stress | i: 1 | activism | prosodic,
   Syl| t ɪ      | 0.15 | primary   | i: 1 | activity | celex,
   Syl| t ɪ      | 0.1  | no stress | i: 2 | advantages | celex,
   Syl| t ɪ      | 0.08 | no stress | i: 3 | analytical | celex ul,
   Syl| t ɪ      | 0.08 | no stress | i: 3 | analytically | celex ul],
  'perc_stressed': 0.45},
 'b ɪ': {'stressed': 97,
  'unstressed': 95,
  'syllables': [Syl| b ɪ      | 0.13 | primary   | i: 1 | abilities | celex,
   Syl| b ɪ      | 0.12 | primary   | i: 1 | ability | celex,
   Syl| b ɪ      | 0.1  | primary   | i: 3 | accessibility | celex,
   Syl| b ɪ      | 0.11 | primary   | i: 1 | ambiguous | celex ul,
   Syl| b ɪ      | 0.09 | primary   | i: 1 | ambition | celex ul],
  'perc_stressed': 0.51},
 's ɝ': {'stressed': 88,
  'unstressed': 103,
  'syllables': [Syl| s ɝ      | 0.2  | primary   | i: 1 | absurdities | celex,
   Syl| s ɝ      | 0.21 | primary   | i: 1 | absurdity | celex,
   Syl| s ɝ      | 0.24 | no stress | i: 2 | aggressor | celex ul,
   Syl| s ɝ      | 0.25 | no stress | i: 2 | announcer | celex ul,
   Syl| s ɝ      | 0.23 | no stress | i: 1 | answer | celex ul],
  'perc_stressed': 0.46},
 'k ɑ n': {'stressed': 75,
  'unstressed': 62,
  'syllables': [Syl| k ɑ n    | 0.28 | primary   | i: 2 | anacondas | celex,
   Syl| k ɑ n    | 0.22 | primary   | i: 0 | cognac | celex,
   Syl| k ɑ n    | 0.19 | primary   | i: 0 | concentrate | celex,
   Syl| k ɑ n    | 0.18 | primary   | i: 0 | concentrated | celex,
   Syl| k ɑ n    | 0.17 | primary   | i: 0 | concentrating | celex],
  'perc_stressed': 0.55},
 'i': {'stressed': 52,
  'unstressed': 58,
  'syllables': [Syl| i        | 0.12 | secondary | i: 1 | anteater | celex ul,
   Syl| i        | 0.05 | no stress | i: 3 | arteriosclerosis | celex,
   Syl| i        | 0.09 | secondary | i: 1 | beefeater | celex ul,
   Syl| i        | 0.1  | no stress | i: 1 | blurry | prosodic,
   Syl| i        | 0.05 | primary   | i: 1 | coequal | celex],
  'perc_stressed': 0.47},
 'aʊ t': {'stressed': 44,
  'unstressed': 54,
  'syllables': [Syl| aʊ t     | 0.16 | no stress | i: 1 | blackout | celex,
   Syl| aʊ t     | 0.15 | no stress | i: 1 | blowout | celex,
   Syl| aʊ t     | 0.23 | no stress | i: 1 | checkout | celex,
   Syl| aʊ t     | 0.12 | no stress | i: 1 | closeout | celex,
   Syl| aʊ t     | 0.2  | no stress | i: 1 | cookout | celex],
  'perc_stressed': 0.45},
 'p i': {'stressed': 43,
  'unstressed': 46,
  'syllables': [Syl| p i      | 0.2  | primary   | i: 1 | appealing | celex,
   Syl| p i      | 0.2  | primary   | i: 1 | appeasing | celex,
   Syl| p i      | 0.2  | no stress | i: 1 | bumpy | celex,
   Syl| p i      | 0.25 | no stress | i: 2 | canopy | celex,
   Syl| p i      | 0.23 | no stress | i: 1 | choppy | celex],
  'perc_stressed': 0.48},
 'm ɝ': {'stressed': 41,
  'unstressed': 46,
  'syllables': [Syl| m ɝ      | 0.11 | no stress | i: 1 | admirable | celex,
   Syl| m ɝ      | 0.18 | no stress | i: 1 | admiration | celex,
   Syl| m ɝ      | 0.19 | no stress | i: 1 | armor | prosodic,
   Syl| m ɝ      | 0.17 | no stress | i: 2 | beachcomber | celex ul,
   Syl| m ɝ      | 0.22 | no stress | i: 1 | bloomer | celex ul],
  'perc_stressed': 0.47},
 'j u': {'stressed': 46,
  'unstressed': 39,
  'syllables': [Syl| j u      | 0.16 | primary   | i: 1 | amusing | celex ul,
   Syl| j u      | 0.16 | no stress | i: 2 | devalue | celex,
   Syl| j u      | 0.12 | primary   | i: 1 | disunion | celex,
   Syl| j u      | 0.1  | primary   | i: 1 | disunity | celex,
   Syl| j u      | 0.08 | secondary | i: 0 | eucalyptus | celex],
  'perc_stressed': 0.54},
 'w eɪ': {'stressed': 38,
  'unstressed': 41,
  'syllables': [Syl| w eɪ     | 0.2  | no stress | i: 1 | airway | celex ul,
   Syl| w eɪ     | 0.27 | no stress | i: 2 | alleyway | celex,
   Syl| w eɪ     | 0.17 | no stress | i: 2 | anyway | celex,
   Syl| w eɪ     | 0.23 | no stress | i: 1 | archway | celex ul,
   Syl| w eɪ     | 0.21 | primary   | i: 1 | awaiting | celex],
  'perc_stressed': 0.48},
 'm æ n': {'stressed': 35,
  'unstressed': 37,
  'syllables': [Syl| m æ n    | 0.28 | no stress | i: 2 | anchorman | celex,
   Syl| m æ n    | 0.33 | no stress | i: 1 | batman | celex,
   Syl| m æ n    | 0.23 | no stress | i: 2 | businessman | celex,
   Syl| m æ n    | 0.28 | no stress | i: 1 | caveman | celex,
   Syl| m æ n    | 0.2  | no stress | i: 1 | clansman | celex],
  'perc_stressed': 0.49},
 's t ɪ': {'stressed': 36,
  'unstressed': 31,
  'syllables': [Syl| s t ɪ    | 0.18 | no stress | i: 2 | acoustically | celex ul,
   Syl| s t ɪ    | 0.17 | no stress | i: 4 | characteristically | celex ul,
   Syl| s t ɪ    | 0.17 | primary   | i: 1 | constituencies | celex,
   Syl| s t ɪ    | 0.16 | primary   | i: 1 | constituency | celex,
   Syl| s t ɪ    | 0.19 | primary   | i: 1 | constituent | celex],
  'perc_stressed': 0.54},
 'æ n': {'stressed': 31,
  'unstressed': 35,
  'syllables': [Syl| æ n      | 0.3  | primary   | i: 0 | an | celex,
   Syl| æ n      | 0.13 | primary   | i: 0 | ancestor | celex ul,
   Syl| æ n      | 0.15 | primary   | i: 0 | ancestors | celex,
   Syl| æ n      | 0.12 | no stress | i: 0 | ancestral | celex,
   Syl| æ n      | 0.14 | primary   | i: 0 | ancestry | celex],
  'perc_stressed': 0.47},
 'b ai': {'stressed': 27,
  'unstressed': 32,
  'syllables': [Syl| b ai     | 0.31 | no stress | i: 2 | alibi | celex,
   Syl| b ai     | 0.19 | no stress | i: 2 | antibiotic | celex,
   Syl| b ai     | 0.17 | no stress | i: 2 | antibiotics | celex,
   Syl| b ai     | 0.21 | secondary | i: 2 | autobiographic | celex,
   Syl| b ai     | 0.25 | secondary | i: 2 | autobiographical | celex ul],
  'perc_stressed': 0.46},
 'f i': {'stressed': 27,
  'unstressed': 32,
  'syllables': [Syl| f i      | 0.27 | no stress | i: 3 | apostrophe | celex,
   Syl| f i      | 0.26 | no stress | i: 5 | autobiography | celex,
   Syl| f i      | 0.22 | no stress | i: 4 | bibliography | celex,
   Syl| f i      | 0.28 | no stress | i: 3 | biography | celex,
   Syl| f i      | 0.17 | no stress | i: 1 | breastfeeding | celex],
  'perc_stressed': 0.46},
 'h ɛ d': {'stressed': 25,
  'unstressed': 29,
  'syllables': [Syl| h ɛ d    | 0.33 | primary   | i: 1 | ahead | celex,
   Syl| h ɛ d    | 0.31 | no stress | i: 2 | arrowhead | celex,
   Syl| h ɛ d    | 0.24 | no stress | i: 1 | beachhead | celex,
   Syl| h ɛ d    | 0.27 | no stress | i: 1 | bighead | celex,
   Syl| h ɛ d    | 0.23 | no stress | i: 1 | blockhead | celex],
  'perc_stressed': 0.46},
 'h aʊ s': {'stressed': 24,
  'unstressed': 29,
  'syllables': [Syl| h aʊ s   | 0.41 | no stress | i: 1 | alehouse | celex,
   Syl| h aʊ s   | 0.34 | no stress | i: 1 | blockhouse | celex,
   Syl| h aʊ s   | 0.41 | no stress | i: 2 | boardinghouse | celex ul,
   Syl| h aʊ s   | 0.4  | no stress | i: 1 | boathouse | celex,
   Syl| h aʊ s   | 0.41 | no stress | i: 1 | bunkhouse | celex],
  'perc_stressed': 0.45},
 'm ai': {'stressed': 27,
  'unstressed': 25,
  'syllables': [Syl| m ai     | 0.2  | primary   | i: 1 | admired | celex,
   Syl| m ai     | 0.19 | primary   | i: 1 | almighty | celex,
   Syl| m ai     | 0.19 | no stress | i: 2 | compromises | celex,
   Syl| m ai     | 0.16 | no stress | i: 2 | compromising | celex,
   Syl| m ai     | 0.17 | no stress | i: 2 | dynamited | celex],
  'perc_stressed': 0.52},
 's ai d': {'stressed': 26,
  'unstressed': 24,
  'syllables': [Syl| s ai d   | 0.44 | no stress | i: 2 | alongside | celex,
   Syl| s ai d   | 0.5  | primary   | i: 1 | aside | celex,
   Syl| s ai d   | 0.34 | primary   | i: 1 | backside | celex,
   Syl| s ai d   | 0.34 | no stress | i: 1 | bedside | celex,
   Syl| s ai d   | 0.38 | primary   | i: 2 | coincide | celex],
  'perc_stressed': 0.52}}
```

