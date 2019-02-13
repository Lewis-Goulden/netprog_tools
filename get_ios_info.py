from netmiko import ConnectHandler
from napalm import get_network_driver
from pprint import pprint

file = open('devices', 'r')

supported_os_types = ['ios', 'asa']

all_device_list = []

for line in file:
    device_info_list = line.strip().split(',')
    device_info = {}
    device_info['name'] = device_info_list[0]
    device_info['ip'] = device_info_list[1]
    device_info['os'] = device_info_list[2]
    device_info['username'] = device_info_list[3]
    device_info['password'] = device_info_list[4]

    all_device_list.append(device_info)

for device in all_device_list:
    if device['os'] in supported_os_types:
        get_network_driver(device['os'])
        driver = get_network_driver(device['os'])
        device = driver(device['ip'],
                        device['username'],
                        device['password'])
        device.open()
        facts = device.get_facts()
        print('Hostname: ' + facts['hostname'])
        print('Vendor: ' + facts['vendor'])
        print('Software Version: ' + facts['os_version'])
        print('Device Model: ' + facts['model'])
        print('Serial Number: ' + facts['serial_number'])
        device.close()
    else:
        print("\n *** " + device['name'] + ' is not an supported device. Skipping.')
