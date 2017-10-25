import time
import string
import os
import re
import SetSerialWindows
import sys
reload(sys) 
sys.setdefaultencoding('utf8')
MTK_2_4G_FREQOFFSET = 48
MTK_5G_FREQOFFSET = 17
mp_iface = 'ra0'

class MTK_MP_Serial:
	ser = None
	def __init__(self, com='COM1', bps=115200, terminal='$'):
		try:
			self.ser = SetSerialWindows.SetSerialWindows(com, bps, terminal)
		except IOError, e:  
			print e
			self.ser.serial_close()
	def reset_mp_rx_5G(self, interface=mp_iface):
		#self.ser.write('iwpriv ' +interface +' set ATE=RXFRAME\r\n', 0.15) 
		self.ser.write('iwpriv ' +interface +' set ResetCounter=0\r\n', 0.2) 
		#self.ser.write('iwpriv ' +interface +' set ATE=RXSTOP\r\n', 0.2) 
	def reset_mp_rx_2_4G(self, interface=mp_iface):
		self.ser.write('iwpriv ' +interface +' set ATE=RXFRAME\r\n', 0.15) 
		self.ser.write('iwpriv ' +interface +' set ResetCounter=0\r\n', 0.2) 
		#self.ser.write('iwpriv ' +interface +' set ATE=RXSTOP\r\n', 0.2) 
		
	def set_mp_rx_cfg(self, channel, rate, bandWidth_set, ant='A', FREQOFFSET=MTK_2_4G_FREQOFFSET, interface=mp_iface):
		print 'channel: %d, rate: %d, bandWidth_set: %s\r\n' % (channel, rate, bandWidth_set)
		ant_set = 1
		if ant.upper() == 'B':
			ant_set = 2
		self.ser.write('iwpriv ' +interface +' set ATE=ATESTART\r\n', 0.15) 
		self.ser.write('iwpriv ' +interface +' set ATECHANNEL=' +str(channel)+ '\r\n', 0.15)
		self.ser.write('iwpriv ' +interface +' set ATETXMODE=1\r\n', 0.15) 
		self.ser.write('iwpriv ' +interface +' set ' +bandWidth_set+ '\r\n', 0.15)
		self.ser.write('iwpriv ' +interface +' set ATERXANT=' +str(ant_set)+ '\r\n', 0.15)
		self.ser.write('iwpriv ' +interface +' set ResetCounter=0\r\n', 0.15) 
		self.ser.write('iwpriv ' +interface +' set ATETXFREQOFFSET=' +str(FREQOFFSET)+ '\r\n', 0.15)
		self.ser.write('iwpriv ' +interface +' set ATE=RXFRAME\r\n', 0.15) 
		
	def set_mp_tx_cfg(self, channel, TXMODE, TXMCS, bandWidth_set, TXPOW, ant='A',TXCNT=100000, TXLEN=1024, FREQOFFSET=MTK_2_4G_FREQOFFSET, interface=mp_iface):
		print 'channel: %d, rate: %d, bandWidth_set: %s\r\n' % (channel, rate, bandWidth_set)
		ant_set = 1
		txpower = 'ATETXPOW0='+str(TXPOW)
		if ant.upper() == 'B':
			ant_set = 2
			txpower = 'ATETXPOW1='+str(TXPOW)
		self.ser.write('iwpriv ' +interface +' set ATE=ATESTART\r\n', 0.15) 
		self.ser.write('iwpriv ' +interface +' set ATECHANNEL=' +str(channel)+ '\r\n', 0.15)
		self.ser.write('iwpriv ' +interface +' set ATETXMODE=' +str(TXMODE)+'\r\n', 0.15) 
		self.ser.write('iwpriv ' +interface +' set ATETXMCS=' +str(TXMCS)+'\r\n', 0.15) 
		self.ser.write('iwpriv ' +interface +' set ' +bandWidth_set+ '\r\n', 0.15)
		self.ser.write('iwpriv ' +interface +' set ATETXANT=' +str(ant_set)+ '\r\n', 0.15)
		self.ser.write('iwpriv ' +interface +' set ATETXLEN=' +str(TXLEN)+ '\r\n', 0.15)
		self.ser.write('iwpriv ' +interface +' set ATETXCNT=' +str(TXCNT)+ '\r\n', 0.15)
		self.ser.write('iwpriv ' +interface +' set ATETXFREQOFFSET=' +str(FREQOFFSET)+ '\r\n', 0.15)
		self.ser.write('iwpriv ' +interface +' set ' +str(txpower)+ '\r\n', 0.15)
		self.ser.write('iwpriv ' +interface +' set ATE=RXFRAME\r\n', 0.15)
		
	def tx_stop(self, interface=mp_iface):
		#self.ser.write('iwpriv ' +interface +' set ATE=TXSTOP\r\n', 0.12)
		out = self.ser.write_readuntill2('iwpriv ' +interface +' set ATE=TXSTOP\r\n') 
		print out
		
	def mp_query(self, interface=mp_iface):
		rx_ok = ''
		out = self.ser.write_readuntill2('iwpriv ' +interface +' stat\r\n') 
		print out
		rx_str = re.split('Rx\s+success\s+=\s+', out)
		if rx_str[0] != out:
			rx_str2 = rx_str[1].split('\n')
			if rx_str2[0] != rx_str[1]:
				rx_ok = rx_str2[0].strip()
		print rx_ok
		return rx_ok.strip()
	def close(self):
		self.ser.serial_close() 