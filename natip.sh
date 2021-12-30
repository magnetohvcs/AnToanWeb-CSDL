#!/bin/bash
iptables -t nat  -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 10.0.0.10:80
iptables -t nat  -A PREROUTING -p tcp --dport 1433 -j DNAT --to-destination 10.0.0.20:1433
iptables -A FORWARD -p tcp -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
sysctl net.ipv4.conf.all.forwarding=0