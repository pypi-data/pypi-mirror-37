"""Energy Control Modules Add-ons
"""

from __future__ import print_function
import sys
import time
import argparse
import textwrap
from isotel.idm import gateway

EC_LOG_BUF_LEN = 992

HEADER_MASK = 0xF0
HEADER_DATA_MASK = 15

LOG_ID_ENERGY = 0x10
LOG_ID_FAULT = 0x20
LOG_ID_TIME_CHANGE = 0x30
LOG_ID_SUBMETERING = 0x40
LOG_ID_TRACKING = 0x50
LOG_ID_ENERGY1 = 0x70

LOG_REASON_SYSTEM_POWER_UP = 1
LOG_REASON_WDT_RESET_OCCUR = 2
LOG_REASON_TIME_CHANGE = 4

STATUS_Ch = dict()
STATUS_Ch['0'] = 'Off'
STATUS_Ch['1'] = 'AntiSmog'
STATUS_Ch['2'] = 'On'


def _eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def download_logs(device, log_range=[1, 10]):
    logs = []
    search_back_max_idx = max(log_range) + 100
    if (search_back_max_idx > EC_LOG_BUF_LEN):
        search_back_max_idx = EC_LOG_BUF_LEN

    search_idx = max(log_range)
    logs_buf = []
    timestamp_found = False

    # search for the first available log with complete timestamp
    _eprint("Preparing to fetch logs ...")
    while (search_idx < search_back_max_idx):
        device.set_value('ec.i', search_idx)
        system_args = device.get_args(15)['args']
        logs_buf.append(system_args)

        header = int(system_args[4:6], 16)
        if ((header & HEADER_MASK) == LOG_ID_TIME_CHANGE):
            timestamp_found = True
            break

        search_idx = search_idx + 1

    if (timestamp_found == False):
        raise ValueError('Log with Timestamp not found!')

        # copy already downloaded logs into buffer, do not download them again
    for i in range(len(logs_buf), 0, -1):
        logs.append(logs_buf[i - 1])

    min_idx = min(log_range) - 1
    if (min_idx < 0):
        min_idx = 0

    for log_idx in range(max(log_range) - 1, min_idx, -1):
        try:
            _eprint("Fetching:", log_idx, " ", end="\r")
            device.set_value('ec.i', log_idx)
            system_args = device.get_args(15)['args']
            logs.append(system_args)
        except:
            _eprint('Error: Stopped due to communication error at log', log_idx)
            return logs

    _eprint("Completed successfully.")
    return logs


def decode_logs(logs):
    # find first log with full timestamp, if all is ok it should be the first one
    for log_idx in range(len(logs)):
        header = int(logs[log_idx][4:6], 16)
        if ((header & HEADER_MASK) == LOG_ID_TIME_CHANGE):
            break

    if (log_idx != 0):
        _eprint('Timestamp missing, ', log_idx, ' logs discarded.')

    abstime = int(logs[log_idx][12:20], 16)
    time.ctime(abstime)
    start_idx = log_idx

    logs_data = []
    for log_idx in range(start_idx, len(logs), 1):
        header = int(logs[log_idx][4:6], 16) & HEADER_MASK

        if ((header == LOG_ID_ENERGY) or (header == LOG_ID_SUBMETERING) or (header == LOG_ID_ENERGY1)):
            # Energy Log
            t = int(logs[log_idx][6:10], 16)
            t_msb = (t & 32768) / 32768
            t = t * 2
            t = t & 0xFFFF

            tlast = abstime & 0xFFFF
            tlast_msb = (abstime & 65536) / 65536

            cas = (abstime & 0xFFFF0000)
            cas = cas + t

            if (t >= tlast):
                if (t_msb != tlast_msb):
                    cas = cas + 65536
            else:
                if (t_msb != tlast_msb):
                    cas = cas + 65536
                else:
                    cas = cas + 131072

            abstime = cas
            energy = int(logs[log_idx][10:16], 16) * 18e-5
            tariff = int(logs[log_idx][4:6], 16) & HEADER_DATA_MASK
            energyA = int(logs[log_idx][16:18], 16) / 255 * energy
            energyB = int(logs[log_idx][18:20], 16) / 255 * energy
            if (header == LOG_ID_ENERGY):
                notes = 'ECL_SYNC'
            elif (header == LOG_ID_SUBMETERING):
                notes = 'SUBMETERING'
            elif (header == LOG_ID_ENERGY1):
                notes = 'TARIFF'
            else:
                notes = ''

            data = dict()
            data['time'] = abstime
            data['type'] = 'ENERGY'
            data['energy'] = energy
            data['energyA'] = energyA
            data['energyB'] = energyB
            data['tariff'] = tariff
            data['notes'] = notes
            logs_data.append(data)
            # print(time.ctime(abstime), '\t', energy, '\t', tariff, '\t ENERGY')

        elif (header == LOG_ID_TIME_CHANGE):
            abstime = int(logs[log_idx][12:20], 16)
            dT = int(logs[log_idx][6:12], 16)
            reason = int(logs[log_idx][4:6], 16) & HEADER_DATA_MASK
            if (reason == LOG_REASON_SYSTEM_POWER_UP):
                reason = 'POWER_UP'
            elif (reason == LOG_REASON_WDT_RESET_OCCUR):
                reason = 'WDT_RESET'
            elif (reason == LOG_REASON_TIME_CHANGE):
                reason = 'TIME_CHANGE'
                if (dT == 0):
                    reason = 'WEAK_TIMESTAMP'

            tariff = int(logs[log_idx][4:6], 16) & HEADER_DATA_MASK

            data = dict()
            data['time'] = abstime
            data['type'] = 'TIMECHANGE'
            data['notes'] = reason
            data['tariff'] = tariff
            data['dt'] = dT
            logs_data.append(data)
            # print(time.ctime(abstime), '\t', dT, '\t', reason, '\t TIMECHANGE')

        elif (header == LOG_ID_FAULT):
            abstime = int(logs[log_idx][6:14], 16)
            loadA = int(logs[log_idx][14:16], 16)
            loadB = int(logs[log_idx][16:18], 16)
            fault = int(logs[log_idx][18:20], 16)
            tariff = int(logs[log_idx][4:6], 16) & HEADER_DATA_MASK

            data = dict()
            data['time'] = abstime
            data['type'] = 'FAULT'
            data['tariff'] = tariff
            data['loadA'] = loadA
            data['loadB'] = loadB
            data['fault'] = fault
            logs_data.append(data)
            # print(time.ctime(abstime), '\t', loadA, '\t', loadB, '\t', fault, '\t FAULT')

    return logs_data


