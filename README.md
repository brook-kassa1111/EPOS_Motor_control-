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




Basic Connection Test:
bashpython test_connection.py
- Tests basic connectivity and enables motor for 5 seconds at 10 RPM.

Minimum Velocity Characterization
bashpython test_min_velocity.py
- Systematically tests velocities from 1-50 RPM and logs data to CSV.
Output:
Console: Real-time status updates
CSV file: velocity_test_YYYYMMDD_HHMMSS.csv

Demo Sequence
bashpython demo_sequence.py
- Runs a professional demonstration sequence:

Ultra-low speed (1 RPM)
Acceleration profile testing
Bidirectional control
Emergency stop

Interactive Control
bashpython interactive_control.py

Manual command-line control:
- EPOS> enable
- EPOS> vel 100
- EPOS> accel 5000
- EPOS> stop
- EPOS> status
- EPOS> quit








