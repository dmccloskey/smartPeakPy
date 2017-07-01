#!/bin/bash
cd /home/user/code
##debug external code
# g++ -L/usr/local/openms-build/lib -I/home/user/code/OpenMS/include -I/usr/local/OpenMS/src/openms/include -I/usr/local/openms-build/src/openms/include -I/usr/local/contrib-build/include -I/usr/include/qt5 -fPIC -g main.cpp /home/user/code/OpenMS/source/_Test.cpp -lOpenMS
##debug tests
g++ -L/usr/local/openms-build/lib -I/home/user/code/OpenMS/include -I/usr/local/OpenMS/src/openms/include -I/usr/local/openms-build/src/openms/include -I/usr/local/contrib-build/include -I/usr/include/qt5 -fPIC -g main.cpp /home/user/code/OpenMS/source/_Test.cpp /home/user/code/OpenMS/tests/_Test_test.cpp -lOpenMS
##debug setup
# g++ -g main.cpp

#manually keep the container running
sleep infinity