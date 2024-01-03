Ik heb de spectral balance (zie artikel Sluijter & van Heuven 1994 in bijlage) berekend voor alle klinkers in all woorden in de MALD dataset. In totaal 67K klinkers.
Spectral balance wordt berekend door de intensiteit van vier frequentie banden te berekenen
0 - 500
500 - 1000
1000 - 2000
2000 - 4000
Ze laten zien dat een lineaire discriminant analyse (LDA) goed onderscheid kan maken op basis van deze vier waardes, waarbij de tendens is dat klinkers met klemtoon meer intensiteit hebben in de lagere frequentie banden (0 - 500, 500-1000). Ze laten ook zien dat als je de frequentie banden aanpast aan de formanten, de LDA beter klemtoon kan voorspellen, maar dat heb ik voor nu buiten beschouwing gelaten.

Als je de vier intensiteit waardes voor de frequentie banden gebruikt om een LDA te trainen krijg je op ongeziene data de volgende performance op het voorspellen van klemtoon:

             | precision   | recall  |f1-score  | support
         0.0   |   0.86      0.84   |   0.85   |  13482
         1.0    |   0.77      0.79   |   0.78   |   8782
   macro avg     |  0.81      0.82    |  0.82   |  22264
weighted avg     |  0.82      0.82     | 0.82   |  22264

Matthews correlation coefficient: 0.631

De LDA doet het iets beter dan de codevectors zie onder. De median lengte van een klinker is 62 milliseconden, dus deze analyse ziet wel ruim 2 keer meer input dan een codevector (25 ms).

MLP performance op basis van codevectors

              precision    recall  f1-score   support

   no_stress       0.73      0.89      0.80    119229
      stress       0.86      0.68      0.76    120607

    accuracy                           0.78    239836
   macro avg       0.79      0.78      0.78    239836
weighted avg       0.80      0.78      0.78    239836

Matthews correlation coefficient: 0.577

Het zou mooi zijn als je zou kunnen inschatten in hoeverre deze spectral balans de performance van de codevectors bepaald.
De LD zou daar misschien bij kunnen helpen.

Ik heb LD1 geplot (de y-as is random jitter zodat het verloop iets beter zichtbaar is). Ongeveer bij nul zie je het omslagpunt tussen klinker zonder of met klemtoon, waarbij < 0 geen klemtoon en > 0 wel klemtoon.
Om in te schatten of spectral balance de performance van codevectors bepaald zou ik het volgende kunnen doen:
Ik zou de klinkers kunnen nemen met klemtoon met een LD1 waarde van < -1 en de klinkers zonder klemtoon met een LD1 waarde van > 1
De verwachting zou dan zijn dat de codevectors slechter zullen scoren dan voor de klinkers met klemtoon met een LD1 waarde > 1 en klinkers zonder klemtoon met een LD1 waarde < -1.

Klinkt dat is een goede aanpak, of hebben jullie andere suggesties?

In een vervolgstap kunnen we kijken of de transformer lagen wellicht beter presteren door dat ze de duur meenemen.

![Screenshot 2024-01-03 at 10 33 20](https://github.com/martijnbentum/E2ELD-cautious-fiesta/assets/19554953/bad95e41-6def-4bfb-a7fc-64b1860ed407)
