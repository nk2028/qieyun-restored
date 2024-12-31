import pickle
import re

with open('raw.pkl', 'rb') as f:
    pages_raw = pickle.load(f)

# pages > page > line > element
pages = []
for page_idx, page_raw in enumerate(pages_raw):
    pages.append([[]])
    page = pages[-1]
    i = 0
    while not page_raw[i][0]:
        i += 1
    while i < len(page_raw):
        e = page_raw[i]
        if e[0] == '\n':
            page.append([])  # new line
            i += 1
            continue
        # i:   [' 東', 0.0]
        # i+1: ['', 72.96]
        # out: [' 東', 72.96]
        if i + 1 < len(page_raw):
            assert page_raw[i + 1][0] == ''
            e[1] = page_raw[i + 1][1]
        # leading space marks a new cell, but not always reliable, so discard it
        e[0] = e[0].removeprefix(' ')
        if ' ' in e[0] or '\xa0' in e[0]:
            print(page_idx, page[-1][0][0], e)
        e[0] = e[0].replace(' ', '')
        e[0] = e[0].replace('\xa0', '')  # non-breaking space
        if e[0] == '蟼' and e[1] > 80 and page[-1][0][0] == '10330':
            # should be the same element
            page[-1][-1][0] += e[0]
        elif e[0]:
            page[-1].append(e)
        i += 2

# pages > page > line > cell > element
pages = [page[1:] for page in pages]
for page_idx, page in enumerate(pages):
    for line_idx, line in enumerate(page):
        if line_idx == 0:
            col_names = [e[0] for e in line]
            col_xs = [e[1] - 2 for e in line]
            col_xs[1] = 30  # 小韻
            col_xs[2] = 40  # 音類
            col_xs.append(1000)
            page[line_idx] = [[e] for e in line]
            continue
        line_new = [[] for _ in col_names]
        for e in line:
            if not e[1]:
                # the coordinate matrix of the last element of some pages is missing
                col_name = '王二'
                if page_idx == 68:
                    col_name = '王一'
                elif page_idx in (38, 256, 286, 289, 300, 312, 326):
                    col_name = '唐'
                i = col_names.index(col_name)
                print(e[0], '>', col_name, 'in',
                      page_idx, '/', line_idx, 'from', '|'.join(col_names))
            else:
                for i in range(len(col_names)):
                    if e[1] < col_xs[i + 1]:
                        break
            # element misalignment
            if line[0][0] == '8012' and i > 7:
                i = 7
            elif line[0][0] == '10330' and i == 4:
                i = 5
            elif line[0][0] == '16035' and i == 2 and e[0] == '欥':
                i = 3
            line_new[i].append(e)
        for i, cell in enumerate(line_new):
            if i < 3:
                continue
            if cell and cell[0][1] > col_xs[i] + 6:
                # cell that has no 字頭
                cell.insert(0, ['', 0])
        page[line_idx] = line_new


def print_line(page_idx, line_idx):
    line = '|'.join(['-'.join([e[0] for e in cell])
                    for cell in pages[page_idx][line_idx]])
    line = line.replace('\U000E0100', '⁰')
    line = line.replace('\U000E0101', '¹')
    line = line.replace('\U000E0102', '²')
    print(page_idx, '/', line_idx, ':', line)


for page_idx, page in enumerate(pages):
    for line_idx, line in enumerate(page):
        if line_idx == 0:
            continue
        if re.search(r'[\U000E0100-\U000E0102]', str(line)):
            # occurence: 瞢¹ 夢² 丰¹ 龜¹ 甾² 災² 喙² 㒹⁰
            print_line(page_idx, line_idx)
        for cell in line:
            for e in cell:
                e[0] = re.sub(r'[\U000E0100-\U000E0102]', '', e[0])
                assert ' ' not in e[0]
                assert '\xa0' not in e[0]
                assert '-' not in e[0]
                assert ',' not in e[0]
                assert not re.search(r'[\U000E0103-\U000E01EF]', e[0])
                assert not re.search(r'[\uFE00-\uFE0F]', e[0])

for page_idx, page in enumerate(pages):
    for line_idx, line in enumerate(page):
        if line_idx == 0:
            continue
        for i, cell in enumerate(line):
            if i < 3:
                continue
            if \
                    page[0][i][0] in ('廣', '唐', '王二') and len(cell) > 1 or \
                    cell and len(cell[0][0]) > 1:
                print_line(page_idx, line_idx)
                continue

with open('pages.pkl', 'wb') as f:
    pickle.dump(pages, f)
