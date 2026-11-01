# Synthetic decision-threshold demonstration

Train one logistic-regression classifier on a reproducibly generated 1,500-row synthetic dataset, then evaluate the same fitted model and held-out test set at thresholds 0.50 and 0.80.

```bash
python -m pip install -r requirements.txt
python experiment.py
```

Results are in `results.json`. Figures in `figures/` illustrate false-positive/false-negative counts and the precision-recall tradeoff. The experiment is **illustrative only** and is not empirical validation of the frontier AI correspondence framework.
