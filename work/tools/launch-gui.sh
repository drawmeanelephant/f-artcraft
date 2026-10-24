#!/bin/bash
export DISPLAY=:99
export LIBGL_ALWAYS_SOFTWARE=1
export WGPU_POWER_PREF=low
cd ~/workspace/vectorcraft/work
exec ~/workspace/vectorcraft/app/vectorcraft-0.13.1-linux-x86_64/bin/vectorcraft --control 7979 --automation-read-root ~/workspace/vectorcraft/work --automation-write-root ~/workspace/vectorcraft/work/out > ~/workspace/vectorcraft/work/gui.log 2>&1
