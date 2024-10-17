# Import required modules/packages/library
import pexpect

# Define variables
ip_address = "192.168.56.101"
username = "cisco"
password = "cisco123!"
new_hostname = "IssaqM"  # Define the new hostname

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

# Display a final success message
print("------------------------------------------------------")
print("")
print("--- Success! Connecting to:", ip_address)
print("    Username:", username)
print("    Password:", password)
print(f"    New Hostname: {new_hostname}")
print("------------------------------------------------------")

# Close the session
session.sendline("exit")
print("--- Connection closed ---")

c = pexpect.spawn('connection stuff')
#login happening here
c.expect('#')
c.sendline('\n')
c.expect('#')
h = c.before 
hostname = h.lstrip()
print "Connected to " + hostname
