#!/bin/bash
cd /home/user/code
g++ -g main.cpp
# gdb --interpreter=mi a.out
##launch the ssh server
/usr/sbin/sshd -D
##manually keep the container running
# sleep infinity
##launch the gbdserver
# gdbserver :22 a.out