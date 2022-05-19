#!/bin/bash

python3 asm.py flag
python3 asm.py prog-dbg
../bin/machine ./prog-dbg.bin 2>dump
python3 solve.py
