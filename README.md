# Restored *Qieyun* and other data from Fujita (2017)

## Source

- Thesis (2017)
  - [Official page](https://nishogakusha.repo.nii.ac.jp/records/2623)
  - [Full text](https://core.ac.uk/works/67634077/)
- Monograph (2023)
  - [Official page](https://www.kohbun.co.jp/%e8%aa%9e%e5%ad%a6%e3%83%bb%e6%96%87%e5%ad%a6%e7%a0%94%e7%a9%b6/%e9%96%8b%e7%af%87%e3%80%80%e5%96%ae%e5%88%8a%e3%80%80no-18/)
  - The content is identical to the main text of the thesis, and its accompanying CD contains a PDF of the entire thesis

## Process

1. Download the full text PDF (see link above) as `fujita.pdf` in the directory
2. `raw.py`: Extract all text elements in the appendix 切韻表 of `fujita.pdf` to `raw.pkl`
3. `pages.py`: Rebuild the table on each page from `raw.pkl` to `pages.pkl`
4. `lines.py`: Stringify all lines in `pages.pkl` to `fujita-data.csv`. Extract restored *Qieyun* data to `切韻 藤田拓海復元.csv` and `切韻 李永富復元.csv`
5. TODO: Compare two restored versions
