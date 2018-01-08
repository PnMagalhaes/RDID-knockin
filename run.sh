#!/bin/sh
gnome-terminal -x sh -c 'python2.7 Server/server.py; exec bash'
gnome-terminal -x sh -c 'python2.7 web-server.py; exec bash'
gnome-terminal -x sh -c 'python2.7 chameleon.py; exec bash'