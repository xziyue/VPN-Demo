from path_mapping import pathMapping, check_path_mapping_integrity
from rel_path import *
import json

check_path_mapping_integrity()


class VPNStep():

    def __init__(self):
        self.arrowStyles = dict()
        self.packetLayers = []
        self.packetHovers = []
        self.description = ''

        for key, val in pathMapping.items():
            self.arrowStyles[val] = 'arrow-normal'


    def set_arrow_emph(self, name):
        assert name in pathMapping
        self.arrowStyles[pathMapping[name]] = 'arrow-emph'

    def prepend_packet_layer(self, layerName, layerHover):
        self.packetLayers.insert(0, layerName)
        self.packetHovers.insert(0, layerHover)

    def set_description(self, des):
        self.description = des

    def get_js(self, stepNum = 1, joinChar='\n'):
        jsLines = []

        # set arrow format
        arrowFmt = 'ssc(\"{}\", \"{}\");'
        for key, val in self.arrowStyles.items():
            jsLines.append(arrowFmt.format(key, val))

        # set description text
        if isinstance(self.description, str):
            jsLines.append(
                'document.getElementById(\"{}\").innerHTML={};'.format('des-text', escape_javascript(escape(self.description)))
            )
        elif isinstance(self.description, list):
            lstFmt = '<ul>{}</ul>'
            itemFmt = '<li>{}</li>'
            lstItems = []
            for item in self.description:
                lstItems.append(itemFmt.format(escape(item)))
            lstStr = lstFmt.format(''.join(lstItems))
            jsLines.append(
                'document.getElementById(\"{}\").innerHTML={};'.format('des-text', escape_javascript(lstStr))
            )

        # update packet detail
        packetTableFmt = '<table class="packet-table">{}</table>'
        packetRowFmt = '<tr><td>{}</td></tr>'
        packetTextFmt1 = '<div class="tooltip dotted-bottom">{}</div>'
        packetTextFmt2 = '<div class="tooltip">{}</div>'
        packetHoverFmt = '<span class="tooltiptext">{}</span>'

        tableRows = []
        for i in range(len(self.packetLayers)):
            packetText = escape(self.packetLayers[i])
            if len(self.packetHovers[i]) > 0:
                packetText += packetHoverFmt.format(escape(self.packetHovers[i]))
                row = packetRowFmt.format(packetTextFmt1.format(packetText))
            else:
                row = packetRowFmt.format(packetTextFmt2.format(packetText))
            tableRows.append(row)
        table = packetTableFmt.format(''.join(tableRows))

        jsLines.append(
            'document.getElementById(\"{}\").innerHTML={};'.format('packet-text', escape_javascript(table))
        )

        # update step number
        jsLines.append(
            'document.getElementById(\"{}\").innerHTML=\"{}\";'.format('step-text', 'Step {}'.format(stepNum))
        )

        # set height
        jsLines.append(
            'setDesHeight();'
        )

        return joinChar.join(jsLines)


allSteps = []

def escape_javascript(literal):
    jsonStr = json.dumps({"scr" : literal})
    jsonStr = jsonStr.lstrip('{').rstrip('}')
    colonLoc = jsonStr.find(':')
    return jsonStr[colonLoc + 1 :].strip()

def escape(txt):
    html_escape_table = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;",
        ">": "&gt;",
        "<": "&lt;",
        '\n' : '<br>'
    }
    return ''.join(html_escape_table.get(c, c) for c in txt)

def generate_javascript():
    jsTemplate = r'''

function init_vpn() {{
    if(!localStorage.getItem("vpn-state")){{
        localStorage.setItem("vpn-state", "0");
        set_vpn_state(0);
    }}else{{
        var step = get_vpn_step();
        set_vpn_state(step);
    }}
}}

// set svg class
function ssc(id, clsVal){{
    document.getElementById(id).className.baseVal=clsVal;
}}

function get_num_vpn_steps() {{
    return {numSteps:};
}}

function get_vpn_step() {{
    var strStep = localStorage.getItem("vpn-state");
    var step = parseInt(strStep);
    return step;
}}

function set_vpn_step(step) {{
    if (step < 0 || step >= get_num_vpn_steps()){{
        console.log("invalid step");
        return false;
    }} else{{
        localStorage.setItem("vpn-state", step.toString());
        return true;
    }}
}}

var vpn_commands = [
{vpnCmd:}
];

function set_vpn_state(step){{
    if(set_vpn_step(step)){{
        eval(vpn_commands[step]);
    }}
}}

function test_vpn_function() {{
{testFunc:}
}}
'''

    vpnCmd = ',\n'.join([escape_javascript(step.get_js(ind + 1, '')) for ind, step in enumerate(allSteps)])

    js = jsTemplate.format(
        numSteps = len(allSteps),
        vpnCmd = vpnCmd,
        testFunc = allSteps[0].get_js(1)
    )

    with open(os.path.join(rootDir, 'vpn-cmd.js'), 'w') as outfile:
        outfile.write(js)

    return js

