from path_mapping import pathMapping

maxKeyLen = max(map(len, pathMapping.keys()))
maxValLen = max(map(len, pathMapping.values()))

lineFmt = '{:<%d} : {:<%d}' % (maxKeyLen, maxValLen)

allKeys = list(pathMapping.keys())
allKeys.sort()

lines = []

for key in allKeys:
    lines.append(lineFmt.format(key, pathMapping[key]))

with open('all_mapping.txt', 'w') as outfile:
    outfile.write('\n'.join(lines))