def get_device_identifier():
    with open('/proc/cpuinfo', 'r') as f:
        for line in f:
            if line.startswith('Serial'):
                return line.strip().split(':')[1].strip()
    return None