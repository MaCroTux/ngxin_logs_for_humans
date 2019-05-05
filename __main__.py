import sys
import re
import json
from bcolors import Bcolors

class Data:
    IP = 'ip'
    DATE = 'date'
    SCHEMA = 'schema'
    DOMAIN = 'domain'
    METHOD = 'method'
    ENDPOINT = 'endPoint'
    PROTOCOL = 'protocol'
    STATUS = 'status'
    REFERER = 'referer'
    AGENT = 'agent'
    GA = 'GA'


def read_line():

    try:
        line_read = sys.stdin.readline()

        if not line_read:
            print('End revice data')
            return False

        return line_read
    except KeyboardInterrupt as message:
        print(message)
        return False


def data_format(line_un_format, regex, data_position):
    matches = re.finditer(regex, line_un_format, re.MULTILINE)

    for matchNum, match in enumerate(matches, start=1):
        groups = match.groups()

        return {
            Data.IP: groups[data_position[Data.IP]],
            Data.DATE: groups[data_position[Data.DATE]],
            Data.SCHEMA: groups[data_position[Data.SCHEMA]],
            Data.DOMAIN: groups[data_position[Data.DOMAIN]],
            Data.METHOD: groups[data_position[Data.METHOD]],
            Data.ENDPOINT: groups[data_position[Data.ENDPOINT]],
            Data.PROTOCOL: groups[data_position[Data.PROTOCOL]],
            Data.STATUS: int(groups[data_position[Data.STATUS]]),
            Data.REFERER: groups[data_position[Data.REFERER]],
            Data.AGENT: groups[data_position[Data.AGENT]]
        }

def read_config():

    config_file = open("nginx.json", "r")
    config_data = config_file.read()

    config =json.loads(config_data)

    return config['exp_reg'], config['data_position']


error_404 = 0
error_500 = 0

exp_reg, data_position = read_config()


while True:

    line = read_line()
    group = data_format(line, exp_reg, data_position)

    if not line:
        break

    color = Bcolors.CEND

    if group[Data.STATUS] == 500:
        error_500 += 1
        color = Bcolors.CREDBG

    if group[Data.STATUS] == 404:
        error_404 += 1
        color = Bcolors.CYELLOW2

    if group[Data.STATUS] == 429:
        error_404 += 1
        color = Bcolors.CBLUE

    print(color + (
        " {0:4d} {1:16s} {2:16s} {3:60s} {4:6s} {5:6s} {6:9s}".format(
            group[Data.STATUS],
            group[Data.IP],
            str(group[Data.DATE]),
            ("[" + group[Data.METHOD] + "]" + group[Data.ENDPOINT])[0:58],
            str(error_500) + ' [500]',
            str(error_404) + ' [404]',
            group[Data.REFERER][0:120]
        )) + Bcolors.CEND
    )
