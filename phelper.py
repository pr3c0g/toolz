# !/usr/bin/env python

import configparser
import argparse
import pprint
import sys
import re
import os


class Colors:
    Red = '\033[31m'
    Blue = '\033[34m'
    Yellow = '\033[33m'
    Purple = '\033[35m'
    endc = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'


def config_match_regex(gitrepo, configpath, host):
    """ This function will match a hostname to all regexes in .cfg files for 
    given config path.
    The intention is to find multiple matches on a file to troubleshoot which directives
    apply to that host."""

    print(f'{Colors.bold}{Colors.Blue}'
          f'Looking for cfg files that have regexes that match specified host..'
          f'{Colors.endc}')
    path = os.path.join(gitrepo, configpath)

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.cfg'):
                match = False
                analysis_regex = {}
                try:
                    print(f"File: {file}:")
                    with open(os.path.join(root, file)) as target:
                                                [analysis_regex.update({n: line})
                            for n, line in enumerate(target)
                            if line.startswith("HOST")]

                    for line, regex in analysis_regex.items():
                        if re.match(regex.split("=")[1].strip("%").strip('\n'), host):
                            match = True
                            print(f'{Colors.Yellow}Match on line:{line}, regex: {regex}{Colors.endc}',end="")

                    if match is False:
                        print(f'No match..')

                except IndexError:
                    print("Pass the hostname you're looking for as an argument")


def sitepp_find_host(host):
    """ Parses site.pp file and checks if specified host
    is a match on any of the node definitions."""

    print(f'\n{Colors.Blue}{Colors.bold}'
          f'Looking for host on site.pp{Colors.endc}')
    try:
        nodes = parse_sitepp()
        for regex in nodes.keys():
            if re.match(sanitize_regex(regex), host):
                print(f"{Colors.Yellow}Match at node {regex}{Colors.endc}")
                pprint.pprint(nodes[regex])
    except IndexError:
        print("Pass the hostname you're looking for as an argument")


def sitepp_find_module(module):
    """ Parses site.pp file and checks on which node definitions,
    the specified module is included"""

    nodes = parse_sitepp()
    try:
        print(f'\n{Colors.bold}{Colors.Blue}'
              f'Looking for entries in site.pp that match module {module}'
              f'{Colors.endc}')
        output = []
        for node in nodes:
            for x in nodes[node]:
                if module in x:
                    output.append(f"> {x} -> {node}")
        output.sort()
        pprint.pprint(output)
        #check_included_modules(nodes, module)
    except IndexError:
        print("If you want to see where a module "
              "is included, please specify it at sys.argv[1].")


def parse_sitepp():
    file = open((os.path.join(gitrepo, 'puppet/manifests/site.pp')), 'r')
    nodes = {}
    for line in file:
        if line.startswith("node"):
            try:
                nodes.update({node: included_modules})
            except NameError:
                pass
            included_modules = []
            node = re.search('^node (.*) {', line).groups()[0]
            continue
        if line.startswith("  include"):
            line = line.rstrip().split()[-1]
            included_modules.append(line)
    return nodes


def sanitize_regex(regex):
    sr = ["/", "'"]
    if regex.startswith(tuple(sr)):
        for i in ((sr[0], ""), (sr[1], "")):
            regex = regex.replace(*i)
    if regex.endswith(".eu.cdc") or \
            regex.endswith(".am.cdc"):
        regex = regex[:-7]
    elif regex.endswith(".aae.cdc"): 
        regex = regex[:-8]
    return regex


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Path to config.cfg file.")
    parser.add_argument("--host", help="Hostname to be checked on site.pp and on cfg files. "
                                       "Can be a FQDN or just hostname.")
    parser.add_argument("--module", help="Module to find on site.pp. "
                                    "Examples: named_server, server, apache, "
                                    "webserver::apache24, ::role:webserver::apache24")

    args = parser.parse_args()
    config = configparser.ConfigParser()
    config.read(args.config)

    gitrepo=config["CONFIGS"]["gitrepo"]
    configpath=config["CONFIGS"]["configpath"]

    print("")

    if args.host:
        config_match_regex(gitrepo, configpath, args.host)
        sitepp_find_host(args.host)
    if args.module: 
        sitepp_find_module(args.module)

