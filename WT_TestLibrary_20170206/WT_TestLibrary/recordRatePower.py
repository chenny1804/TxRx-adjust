import time
import string
import getopt
import os
import sys
import MTK_MP_Serial
import RTL_MP_Serial
import re
import csv
reload(sys) 
sys.setdefaultencoding('utf8')
RTL_model = ['P0', 'P1', 'P2S', '97F', '97F-7357', '97F-7358', '97F-7384']
MTK_model = ['P2', 'R1']

FileName = 'Mp_keyvalue.txt'
model = 'P1'
COM = 'com3'
finish = '$'
mp_iface_2_4G = 'wlan1'
mp_iface_5G = 'wlan0'
LOGPATH='./'
COM = None
bps = 38400
A_channel_5G_20M = [[36, 6.70], [40, 6.82], [44, 6.84], [48, 6.95],[52, 6.95], [56, 6.98], [60, 6.95], [64, 6.95], [149, 6.99], [153, 6.93], [157, 6.80], [161, 6.77], [165, 6.66]]
B_channel_5G_20M = [[36, 6.70], [40, 6.82], [44, 6.84], [48, 6.95],[52, 6.95], [56, 6.98], [60, 6.95], [64, 6.95], [149, 6.99], [153, 6.93], [157, 6.80], [161, 6.77], [165, 6.66]]
A_channel_5G_40M = [[38, 6.70], [46, 6.82], [54, 6.84], [62, 6.95],[151, 6.93], [159, 6.80]]
B_channel_5G_40M = [[38, 6.70], [46, 6.82], [54, 6.84], [62, 6.95],[151, 6.93], [159, 6.80]]
A_channel_5G_80M = [[42, 6.70], [58, 6.82], [155, 6.84]]
B_channel_5G_80M = [[42, 6.70], [58, 6.82], [155, 6.84]]
rate_11B = ['1M', '2M', '5.5M', '11M']
rate_11G = ['6M', '9M', '12M', '18M', '24M', '36M', '48M', '54M']
rate_11N = ['HT-MCS0', 'HT-MCS1', 'HT-MCS2', 'HT-MCS3', 'HT-MCS4', 'HT-MCS5', 'HT-MCS6', 'HT-MCS7', 'HT-MCS8', 'HT-MCS9', 'HT-MCS10', 'HT-MCS11', 'HT-MCS12', 'HT-MCS13', 'HT-MCS14', 'HT-MCS15']
rate_VHT = ['VHT-MCS0', 'VHT-MCS1', 'VHT-MCS2', 'VHT-MCS3', 'VHT-MCS4', 'VHT-MCS5', 'VHT-MCS6', 'VHT-MCS7', 'VHT-MCS8', 'VHT-MCS9', 'VHT-MCS10', 'VHT-MCS11', 'VHT-MCS12', 'VHT-MCS13', 'VHT-MCS14', 'VHT-MCS15']


channel_2_4G = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
channel_5G = ['36', '38', '40', '42', '44', '46', '48', '52', '54', '56', '58', '60', '62', '64', '149', '151', '153', '155', '157', '159', '161', '165']

