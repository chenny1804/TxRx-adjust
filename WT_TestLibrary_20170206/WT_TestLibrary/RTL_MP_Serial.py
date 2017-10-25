import time
import string
import os
import re
import SetSerialWindows
import sys
reload(sys) 
sys.setdefaultencoding('utf8')

mp_iface = 'wlan0'

class RTL_MP_Serial:
	ser = None
	def __init__(self, com='COM1', bps=115200, terminal='$'):
		try:
			self.ser = SetSerialWindows.SetSerialWindows(com, bps, terminal)
			self.ser.write('\r\n', 0.2)
		except IOError, e:  
			print e
			self.ser.serial_close()
			
	def mp_start(self, interface=mp_iface):
		self.ser.write('ifconfig ' +interface +' down\r\n', 0.3)  
		self.ser.write('iwpriv ' +interface +' set_mib mp_specific=1\r\n', 0.3)  
		self.ser.write('ifconfig ' +interface +' up\r\n', 5)  
		self.ser.write('iwpriv ' +interface +' mp_start\r\n', 1.5)  		
		print 'mp_start'
	def mp_start_5g(self, interface=mp_iface):
		self.ser.write('iwpriv ' +interface +' set_mib pa_type=0\r\n', 0.3)
		self.ser.write('iwpriv ' +interface +' set_mib macPhyMode=0\r\n', 0.3)   
		self.ser.write('iwpriv ' +interface +' set_mib mp_specific=1\r\n', 0.3)
		self.ser.write('iwpriv ' +interface +' set_mib phyBandSelect=2\r\n', 0.3) 
		self.ser.write('ifconfig ' +interface +'  down up\r\n', 5)  
		self.ser.write('iwpriv ' +interface +' mp_start\r\n', 1.5)  		
		print 'mp_start'

	def start_mp_rx(self, interface=mp_iface):
		self.ser.write('iwpriv ' +interface +'  mp_arx start\r\n', 0.1)  
	
	def set_mp_rx_cfg(self, channel, rate, bandWidth_set, ant='A', interface=mp_iface):
		print 'channel: %d, rate: %d, bandWidth_set: %s\r\n' % (channel, rate, bandWidth_set)
		cmd = 'iwpriv ' +interface +'  mp_bandwidth ' +bandWidth_set+ ',shortGI=0\r\n'
		self.ser.write(cmd, 0.15) 
		cmd = 'iwpriv ' +interface +' mp_channel ' +str(channel)+ '\r\n'
		#self.ser.write(cmd, 0.15)
		out = self.ser.write_readuntill2(cmd)
		cmd = 'iwpriv ' +interface +'  mp_arx ' +ant.lower()+'\r\n'
		self.ser.write(cmd, 0.15)
		
	def start_mp_ctx(self, channel, rate, power, bandWidth_set, ant='A', interface=mp_iface):
		self.stop_mp_tx(interface)
		print 'channel: %d, rate: %d, bandWidth_set: %s, interface: %s\r\n' % (channel, rate, bandWidth_set, interface)
		cmd = 'iwpriv ' +interface +'  mp_bandwidth ' +bandWidth_set+ ',shortGI=0\r\n'
		out = self.ser.write_readuntill2(cmd)
		cmd = 'iwpriv ' +interface +' mp_channel ' +str(channel)+ '\r\n'
		out = self.ser.write_readuntill2(cmd)
		cmd = 'iwpriv ' +interface +' mp_rate ' +str(rate)+ '\r\n'
		print cmd
		out = self.ser.write_readuntill2(cmd)
		print out
		cmd = '\r\niwpriv ' +interface +'  mp_ant_tx ' +ant.lower()+'\r\n'
		out = self.ser.write_readuntill2(cmd)
		if ant.upper() =='A':
			cmd = 'iwpriv ' +interface +'  mp_txpower patha=' +str(power)+ ',pathb=12\r\n'
		elif ant.upper() =='B':
			cmd = 'iwpriv ' +interface +'  mp_txpower patha=12,pathb=' + str(power)+'\r\n'
		#cmd = 'iwpriv ' +interface +'  mp_txpower patha=' +str(power)+ ',pathb='+ str(power)+'\r\n'
		out = self.ser.write_readuntill2(cmd)
		cmd = 'iwpriv ' +interface +'  mp_ctx pkt,background\r\n'
		out = self.ser.write_readuntill2(cmd)
		
	def stop_mp_rx(self, interface=mp_iface):
		cmd = 'iwpriv ' + interface +' mp_arx stop'
		print cmd
		self.ser.write(cmd + '\r\n', 0.1)
	
	def stop_mp_tx(self, interface=mp_iface):
		cmd = 'iwpriv ' + interface +' mp_ctx stop\r\n'
		print cmd
		out = self.ser.write_readuntill2(cmd)
	def close(self):
		self.ser.serial_close() 
	def mp_query(self, interface=mp_iface):
		tx_ok = ''
		rx_ok = ''
		out = self.ser.write_readuntill2('iwpriv ' +interface +' mp_query\r\n')
		print out
		tx_str = out.split('Tx OK:')
		if tx_str[0] != out:
			tx_str2 = tx_str[1].split(',')
			if tx_str2[0] != tx_str[1]:
				tx_ok = tx_str2[0].strip()
		rx_str = out.split('Rx OK:')
		if rx_str[0] != out:
			rx_str2 = rx_str[1].split(',')
			if rx_str2[0] != rx_str[1]:
				rx_ok = rx_str2[0].strip()
		return tx_ok.strip(), rx_ok.strip()	
		
	def readChannelRatePowerIndex(self, channel, interface=mp_iface, Band='2.4G', try_time=5):
		while try_time > 0:
			cmd = 'iwpriv ' +interface +' set_mib channel=' +str(channel)+ '\r\n'
			out = self.ser.write_readuntill2(cmd)
			print out
			cmd = 'ifconfig ' +interface +' down up\r\n'
			out = self.ser.write_readuntill2(cmd)
			print out
			cmd = '\r\niwpriv ' +interface +' reg_dump\r\n'
			reg_out = self.ser.write_readuntill2(cmd)
			print reg_out
			channel_str = '[Channel-%03d]' % int(channel)
			print channel_str
			if channel_str in reg_out:
				break
			else:
				try_time = try_time -1
				time.sleep(0.3)
		if try_time <= 0:
			raise Exception("set channel error")
		print reg_out
		if str(Band).upper() == '2.4G':
			return self.alaysisChannelRatePowerIndex_2_4G(reg_out)
		elif str(Band).upper() == '5G':
			return self.alaysisChannelRatePowerIndex_5G(reg_out)
		else:
			raise Exception("Band error %s") % str(Band)
	def changeBandWidth(self, interface=mp_iface, bandwidth='20M', try_time=3):
		use40M = '0'
		if bandwidth == '20M':
			use40M = '0'
		elif bandwidth == '40M':
			use40M = '1'
		elif bandwidth == '80M':
			use40M = '2'
		while try_time > 0:
			cmd = 'iwpriv ' +interface +' set_mib bws_enable=0\r\n'
			out = self.ser.write_readuntill2(cmd)
			print out
			cmd = 'iwpriv ' +interface +' set_mib use40M='+use40M +'\r\n'
			out = self.ser.write_readuntill2(cmd)
			print out
			cmd = 'ifconfig ' +interface +' down up\r\n'
			out = self.ser.write_readuntill2(cmd)
			print out
			cmd = '\r\niwpriv ' +interface +' reg_dump\r\n'
			out = self.ser.write_readuntill2(cmd)
			print out
			if bandwidth in out:
				break
			else:
				try_time = try_time -1
				time.sleep(0.3)
		if try_time <= 0:
			raise Exception("set bandwidth error")
	def alaysisChannelRatePowerIndex_5G(self, input):
		rate_power_list = input.split('PathB')
		patha = rate_power_list[0]
		pathb = rate_power_list[1]
		A_11G = re.split('OFDM:\s+', patha)[1].split('\n')[0].split(',')[0:-1]
		
		A_11N_1 = re.split('HT MCS 1SS:\s+', patha)[1].split('\n')[0].split(',')[0:-1]
		A_11N_2 = re.split('HT MCS 2SS:\s+', patha)[1].split('\n')[0].split(',')[0:-1]
		A_11N = A_11N_1 + A_11N_2
		
		A_VHT_1 = re.split('VHT MCS 1SS:\s+', patha)[1].split('\n')[0].split(',')[0:-1]
		A_VHT_2 = re.split('VHT MCS 2SS:\s+', patha)[1].split('\n')[0].split(',')[0:-1]
		A_VHT = A_VHT_1 + A_VHT_2
		
		B_11G = re.split('OFDM:\s+', pathb)[1].split('\n')[0].split(',')[0:-1]
		B_11N_1 = re.split('HT MCS 1SS:\s+', pathb)[1].split('\n')[0].split(',')[0:-1]
		B_11N_2 = re.split('HT MCS 2SS:\s+', pathb)[1].split('\n')[0].split(',')[0:-1]
		B_11N = B_11N_1 + B_11N_2
		
		B_VHT_1 = re.split('VHT MCS 1SS:\s+', pathb)[1].split('\n')[0].split(',')[0:-1]
		B_VHT_2 = re.split('VHT MCS 2SS:\s+', pathb)[1].split('\n')[0].split(',')[0:-1]
		B_VHT = B_VHT_1 + B_VHT_2
		print A_11G
		print A_11N
		print A_VHT
		print B_11G
		print B_11N
		print B_VHT
		return [[A_11G, A_11N, A_VHT], [B_11G, B_11N, B_VHT]]
	def alaysisChannelRatePowerIndex_2_4G(self, input):
		#A_11G
		A_11G_1 = re.split('A_Rate18_06\S+\s+0x', str(input))[1].split('\n')[0].strip()
		A_11G_2 = re.split('A_Rate54_24\S+\s+0x', str(input))[1].split('\n')[0].strip()
		A_11G_Str = A_11G_2 + A_11G_1
		A_11G_list = re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", A_11G_Str).strip().split(' ')[::-1]
		#B_11G
		B_11G_1 = re.split('B_Rate18_06\S+\s+0x', str(input))[1].split('\n')[0].strip()
		B_11G_2 = re.split('B_Rate54_24\S+\s+0x', str(input))[1].split('\n')[0].strip()
		B_11G_Str = B_11G_2 + B_11G_1
		B_11G_list = re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", B_11G_Str).strip().split(' ')[::-1]
		
		#A_11N
		A_11N_1 = re.split('A_Mcs03_Mcs00\S+\s+0x', str(input))[1].split('\n')[0].strip()
		A_11N_2 = re.split('A_Mcs07_Mcs04\S+\s+0x', str(input))[1].split('\n')[0].strip()
		A_11N_3 = re.split('A_Mcs11_Mcs08\S+\s+0x', str(input))[1].split('\n')[0].strip()
		A_11N_4 = re.split('A_Mcs15_Mcs12\S+\s+0x', str(input))[1].split('\n')[0].strip()
		A_11N_Str = A_11N_4 + A_11N_3 + A_11N_2 + A_11N_1
		A_11N_list = re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", A_11N_Str).strip().split(' ')[::-1]
		#B_11N
		B_11N_1 = re.split('B_Mcs03_Mcs00\S+\s+0x', str(input))[1].split('\n')[0].strip()
		B_11N_2 = re.split('B_Mcs07_Mcs04\S+\s+0x', str(input))[1].split('\n')[0].strip()
		B_11N_3 = re.split('B_Mcs11_Mcs08\S+\s+0x', str(input))[1].split('\n')[0].strip()
		B_11N_4 = re.split('B_Mcs15_Mcs12\S+\s+0x', str(input))[1].split('\n')[0].strip()
		B_11N_Str = B_11N_4 + B_11N_3 + B_11N_2 + B_11N_1
		B_11N_list = re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", B_11N_Str).strip().split(' ')[::-1]	

		#11B
		A_11B_1M = re.split('A_CCK1_Mcs32\S+\s+0x', str(input))[1].split('\n')[0].strip()[4:6]
		print A_11B_1M
		A_11B_1 = re.split('A_CCK11_2_B_CCK11\S+\s+0x', str(input))[1].split('\n')[0].strip()
		A_11B_list = re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", A_11B_1).strip().split(' ')
		print A_11B_list
		B_11B_1 = re.split('B_CCK5_1_Mcs32\S+\s+0x', str(input))[1].split('\n')[0].strip()
		B_11B_list = re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", B_11B_1).strip().split(' ')[0:-1][::-1]
		B_11B_list.append(A_11B_list[-1]) 
		print B_11B_list
		A_11B_list[-1] = A_11B_1M
		A_11B_list = A_11B_list[::-1]	
		print A_11B_list
		return [[A_11B_list, A_11G_list, A_11N_list], [B_11B_list, B_11G_list, B_11N_list]]
		
if __name__ == '__main__':
	rms = RTL_MP_Serial('COM8', 38400, '#')
	rms.readChannelRatePowerIndex('6', 'wlan1', '2.4G')	
		
