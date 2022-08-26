#!/bin/bash
BRIGHTNESS=$(cat /home/marc/LinuxSystemFiles/pixoo-awesome/pixoo_m_brightness.txt)
echo ${BRIGHTNESS:-20}
