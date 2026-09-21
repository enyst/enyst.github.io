#!/usr/bin/env python3
"""Offline follow-up: distinguish confidence signals; no calibration fit or API call."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
rows = json.loads((ROOT / 'results.json').read_text())['runs']
binary = []
for row in rows:
    for name, answer in row['response']['answers'].items():
        if answer['type'] != 'choice' or len(answer['probabilities']) != 2:
            continue
        top = max(answer['probabilities'].values())
        binary.append({'case': row['case']['id'], 'question': name,
                       'top_probability': top, 'api_confidence': answer['confidence'],
                       'absolute_formula_gap': abs(answer['confidence'] - (2 * top - 1))})
# Replay the pinned author's bin-boundary expression on a diagnostic pair.
# This is not a recalculation of their full dataset or fitted calibrators.
scores, labels = [0.0, 1.0], [1, 1]
def ece(include_zero):
    total = 0.0
    for index in range(10):
        lo, hi = index / 10, (index + 1) / 10
        members = [i for i, p in enumerate(scores)
                   if (lo < p <= hi) or (include_zero and index == 0 and p == 0)]
        if members:
            prediction = sum(scores[i] for i in members) / len(members)
            observed = sum(labels[i] for i in members) / len(members)
            total += len(members) / len(scores) * abs(prediction - observed)
    return total
report = {'source_revision': '9788ecc5526b32da9fa9b9b38964586060677c77',
          'new_api_calls': 0, 'binary_choice_count': len(binary),
          'max_absolute_formula_gap': max(x['absolute_formula_gap'] for x in binary),
          'binary_choices': binary,
          'ece_boundary_diagnostic': {'scores': scores, 'labels': labels,
              'original_open_left_bins': ece(False), 'zero_inclusive_first_bin': ece(True)},
          'scope': 'Saved-answer inspection and isolated metric boundary check; no OpenHands calibration claim.'}
assert len(binary) == 12
assert report['max_absolute_formula_gap'] <= .0100001
assert ece(False) == 0 and ece(True) == .5
(ROOT / 'confidence-inspection.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({k:v for k,v in report.items() if k != 'binary_choices'}, indent=2))
