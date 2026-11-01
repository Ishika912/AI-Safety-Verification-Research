"""Illustrative ML experiment: same model, different decision threshold.

This is NOT a frontier-AI safety evaluation or proof of deployment identity.
"""
from pathlib import Path
import json
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
from sklearn.model_selection import train_test_split

OUT = Path(__file__).resolve().parent
X, y = make_classification(
    n_samples=1500, n_features=12, n_informative=6, n_redundant=2,
    weights=[0.7, 0.3], class_sep=0.85, flip_y=0.05, random_state=42
)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, stratify=y, random_state=42
)
model = LogisticRegression(max_iter=2000, random_state=42)
model.fit(X_train, y_train)
probabilities = model.predict_proba(X_test)[:, 1]

results = []
for threshold in [0.50, 0.80]:
    predictions = (probabilities >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_test, predictions, labels=[0, 1]).ravel()
    results.append({
        'threshold': threshold,
        'accuracy': round(float(accuracy_score(y_test, predictions)), 4),
        'precision': round(float(precision_score(y_test, predictions, zero_division=0)), 4),
        'recall': round(float(recall_score(y_test, predictions, zero_division=0)), 4),
        'true_positive': int(tp), 'false_positive': int(fp),
        'true_negative': int(tn), 'false_negative': int(fn),
    })

with open(OUT / 'results.json', 'w', encoding='utf-8') as f:
    json.dump({'dataset': 'synthetic sklearn.make_classification',
               'test_samples': len(y_test),
               'same_trained_model': True,
               'results': results}, f, indent=2)

for item in results:
    print(f"Threshold {item['threshold']:.2f}: accuracy={item['accuracy']:.3f}, "
          f"precision={item['precision']:.3f}, recall={item['recall']:.3f}, "
          f"FP={item['false_positive']}, FN={item['false_negative']}")
print('Saved results.json')
