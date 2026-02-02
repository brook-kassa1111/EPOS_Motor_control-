import ctypes
import time
import os
import sys

class EPOS4Controller:
    """Control EPOS4 motor controller via Command Library"""
    
    def __init__(self):
        # Load EPOS Command Library DLL
        # Default path: C:\Program Files (x86)\maxon motor ag\EPOS Positioning Controller\
        #dll_path = r"C:\Program Files (x86)\maxon motor ag\EPOS Positioning Controller\EPOS Command Library\EposCmd64.dll"
        # Need to change this to right path or maybe I can include it the read me ?
        possible_paths = [
        r"C:\Program Files (x86)\maxon motor ag\EPOS IDX\EPOS4\04 Programming\Windows DLL\LabVIEW\maxon EPOS\Resources\EposCmd64.dll",
        # Backup paths
        r"C:\Program Files (x86)\maxon motor ag\EPOS IDX\EPOS4\04 Programming\Windows DLL\LabVIEW\EposCmd64.dll",
        ]
        dll_path = None  # Start with None, then search
        for path in possible_paths:    
            if os.path.exists(path):  # ← Check 'path', not 'dll_path'
               dll_path = path
               break
        if dll_path is None:
            print("ERROR: Could not find EposCmd64.dll")
            print("Please install EPOS Studio from:")
            print("https://www.maxongroup.com/en/drives-and-systems/controls/positioning-controllers")
            print("\nOr update the path in epos_controller.py")
            sys.exit(1)

        # Load the DLL
        try:
            self.epos = ctypes.CDLL(dll_path)
        except Exception as e:
            print(f"ERROR: Failed to load DLL: {e}")
            sys.exit(1)

        self.device_handle = None
        self.node_id = 1

        print(f"Loaded EPOS Command Library from: {dll_path}")
        
    def open_device(self):
        """Open connection to EPOS4 controller"""
        # Device name for USB connection
        device_name = ctypes.c_char_p(b"EPOS4")
        protocol_stack_name = ctypes.c_char_p(b"MAXON SERIAL V2")
        interface_name = ctypes.c_char_p(b"USB")
        port_name = ctypes.c_char_p(b"USB0")  # Adjust if needed
        
        error_code = ctypes.c_uint(0)
        
        # Open device
        self.device_handle = self.epos.VCS_OpenDevice(
            device_name,
            protocol_stack_name,
            interface_name,
            port_name,
            ctypes.byref(error_code)
        )
        
        if self.device_handle == 0:
            print(f"Error opening device: {error_code.value}")
            return False
        
        print("Successfully connected to EPOS4")
        return True
    
    def close_device(self):
        """Close connection"""
        if self.device_handle:
            error_code = ctypes.c_uint(0)
            self.epos.VCS_CloseDevice(self.device_handle, ctypes.byref(error_code))
            print("Device closed")
    
    def clear_fault(self):
        """Clear any fault state"""
        error_code = ctypes.c_uint(0)
        result = self.epos.VCS_ClearFault(
            self.device_handle,
            self.node_id,
            ctypes.byref(error_code)
        )
        return result != 0
    
    def enable_motor(self):
        """Enable motor for operation"""
        error_code = ctypes.c_uint(0)
        
        # State machine: Fault Reset → Switch On → Enable Operation
        result = self.epos.VCS_SetEnableState(
            self.device_handle,
            self.node_id,
            ctypes.byref(error_code)
        )
        
        if result:
            print("Motor enabled")
            return True
        else:
            print(f"Error enabling motor: {error_code.value}")
            return False
    
    def disable_motor(self):
        """Disable motor"""
        error_code = ctypes.c_uint(0)
        result = self.epos.VCS_SetDisableState(
            self.device_handle,
            self.node_id,
            ctypes.byref(error_code)
        )
        
        if result:
            print("Motor disabled")
            return True
        return False
    
    def set_velocity_mode(self):
        """Set Profile Velocity Mode"""
        error_code = ctypes.c_uint(0)
        mode = ctypes.c_char(3)  # Profile Velocity Mode = 3
        
        result = self.epos.VCS_SetOperationMode(
            self.device_handle,
            self.node_id,
            mode,
            ctypes.byref(error_code)
        )
        
        if result:
            print("Set to Profile Velocity Mode")
            return True
        else:
            print(f"Error setting mode: {error_code.value}")
            return False
    
    def set_velocity(self, velocity_rpm):
        """
        Set target velocity
        
        Args:
            velocity_rpm: Target velocity in RPM (positive or negative)
        """
        error_code = ctypes.c_uint(0)
        velocity = ctypes.c_long(velocity_rpm)
        
        result = self.epos.VCS_MoveWithVelocity(
            self.device_handle,
            self.node_id,
            velocity,
            ctypes.byref(error_code)
        )
        
        if result:
            print(f"Set velocity to {velocity_rpm} RPM")
            return True
        else:
            print(f"Error setting velocity: {error_code.value}")
            return False
    
    def set_velocity_profile(self, acceleration, deceleration):
        """
        Set velocity profile parameters
        
        Args:
            acceleration: Acceleration in RPM/s
            deceleration: Deceleration in RPM/s
        """
        error_code = ctypes.c_uint(0)
        accel = ctypes.c_uint(acceleration)
        decel = ctypes.c_uint(deceleration)
        
        result = self.epos.VCS_SetVelocityProfile(
            self.device_handle,
            self.node_id,
            accel,
            decel,
            ctypes.byref(error_code)
        )
        
        if result:
            print(f"Set acceleration to {acceleration} RPM/s")
            return True
        else:
            print(f"Error setting profile: {error_code.value}")
            return False
    
    def halt_velocity_movement(self):
        """Stop motor movement (quick stop)"""
        error_code = ctypes.c_uint(0)
        
        result = self.epos.VCS_HaltVelocityMovement(
            self.device_handle,
            self.node_id,
            ctypes.byref(error_code)
        )
        
        if result:
            print("Motor stopped")
            return True
        return False
    
    def get_velocity_actual(self):
        """Get actual velocity"""
        error_code = ctypes.c_uint(0)
        velocity = ctypes.c_long(0)
        
        result = self.epos.VCS_GetVelocityIsAveraged(
            self.device_handle,
            self.node_id,
            ctypes.byref(velocity),
            ctypes.byref(error_code)
        )
        
        if result:
            return velocity.value
        return None
    
    def get_position_actual(self):
        """Get actual position"""
        error_code = ctypes.c_uint(0)
        position = ctypes.c_long(0)
        
        result = self.epos.VCS_GetPositionIs(
            self.device_handle,
            self.node_id,
            ctypes.byref(position),
            ctypes.byref(error_code)
        )
        
        if result:
            return position.value
        return None
    
    def get_current_actual(self):
        """Get actual current in mA"""
        error_code = ctypes.c_uint(0)
        current = ctypes.c_short(0)
        
        result = self.epos.VCS_GetCurrentIsAveraged(
            self.device_handle,
            self.node_id,
            ctypes.byref(current),
            ctypes.byref(error_code)
        )
        
        if result:
            return current.value
        return None
    
    def print_status(self):
        """Print current motor status"""
        vel = self.get_velocity_actual()
        pos = self.get_position_actual()
        curr = self.get_current_actual()
        
        print(f"Status: Vel={vel} RPM | Pos={pos} counts | Current={curr} mA")


