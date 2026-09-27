# YAPPERS_PhamThoaiNhaPhuong_BI10_R01_data

Supporting files for the slide deck `YAPPERS_PhamThoaiNhaPhuong_BI10_R01.pptx` (BI10 Round 01, Group YAPPERS).

| Path | What it is |
|---|---|
| `notebook/full_pipeline.ipynb` | Full analysis (data checks, Tasks 1–5), saved with outputs. Every number on the slides is printed here; its appendix draws every deck chart. |
| `data/task4_features.csv` | Task 4 preprocessed dataset: 999 customers × 23 columns (features, z-scaled model inputs, cluster, segment). |
| `data/data_dictionary_task4.md` | Column definitions for `task4_features.csv`. |
| `figures/deck_*.png` | The 21 charts used in the deck. |
| `scripts/full_pipeline_src.py` | Source of the notebook (percent-format cells). |
| `scripts/py2nb.py` | Converts the source into the notebook. |
| `scripts/build_deck.js` | Builds the deck from the charts (Node + pptxgenjs). |

## How to reproduce
1. Open `notebook/full_pipeline.ipynb` in Google Colab and choose **Runtime → Run all** (about 3–4 minutes). The notebook downloads the two datasets from public Google Drive links; no token or extra package is needed.
2. The charts are written to `outputs/figures/deck_*.png` and `task4_features.csv` to the working directory.

`financial_health_score` is used as a wellbeing indicator only: never to approve or deny credit, cut a limit, raise a rate or block an account.
