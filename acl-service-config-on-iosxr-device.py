import pexpect
import time
import pdb

address = '127.0.0.1'
username = 'admin'
password = 'admin'
port = '2024'
login_endpromt = 'admin@ncs>'
config_endpromt = 'admin@ncs%'
class device:
	"""docstring for device"""
	def __init__(self, address, username, password, port, login_endpromt):
		self.address = address
		self.username = username
		self.password = password
		self.port = port
		self.endpromt = login_endpromt

	def login(self):
		ssh_key = 'Are you sure you want to continue connecting (yes/no)?'
		child = pexpect.spawn('ssh -p {} {}@{}' .format(port, username, address))
		self.child = child
		login_promt = child.expect([ssh_key, 'password:', pexpect.EOF])
		if login_promt == 0:
			child.sendline('yes')
			child.expect('password:')
			child.sendline(password)
			child.expect(login_endpromt)
		if login_promt == 1:
			child.sendline(password)
			child.expect(login_endpromt)
		if login_promt == 2:
			print('Unable to connect to host-{} for user-{} through port-{}' .format(address, username, port))
		print(child.before)

	def sendCommand(self, command, prompt):
		self.child.sendline(command)
		self.child.expect(prompt)
		print(self.child.before)
		return self.child.before

h1 = device(address, username, password, port, login_endpromt)
h1.login()
h1.sendCommand('set paginate false', login_endpromt)
h1.sendCommand('request packages reload', login_endpromt)
h1.sendCommand('configure', config_endpromt)
h1.sendCommand('run show users', config_endpromt)
h1.sendCommand('run show services acl_lab', config_endpromt)

h1.sendCommand('set services acl_lab ingress devices iosxr0 interfaces GigabitEthernet 0/0/0/0', config_endpromt)
h1.sendCommand('commit dry-run outformat xml', config_endpromt)
h1.sendCommand('commit', config_endpromt)
h1.sendCommand('run show configuration devices device iosxr0 config interfaces interface GigabitEthernet 0/0/0/0', config_endpromt)
h1.sendCommand('run show configuration devices device iosxr0 | display json', config_endpromt)

h1.sendCommand('set services acl_lab ingress devices iosxr1 interfaces GigabitEthernet 0/0/0/0', config_endpromt)
h1.sendCommand('commit dry-run outformat xml', config_endpromt)
h1.sendCommand('commit', config_endpromt)
h1.sendCommand('run show configuration devices device iosxr1 config interfaces interface GigabitEthernet 0/0/0/0', config_endpromt)
h1.sendCommand('run show configuration devices device iosxr1 | display json', config_endpromt)
h1.sendCommand('run show services acl_lab', config_endpromt)
