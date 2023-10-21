#!/bin/bash -eu

# Trace system call

strace -o ./log/hello.log ./bin/hello

strace -o ./log/hello.py.log python3 ./src/hello.py

# With elapsed time in second
strace -T -o ./log/hello_time.log ./bin/hello
# In microsecond
# strace -tt -o ./log/hello_time.log ./bin/hello
