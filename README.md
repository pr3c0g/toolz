# Repository Description
 
This repo contains many tools (lol 2) developed to assist in daly tasks

## Tools description
__tunnels.py__: Python3 script, shows all currently connected ssh sessions, and describing each tunnel or SOCKS proxy host and port.
Initially intended to help identify local ssh tunnel ports, that were established to monitor ElasticSearch clusters with cerebro.

__rssh.sh__: bash script. A Repeating SSH until it succeeds. Initially intended to ssh until success after rebooting a system, since I grew bored of trying over and over again until sshd was running on the other side. Looked like a cool learning experience.

__phelper.py__: Python3 script. Helper functions to deal with a large puppet codebase.
