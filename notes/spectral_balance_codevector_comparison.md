Fitted LM with middle codevector and spectral balance value for a given vowel

intercept 0.148 <br>
slope 0.244 <br>
r² 0.049 <br>

Plot of LDA score of codevector (y axis) and LDA score of spectral balance (x axis)

<img width="817" alt="Screenshot 2024-02-06 at 16 21 04" src="https://github.com/martijnbentum/E2ELD-cautious-fiesta/assets/19554953/04c92894-b1f4-4b9f-8c9b-276e5f759e35">

The LM might be influenced by outliers
Check with z transformed values and exclude abs(z-values) > 4

intercept -0.003 <br>
slope 0.233 <br>
r² 0.051 <br>

Very similar results

Plot of LDA score of codevector (y axis) and LDA score of spectral balance (x axis), z-transformed and outliers excluded
<img width="818" alt="Screenshot 2024-02-06 at 16 20 51" src="https://github.com/martijnbentum/E2ELD-cautious-fiesta/assets/19554953/8885270a-6e67-474f-9650-509d281594e7">


OBSOLETE:
There are many codevector values for one spectral balance value.

Fitted a linear model to predict LDA score of codevector based on LDA score of spectral balance


intercept 0.039 <br>
slope 0.174 <br>
r² 0.022 <br>

Plot of LDA score of codevector (y axis) and LDA score of spectral balance (x axis)

![Screenshot 2024-01-23 at 17 53 23](https://github.com/martijnbentum/E2ELD-cautious-fiesta/assets/19554953/5719be07-9bec-4bb2-9636-542a2daace4f)

Current analysis is probably incorrect. For each spectral balance LDA score there are multiple codevectors
because codevectors are based on 25 ms frame and the spectral balance LDA score is based on the whole vowel (see below).

```python
[['summons', 'ʌ', False, 3, -0.003, 6, 1.7276774174408558],
 ['summons', 'ʌ', False, 3, -0.003, 7, 1.898354212485704],
 ['summons', 'ʌ', False, 3, -0.003, 8, 1.52817501315193],
 ['summons', 'ʌ', False, 3, -0.003, 12, 0.051910846940567815],
 ['summons', 'ʌ', False, 3, -0.003, 13, -0.6737850756279639],
 ['summons', 'ʌ', False, 3, -0.003, 14, -1.986818969687019],
 ['exquisite', 'ʌ', False, 7, -0.148, 24, -0.003613077938651399],
 ['exquisite', 'ʌ', False, 7, -0.148, 25, 0.07687753683255541],
 ['exquisite', 'ʌ', False, 7, -0.148, 35, 0.8787741034701082],
 ['exquisite', 'ʌ', False, 7, -0.148, 40, -1.686873829251849],
 ['exquisite', 'ʌ', False, 7, -0.148, 41, -1.686873829251849],
 ['exquisite', 'ʌ', False, 7, -0.148, 42, -1.9302564399858362],
 ['biblical', 'ʌ', False, 6, 0.132, 65, 1.2883139059435091],
 ['biblical', 'ʌ', False, 6, 0.132, 66, 1.794309262815711],
 ['biblical', 'ʌ', False, 6, 0.132, 67, 0.7579546330819888],
 ['biblical', 'ʌ', False, 6, 0.132, 75, -0.9067437455938532],
 ['biblical', 'ʌ', False, 6, 0.132, 76, -0.8722835255072455],
 ['biblical', 'ʌ', False, 6, 0.132, 81, -0.9558569182384546]]
```
