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
mp_iface_5G = None
LOGPATH='./'
COM = None
bps = 38400
channel_5G_20M = ['36', '40', '44', '48', '52', '56', '60', '64', '149', '153', '157', '161', '165']
channel_5G_40M = ['38', '46', '54', '62', '151', '159']
channel_5G_80M = ['42', '58', '155']
rate_11B = ['1M', '2M', '5.5M', '11M']
rate_11G = ['6M', '9M', '12M', '18M', '24M', '36M', '48M', '54M']
rate_11N_20M = ['HT20-MCS0', 'HT20-MCS1', 'HT20-MCS2', 'HT20-MCS3', 'HT20-MCS4', 'HT20-MCS5', 'HT20-MCS6', 'HT20-MCS7', 'HT20-MCS8', 'HT20-MCS9', 'HT20-MCS10', 'HT20-MCS11', 'HT20-MCS12', 'HT20-MCS13', 'HT20-MCS14', 'HT20-MCS15']
rate_11N_40M = ['HT40-MCS0', 'HT40-MCS1', 'HT40-MCS2', 'HT40-MCS3', 'HT40-MCS4', 'HT40-MCS5', 'HT40-MCS6', 'HT40-MCS7', 'HT40-MCS8', 'HT40-MCS9', 'HT40-MCS10', 'HT40-MCS11', 'HT40-MCS12', 'HT40-MCS13', 'HT40-MCS14', 'HT40-MCS15']
rate_VHT_20M = ['VHT20-MCS0', 'VHT20-MCS1', 'VHT20-MCS2', 'VHT20-MCS3', 'VHT20-MCS4', 'VHT20-MCS5', 'VHT20-MCS6', 'VHT20-MCS7', 'VHT20-MCS8', 'VHT20-MCS9', 'VHT20-MCS10', 'VHT20-MCS11', 'VHT20-MCS12', 'VHT20-MCS13', 'VHT20-MCS14', 'VHT20-MCS15']
rate_VHT_40M = ['VHT40-MCS0', 'VHT40-MCS1', 'VHT40-MCS2', 'VHT40-MCS3', 'VHT40-MCS4', 'VHT40-MCS5', 'VHT40-MCS6', 'VHT40-MCS7', 'VHT40-MCS8', 'VHT40-MCS9', 'VHT40-MCS10', 'VHT40-MCS11', 'VHT40-MCS12', 'VHT40-MCS13', 'VHT40-MCS14', 'VHT40-MCS15']
rate_VHT_80M = ['VHT80-MCS0', 'VHT80-MCS1', 'VHT80-MCS2', 'VHT80-MCS3', 'VHT80-MCS4', 'VHT80-MCS5', 'VHT80-MCS6', 'VHT80-MCS7', 'VHT80-MCS8', 'VHT80-MCS9', 'VHT80-MCS10', 'VHT80-MCS11', 'VHT80-MCS12', 'VHT80-MCS13', 'VHT80-MCS14', 'VHT80-MCS15']

channel_2_4G_20M = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
channel_2_4G_40M = ['3', '4', '5', '6', '7', '8', '9', '10', '11']


