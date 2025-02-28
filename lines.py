import pickle

tones = '平上去入'
rimes = [
    '東冬鍾江支脂之微魚虞模齊佳皆灰咍眞臻文殷元魂痕寒刪山先仙蕭宵肴豪歌麻覃談陽唐庚耕清青尤侯幽侵鹽添蒸登咸銜嚴凡',
    '董腫講紙旨止尾語麌姥薺蟹駭賄海軫吻隱阮混佷旱潸産銑獮篠小巧晧哿馬感敢養蕩梗耿静迥有厚黝寑琰忝拯等豏檻　范',
    '送宋用絳寘至志未御遇暮泰霽祭卦怪夬隊代廢震問焮願慁恨翰諫襇霰線嘯笑效号箇禡勘闞漾宕敬諍勁徑宥候幼沁豔㮇證嶝陷鑑　梵',
    '屋沃燭覺質物櫛迄月没末黠鎋屑薛錫昔麥陌合盍洽狎葉怗緝藥鐸職德業乏',
]
rimes_aligned = [
    '東冬鍾江支脂之微魚虞模齊　　佳皆　灰咍　眞臻文殷元魂痕寒刪山先仙蕭宵肴豪歌麻陽唐庚耕清青蒸登尤侯幽侵覃談鹽添咸銜嚴凡',
    '董｜腫講紙旨止尾語麌姥薺　　蟹駭　賄海　軫｜吻隱阮混佷旱潸産銑獮篠小巧晧哿馬養蕩梗耿静迥拯等有厚黝寑感敢琰忝豏檻　范',
    '送宋用絳寘至志未御遇暮霽祭泰卦怪夬隊代廢震｜問焮願慁恨翰諫襇霰線嘯笑效号箇禡漾宕敬諍勁徑證嶝宥候幼沁勘闞豔㮇陷鑑　梵',
    '屋沃燭覺　　　　　　　　　　　　　　　　質櫛物迄月没｜末鎋黠屑薛　　　　　　藥鐸陌麥昔錫職德　　　緝合盍葉怗洽狎業乏',
]
# fujita: 眞産静没
# nk2028: 真產靜沒
# keep characters as in Fujita, except in 音韻地位描述
rime_to_韻 = {}
for e in zip(*rimes_aligned):
    韻 = e[0].replace('眞', '真').replace('　', e[2])
    for rime in e:
        if rime != '　' and rime != '｜':
            rime_to_韻[rime] = 韻
聲母to母 = dict(zip('非敷奉微娘群羊', '幫滂並明孃羣以'))
等類to等 = dict(zip('1234ABC', '一二三四三三三'))
等類to類 = dict(zip('1234ABC', [''] * 4 + ['A', 'B', 'C']))
fujita_desc_err = {
    ('平', '眞', '匣A開'),  # 礥
    ('平', '幽', '生3'),  # 犙
    ('去', '霽', '徹3開'),  # 𥱻
}
nk2028_desc_patch = {
    '云合一歌平': '匣合一歌平',  # 㗻
    '端開二佳上': '知開二佳上',  # 𢖇
    '云合一灰上': '云合三C廢上',  # 倄
    '端開三庚上': '端開二庚上',  # 打
    '來開三庚上': '來開二庚上',  # 冷
    '初開三清上': '初開三庚上',  # 涇
    '定開三脂去': '定開四脂去',  # 地
    '影二山入': '影開二山入',  # 穵
    '日開二刪入': '孃開二刪入',  # 𩭿
    '幫三B清入': '幫三B庚入',  # 碧
    '幫三B耕入': '幫三B庚入',  # 碧
    '並三B耕入': '並三B庚入',  # 欂
}
compatibility_patch = dict(zip(
    '靈僧節練器兀都突貫海鶴隆梅視逸穀屮著練謁塚喝臭謹',
    '靈僧節練器兀都突貫海鶴隆梅視逸穀屮著練謁塚喝臭謹',
))


def fujita_tuple_to_nk2028_desc(fujita_tuple):
    if fujita_tuple in fujita_desc_err:
        return ''
    聲 = fujita_tuple[0]
    韻 = rime_to_韻.get(fujita_tuple[1], '嚴')
    母 = 聲母to母.get(fujita_tuple[2][0], fujita_tuple[2][0])
    等 = 等類to等[fujita_tuple[2][1]]
    類 = 等類to類[fujita_tuple[2][1]]
    呼 = fujita_tuple[2][2:]
    if 母 in '幫滂並明':
        韻 = 韻.replace('咍', '灰')  # 𤗏啡䆀俖倍䆀
    else:
        韻 = 韻.replace('凡', '嚴')  # 凵劒欠俺猲
        if not 呼:
            if 韻 in '之魚咍臻殷痕蕭宵肴豪幽侵覃談鹽添咸銜嚴':
                呼 = '開'
            elif 韻 in '虞灰文魂凡':
                呼 = '合'
        if 呼 == '開':
            韻 = 韻.replace('魂', '痕')  # 麧
            if 母 in '莊初崇生俟':
                韻 = 韻.replace('真', '臻')  # 櫬㓼𪗨
                韻 = 韻.replace('殷', '臻')  # 齔
    if 等 == '三':
        韻 = 韻.replace('冬', '鍾')  # 恭蜙樅
        韻 = 韻.replace('齊', '祭')  # 臡栘
        韻 = 韻.replace('咍', '廢')  # 茝
        if not 類 and 母 in '幫滂並明見溪羣疑影曉匣云':
            if 韻 in '東鍾之微魚虞廢殷元文歌陽尤嚴凡':
                類 = 'C'
            elif 母 == '云':
                類 = 'B'
            elif 韻 == '蒸':
                類 = 'C'
    else:
        韻 = 韻.replace('鍾', '冬')  # 湩𪁪
    nk2028_desc = ''.join([母, 呼, 等, 類, 韻, 聲])
    if nk2028_desc in nk2028_desc_patch:
        nk2028_desc = nk2028_desc_patch[nk2028_desc]
    return nk2028_desc


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
            None,  # 音韻地位描述
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
        line_new[2] = fujita_tuple_to_nk2028_desc((
            line_new[3], line_new[4], line_new[7],
        ))
        for i, cell in enumerate(line_new):
            for pair in compatibility_patch.items():
                cell = cell.replace(*pair)
            line_new[i] = cell
        lines.append(line_new)
    if len(page) < 59:
        print(tones[tone_idx], rimes[tone_idx][rime_idx], 'END')
        tone_idx += 1
        rime_idx = 0
        last_small_rime_id = '1'

# import re
# for line in lines:
#     for cell in line:
#         for match in re.findall(r'[\uF900-\uFAFF\U0002F800-\U0002FA1F]', cell):
#             print(match, line)

with open('fujita-data.csv', 'w', encoding='utf-8') as f:
    f.write(','.join(
        ['頁', '行', '音韻地位描述', '聲調', '韻目', '序数', '小韻', '音類'] +
        [''] * (max(len(line) for line in lines) - 5)) + '\n')
    for line in lines:
        f.write(','.join(line) + '\n')

for filename, prefix in [
    ('切韻 藤田拓海復元.csv', '本稿推定-'),
    ('切韻 李永富復元.csv', '李永富[1973]推定-'),
]:
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(','.join(
            ['頁', '行', '音韻地位描述', '聲調', '韻目', '序数', '小韻', '音類', '字頭', '釋義']) + '\n')
        for line in lines:
            flag = False
            for cell in line:
                if cell.startswith(prefix):
                    flag = True
                    break
            if flag:
                f.write(','.join(line[:8] + cell.split('-')[1:]) + '\n')
