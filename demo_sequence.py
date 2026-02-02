#!/usr/bin/env python3
"""
Demo sequence for presentation
Shows various motor control capabilities
"""

from epos_controller import EPOS4Controller
import time

def demo():
    controller = EPOS4Controller()
    
    try:
        print("\n" + "="*60)
        print("  EPOS4 Motor Control ")
        print("="*60 + "\n")
        
        # Connect
        print("Connecting to EPOS4...")
        controller.open_device()
        controller.clear_fault()
        controller.set_velocity_mode()
        controller.enable_motor()
        
        input("\nPress Enter to start demo...")
        
        # Demo 1: Ultra-low speed precision
        print("\n[Demo 1] Ultra-Low Speed Precision")
        print("Setting velocity to 1 RPM ...")
        controller.set_velocity_profile(500, 500)
        controller.set_velocity(1)
        
        
        print("...one full rotation in the next 60 seconds...")
        
        for i in range(12):
            time.sleep(5)
            vel = controller.get_velocity_actual()
            print(f"  {(i+1)*5}s: Actual velocity = {vel} RPM")
        
        controller.set_velocity(0)
        input("\nPress Enter for next demo...")
        
        # Demo 2: Smooth acceleration profiles
        print("\n[Demo 2] Smooth Acceleration Profiles")
        print("Testing different acceleration rates...\n")
        
        profiles = [
            (500, "Very Gentle"),
            (2000, "Mediumish"),
            (10000, "Aggresiveish")
        ]
        
        for accel, desc in profiles:
            print(f"  {desc} acceleration ({accel} RPM/s)")
            controller.set_velocity_profile(accel, accel)
            
            print("    Ramping up to 500 RPM...")
            controller.set_velocity(500)
            time.sleep(2)
            
            print("    Ramping down to 0...")
            controller.set_velocity(0)
            time.sleep(2)
            print()
        
        input("\nPress Enter for next demo...")
        
        # Demo 3: Direction changes 
        print("\n[Demo 3] Bidirectional Control ")
        controller.set_velocity_profile(3000, 3000)
        
        sequence = [
            (100, "Forward scan"),
            (300, "Fast scan"),
            (-100, "Reverse scan"),
            (0, "Hold position")
        ]
        
        for vel, desc in sequence:
            print(f"  {desc}: {vel} RPM")
            controller.set_velocity(vel)
            time.sleep(3)
            controller.print_status()
        
        input("\nPress Enter for next demo...")
        
        # Demo 4: Emergency stop
        print("\n[Demo 4] Emergency Stop ")
        print("Spinning up to 500 RPM")
        controller.set_velocity(500)
        time.sleep(3)
        
        print("EMERGENCY STOP")
        controller.halt_velocity_movement()
        
        print("Motor stopped and holding position")
        time.sleep(2)
        controller.print_status()
        
        print("\n" + "="*60)
        print("  Demo Complete")
        print("="*60 + "\n")
        
        # Cleanup
        controller.disable_motor()
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted - stopping motor...")
        controller.halt_velocity_movement()
        controller.disable_motor()
    
    finally:
        controller.close_device()

if __name__ == "__main__":
    demo()