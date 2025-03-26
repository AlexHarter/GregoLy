#!/bin/sh

CC=gcc

mkdir -p build
$(CC) -o build/gregoly gregoly.c -static -nolibc