def test_minimum_velocity(controller):
    """Test minimum detectable velocity"""
    print("\n=== Minimum Velocity Test ===")
    
    # Set gentle acceleration
    controller.set_velocity_profile(acceleration=1000, deceleration=1000)
    
    test_velocities = [1, 5, 10, 20, 50, 100, 500]
    
    for vel in test_velocities:
        print(f"\nTesting {vel} RPM...")
        controller.set_velocity(vel)
        
        # Monitor for 5 seconds
        for i in range(5):
            time.sleep(1)
            controller.print_status()
        
        input("Press Enter to continue to next velocity")
    
    # Stop
    controller.halt_velocity_movement()


def test_acceleration_profiles(controller):
    """Test different acceleration settings"""
    print("\n Acceleration Profile Test ")
    
    accel_values = [500, 2000, 5000, 10000]
    
    for accel in accel_values:
        print(f"\nTesting acceleration: {accel} RPM/s")
        controller.set_velocity_profile(acceleration=accel, deceleration=accel)
        
        # Ramp up
        print("Ramping up to 1000 RPM...")
        controller.set_velocity(1000)
        time.sleep(3)
        controller.print_status()
        
        # Ramp down
        print("Ramping down to 0...")
        controller.set_velocity(0)
        time.sleep(3)
        controller.print_status()


def demo_sequence(controller):
    """Complete demo sequence"""
    print("\n Demo Sequence ")
    
    # Set moderate acceleration
    controller.set_velocity_profile(acceleration=3000, deceleration=3000)
    
    # Slow scan
    print("\nSlow scan: 100 RPM")
    controller.set_velocity(100)
    time.sleep(5)
    controller.print_status()
    
    # Faster scan
    print("\nFaster scan: 300 RPM")
    controller.set_velocity(300)
    time.sleep(3)
    controller.print_status()
    
    # Reverse
    print("\nReverse: -100 RPM")
    controller.set_velocity(-100)
    time.sleep(3)
    controller.print_status()
    
    # Stop
    print("\nStopping ?")
    controller.halt_velocity_movement()
    time.sleep(1)
    controller.print_status()


def main():
    """Main test program"""
    print("EPOS4 Motor Control Test")
    print("=" * 50)
    
    # Create controller instance
    controller = EPOS4Controller()
    
    try:
        # Connect to EPOS4
        if not controller.open_device():
            sys.exit(1)
        
        # Clear any faults
        controller.clear_fault()
        
        # Set velocity mode
        controller.set_velocity_mode()
        
        # Enable motor
        controller.enable_motor()
        
        # Run tests
        print("\nSelect test:")
        print("1. Minimum velocity test")
        print("2. Acceleration profile test")
        print("3. Demo sequence")
        print("4. All tests")
        
        choice = input("\nEnter choice (1-4): ")
        
        if choice == '1':
            test_minimum_velocity(controller)
        elif choice == '2':
            test_acceleration_profiles(controller)
        elif choice == '3':
            demo_sequence(controller)
        elif choice == '4':
            test_minimum_velocity(controller)
            test_acceleration_profiles(controller)
            demo_sequence(controller)
        else:
            print("Invalid choice")
        
        # Disable motor
        controller.disable_motor()
        
    except KeyboardInterrupt:
        print("\n\nEmergency stop!")
        controller.halt_velocity_movement()
        controller.disable_motor()
    
    finally:
        # Close connection
        controller.close_device()


if __name__ == "__main__":
    main()