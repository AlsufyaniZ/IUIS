# IUIS – IEI Finder

`index.html` is the whole site: a searchable copy of the IUIS 2024 classification of inborn errors of immunity (Poli et al., J Hum Immun 2025).

## Checking the data before each upload

Run:

```
python3 tools/check_genes.py
```

It compares every row embedded in `index.html` with `tools/iuis2024_source_rows.tsv` (all 603 gene rows of Tables I–X, extracted from the published article) and lists any gene that is missing, misspelled or has a different inheritance. It exits with an error if anything is missing, so do not upload until it prints `OK`.

## Gene symbols

Each entry keeps the gene name exactly as printed in the report (`g`) and also stores the current HGNC symbol (`y`) plus older names (`al`). Search matches all of them, so both `TMEM173` and `STING1`, or `TAZ` and `TAFAZZIN`, find the same entry.

New rows added after the first release are appended to the end of the data with an `at` field (the row they follow), so saved entries and gene panels in users' browsers keep pointing at the right rows.

## OMIM numbers

Every entry now shows two numbers where they exist:

* **Gene MIM** – the OMIM gene entry, taken from HGNC (October 2026 release) for the entry's HGNC symbol.
* **Disease MIM** – the OMIM disease entry given in the report (either the IUIS January 2025 version or the published article), checked against OMIM's disease list. Six numbers that pointed to the wrong gene or disease (C1S ×2, STN1, CTC1, PSMB9 ×2) were corrected and the correction is noted on the entry.

When the report gives no disease number, the entry lists the OMIM disorders linked to that gene instead of guessing one. `tools/omim_numbers.tsv` lists every row with both numbers for review.
