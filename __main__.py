import sys
import re
import json

class bcolors:

    CEND = '\33[0m'
    CBOLD = '\33[1m'
    CITALIC = '\33[3m'
    CURL = '\33[4m'
    CBLINK = '\33[5m'
    CBLINK2 = '\33[6m'
    CSELECTED = '\33[7m'

    CBLACK = '\33[30m'
    CRED = '\33[31m'
    CGREEN = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE = '\33[34m'
    CVIOLET = '\33[35m'
    CBEIGE = '\33[36m'
    CWHITE = '\33[37m'

    CBLACKBG = '\33[40m'
    CREDBG = '\33[41m'
    CGREENBG = '\33[42m'
    CYELLOWBG = '\33[43m'
    CBLUEBG = '\33[44m'
    CVIOLETBG = '\33[45m'
    CBEIGEBG = '\33[46m'
    CWHITEBG = '\33[47m'

    CGREY = '\33[90m'
    CRED2 = '\33[91m'
    CGREEN2 = '\33[92m'
    CYELLOW2 = '\33[93m'
    CBLUE2 = '\33[94m'
    CVIOLET2 = '\33[95m'
    CBEIGE2 = '\33[96m'
    CWHITE2 = '\33[97m'

    CGREYBG = '\33[100m'
    CREDBG2 = '\33[101m'
    CGREENBG2 = '\33[102m'
    CYELLOWBG2 = '\33[103m'
    CBLUEBG2 = '\33[104m'
    CVIOLETBG2 = '\33[105m'
    CBEIGEBG2 = '\33[106m'
    CWHITEBG2 = '\33[107m'


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
            print('Flujo de datos cortado')
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

    color = bcolors.CEND

    if group[Data.STATUS] == 500:
        error_500 += 1
        color = bcolors.CREDBG

    if group[Data.STATUS] == 404:
        error_404 += 1
        color = bcolors.CYELLOW2

    if group[Data.STATUS] == 429:
        error_404 += 1
        color = bcolors.CBLUE

    print(color + (
        " {0:4d} {1:16s} {2:16s} {3:60s} {4:6s} {5:6s} {6:9s}".format(
            group[Data.STATUS],
            group[Data.IP],
            str(group[Data.DATE]),
            ("[" + group[Data.METHOD] + "]" + group[Data.ENDPOINT])[0:58],
            str(error_500) + ' [500]',
            str(error_404) + ' [404]',
            group[Data.REFERER][0:120]
        )) + bcolors.CEND
    )
