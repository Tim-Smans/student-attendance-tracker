def get_device_identifier():
    """
    Retrieves the device serial number from the '/proc/cpuinfo' file.

    This function reads the CPU information from the system file '/proc/cpuinfo',
    searches for the line starting with 'Serial', and extracts the serial number
    by splitting the line at the colon and stripping any whitespace.

    Returns:
        str: The serial number of the device if found, otherwise None.
    """

    with open('/proc/cpuinfo', 'r') as f:
        for line in f:
            if line.startswith('Serial'):
                return line.strip().split(':')[1].strip()
    return None