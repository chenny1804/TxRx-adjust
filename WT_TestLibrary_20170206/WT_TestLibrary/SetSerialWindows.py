#!/usr/bin/python
# -*- coding: cp936 -*-

import serial
import os
import time
import sys

class SetSerialWindows:
	ser = None
	terminalChar = '$'
	def __init__(self, com='COM1', bps=115200, terminal='$'):
		self.terminalChar = str(terminal)
		try:
			self.ser = serial.Serial(str(com),int(bps))
		except IOError, e:  
			print e
			self.ser.close()
		
	def write(self, cmd, sleep=0):
		cmd = cmd + '\n'
		self.ser.write(cmd)
		#print sleep
		time.sleep(sleep)
		#self.serial_flush()

		
	def readuntill(self, terminalChar, sleep=1):
		data = ''
		time.sleep(sleep)		 
		while True:
			data = data + self.ser.read(self.ser.inWaiting())
			data_list = data.split(terminalChar)
			data_len = len(data_list)
			time_end = time.time()
			if data_len >=2:
				break
		return data
	def readuntilDefault(self, sleep=1):
		data = ''
		time.sleep(sleep)		 
		while True:
			data = data + self.ser.read(self.ser.inWaiting())
			data_list = data.split(self.terminalChar)
			data_len = len(data_list)
			time_end = time.time()
			if data_len >=2:
				break
		return data
	def write_readuntillSpecialChar(self, cmd, SpecilChar, sleep=1):
		data = ''
		cmd = cmd + '\n'
		self.ser.write(cmd)
		time.sleep(sleep)		 
		while True:
			data = data + self.ser.read(self.ser.inWaiting())
			data_list = data.split(SpecilChar)
			data_len = len(data_list)
			time_end = time.time()
			if data_len >=2:
				break
		return data	
		
	def write_readuntillSpecialChar2(self, cmd, SpecilChar, sleep=0.1, timeout=10):
		data = ''
		cmd = cmd + '\n'
		self.ser.write(cmd)
		time.sleep(sleep)
		time_start = time.time()
		while True:
			data = data + self.ser.read(self.ser.inWaiting())
			data_list = data.split(SpecilChar)
			data_len = len(data_list)
			if data_len >=2:
				break
			time_end = time.time()
			if (time_end - time_start) > timeout:
				print 'timeout\n'
				break
			time.sleep(sleep)
		self.serial_flush()#貌似没用
		return data	
		
	def write_readuntill(self, cmd, sleep=1):
		data = ''
		cmd = cmd + '\n'
		self.ser.write(cmd)
		time.sleep(sleep)		 
		while True:
			data = data + self.ser.read(self.ser.inWaiting())
			data_list = data.split(self.terminalChar)
			data_len = len(data_list)
			time_end = time.time()
			if data_len >=2:
				break
		return data	
		
	def write_readuntill2(self, cmd, sleep=0.1, timeout=10):
		data = ''
		cmd = cmd + '\r\n'
		self.ser.write(cmd)
		time.sleep(sleep)
		time_start = time.time()
		while True:
			data = data + self.ser.read(self.ser.inWaiting())
			data_list = data.split(self.terminalChar)
			data_len = len(data_list)
			if data_len >=2:
				break
			time_end = time.time()
			if (time_end - time_start) > timeout:
				print 'timeout\n'
				break
			time.sleep(sleep)
		self.serial_flush()#貌似没用
		return data	
	def readuntill_timeout(self, terminalChar, sleep=1, timeout=5):
		data = ''
		time.sleep(sleep)		 
		time_start = time.time()
		while True:
			data = data + self.ser.read(self.ser.inWaiting())
			data_list = data.split(terminalChar)
			data_len = len(data_list)
			if data_len >=2 :
				break
			time_end = time.time()
			if (time_end - time_start) > timeout:
				print 'timeout\n'
				break
		return data	
	def serial_close(self):
		self.ser.close()
		
	def serial_flush(self):
		self.ser.flush()
		
if __name__=='__main__':
	ser = SetSerialWindows('COM8', 38400, '/ $')
	ret = ser.write_readuntill2('iwpriv wlan0 mp_query')
	print ret
	print len(ret)
