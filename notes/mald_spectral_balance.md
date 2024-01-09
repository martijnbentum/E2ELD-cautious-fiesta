Spectral balance was calculated based on the article Sluijter & van Heuven 1994 (Spectral balance as an acoustic correlate of linguistic stress). It was calculated for all vowels in all words in the MALD dataset.  In total 67K vowels.
Spectral balance computes the intensity of four frequecy bands 
0 - 500
500 - 1000
1000 - 2000
2000 - 4000
Sluijter & van Heuven (1994) show that linair discriminant analysis can classify stress based on the intensity of these four frequency bands. The intensity of lower frequency bands shows a slower drop off for stressed vowels compared to unstressed vowels.
A further classification improvement can be obtained by changing the frequency bands based on the formants. This was not attempted for the current analysis.

LDA classification performance on unseen data based on the inensity values of the aforementioned frequecy bands:

   |         |  precision  |  recall | f1-score  | support |
   |---------|-------------|---------|-----------|---------|
  | no_stress |       0.86 |     0.84   |   0.85  |  13482 |
   |   stress  |     0.77   |   0.79   |   0.78   | 8782|  
   | |
   |accuracy| | | 0.82 | 22264 |
   | macro avg   |    0.81   |   0.82   |   0.82   | 22264|
| weighted avg    |   0.802  |   0.82    |  0.82   | 22264|

Matthews correlation coefficient: 0.631

De LDA performs marginally better than codevectors (zie onder). De median duration of a vowel is 62 milliseconds, so this classifier sees twice the audio input compared to a codevector (25 ms).

MLP performance op basis van codevectors

   |         |  precision  |  recall | f1-score  | support |
   |---------|-------------|---------|-----------|---------|
  | no_stress |       0.73 |     0.89   |   0.80  |  119229 |
   |   stress  |     0.86   |   0.68   |   0.76   | 120607|  
   | |
   |accuracy| | | 0.78 | 239836 |
   | macro avg   |    0.79   |   0.78   |   0.78   | 239836|
| weighted avg    |   0.80   |   0.78    |  0.78   | 239836|

Matthews correlation coefficient: 0.577

LDA score counts for stressed and unstressed vowels
<img width="827" alt="Screenshot 2024-01-09 at 17 31 46" src="https://github.com/martijnbentum/E2ELD-cautious-fiesta/assets/19554953/d5f0a0b1-c2dc-4880-8bb7-beefeb7c0992">


Scatterplot

<img width="817" alt="Screenshot 2024-01-09 at 17 22 27" src="https://github.com/martijnbentum/E2ELD-cautious-fiesta/assets/19554953/f8b08918-a9f8-4353-9c03-129e8027ce3b">

Counts of mean difference in ld1 score between stressed and unstressed vowels in the same word
(ld1 score stressed vowel - mean(ld1 score unstressed vowels)) - same word

<img width="830" alt="Screenshot 2024-01-09 at 17 23 18" src="https://github.com/martijnbentum/E2ELD-cautious-fiesta/assets/19554953/d790c62b-3326-4bac-80e4-2ba74b3c64f7">


Counts of difference in ld1 score between stressed and unstressed vowel in the same word
(ld1 score stressed vowel - ld1 score unstressed vowel) - same word
<img width="808" alt="Screenshot 2024-01-09 at 17 24 03" src="https://github.com/martijnbentum/E2ELD-cautious-fiesta/assets/19554953/bf5def3f-31e7-45fa-8d01-dd2c915b28a7">


I computed the intensity in four frequency bands. The plots below show the values in the different frequency bands

Mean Intensity in dB for stressed and unstressed vowels for four frequency bands
<img width="797" alt="Screenshot 2024-01-09 at 17 27 00" src="https://github.com/martijnbentum/E2ELD-cautious-fiesta/assets/19554953/fa963284-46e9-4f02-82a1-a29ec86756b5">


Intensity in dB for stressed and unstressed vowels for four frequency bands per vowel
<img width="1540" alt="Screenshot 2024-01-09 at 17 30 34" src="https://github.com/martijnbentum/E2ELD-cautious-fiesta/assets/19554953/b01f9111-f946-4541-9b03-b49d7b68c342">





Het zou mooi zijn als je zou kunnen inschatten in hoeverre deze spectral balans de performance van de codevectors bepaald.
De LD zou daar misschien bij kunnen helpen.

Ik heb LD1 geplot (de y-as is random jitter zodat het verloop iets beter zichtbaar is, scatterplot). Ongeveer bij nul zie je het omslagpunt tussen klinker zonder of met klemtoon, waarbij < 0 geen klemtoon en > 0 wel klemtoon.
Om in te schatten of spectral balance de performance van codevectors bepaald zou ik het volgende kunnen doen:
Ik zou de klinkers kunnen nemen met klemtoon met een LD1 waarde van < -1 en de klinkers zonder klemtoon met een LD1 waarde van > 1
De verwachting zou dan zijn dat de codevectors slechter zullen scoren dan voor de klinkers met klemtoon met een LD1 waarde > 1 en klinkers zonder klemtoon met een LD1 waarde < -1.

Klinkt dat is een goede aanpak, of hebben jullie andere suggesties?

In een vervolgstap kunnen we kijken of de transformer lagen wellicht beter presteren door dat ze de duur meenemen.



