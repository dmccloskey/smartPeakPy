#!/bin/bash
cd /home/user/code
g++ -g main.cpp
# gdb --interpreter=mi a.out
# /usr/sbin/sshd -D
# sleep infinity
gdbserver :3000 a.out