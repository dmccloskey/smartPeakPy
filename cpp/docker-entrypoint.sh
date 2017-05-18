#!/bin/bash
cd /home/user/code
g++ -g main.cpp > a.exe
gdb --interpreter=mi a.exe