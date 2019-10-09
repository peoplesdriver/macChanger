#!/usr/bin/env python3

import subprocess
import optparse
import re

# function to get all the interfaces available
def get_interfaces():
    print("Interfaces available")
    subprocess.call("ifconfig", shell=True)


# function to get the command line arguments with the help of 'optparse' module
def get_arguments():
    print("Warning! You need root privileges to use this program")
    print("Usage example:\n\tpython3 macChanger.py -d default")
    print("\tpython3 macChanger.py -i eth0 -m 00:11:22:33:44:55")
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    parser.add_option("-v", "--view", dest="all", help="View all interfaces available")
    parser.add_option("-d", "--default", dest="default", help="Get arguments from user input")
    (options, arguments) = parser.parse_args()
    if options.all:
        get_interfaces()
    elif options.interface and options.new_mac:
        change_mac(options.interface, options.new_mac)
        if options.new_mac == check_mac_address(options.interface):
            print("[+] MAC address change was successfull!")
        else:
            print("[-] MAC address not changed!")
    elif options.default:
        start_default()
    elif not options.interface:
        print("[-] Please enter an interface name ex. -i eth0")
    elif not options.new_mac:
        print("[-] Please enter a MAC address ex. -m 00:11:22:33:44:55")
    else:
        print("[-] Please enter an option:\n\texample:\t-d default\n\t\t-i eth0 -m 00:11:22:33:44:55")


# function to get the interface name from user input
def get_interface():
    return input("Enter interface name >>> ")


# function to get the MAC address from user input
def get_mac():
    return input("Enter MAC address >>> ")


# function to start the program in default mode
def start_default():
    get_interfaces()
    change_mac(get_interface(), get_mac())


# function to change the mac address
# we need to pass to parameters: interface name and mac address
def change_mac(interface, new_mac):
    if interface == "lo":
        print("[-] The interface is not having a MAC address")
    else:
        print(f"[+] Changing MAC address for {interface} to {new_mac}")
        subprocess.call(["ifconfig", interface, "down"])
        subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
        subprocess.call(["ifconfig", interface, "up"])


# function to start the program
def start_program():
    subprocess.call("clear", shell=True)
    get_arguments()


# function to check if MAC address was changed
def check_mac_address(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    regex = re.compile(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w ")
    mac_search = re.search(regex, str(ifconfig_result))
    if mac_search:
        return str(mac_search.group(0)).strip()
    else:
        print("[-] The MAC address could not be read")


start_program()
