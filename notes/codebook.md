Study of the wav2vec 2.0 codebook

Based on the small multi language wav2vec 2.0 model:
"facebook/wav2vec2-xls-r-300m"

The model also has codebook stored from training. The codebook is a matrix (640 X 384)
Actually the matrix consists of two codebooks, the first and last 320 rows. 
The model also contains a quantizer method that can map the cnn output (512) to a codevector output (768).
The codevector output first half v[:384] corresponds to a row in the first 320 rows in the codebook matrix
and the codevector output in the second half v[384:] corresponds to row in the second 320 row in the codebook matrix.
The code vector can be stored as two indices.


I wanted to recreate the plot in appendix d of the wav2vec 2.0 model. I applied the model on component k from CGN.
I used the quantizer to map the cnn output to a codevector. The codevector consists of two halves. The first halves is equal to
a vector in the first 320 rows of the stored codebook and the second half is equal to a vector in the last 320 rows in the 
codebook matrix. For each frame I stored the two indices.

See also:
https://github.com/martijnbentum/CGN_AUDIO_EXTRACT/blob/master/ld/codebook.py


Based on the awd (forced aligned - probably HTK) phoneme transcriptions I assigned each frame from the wav2vec 2.0 output a 
phoneme label - The phoneme label that most overlapped the wav2vec 2.0 output frame. The wav2vec 2.0 output frames are 25 ms in 
duration and have a step of 20 ms.

Each frame had a codevector with phoneme label. For each codevector type I counted the corresponding phoneme labels.
Based on the phoneme - codevector counts I created the plots below

code can be found here:
https://github.com/martijnbentum/CGN_AUDIO_EXTRACT/blob/master/ld/codevectors.py





Conditional probability P( phoneme | codevector )

![Screenshot 2023-11-23 at 16 23 36](https://github.com/martijnbentum/E2ELD-cautious-fiesta/assets/19554953/638bc027-bc87-46f6-ac68-95f8dd53d675)


Phoneme - phoneme confusion matrix

![Screenshot 2023-11-23 at 16 23 58](https://github.com/martijnbentum/E2ELD-cautious-fiesta/assets/19554953/0d745b34-2465-45af-bf27-0ee04ccfcbcd)



Conditional probability P( codevector | phoneme )

![Screenshot 2023-11-23 at 16 23 31](https://github.com/martijnbentum/E2ELD-cautious-fiesta/assets/19554953/ff63bcae-4329-45d4-95fe-da4dc693b975)
