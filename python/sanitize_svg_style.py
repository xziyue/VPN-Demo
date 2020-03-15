from rel_path import *
from path_mapping import pathMapping, check_path_mapping_integrity


doc = check_path_mapping_integrity()

# convert svg styles for paths into css
targetIds = [val for key, val in pathMapping.items()]

svgNode = doc.getElementsByTagName('svg')[0]

# modify svg width and height for web
svgNode.setAttribute('height', '100%')
svgNode.setAttribute('width', '100%')

# get the style of arrows
paths = doc.getElementsByTagName('path')

arrowNormalItems = []

for path in paths:
    if path.getAttribute('id') in targetIds:

        # create public style
        if len(arrowNormalItems) == 0:
            for item in path.getAttribute('style').split(';'):
                item = item.strip()
                if len(item) > 0:
                    l, r = item.split(':')
                    if l.strip() != 'marker-end':
                        arrowNormalItems.append(item)

        # parse old style
        pathStyle = path.getAttribute('style')

        marker = None
        for item in pathStyle.split(';'):
            item = item.strip()
            if len(item) > 0:
                l, r = item.split(':')
                if l.strip() == 'marker-end':
                    marker = item

        # modify style
        path.removeAttribute('style')
        path.setAttribute('class', 'arrow-normal')
        if marker is not None:
            path.setAttribute('style', marker)
            print(marker)

# normal styles
arrowNormal = '.arrow-normal {{ {} }}'.format(';'.join(arrowNormalItems) + ';')

# emph styles
arrowEmphItems = []
for item in arrowNormalItems:
    if not 'dash' in item:
        arrowEmphItems.append(item)

arrowEmph = '.arrow-emph {{ {} }}'.format(';'.join(arrowEmphItems) + ';')



styleNode = doc.createElement('style')
styleNodeText = doc.createTextNode('\n'.join([arrowNormal, arrowEmph]))
styleNode.appendChild(styleNodeText)

defs = doc.getElementsByTagName('defs')[0]
svgNode.insertBefore(styleNode, doc.getElementsByTagName('defs')[0])

with open(os.path.join(rootDir, 'diagram-css.svg'), 'w') as outfile:
    outfile.write(doc.toxml())
