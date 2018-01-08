#!/bin/sh
#chameleon with sudo
#udp server 5005
gnome-terminal -x sh -c 'python2.7 chameleon.py; exec bash'
gnome-terminal -x sh -c 'python2.7 Server/server.py; exec bash'
#udp client 5005
gnome-terminal -x sh -c 'python2.7 web-server.py; exec bash'
