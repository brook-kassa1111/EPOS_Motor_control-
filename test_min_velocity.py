#!/usr/bin/env python3
"""
Minimum Velocity Characterization Test
Systematically tests and logs slowest stable speed
"""

from epos_controller import EPOS4Controller
import time
import csv
from datetime import datetime

def test_min_velocity():
    controller = EPOS4Controller()
    
    try:
        # Setup
        controller.open_device()
        controller.clear_fault()
        controller.set_velocity_mode()
        controller.enable_motor()
        controller.set_velocity_profile(1000, 1000)  # Gentle
        
        # Test velocities
        test_velocities = [1, 2, 3, 5, 10, 20, 50]
        
        # Prepare CSV logging
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_file = f"velocity_test_{timestamp}.csv"
        
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Target_RPM', 'Time_s', 'Actual_RPM', 
                           'Position', 'Current_mA'])
            
            for target_vel in test_velocities:
                print(f"\n{'='*50}")
                print(f"Testing {target_vel} RPM")
                print(f"{'='*50}")
                
                controller.set_velocity(target_vel)
                
                # Log data for 10 seconds at 10 Hz
                start_time = time.time()
                for i in range(100):
                    elapsed = time.time() - start_time
                    vel = controller.get_velocity_actual()
                    pos = controller.get_position_actual()
                    curr = controller.get_current_actual()
                    
                    writer.writerow([target_vel, elapsed, vel, pos, curr])
                    
                    print(f"t={elapsed:.1f}s | "
                          f"Vel={vel} RPM | "
                          f"Pos={pos} | "
                          f"I={curr} mA", end='\r')
                    
                    time.sleep(0.1)
                
                print()  # New line
                
                # Pause between to go to the next tests
                controller.set_velocity(0)
                time.sleep(2)
        
        print(f"\nData saved to: {csv_file}")
        
        # Stop
        controller.halt_velocity_movement()
        controller.disable_motor()
        
    finally:
        controller.close_device()

if __name__ == "__main__":
    test_min_velocity()