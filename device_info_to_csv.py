# Script to gather network device infomation, and dump this infomation into a CSV file.

import napalm
import sys
import os
import csv


def main(devices_csv, all_device_list, supported_os_types):
    """Sort and connect to each device from CSV and write to device_info.csv"""

    if not (os.path.exists(devices_csv) and os.path.isfile(devices_csv)):
        msg = 'Missing or invalid devices file {0}'.format(devices_csv)
        raise ValueError(msg)

    with open(devices_csv) as input_device_data:
        device_info_list = csv.reader(input_device_data, delimiter=',')
        for line in device_info_list:
            device_info = {}
            device_info['name'] = line[0]
            device_info['ip'] = line[1]
            device_info['os'] = line[2]
            device_info['username'] = line[3]
            device_info['password'] = line[4]
            all_device_list.append(device_info)

    for device in all_device_list:
        if device['os'] in supported_os_types:
            napalm.get_network_driver(device['os'])
            driver = napalm.get_network_driver(device['os'])
            device = driver(device['ip'],
                            device['username'],
                            device['password'])
            device.open()
            facts = device.get_facts()

            with open('device_info_output.csv', mode='a') as output:
                device_info_writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                device_info_writer.writerow([facts['hostname'], facts['vendor'], facts['model'], facts['serial_number'], facts['os_version']])



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please provide the full path to your devices.csv (Format = hostname,ip-address,vendor,username,password')
        sys.exit(1)
    devices_csv = sys.argv[1]
    all_device_list = []
    supported_os_types = ['ios', 'asa']
    main(devices_csv, all_device_list, supported_os_types)
