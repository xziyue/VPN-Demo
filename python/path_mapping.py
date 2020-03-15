from rel_path import *

_userMachine = {
    'up-sock-out' : 'path907',
    'up-sock-in' : 'path907-2',
    'vp-sock-out' : 'path907-0',
    'vp-sock-in' : 'path907-2-9',
    'vp-tun-out' : 'path907-0-2',
    'vp-tun-in' : 'path907-2-9-6',
    'us-2-ps' : 'path1342',
    'ps-2-us' : 'path1342-2',
    'ps-2-r' : 'path907-03',
    'r-2-ps' : 'path907-2-6',
    'r-2-eth0' : 'path907-0-2-9',
    'eth0-2-r' : 'path907-2-9-6-4',
    'r-2-tun' : 'path1342-2-1',
    'tun-2-r' : 'path1342-6'
}


_vpnServer = {
    'vp-sock-out': 'path907-0-7',
    'vp-sock-in': 'path907-2-9-1',
    'vp-tun-out': 'path907-0-2-2',
    'vp-tun-in': 'path907-2-9-6-6',
    'us-2-ps': 'path1342-1',
    'ps-2-us': 'path1342-2-7',
    'ps-2-r': 'path907-03-9',
    'r-2-ps': 'path907-2-6-7',
    'r-2-eth0': 'path907-0-2-9-1',
    'eth0-2-r': 'path907-2-9-6-4-5',
    'r-2-tun': 'path1342-2-1-1',
    'tun-2-r': 'path1342-6-7',
    'r-2-eth1' : 'path907-2-9-6-4-5-1',
    'eth1-2-r' : 'path907-0-2-9-1-8'
}

_machineInNetwork = {
    'up-sock-out' : 'path907-4-8',
    'up-sock-in' : 'path907-2-8-9',
    'us-2-ps' : 'path1342-1-3',
    'ps-2-us' : 'path1342-2-7-0',
    'ps-2-r' : 'path907-03-9-5',
    'r-2-ps' : 'path907-2-6-7-4',
    'r-2-eth0' : 'path907-0-2-9-1-9',
    'eth0-2-r' : 'path907-2-9-6-4-5-2'
}

pathMapping = {
    'nwk-user-2-vs' : 'path907-0-2-9-1-1-9',
    'nwk-vs-2-user' : 'path907-0-2-9-1-1',
    'nwk-vs-2-mpn' : 'path907-2-9-6-4-5-1-8',
    'nwk-mpn-2-vs' : 'path907-2-9-6-4-5-1-8-1'
}

for key, val in _userMachine.items():
    pathMapping['mach-user-' + key] = val

for key, val in _vpnServer.items():
    pathMapping['mach-vs-' + key] = val

for key, val in _machineInNetwork.items():
    pathMapping['mach-mpn-' + key] = val

def check_path_mapping_integrity():
    from xml.dom import minidom

    # make sure there is no duplicated name
    names = dict()
    for key, val in pathMapping.items():
        if val in names:
            raise RuntimeError('duplicated path name \"{}\" for key \"{}\" and \"{}\"'.format(
                val, names[val], key
            ))
        else:
            names[val] = key

    # make sure every path name exists in the svg

    with open(os.path.join(svgDir, 'diagram-plain.svg'), 'rb') as infile:
        svg = infile.read()

    doc = minidom.parseString(svg)

    pathIds = [path.getAttribute('id') for path in doc.getElementsByTagName('path')]

    for key, val in pathMapping.items():
        if val not in pathIds:
            raise RuntimeError('unable to find path name \"{}\" for key \"{}\"'.format(val, key))

    return doc