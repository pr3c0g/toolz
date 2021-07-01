#!/usr/bin/env python3

import os
import subprocess
import re
import time
from tabulate import tabulate

P = re.compile('.*\\d:\\d{2}\\.\\d{2} (.*)')


class Colors:
    Red = '\033[31m'
    Blue = '\033[34m'
    Yellow = '\033[33m'
    Purple = '\033[35m'
    endc = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'


def get_ssh_procs():

    ps = subprocess.Popen(('ps', 'axu'), stdout=subprocess.PIPE)

    try:
        output = subprocess.check_output(
            ('grep', 'ssh '), stdin=ps.stdout).decode("UTF-8").split('\n')
        ps.wait()
        output.remove("")

    except subprocess.CalledProcessError:
        output = ""
        return None

    ssh_procs = []
    for proc in output:
        if 'grep' not in proc:
            ssh_procs.append(P.match(proc).group(1))

    return ssh_procs


def build_tables():

    jump_table = []
    tunnel_table = []
    socks_table = []

    for proc in ssh_procs:

        # ssh -D 9876 HOST
        if "-D" in proc:
            target = proc.split(' ')[-1]
            port = proc.split(' ')[-2]
            socks_table.append((target, port))
            continue

        # ssh -q -W HOST:22 JUMPHOST
        if "-q -W" in proc:
            target = proc.split(' ')[-1]
            jump_host = proc.split(' ')[-2].rstrip(':22')
            jump_table.append((target, jump_host))
            continue

        # ssh -L 9200:localhost:9200 HOST
        if "-L" in proc:
            target = proc.split(' ')[-1]
            local_port = proc.split(" ")[-2].split(":")[-3]
            target_port = proc.split(" ")[-2].split(":")[-1]
            tunnel_table.append([(target, local_port, target_port)])
            continue

    return jump_table, \
        tunnel_table, \
        socks_table


if __name__ == "__main__":

    while True:
        try:
            os.system('clear')
            ssh_procs = get_ssh_procs()

            if not ssh_procs:
                print(f'{Colors.Blue}No ssh processes found{Colors.endc}')

            else:
                jump_table, tunnel_table, socks_table = build_tables()
                if socks_table:
                    print(f'{Colors.Blue}{Colors.bold}\nSOCKS Proxies{Colors.endc}')
                    print(tabulate(
                        socks_table, headers=['Target', 'Port'],
                        tablefmt="plain"))
                if tunnel_table:
                    print(f'{Colors.Blue}{Colors.bold}\nSSH Tunnels{Colors.endc}')
                    print(tabulate(
                        tunnel_table, headers=['Target', 'Local Port', 'Target Port'],
                        tablefmt="plain"))
                if jump_table:
                    print(f'{Colors.Blue}{Colors.bold}\nSSH Jumps{Colors.endc}')
                    print(tabulate(
                        jump_table, headers=['Jump Host', 'Target'],
                        tablefmt="plain"))

            for _ in range(10):
                print('. ', end=" ", flush=True)
                time.sleep(1)

        except KeyboardInterrupt:
            os.system('clear')
            print("rude exit my friend ...")
            break