# 1
step = VPNStep()
step.set_arrow_emph('mach-user-up-sock-out')
step.set_arrow_emph('mach-user-us-2-ps')
step.prepend_packet_layer('Data', '')
step.set_description('User program tries to use telnet service on the Machine in Private Network. '
                      'It sends a TCP packet to port 23 of the target machine.')
allSteps.append(step)

# 2
step = VPNStep()
step.set_arrow_emph('mach-user-ps-2-r')
step.set_arrow_emph('mach-user-r-2-tun')
step.prepend_packet_layer('Data', '')
step.prepend_packet_layer('UDP', 'src port=56630\ndst port=23')
step.prepend_packet_layer('IP', 'src IP=10.0.5.56\ndst IP=10.0.1.3')
step.set_description([
    'The protocol stack adds UDP header and IP header to the packet.',
    'Based on the routing table, the packet is routed to the tun interface. Therefore, the source IP is '
    '10.0.5.56.'
])
allSteps.append(step)

# 3
step = VPNStep()
step.set_arrow_emph('mach-user-vp-tun-in')
step.set_arrow_emph('mach-user-vp-sock-out')
step.set_arrow_emph('mach-user-us-2-ps')
step.set_arrow_emph('mach-user-ps-2-r')
step.prepend_packet_layer('Data', '')
step.prepend_packet_layer('TCP', 'src port=56630\ndst port=23')
step.prepend_packet_layer('IP', 'src IP=10.0.5.56\ndst IP=10.0.1.3')
step.prepend_packet_layer('UDP', 'src port=56632\n\dst port=1194')
step.prepend_packet_layer('IP', '')
step.set_description([
    'The VPN program receives the packet from tun interface. Using the old packet as payload, '
    'the new packet is sent to VPN server\'s IP address and VPN service port number.',
    'Usually, the payload is encrypted to prevent eavesdropping. For demonstration purposes, '
    'this security measure is not performed.'
])
allSteps.append(step)

# 4
step = VPNStep()
step.set_arrow_emph('mach-user-r-2-eth0')
step.set_arrow_emph('nwk-user-2-vs')
step.prepend_packet_layer('Data', '')
step.prepend_packet_layer('TCP', 'src port=56630\ndst port=23')
step.prepend_packet_layer('IP', 'src IP=10.0.5.56\ndst IP=10.0.1.3')
step.prepend_packet_layer('UDP', 'src port=56632\ndst port=1194')
step.prepend_packet_layer('IP', 'src IP=67.244.154.12\ndst IP=128.230.84.25')
step.set_description([
    'The routing table decides that the packet should go through eth0. Therefore, '
    'the source IP of the packet is 67.244.154.12.',
    'The packet is sent to the Internet and eventually reaches the VPN server.'
])
allSteps.append(step)

# 5
step = VPNStep()
step.set_arrow_emph('mach-vs-eth0-2-r')
step.set_arrow_emph('mach-vs-r-2-ps')
step.set_arrow_emph('mach-vs-ps-2-us')
step.set_arrow_emph('mach-vs-vp-sock-in')
step.prepend_packet_layer('Data', '')
step.prepend_packet_layer('TCP', 'src port=56630\ndst port=23')
step.prepend_packet_layer('IP', 'src IP=10.0.5.56\ndst IP=10.0.1.3')
step.set_description([
    'Since the packet is intended to reach this machine\'s IP address, it is passed to '
    'the protocol stack.',
    'Based on the dst port number, the payload of the packet is passed to the VPN program.',
    'The VPN program will perform integrity check and decryption over the payload to retrieve '
    'the original packet.'
])
allSteps.append(step)

# 6
step = VPNStep()
step.set_arrow_emph('mach-vs-vp-tun-out')
step.set_arrow_emph('mach-vs-tun-2-r')
step.set_arrow_emph('mach-vs-r-2-eth1')
step.set_arrow_emph('nwk-vs-2-mpn')
step.prepend_packet_layer('Data', '')
step.prepend_packet_layer('TCP', 'src port=56630\ndst port=23')
step.prepend_packet_layer('IP', 'src IP=10.0.5.56\ndst IP=10.0.1.3')
step.set_description([
    'The VPN program writes the packet to the tun interface.',
    'The tun interface passes the packet to the kernel for routing. Based on the '
    'dst IP address, the packet goes out through eth1.',
    'The packet is put into internal network and reaches Machine in Private Network.'
])
allSteps.append(step)


# 7
step = VPNStep()
step.set_arrow_emph('mach-mpn-eth0-2-r')
step.set_arrow_emph('mach-mpn-r-2-ps')
step.set_arrow_emph('mach-mpn-ps-2-us')
step.set_arrow_emph('mach-mpn-up-sock-in')
step.prepend_packet_layer('Data', '')
step.set_description([
    'Since the packet is intended to reach this machine\'s IP address, it is passed to '
    'the protocol stack.',
    'Based on the dst port number, the payload of the packet is passed to the user program. '
    'In this case, it is the telnet server.'
])
allSteps.append(step)


print(generate_javascript())