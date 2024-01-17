Collected all frames (n=744635) with corresponding codevectors from the MALD words. 
Each frame has label unstressed / stressed based on the stress of the phoneme it most overlaps with.

### LDA classifier trained on 67% the codevectors with labels tested on 33% unseen data

## only vowels

   |         |  precision  |  recall | f1-score  | support |
   |---------|-------------|---------|-----------|---------|
  | no_stress |       0.82 |     0.79   |   0.81  |  44042 |
   |   stress  |     0.78   |   0.81   |   0.79   | 40158|  
   | |
   |accuracy| | | 0.80 | 84200 |
   | macro avg   |    0.80   |   0.80   |   0.90   | 84200|
| weighted avg    |   0.80  |   0.80    |  0.80   | 84200|

Matthews correlation coefficient: 0.631

## all phonemes (consonants & vowels)

   |         |  precision  |  recall | f1-score  | support |
   |---------|-------------|---------|-----------|---------|
  | no_stress |       0.93 |     0.94   |   0.93  |  208684 |
   |   stress  |     0.67   |   0.64   |   0.65   | 40676|  
   | |
   |accuracy| | | 0.89 | 249360 |
   | macro avg   |    0.81   |   0.82   |   0.79   | 249360|
| weighted avg    |   0.802  |   0.82    |  0.89   | 249360|

Matthews correlation coefficient: 0.590



LDA on codevectors a bit better than MLP on codevectors

### MLP performance based on codevectors

   |         |  precision  |  recall | f1-score  | support |
   |---------|-------------|---------|-----------|---------|
  | no_stress |       0.73 |     0.89   |   0.80  |  119229 |
   |   stress  |     0.86   |   0.68   |   0.76   | 120607|  
   | |
   |accuracy| | | 0.78 | 239836 |
   | macro avg   |    0.79   |   0.78   |   0.78   | 239836|
| weighted avg    |   0.80   |   0.78    |  0.78   | 239836|

Matthews correlation coefficient: 0.577

### LDA Performance based on codevector seems to be different compared to LDA performance based on spectral balance

   |         |  precision  |  recall | f1-score  | support |
   |---------|-------------|---------|-----------|---------|
  | no_stress |       0.86 |     0.84   |   0.85  |  13482 |
   |   stress  |     0.77   |   0.79   |   0.78   | 8782|  
   | |
   |accuracy| | | 0.82 | 22264 |
   | macro avg   |    0.81   |   0.82   |   0.82   | 22264|
| weighted avg    |   0.802  |   0.82    |  0.82   | 22264|

Matthews correlation coefficient: 0.631


# Plots LDA based on codevector 

## only vowels
LDA histogram for unstressed stressed codevectors
<img width="598" alt="Screenshot 2024-01-17 at 18 17 15" src="https://github.com/martijnbentum/E2ELD-cautious-fiesta/assets/19554953/e500b063-1dc1-4975-9e31-08012f6f42da">

Scatterplot with random jitter on y-axis and ld1 score on x axis
<img width="599" alt="Screenshot 2024-01-17 at 18 16 38" src="https://github.com/martijnbentum/E2ELD-cautious-fiesta/assets/19554953/fb2a14db-f67a-425e-b30c-d44fbd5c68e4">

## all phonemes (vowels & consonants)

LDA histogram for unstressed stressed codevectors
<img width="596" alt="Screenshot 2024-01-17 at 16 35 49" src="https://github.com/martijnbentum/E2ELD-cautious-fiesta/assets/19554953/82cdd609-6262-481a-a29d-b05e2ca0a59d">

Scatterplot with random jitter on y-axis and ld1 score on x axis
<img width="587" alt="Screenshot 2024-01-17 at 16 35 59" src="https://github.com/martijnbentum/E2ELD-cautious-fiesta/assets/19554953/c65ff7d9-2687-4100-ab89-654d57b0e958">

