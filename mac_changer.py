#!/usr/bin/env/ python3

import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", dest="interface", help="Interface to change its MAC Adress")
    parser.add_option("-m", dest="new_mac", help="New MAC Adress for Interface")
    parser.add_option("-p", dest="new_txpower", help="Change TxPower to n dB")
    options = parser.parse_args()[0]
    return options

def change_mac(interface, new_mac):
    print("[+] Changing MAC for " + interface +  " to " + new_mac)
    subprocess.run(["sudo","ifconfig", interface,"down"])
    subprocess.run(["sudo","ifconfig", interface,"hw","ether", new_mac])
    subprocess.run(["sudo","ifconfig", interface,"up"])

def check_mac(interface):
    ifconfig_result = subprocess.check_output(["sudo", "ifconfig",interface])
    search_result_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    print("[+] MAC was changed to: " + search_result_mac.group(0))

def change_power(interface, new_txpower):
    print("[+] Changing TxPower for " + interface + " to " + new_txpower + " dB")
    subprocess.run(["sudo","ifconfig", interface,"down"])
    subprocess.run(["sudo","iwconfig", interface,"txpower", new_txpower])
    subprocess.run(["sudo","ifconfig", interface,"up"])

def check_power(interface):
    iwconfig_result = subprocess.check_output(["sudo", "iwconfig",interface])
    search_result_power = re.search(r"\w\w\W\w\w\w\w\w\W\w\w\s", str(iwconfig_result))
    print("[+] Changed to " + search_result_power.group(0))

options = get_arguments()

change_mac(options.interface,options.new_mac)
check_mac(options.interface)
change_power(options.interface,options.new_txpower)
check_power(options.interface)