def recoreRatePowerIndex_RTL(rms, iface1='wlan1', iface2='wlan0', fileName=FileName):
	rate_2_4G = {}
	channel_rate_2_4G = {}
	rate_2_4G_40M = {}
	channel_rate_2_4G_20M = {}
	rate_5G = {}
	channel_rate_5G = {}
	
	rms.changeBandWidth(iface1, '20M')
	for channel in channel_2_4G_20M:
		rate_list = rms.readChannelRatePowerIndex(channel, iface1)
		print rate_list
		rate_len = len(rate_list)
		i = 0
		channel_rate_2_4G_20M[channel] = {}
		for rate in rate_11B:
			if rate_len == 2:
				#rate_2_4G[str(rate)] = [rate_list[0][0][i], rate_list[1][0][i]]
				channel_rate_2_4G_20M[channel][str(rate)] = [rate_list[0][0][i], rate_list[1][0][i]]
			elif rate_len == 1:
				#rate_2_4G[str(rate)] = [rate_list[0][0][i], rate_list[1][0][i]]
				channel_rate_2_4G_20M[channel][str(rate)] = [rate_list[0][0][i], rate_list[1][0][i]]
			else:
				raise Exception("ANT > 2: %d\n") %  rate_len
			i = i + 1
		i = 0
		for rate in rate_11G:
			if rate_len == 2:
				#rate_2_4G[str(rate)] = [rate_list[0][1][i], rate_list[1][1][i]]
				channel_rate_2_4G_20M[channel][str(rate)] = [rate_list[0][1][i], rate_list[1][1][i]]
			elif rate_len == 1:
				#rate_2_4G[str(rate)] = [rate_list[0][1][i], rate_list[1][1][i]]
				channel_rate_2_4G_20M[channel][str(rate)] = [rate_list[0][1][i], rate_list[1][1][i]]
			i = i + 1
		i = 0
		for rate in rate_11N_20M:
			if rate_len == 2:
				#rate_2_4G[str(rate)] = [rate_list[0][2][i], rate_list[1][2][i]]
				channel_rate_2_4G_20M[channel][str(rate)] = [rate_list[0][2][i], rate_list[1][2][i]]
			elif rate_len == 1:
				#rate_2_4G[str(rate)] = [rate_list[0][2][i], rate_list[1][2][i]]
				channel_rate_2_4G_20M[str(rate)] = [rate_list[0][2][i], rate_list[1][2][i]]
			i = i + 1
	channel_rate_2_4G = channel_rate_2_4G_20M
	print channel_rate_2_4G['1']['6M'], channel_rate_2_4G['1']['54M'], channel_rate_2_4G['1']['1M'], channel_rate_2_4G['1']['11M'],  channel_rate_2_4G['1']['HT20-MCS0'], channel_rate_2_4G['1']['HT20-MCS7']
	print channel_rate_2_4G['3']['6M'], channel_rate_2_4G['3']['54M'], channel_rate_2_4G['3']['1M'], channel_rate_2_4G['3']['11M'],  channel_rate_2_4G['3']['HT20-MCS0'], channel_rate_2_4G['3']['HT20-MCS7']
	print channel_rate_2_4G['6']['6M'], channel_rate_2_4G['6']['54M'], channel_rate_2_4G['6']['1M'], channel_rate_2_4G['6']['11M'],  channel_rate_2_4G['6']['HT20-MCS0'], channel_rate_2_4G['6']['HT20-MCS7']
	print channel_rate_2_4G['13']['6M'], channel_rate_2_4G['13']['54M'], channel_rate_2_4G['13']['1M'], channel_rate_2_4G['13']['11M'],  channel_rate_2_4G['13']['HT20-MCS0'], channel_rate_2_4G['13']['HT20-MCS7']
	
	rms.changeBandWidth(iface1, '40M')
	for channel in channel_2_4G_40M:
		rate_list = rms.readChannelRatePowerIndex(channel, iface1)
		print rate_list
		rate_len = len(rate_list)
		i = 0
		rate_2_4G_40M[channel] = {}
		for rate in rate_11N_40M:
			if rate_len == 2:
				rate_2_4G_40M[channel][str(rate)] = [rate_list[0][2][i], rate_list[1][2][i]]
			elif rate_len == 1:     
				rate_2_4G_40M[channel][str(rate)] = [rate_list[0][2][i], rate_list[1][2][i]]
			i = i + 1
		channel_rate_2_4G[channel] = dict(channel_rate_2_4G[channel], **rate_2_4G_40M[channel])
	print channel_rate_2_4G['1']['6M'], channel_rate_2_4G['1']['54M'], channel_rate_2_4G['1']['1M'], channel_rate_2_4G['1']['11M'],  channel_rate_2_4G['1']['HT20-MCS0'], channel_rate_2_4G['1']['HT20-MCS7']
	print channel_rate_2_4G['3']['6M'], channel_rate_2_4G['3']['54M'], channel_rate_2_4G['3']['1M'], channel_rate_2_4G['3']['11M'],  channel_rate_2_4G['3']['HT20-MCS0'], channel_rate_2_4G['3']['HT20-MCS7'], channel_rate_2_4G['3']['HT40-MCS0'], channel_rate_2_4G['3']['HT40-MCS7']
	print channel_rate_2_4G['6']['6M'], channel_rate_2_4G['6']['54M'], channel_rate_2_4G['6']['1M'], channel_rate_2_4G['6']['11M'],  channel_rate_2_4G['6']['HT20-MCS0'], channel_rate_2_4G['6']['HT20-MCS7'], channel_rate_2_4G['6']['HT40-MCS0'], channel_rate_2_4G['6']['HT40-MCS7']
	print channel_rate_2_4G['11']['6M'], channel_rate_2_4G['11']['54M'], channel_rate_2_4G['11']['1M'], channel_rate_2_4G['11']['11M'],  channel_rate_2_4G['11']['HT20-MCS0'], channel_rate_2_4G['11']['HT20-MCS7'], channel_rate_2_4G['11']['HT40-MCS0'], channel_rate_2_4G['11']['HT40-MCS7']
	print channel_rate_2_4G['13']['6M'], channel_rate_2_4G['13']['54M'], channel_rate_2_4G['13']['1M'], channel_rate_2_4G['13']['11M'],  channel_rate_2_4G['13']['HT20-MCS0'], channel_rate_2_4G['13']['HT20-MCS7']
	if iface2 != None:
		rms.changeBandWidth(iface2, '20M')
		for channel in channel_5G_20M:
			rate_list = rms.readChannelRatePowerIndex(channel, iface2, '5G')
			print rate_list
			i = 0
			rate_len = len(rate_list)
			channel_rate_5G[channel] = {}
			for rate in rate_11G:
				if rate_len == 2:
					channel_rate_5G[channel][str(rate)] = [rate_list[0][0][i], rate_list[1][0][i]]
				elif rate_len == 1:
					channel_rate_5G[channel][str(rate)] = [rate_list[0][0][i], rate_list[1][0][i]]
				else:
					raise Exception("ANT > 2: %d\n") %  rate_len
				i = i + 1
			i = 0
			for rate in rate_11N_20M:
				if rate_len == 2:
					channel_rate_5G[channel][str(rate)] = [rate_list[0][1][i], rate_list[1][1][i]]
				elif rate_len == 1:
					channel_rate_5G[channel][str(rate)] = [rate_list[0][1][i], rate_list[1][1][i]]
				i = i + 1	
			i = 0
			for rate in rate_VHT_20M:
				if rate_len == 2:
					channel_rate_5G[channel][str(rate)] = [rate_list[0][2][i], rate_list[1][2][i]]
				elif rate_len == 1:
					channel_rate_5G[channel][str(rate)] = [rate_list[0][2][i], rate_list[1][2][i]]
				i = i + 1
		'''
		rms.changeBandWidth(iface2, '40M')
		for channel in channel_5G_40M:
			rate_list = rms.readChannelRatePowerIndex(channel, iface2, '5G')
			print rate_list
			i = 0
			rate_len = len(rate_list)
			channel_rate_5G[channel] = {}
			for rate in rate_11N_40M:
				if rate_len == 2:
					channel_rate_5G[channel][str(rate)] = [rate_list[0][1][i], rate_list[1][1][i]]
				elif rate_len == 1:
					channel_rate_5G[channel][str(rate)] = [rate_list[0][1][i], rate_list[1][1][i]]
				i = i + 1
			
			i = 0
			for rate in rate_VHT_40M:
				if rate_len == 2:
					channel_rate_5G[channel][str(rate)] = [rate_list[0][2][i], rate_list[1][2][i]]
				elif rate_len == 1:
					channel_rate_5G[channel][str(rate)] = [rate_list[0][2][i], rate_list[1][2][i]]
				i = i + 1
		rms.changeBandWidth(iface2, '80M')
		for channel in channel_5G_80M:
			rate_list = rms.readChannelRatePowerIndex(channel, iface2, '5G')
			print rate_list	
			i = 0
			channel_rate_5G[channel] = {}
			for rate in rate_VHT_80M:
				if rate_len == 2:
					channel_rate_5G[channel][str(rate)] = [rate_list[0][2][i], rate_list[1][2][i]]
				elif rate_len == 1:
					channel_rate_5G[channel][str(rate)] = [rate_list[0][2][i], rate_list[1][2][i]]
				i = i + 1
		'''
	print channel_rate_2_4G['1']['6M'], channel_rate_2_4G['1']['54M'], channel_rate_2_4G['1']['1M'], channel_rate_2_4G['1']['11M'],  channel_rate_2_4G['1']['HT20-MCS0'], channel_rate_2_4G['1']['HT20-MCS7']
	print channel_rate_2_4G['3']['6M'], channel_rate_2_4G['3']['54M'], channel_rate_2_4G['3']['1M'], channel_rate_2_4G['3']['11M'],  channel_rate_2_4G['3']['HT20-MCS0'], channel_rate_2_4G['3']['HT20-MCS7'], channel_rate_2_4G['3']['HT40-MCS0'], channel_rate_2_4G['3']['HT40-MCS7']
	print channel_rate_2_4G['6']['6M'], channel_rate_2_4G['6']['54M'], channel_rate_2_4G['6']['1M'], channel_rate_2_4G['6']['11M'],  channel_rate_2_4G['6']['HT20-MCS0'], channel_rate_2_4G['6']['HT20-MCS7'], channel_rate_2_4G['6']['HT40-MCS0'], channel_rate_2_4G['6']['HT40-MCS7']
	print channel_rate_2_4G['11']['6M'], channel_rate_2_4G['11']['54M'], channel_rate_2_4G['11']['1M'], channel_rate_2_4G['11']['11M'],  channel_rate_2_4G['11']['HT20-MCS0'], channel_rate_2_4G['11']['HT20-MCS7'], channel_rate_2_4G['11']['HT40-MCS0'], channel_rate_2_4G['11']['HT40-MCS7']
	print channel_rate_2_4G['13']['6M'], channel_rate_2_4G['13']['54M'], channel_rate_2_4G['13']['1M'], channel_rate_2_4G['13']['11M'],  channel_rate_2_4G['13']['HT20-MCS0'], channel_rate_2_4G['13']['HT20-MCS7']
	#print channel_rate_5G['36']['6M'], channel_rate_5G['36']['54M'], channel_rate_5G['36']['HT20-MCS0'], channel_rate_5G['36']['HT20-MCS7'],  channel_rate_5G['36']['VHT20-MCS0'], channel_rate_5G['36']['VHT20-MCS8']
	#print channel_rate_5G['56']['6M'], channel_rate_5G['56']['54M'], channel_rate_5G['56']['HT20-MCS0'], channel_rate_5G['56']['HT20-MCS7'],  channel_rate_5G['56']['VHT20-MCS0'], channel_rate_5G['56']['VHT20-MCS8']	
	#print channel_rate_5G['149']['6M'], channel_rate_5G['149']['54M'], channel_rate_5G['149']['HT20-MCS0'], channel_rate_5G['149']['HT20-MCS7'],  channel_rate_5G['149']['VHT20-MCS0'], channel_rate_5G['149']['VHT20-MCS8']
	#print channel_rate_5G['165']['6M'], channel_rate_5G['165']['54M'], channel_rate_5G['165']['HT20-MCS0'], channel_rate_5G['165']['HT20-MCS7'],  channel_rate_5G['165']['VHT20-MCS0'], channel_rate_5G['165']['VHT20-MCS8']

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
	#print '-----------------start-----------------'
	mp_serial =  None
	if model in RTL_model:
		mp_serial = RTL_MP_Serial.RTL_MP_Serial(COM, bps, finish)
		recoreRatePowerIndex_RTL(mp_serial, mp_iface_2_4G, mp_iface_5G, FileName)
	elif model in MTK_model:
		pass
	else:
		raise Exception("mode error %s") % str(mode)
	mp_serial.close()
	