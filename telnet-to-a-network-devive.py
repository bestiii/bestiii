# Import required modules/packages/library
from netmiko import ConnectHandler

# Define the device details
device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.101',
    'username': 'cisco',
    'password': 'cisco123!',
    'secret': 'cisco123!',  # Enable password
}

# Define variables
new_hostname = "Hayes.Router"  # New hostname to set on the device
config_file = "running_config.txt"  # Local file to save the running configuration

try:
    # Establish an SSH connection to the device
    connection = ConnectHandler(**device)

    # Enter enable mode
    connection.enable()

    # Change the hostname to "Hayes'Router"
    connection.send_config_set([f'hostname {new_hostname}'])

    # Verify the hostname change
    print(f"--- Success! Hostname changed to {new_hostname}")

    # Retrieve the running configuration
    running_config = connection.send_command('show running-config')

    # Display the running configuration
    print("--- Running Configuration ---")
    print(running_config)

    # Save the running configuration to a local file
    with open(config_file, "w") as file:
        file.write(running_config)

    print(f"--- Success! Running configuration saved to {config_file}")

    # Display a final success message
    print("------------------------------------------------------------------")
    print(f"---               Success! Connected to: {device['ip']}")
    print(f"                                  Username: {device['username']}")
    print(f"                          New Hostname: {new_hostname}")
    print(f"         Running configuration saved to: {config_file}")
    print("------------------------------------------------------------------")

    # Close the connection
    connection.disconnect()

except Exception as e:
    print(f"--- FAILURE! Could not complete the operation: {e}")
