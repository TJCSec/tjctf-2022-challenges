#!/bin/bash

pyinstaller main.py -n boxed --onefile --hidden-import=scipy.linalg --noconfirm
