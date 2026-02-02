# EPOS_Motor_control
Python-based motor control system for Maxon EPOS4 positioning controllers. Designed for precision motor control in aerospace applications, with support for ultra-low velocity control (down to 1 RPM) and automated testing sequences.


1. Ultra-Low Speed Control: Precise velocity control down to 1 RPM
2. Automated Testing: Scripted sequences for minimum velocity characterization
3. Professional Demo Mode: Repeatable demonstration sequences
4. Data Logging: CSV export for velocity, position, and current data
5. Easy Integration: Clean API for embedded system integration
6. Safety Features: Fault detection, emergency stop, motion profiling

 Hardware Requirements

EPOS4 Positioning Controller (Maxon)
  * Tested with EPOS4 Compact 50/15 EtherCAT
  * Should work with other EPOS4 variants

Brushless EC Motor with encoder or hall sensors
24V Power Supply (current rating depends on motor)
USB Cable (PC to EPOS4 for initial setup)


Python Packages
uses only Python standard library:
ctypes - DLL interface
os - File path handling
sys - System functions
time - Timing functions


How to find your DLL:

         Open File Explorer
Navigate to: C:\Program Files (x86)\maxon motor ag\
Look for folders like:
EPOS IDX\EPOS4\04 Programming\Windows DLL\
EPOS Positioning Controller\EPOS Command Library\

Find either:
EposCmd64.dll (for 64-bit Python) ← Most common
EposCmd.dll (for 32-bit Python)

Copy the full path and add it to possible_paths list
