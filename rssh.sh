#!/usr/local/bin/bash

wait_for_ping() {
  trap '{ echo -e "\033[0;31mCancelled!\033[0;00m" ; exit 1; }' INT  
  echo -en "\033[0;33mPinging $host .\033[0;00m"
  # because of -t 1, ping fails to trap internally, triggering SIGALRM, so we need to trap that
  trap '{echo "alarm"}' SIGALRM 
  until ping -t 1 "${host//.*}" &> /dev/null; do
    echo -n "."
    sleep 1
  done
  echo -e "\033[0;33m ok!\033[0;00m"
}

check_ssh(){
  nmap -Pn -p 22 "${host//.*}" 2>&1 \
    | grep -qE '22/tcp.*(filtered|open)'
}

main() {
  host="${@: -1}"
  while true; do
    wait_for_ping "$@"
    if check_ssh "$host"; then
      ssh "$@"
      [[ $? == 0 ]] && exit 0
    fi
    echo -en "\033[0;33mChecking ping again ... \033[0;00m"
  done
}

main "$@"
