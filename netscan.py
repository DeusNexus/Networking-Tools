#!usr/bin/env python

import scapy.all as scapy
import optparse
import socket

'''
Script to scan the given ip range for ip/mac/hostname of network clients.
'''

def get_arguements():
        parser = optparse.OptionParser()
        parser.add_option("-p","--ip",dest="ip",help="Enter IP or Range to search for client(s), default=192.168.1.0/24", default="192.168.1.0/24")
        options = parser.parse_args()[0]
        
        return options

def scan(ip):
        arp_request = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast/arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=3, verbose=False)[0]

        clients = []
        for element in answered_list:
                host = host_lookup(str(element[1].psrc))
                client = {"ip":element[1].psrc, "mac":element[1].hwsrc,"h_name":host}
                clients.append(client)

        return clients

def host_lookup(client_ip):
        host = socket.gethostbyaddr(client_ip)[0]
        return host

def print_list(clients):
        print("IP \t\t\tMAC\t\t\tHost-Name\n------------------------------------------------------------")
        for client in clients:
                print(client["ip"] + "\t\t" + client["mac"]+"\t" + client["h_name"])

try:
        options = get_arguements()
        clients = scan(options.ip)
        print_list(clients)

except:
        print("\n[-] Something went wrong, check 'netscan.py --help' for available options.\n")