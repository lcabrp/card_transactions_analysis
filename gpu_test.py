# Use the new bindings:
from cupy.cuda.bindings import runtime, driver

# Example usage:
gpu_count = runtime.getDeviceCount()
print("GPU count:", gpu_count)
if gpu_count > 0:
    props = runtime.getDeviceProperties(0)
    print("GPU name:", props['name'])
else:
    print("No CUDA-capable GPU detected.")
