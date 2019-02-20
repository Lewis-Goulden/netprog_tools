from napalm import get_network_driver
 
def main():
    device = {}
    with open('/Users/evangoulden/Documents/Python Projects/iMac Project/devices.csv', 'r') as devices_data:
        for lines in devices_data:
            line = lines.split(sep=',')
            device['name'] = line[0]
            device['ip_address'] = line[1]
            device['fqdn'] = line[2]
            device['os'] = line[3]
            device['username'] = line[4]
            device['password'] = line[5]
            supported_devices = ['ios', 'procurve']
            if device['os'] in supported_devices:
                driver = get_network_driver(device['os'])
                connected_device = driver(device['ip_address'], device['username'], device['password'])
                try:
                    connected_device.open()
                    facts = connected_device.get_facts()
 
                except:
                    print("Could not connect to the specified device, check your connection...")
 
                print(facts['vendor'])
                print(facts['os_version'])
                print(facts['model'])
                print(facts['serial_number'])
 
            else:
                print("The device is not of a supported type, please try a supported type.")
 
   
if __name__ == "__main__":
    main()