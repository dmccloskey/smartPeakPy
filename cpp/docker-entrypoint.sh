#!/bin/bash
cd /home/user/code
g++ -L/usr/local/openms-build/lib -I/home/user/code/OpenMS/include -I/usr/local/OpenMS/src/openms/include -I/usr/local/openms-build/src/openms/include -I/usr/local/contrib-build/include -I/usr/include/qt5 -fPIC -g main.cpp /home/user/code/OpenMS/source/_test.cpp -lOpenMS
#g++ -g main.cpp
# gdb --interpreter=mi a.out
##launch the ssh server
# /usr/sbin/sshd -D
#manually keep the container running
sleep infinity
##launch the gbdserver
# gdbserver :3000 a.out