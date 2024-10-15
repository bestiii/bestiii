# Import required modules/packages/library
import pexpect

# Define variables
ip_address = "192.168.56.101"
username = "cisco"
password = "cisco123!"
new_hostname = "IssaqM"  # Define the new hostname
config_file = "running_config.txt"  # Local file to save the running configuration

# Create telnet session
session = pexpect.spawn("telnet " + ip_address, encoding="utf-8")
result = session.expect(["Username:", pexpect.TIMEOUT])

# Check for error, if exists then display error and exit
if result != 0:
    print("--- FAILURE! creating session for:", ip_address)
    exit()

# Session is expecting username, enter details
session.sendline(username)
result = session.expect(["Password:", pexpect.TIMEOUT])

# Check for error, if exists then display error and exit
if result != 0:
    print("--- FAILURE! entering username:", username)
    exit()

# Session is expecting password, enter details
session.sendline(password)
result = session.expect(["#", pexpect.TIMEOUT])

# Check for error, if exists then display error and exit
if result != 0:
    print("--- FAILURE! entering password:", password)
    exit()

# Change the hostname of the device to "IssaqM"
# Enter configuration mode and set the new hostname
session.sendline("configure terminal")
session.expect(["#", pexpect.TIMEOUT])
session.sendline(f"hostname {new_hostname}")
result = session.expect(["#", pexpect.TIMEOUT])

# Check if the hostname change was successful
if result != 0:
    print("--- FAILURE! changing hostname to:", new_hostname)
else:
    print(f"--- Success! Hostname changed to {new_hostname}")

# Exit configuration mode to return to privileged EXEC mode
session.sendline("end")
result = session.expect(["#", pexpect.TIMEOUT])

# Check if exiting configuration mode was successful
if result != 0:
    print("--- FAILURE! exiting configuration mode")
    exit()

# Send command to show the running configuration
session.sendline("show running-config")
result = session.expect(["#", pexpect.TIMEOUT], timeout=20)  # Increase timeout to 20 seconds

# Check if the command was successful
if result != 0:
    print("--- FAILURE! retrieving running configuration")
    print("--- Debug: Output so far ---")
    print(session.before)  # Display the output up to this point for debugging
else:
    # Capture the output of the running configuration
    running_config = session.before
    # Display the running configuration
    print("--- Running Configuration ---")
    print(running_config)
    # Save the output to a local file
    with open(config_file, "w") as file:
        file.write(running_config)
    print(f"--- Success! Running configuration saved to {config_file}")

# Display a final success message
print("------------------------------------------------------")
print("")
print("--- Success! connecting to:", ip_address)
print("    Username:", username)
print("    Password:", password)
print(f"    New Hostname: {new_hostname}")
print(f"    Running configuration saved to: {config_file}")
print("------------------------------------------------------")
