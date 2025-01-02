with open('fujita-data.csv', encoding='utf-8') as f:
    next(f)
    lines = [line.strip().split(',') for line in f]

for i in range(len(lines) - 1):
    if lines[i][6] and lines[i + 1][6] and lines[i][6] == lines[i + 1][6] and lines[i][4] != '拯':
        assert lines[i][7] == lines[i + 1][7]

prefixes = ['本稿推定', '李永富[1973]推定']
small_rimes = [set(), set()]
for line in lines:
    for i, prefix in enumerate(prefixes):
        if any(cell for cell in line if cell.startswith(prefix)):
            small_rimes[i].add((line[4], line[6], line[7]))

diffss = [
    small_rimes[0] - small_rimes[1],
    small_rimes[1] - small_rimes[0],
]
with open('small-rime-diffs.csv', 'w', encoding='utf-8') as f:
    for diffs in diffss:
        for line in lines:
            if (line[4], line[6], line[7]) in diffs:
                f.write(','.join(line) + '\n')
