# Strict separation for the noisy-GHZ witness

The note answers the equality question in Xu et al., arXiv:2211.05563v1,
Section 4.2, page 12. For every party count and local dimension at least three,
it gives a noise probability with a strict gap between the optimized
single-witness bound and the convex-roof geometric measure relative to
biseparable states. At three qutrits and noise 3/8, the witness bound is exactly
1/9 and the convex roof is at least 13/108.

## Files and reconstruction

- `note.tex` is the complete main source, including its bibliography.
- `note.pdf` is the typeset note.
- `verify.py` requires Python 3.9 or later and only the standard library.
- `verification.json` contains its exact rational and finite-enumeration results.
- `metadata.json` identifies the note, creators, license, and original problem.

Build with Tectonic 0.17.0:

```sh
tectonic note.tex
```

Alternatively, use a standard TeX installation:

```sh
pdflatex note.tex
pdflatex note.tex
```

The bibliography is embedded; BibTeX and external data files are unnecessary.
Reproduce the finite arithmetic checks with:

```sh
python3 verify.py --output verification.json
```

## Mathematical coverage

Theorem 1 proves the strict separation for all n,d >= 3 in writing.
Corollary 1 proves strict separation for three qutrits throughout
27/74 < p < 9/22. The exact value of the convex roof is not asserted.

The pinned Lean source is
https://github.com/the-omega-institute/trureturing/blob/cc684e6326490f9173bfefcadb0294ee6ccbb0b5/D5/S3/Quantum/Entanglement/Witness/NoisyGhzWitnessBoundGap.lean .
Its `D5.S3.Quantum.Entanglement.Witness.NoisyGhzWitnessBoundGap.result`
states that the universal equality is false. Its proof uses the bounds
epsilon <= 1/9 and E_G >= 13/108 at n=d=3 and p=3/8.
The equality epsilon=1/9, the general all-parameter result, and the noise
interval are written proofs in the note. The Python program independently
checks rational matrix identities at the base example, support ranks for
3 <= d <= 5 and 3 <= n <= 6, and scalar identities for 3 <= d <= 40 and
3 <= n <= 12; those finite checks are not substituted for the general proof.

## Creators and license

1. Haobo Ma — ChronoAI Pte Ltd, Singapore.
2. Wenlin Zhang — National University of Singapore; ChronoAI Pte Ltd, Singapore.

CC BY 4.0 (`cc-by-4.0`).
