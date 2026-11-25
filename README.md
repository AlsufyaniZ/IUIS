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
