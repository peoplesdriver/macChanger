#!/usr/bin/env python3

import subprocess
import optparse


# function to get all the interfaces available
def get_interfaces():
    print("Interfaces available")
    subprocess.call("ifconfig", shell=True)


# function to get the command line arguments with the help of 'optparse' module
def get_arguments():
    print("Warning! you need to have root privileges to use this program")
    print("Usage example:\n\tpython3 macChanger.py -d default")
    print("\tpython3 macChanger.py -i eth0 -m 00:11:22:33:44:55")
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    parser.add_option("-d", "--default", dest="default", help="Get arguments from user input")
    (options, arguments) = parser.parse_args()
    if options.interface and options.new_mac:
        change_mac(options.interface, options.new_mac)
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
    print(f"[+] Changing MAC address for {interface} to {new_mac}")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


# function to start the program
def start_program():
    subprocess.call("clear", shell=True)
    get_arguments()


start_program()
