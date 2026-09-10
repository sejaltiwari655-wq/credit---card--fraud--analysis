# Fraud Detection Model Report

Train size: 199,364 | Test size: 85,443
Fraud in train: 344 | Fraud in test: 148


## Logistic Regression (class_weight=balanced)

- ROC-AUC: **0.9680**
- PR-AUC (average precision): **0.7041**

Confusion matrix (rows = actual, cols = predicted):

```
[[83485  1810]
 [   18   130]]
```

```
              precision    recall  f1-score   support

       Legit       1.00      0.98      0.99     85295
       Fraud       0.07      0.88      0.12       148

    accuracy                           0.98     85443
   macro avg       0.53      0.93      0.56     85443
weighted avg       1.00      0.98      0.99     85443

```


## Random Forest (class_weight=balanced)

- ROC-AUC: **0.9655**
- PR-AUC (average precision): **0.7895**

Confusion matrix (rows = actual, cols = predicted):

```
[[85278    17]
 [   37   111]]
```

```
              precision    recall  f1-score   support

       Legit       1.00      1.00      1.00     85295
       Fraud       0.87      0.75      0.80       148

    accuracy                           1.00     85443
   macro avg       0.93      0.87      0.90     85443
weighted avg       1.00      1.00      1.00     85443

```
