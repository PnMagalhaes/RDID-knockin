#!/bin/sh
#chameleon with sudo
#udp server 5005
gnome-terminal -x sh -c 'sudo python2.7 integration\ tests/chameleon.py; exec bash'
#ad hoc argv[1] = 192.168.43.6, argv[2] = 8080 on hot spot ssi : Redmi , pass: 1234lol
gnome-terminal -x sh -c 'python2.7 Server/server.py 192.168.43.6 8080; exec bash'
#udp client 5005
#cherrypy argv[1] = localhost, argv[2] = 8080
gnome-terminal -x sh -c 'python2.7 web-server.py "localhost" 8080; exec bash'
