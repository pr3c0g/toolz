#!/usr/local/bin/bash

wait_for_ping() {
  trap '{ echo "Cancelled!" ; exit 1; }' INT  
  echo -n "Pinging" "$host" "."
  # because of -t 1, ping fails to trap internally, triggering SIGALRM, so we need to trap that
  trap '{echo "alarm"}' SIGALRM 
  until ping -t 1 "${host//.*}" &> /dev/null; do
    echo -n "."
    sleep 1
  done
  echo " ok!"
}

check_ssh(){
  nmap -Pn -p 22 "${host//.*}" 2>&1 \
    | grep -qE '22/tcp.*(filtered|open)'
}

main() {
  host="${@: -1}"
  while true; do
    wait_for_ping "$@"
    check_ssh "$host" && ssh "$@"; exit 0
    echo "Can't ssh, checking ping again .."
  done
}

main "$@"
