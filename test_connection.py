from epos_controller import EPOS4Controller

controller = EPOS4Controller()
if controller.open_device():
    print("Connected to EPOS4")
    controller.clear_fault()
    controller.set_velocity_mode()
    controller.enable_motor()
    
    print("Motor enabled")
    print("Testing 10 RPM...")
    controller.set_velocity(10)
    
    import time
    time.sleep(5)
    
    controller.print_status()
    controller.halt_velocity_movement()
    controller.disable_motor()
    controller.close_device()
    print("Test complete")
else:
    print("Failed to connect")