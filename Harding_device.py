from netmiko import ConnectHandler

# Define device connection details
device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.1.1',
    'username': 'admin',
    'password': 'password',
    'secret': 'password'
}

# Define hardening checks and commands
hardening_checks = {
    "SSH enabled": {
        "check": "ip ssh version 2",
        "command": "ip ssh version 2"
    },
    "Telnet disabled": {
        "check": "no service telnet",
        "command": "no service telnet"
    },
    "Password encryption": {
        "check": "service password-encryption",
        "command": "service password-encryption"
    },
    "Syslog configured": {
        "check": "logging host",
        "command": "logging host 192.168.1.200"
    },
    "Login Password Retry Lockout": {
        "check": "aaa authentication login default local",
        "command": [
            "aaa new-model",
            "aaa local authentication attempts max-fail 3",
            "aaa authentication login default local"
        ]
    }
}

# Function to check and apply hardening configurations
def check_hardening(running_config, connection):
    for check, details in hardening_checks.items():
        rule = details["check"]       # Rule to look for in the current running config
        command = details["command"]  # Command to apply if the rule is missing

        # Check if the rule exists in the running configuration
        if rule in running_config:
            print(f"[PASS] {check}")
        else:
            print(f"[FAIL] {check}")
            
            # Prompt user to apply the missing configuration or skip it
            user_input = input(f"{check} not configured. Press 1 to configure, press 2 to skip: ")

            if user_input == '1':
                # Apply the configuration if the user chooses to do so
                if isinstance(command, list):  # If multiple commands are needed
                    connection.send_config_set(command)
                else:  # For a single command
                    connection.send_config_set([command])

                print(f"--- {check} has been configured.")
            elif user_input == '2':
                # Skip the configuration if the user chooses not to apply it
                print(f"--- Skipping configuration for {check}")

# Main script to connect to device and apply hardening
try:
    # Establish a connection to the device
    connection = ConnectHandler(**device)

    # Enter enable mode to access privileged commands
    connection.enable()

    # Retrieve the running configuration to perform the checks
    running_config = connection.send_command('show running-config')

    # Perform hardening checks and configure if needed
    check_hardening(running_config, connection)

    # Disconnect from the device once the task is complete
    connection.disconnect()
    print("--- Disconnected from the device.")

except Exception as e:
    print(f"--- FAILURE! Could not complete the operation: {e}")
