import os
_thisDir, _ = os.path.split(__file__)
rootDir = os.path.abspath(os.path.split(_thisDir)[0])
pyDir = os.path.join(rootDir, 'python')
svgDir = os.path.join(rootDir, 'svg')