# Mald dataset, English words 1 speaker

Developed code in CGN audio extract respository to train probing classifier based on wav2vec 2.0 feature vectors
https://github.com/martijnbentum/CGN_AUDIO_EXTRACT/tree/master/ld

The classifier is a multi-layer perceptron from the scikit-learn module

Probing classifier results based on dataset described below.
Classifiers trained on mean feature vector (based on the time frames within the vowel, syllable and all frames of the word. Minimally 1 frame is used even if the vowel or syllable is shorter.

Word condition is a control. Expected it to perform at chance level, because the input to the classifier is the mean of all frames from the whole word (not just the target syllable) so unsure why it is still performing above chance.

<img width="608" alt="Screenshot 2023-11-01 at 15 01 06" src="https://github.com/martijnbentum/E2ELD-cautious-fiesta/assets/19554953/261ab6ef-8b4a-4772-b2df-cc312f11ae8c">


Selected syllables
'''python
 _,sd = ds.stress_variability_mald(d,50,0.05,n_include=None)  
''''
Syllable type with minimally 50 occurences and of 45 - 55% occurences
are stressed or unstressed (well balanced)

Number of syllables 2,424

### syllable duration
||mean|median|std|min|max|
|-|---|------|---|---|---|
|stressed|166|159|64|42|530|
|unstressed|158|149|77|30|466|

![Screenshot 2023-10-02 at 16 21 00](https://github.com/martijnbentum/E2ELD-cautious-fiesta/assets/19554953/a5d908e9-af69-42e6-aa65-2482c58eaf34)

### vowel duration
||mean|median|std|min|max|
|-|---|------|---|---|---|
|stressed|72|60|45|30|290|
|unstressed|68|50|42|30|238|

<img width="586" alt="Screenshot 2023-10-06 at 16 18 24" src="https://github.com/martijnbentum/E2ELD-cautious-fiesta/assets/19554953/019b25f9-c904-4896-8fb1-fc4cd62620ee">

syllable list

- l ɪ             295
- s ɪ             277
- t ɪ             252
- b ɪ             192
- s ɝ             191
- k ɑ n           137
- i               110
- aʊ t            98
- p i             89
- m ɝ             87
- j u             85
- w eɪ            79
- m æ n           72
- s t ɪ           67
- æ n             66
- b ai            59
- f i             59
- h ɛ d           54
- h aʊ s          53
- m ai            52
- s ai d          50
