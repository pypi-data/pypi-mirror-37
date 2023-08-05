import re
import socket
import time


class Ftp(object):
	def __init__(self, host=None, port=None, user=None, pwd=None):
		self.host = '47.95.120.193'
		self.port = 21
		self.user = 'asdwan'
		self.pwd = 'qws168'
		self.sock = socket.socket()
		self.logg = 0
		if host:
			self.host = host
			self.port = port
			self.connect()
			if user:
				self.user = user
				self.pwd = pwd
				self.login()

	def get_return(self, s):
		data = s.recv(1024)
		return data

	def gb2str(self):
		data = self.get_return(self.sock).replace(b'\r\n', b'\n')
		if self.logg > 0:
			print(data.decode('gb2312', 'ignore'), end='')
		return data.decode('gb2312', 'ignore')

	def connect(self):
		self.sock.connect((self.host, self.port))
		self.welcome = self.get_return(self.sock).replace(b'\r\n', b'\n').decode('gb2312', 'ignore')

	def get_welcome(self):
		print(self.welcome)

	def login(self):
		self.sock.sendall('USER {}\r\n'.format(self.user).encode())
		self.gb2str()
		self.sock.sendall('PASS {}\r\n'.format(self.pwd).encode())
		rev = self.gb2str()
		if '230 OK' in rev:
			print('登陆成功')
			self.sock.sendall(b'TYPE I\r\n')
			self.gb2str()
		self.create_sock()
	def download(self, path, filename):
		while True:
			try:
				self.newSock.close()
				self.create_sock()
				print('开始下载:', filename)
				self.sock.sendall(b'RETR %b\r\n' % filename.encode())
				text = b''
				with open(path+filename, 'wb') as f:
					while True:
						data = self.newSock.recv(1024)
						if data != b'':
							f.write(data)
							f.flush()
						else:
							break
				self.gb2str()
				print('下载完成:', filename)
				break
			except Exception as e:
				print(e)

	def cd(self, path):
		self.sock.sendall(b'CWD %b\r\n' % path.encode())
		self.gb2str()

	def create_sock(self):
		self.sock.sendall(b'PASV\r\n')
		rev = self.gb2str()
		ports = re.findall('\d+', rev)
		self.newPort = int(ports[5]) * 256 + int(ports[6])
		self.newSock = socket.socket()
		self.newSock.connect((self.host, self.newPort))
	def get_dir(self):
		self.sock.sendall(b'LIST\r\n')
		self.gb2str()
		data = self.newSock.recv(102400)
		files = re.findall(b'(.+?)\r\n', data)
		self.files_dict = {}
		self.files = []
		print(len(files))
		for i in files:
			attrs = re.findall(b'[drwx-]{10}', i)[0]
			if attrs[0] == 'd':
				attr = '文件夹'
			else:
				attr = '文件'
			name = re.findall(b' ([\S]*)$', i)[0]
			# if name == b'.' or name == b'..':
			# 	continue
			self.files_dict[name.decode('gb2312', 'ignore')] = attr
			self.files.append(name.decode('gb2312', 'ignore'))
		self.gb2str()
		self.create_sock()


	def mget(self, path, filename):
		print(filename)
		for i in self.files:
			if filename in i:
				# if '0622' in i:
				# 	continue
				time.sleep(0.5)
				self.download(path, i)

	def put(self, filename):
		self.create_sock()
		print('开始上传:', filename)

		self.sock.sendall(b'STOR %b\r\n' % filename.encode('gbk', errors='ignore'))
		self.gb2str()
		with open(filename, 'rb') as f:
			while True:
				data = f.read(1024)
				if len(data) == 0:
					break
				self.newSock.sendall(data)
		self.newSock.close()
		self.gb2str()

if __name__ == '__main__':
	s = Ftp('47.95.120.193', 21, 'asdwan', 'qws168')
	today = '20180920'
	s.logg = 2
	# s.cd('usedcar')
	# s.get_dir()
	s.put('README')
# s.download('gf_car_used_20180903.txt')
# s.download('gf_car_used_20180904.txt')
# s.download('gf_car_used_20180901.txt')
# s.download('gf_car_used_20180902.txt')