def display_logs(logs_data, log_type='ENERGY'):
    if (log_type == 'ENERGY'):
        print('Time', '\t', 'Log Type', '\t', 'Energy [kWh]', '\t', 'EnergyA [kWh]', '\t', 'EnergyB [kWh]', '\t',
              'Tariff', '\t',
              'Notes')

    for i in range(len(logs_data)):
        if (logs_data[i]['type'] == 'ENERGY' and log_type == 'ENERGY'):
            print(time.ctime(logs_data[i]['time']), '\t', logs_data[i]['type'], '\t',
                  format(logs_data[i]['energy'], '.4f'),
                  '\t', format(logs_data[i]['energyA'], '.4f'), '\t', format(logs_data[i]['energyB'], '.4f'), '\t',
                  logs_data[i]['tariff'], '\t', logs_data[i]['notes'])

        if (logs_data[i]['type'] == 'TIMECHANGE' and log_type == 'TIMECHANGE'):
            print(time.ctime(logs_data[i]['time']), '\t', logs_data[i]['type'], '\t', logs_data[i]['tariff'],
                  '\t', logs_data[i]['dt'], '\t', logs_data[i]['notes'])

        if (logs_data[i]['type'] == 'FAULT' and log_type == 'FAULT'):
            print(time.ctime(logs_data[i]['time']), '\t', logs_data[i]['type'], '\t', logs_data[i]['tariff'],
                  '\t', logs_data[i]['loadA'], '\t', logs_data[i]['loadB'], '\t', logs_data[i]['fault'])


def display_status(device):
    return [STATUS_Ch[device.get_value('ec.ChA')], STATUS_Ch[device.get_value('ec.ChB')]]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            Energy Control Modules Utility
            ----------------------------------------------------------------------
            Provide the device name of which module's you wish to fetch
            logs with -d option or leave blank to show available EC modules.
           '''))
    parser.add_argument("--gateway", help="gateway address, defaults to http://localhost:33000", required=False,
                        default='http://localhost:33000')
    parser.add_argument("-d",
                        help="Device to dump log data, like: 'EC-D16-20AHR-L2A-1.2.0-1901-1 50678419 (00043E29B4CD)'",
                        required=False, default=None)
    parser.add_argument("-N", help="Number of logs to dump, default is 20 and max is 992", required=False, type=int,
                        default=20)
    parser.add_argument("-t", help="Type of log, defaults to ENERGY", required=False, default='ENERGY',
                        choices=['ENERGY', 'FAULT', 'TIMECHANGE'])
    args = parser.parse_args()

    srv = gateway.Group(gateway=args.gateway)

    last_log = args.N
    if last_log > EC_LOG_BUF_LEN:
        last_log = EC_LOG_BUF_LEN
        _eprint("EC may contains up to", EC_LOG_BUF_LEN, "logs.")

    if args.d:
        ec = gateway.Device(srv, args.d, advanced=True, development=True, hidden=True)
        logs = download_logs(ec, [1, last_log])
        logs_decoded = decode_logs(logs)
        display_logs(logs_decoded, args.t)
    else:
        for x in srv.get_device_list():
            if 'EC-D16-' in x['name']:
                _eprint(x['name'],
                        display_status(gateway.Device(srv, x['name'], advanced=True, development=True, hidden=True)))