def recoreRatePowerIndex_RTL(rms, iface1='wlan1', iface2='wlan0', fileName=FileName):
	rate_2_4G = {}
	channel_rate_2_4G = {}
	rate_5G = {}
	channel_rate_5G = {}
	
	for channel in channel_2_4G:
		rate_list = rms.readChannelRatePowerIndex(channel, iface1)
		print rate_list
		rate_len = len(rate_list)
		i = 0
		
		for rate in rate_11B:
			if rate_len == 2:
				rate_2_4G[str(rate)] = [rate_list[0][0][i], rate_list[1][0][i]]
			elif rate_len == 1:
				rate_2_4G[str(rate)] = [rate_list[0][0][i], rate_list[1][0][i]]
			else:
				raise Exception("ANT > 2: %d\n") %  rate_len
			i = i + 1
		i = 0
		for rate in rate_11G:
			if rate_len == 2:
				rate_2_4G[str(rate)] = [rate_list[0][1][i], rate_list[1][1][i]]
			elif rate_len == 1:
				rate_2_4G[str(rate)] = [rate_list[0][1][i], rate_list[1][1][i]]
		i = 0
		for rate in rate_11N:
			if rate_len == 2:
				rate_2_4G[str(rate)] = [rate_list[0][2][i], rate_list[1][2][i]]
			elif rate_len == 1:
				rate_2_4G[str(rate)] = [rate_list[0][2][i], rate_list[1][2][i]]
			i = i + 1
		channel_rate_2_4G[channel] = rate_2_4G
		
	for channel in channel_5G:
		rate_list = rms.readChannelRatePowerIndex(channel, iface2, '5G')
		print rate_list
		i = 0
		rate_len = len(rate_list)
		for rate in rate_11G:
			if rate_len == 2:
				rate_5G[str(rate)] = [rate_list[0][0][i], rate_list[1][0][i]]
			elif rate_len == 1:
				rate_5G[str(rate)] = [rate_list[0][0][i], rate_list[1][0][i]]
			else:
				raise Exception("ANT > 2: %d\n") %  rate_len
			i = i + 1
			i = 0
		i = 0
		for rate in rate_11N:
			if rate_len == 2:
				rate_5G[str(rate)] = [rate_list[0][1][i], rate_list[1][1][i]]
			elif rate_len == 1:
				rate_5G[str(rate)] = [rate_list[0][1][i], rate_list[1][1][i]]
			i = i + 1
		i = 0
		for rate in rate_VHT:
			if rate_len == 2:
				rate_5G[str(rate)] = [rate_list[0][2][i], rate_list[1][2][i]]
			elif rate_len == 1:
				rate_5G[str(rate)] = [rate_list[0][2][i], rate_list[1][2][i]]
			i = i + 1
		channel_rate_5G[channel] = rate_5G
	#os.system('echo ' + str(channel_rate_2_4G) +'\n>' +fileName)
	#os.system('echo ' + str(channel_rate_5G) +'\n>>' +fileName)
	with open(fileName, 'w+') as fd:
		fd.write(str(channel_rate_2_4G) +'\n')
		fd.write(str(channel_rate_5G) +'\n')
if __name__ == '__main__':
	try:
		opts, args = getopt.getopt(sys.argv[1:], "h:m:f:i:C:r:B:F:", ["help","mode=", "finish=", "interface=", "COM=", "rate=", "iface1=",  "iface2=", "File="])
	except getopt.GetoptError:
		print "getopt error!"
	if len(opts) == 0:
		usage()
		sys.exit()
	for o,a in opts:
		if o in ("-h","--help"):
			usage()
			sys.exit()
		elif o in ("-m","--mode"):
			model=a.upper()
			print 'mode: %s\n' % model
		elif o in ("-f","--finish"):
			finish=str(a)
			print 'finish: %s\n' % finish
		elif o in ("-F","--File"):
			FileName=a
			print 'finish: %s\n' % finish
		elif o in ("-i","--interface"):
			mp_iface=a
			print 'mp_iface: %s\n' % mp_iface
		elif o in ("-C","--COM"):
			COM=str(a)
			print 'COM: %s\n' % COM
		elif o in ("-B","--Band"):
			band=a.upper()
			print 'Band: %s\n' % band
		elif o in ("-r","--rate"):
			bps=int(a)
			print 'bps: %d\n' % bps
		elif o in ("--iface1"):
			mp_iface_2_4G=str(a)
			print 'mp_iface_2_4G: %s\n' % mp_iface_2_4G
		elif o in ("--iface2"):
			mp_iface_5G=str(a)
			print 'mp_iface_5G: %s\n' % mp_iface_5G
		else:
			usage()
			sys.exit()
	#print 'mp_iface: %s\n' % mp_iface
	mp_serial =  None
	if model in RTL_model:
		mp_serial = RTL_MP_Serial.RTL_MP_Serial(COM, bps, finish)
		recoreRatePowerIndex_RTL(mp_serial, mp_iface_2_4G, mp_iface_5G, FileName)
	elif model in MTK_model:
		pass
	else:
		raise Exception("mode error %s") % str(mode)
	mp_serial.close()
	