# Restored *Qieyun* and other data from Fujita (2017; 2023)

## Source

- Thesis\
  藤田拓海. 2017. 陸法言『切韻』研究. 東京: 二松学舎大学. (博士学位論文)
  - [Official page](https://nishogakusha.repo.nii.ac.jp/records/2623)
  - [Full text](https://core.ac.uk/works/67634077/)
- Monograph\
  藤田拓海. 2023. 陸法言『切韻』研究 (開篇 單刊 18). 東京: 好文出版.
  - [Official page](https://www.kohbun.co.jp/%e8%aa%9e%e5%ad%a6%e3%83%bb%e6%96%87%e5%ad%a6%e7%a0%94%e7%a9%b6/%e9%96%8b%e7%af%87%e3%80%80%e5%96%ae%e5%88%8a%e3%80%80no-18/)
  - The content is identical to the main text of the thesis, and its accompanying CD contains a PDF of the entire thesis

## Extracted data

- [`fujita-data.csv`](fujita-data.csv): Complete data of the appendix *Qieyun* Table 切韻表
- [`切韻 藤田拓海復元.csv`](切韻%20藤田拓海復元.csv): *Qieyun* 切韻 restored by Fujita Takumi 藤田拓海
- [`切韻 李永富復元.csv`](切韻%20李永富復元.csv): *Qieyun* 切韻 restored by Li Yongfu 李永富
- [`small-rime-diffs.csv`](small-rime-diffs.csv): Differences of the existence of small rimes between the two restored versions
- [`to_tshet_uinh_data/small_rimes.csv`](to_tshet_uinh_data/small_rimes.csv): Small rimes that appear in either version

Phonological position descriptions 音韻地位描述 in [TshetUinh.js](https://github.com/nk2028/tshet-uinh-js) v0.15 format are also added to these files. Corresponding *Guangyun* 廣韻 small rime numbers and phonological position descriptions of *fanqie* 反切 spellers are also added to [`to_tshet_uinh_data/small_rimes.csv`](to_tshet_uinh_data/small_rimes.csv).

## Process

1. Download the full text PDF (see link above) as `fujita.pdf` in the directory
2. `raw.py`: Extract all text elements in the appendix *Qieyun* Table 切韻表 of `fujita.pdf` to `raw.pkl`
3. `pages.py`: Rebuild the table on each page from `raw.pkl` to `pages.pkl`
4. `lines.py`: Stringify all lines in `pages.pkl` to `fujita-data.csv` and extract restored *Qieyun* data to `切韻 藤田拓海復元.csv` and `切韻 李永富復元.csv`
5. `small-rime-diffs.py`: Compare the two restored versions and save to `small-rime-diffs.csv`
6. `to_tshet_uinh_data/small_rimes.py`: Combine small rimes in two versions, extract/add other fields, and generate `to_tshet_uinh_data/small_rimes.csv`

Results of processes 2 to 6 have been deposited into this repo.
