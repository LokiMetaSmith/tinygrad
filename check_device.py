from tinygrad.device import Device
print(f"Device.DEFAULT: {Device.DEFAULT}")
try:
    d = Device[Device.DEFAULT]
    print(f"Device class: {type(d)}")
    print(f"Allocator class: {type(d.allocator)}")
    # Check if _copyout is implemented
    import inspect
    print(f"_copyout implemented: {hasattr(d.allocator, '_copyout')}")
except Exception as e:
    print(f"Error getting device: {e}")
