import pickle

tones = '平上去入'
rimes = [
    '東冬鍾江支脂之微魚虞模齊佳皆灰咍眞臻文殷元魂痕寒刪山先仙蕭宵肴豪歌麻覃談陽唐庚耕清青尤侯幽侵鹽添蒸登咸銜嚴凡',
    '董腫講紙旨止尾語麌姥薺蟹駭賄海軫吻隱阮混佷旱潸産銑獮篠小巧晧哿馬感敢養蕩梗耿静迥有厚黝寑琰忝拯等豏檻　范',
    '送宋用絳寘至志未御遇暮泰霽祭卦怪夬隊代廢震問焮願慁恨翰諫襇霰線嘯笑效号箇禡勘闞漾宕敬諍勁徑宥候幼沁豔㮇證嶝陷鑑　梵',
    '屋沃燭覺質物櫛迄月没末黠鎋屑薛錫昔麥陌合盍洽狎葉怗緝藥鐸職德業乏',
]
# thesis: 眞産静没
# nk2028: 真產靜沒
# keep characters as in the thesis

with open('pages.pkl', 'rb') as f:
    pages = pickle.load(f)

lines = []
tone_idx = 0
rime_idx = 0
last_small_rime_id = '1'
for page_idx, page in enumerate(pages):
    col_names = [cell[0][0] for cell in page[0]]
    for line_idx, line in enumerate(page[1:]):
        small_rime_id = line[1][0][0] if line[1] else None
        if small_rime_id == '1' and small_rime_id != last_small_rime_id or line[0][0][0] in ('10902', '10949', '15215'):
            rime_idx += 1
            if \
                    line[-2] and rimes[tone_idx][rime_idx] != line[-2][0][0] or \
                    line[-1] and rimes[tone_idx][rime_idx] != line[-1][0][0]:
                print(tones[tone_idx], rimes[tone_idx][rime_idx] + line[-2][0][0] + line[-1][0][0],
                      '|'.join([''.join([e[0] for e in cell]) for cell in line]))
        last_small_rime_id = small_rime_id

        line_new = [
            str(page_idx + 1),
            str(line_idx + 1),
            tones[tone_idx],
            rimes[tone_idx][rime_idx].replace('　', ''),
        ]
        for i, cell in enumerate(line):
            cell_new = []
            if i < 3:
                cell_new.append(''.join([e[0] for e in cell]))
            else:
                if not cell:
                    continue
                cell_new.append(col_names[i])
                cell_new.append(cell[0][0])
                if len(cell) > 1:
                    cell_new.append(''.join([e[0] for e in cell[1:]]))
            line_new.append('-'.join(cell_new))
        lines.append(line_new)
    if len(page) < 59:
        print(tones[tone_idx], rimes[tone_idx][rime_idx], 'END')
        tone_idx += 1
        rime_idx = 0
        last_small_rime_id = '1'

with open('fujita-data.csv', 'w', encoding='utf-8') as f:
    f.write(','.join(
        ['頁', '行', '聲調', '韻目', '序数', '小韻', '音類'] +
        [''] * (max(len(line) for line in lines) - 4)) + '\n')
    for line in lines:
        f.write(','.join(line) + '\n')

for filename, prefix in [
    ('切韻 藤田拓海復元.csv', '本稿推定-'),
    ('切韻 李永富復元.csv', '李永富[1973]推定-'),
]:
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(','.join(
            ['頁', '行', '聲調', '韻目', '序数', '小韻', '音類', '字頭', '釋義']) + '\n')
        for line in lines:
            flag = False
            for cell in line:
                if cell.startswith(prefix):
                    flag = True
                    break
            if flag:
                f.write(','.join(line[:7] + cell.split('-')[1:]) + '\n')
