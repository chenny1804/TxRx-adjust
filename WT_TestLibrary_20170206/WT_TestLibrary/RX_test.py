import time
import WT_TestLibrary
import string
import getopt
import telnetlib
import os
import sys
import MTK_MP_Serial
import RTL_MP_Serial
import re
import csv
reload(sys) 
sys.setdefaultencoding('utf8')
from pyExcelerator import *

power_start = -10
power_end = -110
rx_ok_minPer = 0.8
ANTA = 'A'
model = 'P1'
MTK_2_4G_FREQOFFSET = 48
MTK_5G_FREQOFFSET = 17
pass_standard = 0.92

a_wireAtt_file = None
b_wireAtt_file = None
power_start_file = None
RTL_model = ['P0', 'P1', 'P2S', '97F', '97F-7357', '97F-7358', '97F-7384']
MTK_model = ['P2', 'R1']


#[channel, wireAtt]
A_channel_2_4G = [[1, 6.70], [2, 6.82], [3, 6.84], [4, 6.95], [5, 6.98], [6, 6.99], [7, 6.93], [8, 6.80], [9, 6.77], [10, 6.66], [11, 6.72], [12, 6.71], [13, 6.76]]
B_channel_2_4G = [[1, 6.59], [2, 6.77], [3, 6.83], [4, 7.01], [5, 7.13], [6, 7.19], [7, 7.13], [8, 6.99], [9, 6.88], [10, 6.72], [11, 6.78], [12, 6.80], [13, 6.89]]
A_channel_2_4G_40M = [[3, 6.84], [4, 6.95], [5, 6.98], [6, 6.99], [7, 6.93], [8, 6.80], [9, 6.77], [10, 6.66], [11, 6.72]]
B_channel_2_4G_40M = [[3, 6.83], [4, 7.01], [5, 7.13], [6, 7.19], [7, 7.13], [8, 6.99], [9, 6.88], [10, 6.72], [11, 6.78]]
A_channel_5G_20M = [[36, 6.70], [40, 6.82], [44, 6.84], [48, 6.95],[52, 6.95], [56, 6.98], [60, 6.95], [64, 6.95], [149, 6.99], [153, 6.93], [157, 6.80], [161, 6.77], [165, 6.66]]
B_channel_5G_20M = [[36, 6.70], [40, 6.82], [44, 6.84], [48, 6.95],[52, 6.95], [56, 6.98], [60, 6.95], [64, 6.95], [149, 6.99], [153, 6.93], [157, 6.80], [161, 6.77], [165, 6.66]]
A_channel_5G_40M = [[38, 6.70], [46, 6.82], [54, 6.84], [62, 6.95],[151, 6.93], [159, 6.80]]
B_channel_5G_40M = [[38, 6.70], [46, 6.82], [54, 6.84], [62, 6.95],[151, 6.93], [159, 6.80]]
A_channel_5G_80M = [[42, 6.70], [58, 6.82], [155, 6.84]]
B_channel_5G_80M = [[42, 6.70], [58, 6.82], [155, 6.84]]



freq_base_2_4g = 2412
freq_base_5GLow = 5180
freq_base_5GHigh= 5745

#[rate_name, mp_rate_index, rate_file, wt200_power_start]]
rate_11B = [['1M', 2, '1 Mbps(DSSS).csv', -76], ['2M', 4, '2 Mbps(DSSS).csv', -76], ['5.5M', 11, '5.5 Mbps(DSSS).csv', -76], ['11M', 22, '11 Mbps(DSSS).csv', -76]]
rate_11G = [['6M', 12, '6 Mbps(OFDM).csv', -63], ['9M', 18, '9 Mbps(OFDM).csv', -63], ['12M', 24, '12 Mbps(OFDM).csv', -63], ['18M', 36, '18 Mbps(OFDM).csv', -63], ['24M', 48, '24 Mbps(OFDM).csv', -63], ['36M', 72, '36 Mbps(OFDM).csv', -63], ['48M', 96, '48 Mbps(OFDM).csv', -63], ['54M', 108, '54 Mbps(OFDM).csv', -63]]
rate_11N_base = 128
rate_11N_20M = [['HT20-MCS0', 128, 'HT20-MCS0.CSV', -63], ['HT20-MCS1', 129, 'HT20-MCS1.CSV', -63], ['HT20-MCS2', 130, 'HT20-MCS2.CSV', -63], ['HT20-MCS3', 131, 'HT20-MCS3.CSV', -63],['HT20-MCS4', 132, 'HT20-MCS4.CSV', -63],['HT20-MCS5', 133, 'HT20-MCS5.CSV', -63],['HT20-MCS6', 134, 'HT20-MCS6.CSV', -63],['HT20-MCS7', 135, 'HT20-MCS7.CSV', -63]]
rate_11N_40M = [['HT40-MCS0', 128, 'HT40-MCS0.CSV', -63], ['HT40-MCS1', 129, 'HT40-MCS1.CSV', -63], ['HT40-MCS2', 130, 'HT40-MCS2.CSV', -63], ['HT40-MCS3', 131, 'HT40-MCS3.CSV', -63],['HT40-MCS4', 132, 'HT40-MCS4.CSV', -63],['HT40-MCS5', 133, 'HT40-MCS5.CSV', -63],['HT40-MCS6', 134, 'HT40-MCS6.CSV', -63],['HT40-MCS7', 135, 'HT40-MCS7.CSV', -63]]

rate_5G_20M = [['VHT20-MCS0', 128, 'VHT20-MCS0.CSV', -60], ['VHT20-MCS1', 129, 'VHT20-MCS1.CSV', -60], ['VHT20-MCS2', 130, 'VHT20-MCS2.CSV', -60], ['VHT20-MCS3', 131, 'VHT20-MCS3.CSV', -60],['VHT20-MCS4', 132, 'VHT20-MCS4.CSV', -60],['VHT20-MCS5', 133, 'VHT20-MCS5.CSV', -60],['VHT20-MCS6', 134, 'VHT20-MCS6.CSV', -60],['VHT20-MCS7', 135, 'VHT20-MCS7.CSV', -60],['VHT20-MCS8', 135, 'VHT20-MCS8.CSV', -60]]
rate_5G_40M = [['VHT40-MCS0', 128, 'VHT40-MCS0.CSV', -60], ['VHT40-MCS1', 129, 'VHT40-MCS1.CSV', -60], ['VHT40-MCS2', 130, 'VHT40-MCS2.CSV', -60], ['VHT40-MCS3', 131, 'VHT40-MCS3.CSV', -60],['VHT40-MCS4', 132, 'VHT40-MCS4.CSV', -60],['VHT40-MCS5', 133, 'VHT40-MCS5.CSV', -60],['VHT40-MCS6', 134, 'VHT40-MCS6.CSV', -60],['VHT40-MCS7', 135, 'VHT40-MCS7.CSV', -60],['VHT40-MCS8', 135, 'VHT40-MCS8.CSV', -60],['VHT40-MCS9', 135, 'VHT40-MCS9.CSV', -60]]
rate_5G_80M = [['VHT80-MCS0', 128, 'VHT80-MCS0.CSV', -60], ['VHT80-MCS1', 129, 'VHT80-MCS1.CSV', -60], ['VHT80-MCS2', 130, 'VHT80-MCS2.CSV', -60], ['VHT80-MCS3', 131, 'VHT80-MCS3.CSV', -60],['VHT80-MCS4', 132, 'VHT80-MCS4.CSV', -60],['VHT80-MCS5', 133, 'VHT80-MCS5.CSV', -60],['VHT80-MCS6', 134, 'VHT80-MCS6.CSV', -60],['VHT80-MCS7', 135, 'VHT80-MCS7.CSV', -60],['VHT80-MCS8', 135, 'VHT80-MCS8.CSV', -60],['VHT80-MCS9', 135, 'VHT80-MCS9.CSV', -60]]


bandWidth_20M_RTL = '40M=0'
bandWidth_40M_RTL = '40M=1'
bandWidth_80M_RTL = '40M=2'
bandWidth_20M_MTK = 'ATETXBW=0'
bandWidth_40M_MTK = 'ATETXBW=1'
bandWidth_80M_MTK = 'ATETXBW=2'

#demod
WT_DEMOD_11AG = 0                        
WT_DEMOD_11B = 1                           
WT_DEMOD_11N_20M = 2                       
WT_DEMOD_11N_40M = 3                       
WT_DEMOD_11AC_20M = 4                      
WT_DEMOD_11AC_40M = 5                      
WT_DEMOD_11AC_80M = 6                      
WT_DEMOD_11AC_160M = 7                    
WT_DEMOD_11AC_80_80M = 8                 
WT_DEMOD_BT = 9
WT_DEMOD_ZIGBEE = 10
WT_DEMOD_UNKNOW = 0xFF     

#Error Code
WT_ERR_CODE_OK = 0
WT_ERR_CODE_CONNECT_FAIL =1			
WT_ERR_CODE_UNKNOW_PARAMETER =2		 
WT_ERR_CODE_OUT_OF_MEMORY = 3		
WT_ERR_CODE_NO_DATA_CAPTURED = 4	 
WT_ERR_CODE_TIMEOUT = 5				 
WT_ERR_CODE_VsgInaccuracy = 6		
WT_ERR_CODE_GENERAL_ERROR = 7		
WT_ERR_CODE_BANDWIDTH_ERROR = 8      
WT_ERR_CODE_SIGNALTYPE_ERROR = 9     
WT_ERR_CODE_FRM_ERROR = 10           
WT_ERR_CODE_PARAMETER_MISMATCH = 11  				        
WT_ERR_CODE_PSDU_ERROR = 12          
WT_ERR_CODE_PSDU_CONVERT_FAIL = 13   
WT_ERR_CODE_OUTDATA_INVALID = 14     							        
WT_ERR_CODE_GENERATE_FAIL = 15       
WT_ERR_CODE_TESTER_NO_WAVE = 16      
WT_ERR_CODE_LAST = 17

wt_server = '192.168.10.254'
client_ip = '192.168.0.1'
username = 'admin'
password = '12345678'
finish = '$'
mp_iface = 'wlan1'
band = '2.4G'
LOGPATH='./log/'
RF_PORT_Default = 1
SIG_USERFILE = 0
COM = None
bps = 38400
wave_file_base = 'C:/Program Files (x86)/xgiga/WT200.wave/'
#wave_file_base = 'C:/Program Files/xgiga/WT200.wave/'

external_att = 1.45

def usage():
	print '''usage:
	python Rx_test.py -m P2 -s 192.168.10.254 -C COM3 -b 38400 -f $ -i wlan0 -B 5G
	-m model eg:P2, p1, P0, 97f
	-s wt200 server_ip 
	-C serial port, eg:COM3
	-r  Baud rate, eg:38400, 57600, 115200
	-f finish terminal char, eg: #, $, >
	-i mp_interface, eg:ra0, wlan1, wlan0
	-B Band, eg:2.4G, 5g
	-a ANTA A wires ATT file
	-b ANTA B wires ATT file
	--fa ANTA A wires ATT file
	--fb ANTA B wires ATT file
	-P power_start_file 
	'''

def get_rate_min_ok(rate_list, file_list, log_path, data_list, pass_standard=pass_standard, index=0):
	power = -1
	rx_ok_percent = -1
	for rate in rate_list:
		data_list.append([rate[0], [[], []], [[], []]])
		for dirName in file_list:
			txt_list = dirName.split('.txt')
			if txt_list[0] == dirName:
				continue
			filename_list = txt_list[0].split('_')
			if filename_list[3] == rate[0]:
				with open( os.path.join(log_path, dirName), 'r') as fd:
					lines = fd.readlines()
					j = 1
					for line in lines[1:]:
						line_list = re.split('\s+', line.strip())
						print line_list
						if line_list[0] != line and float(line_list[3][0:-1]) < pass_standard * 100 and str(line_list[3][0:-1]).strip() != '-100':
							break
						j = j + 1
					if j != 1:
						j = j -1
						line_list = re.split('\s+', lines[j].strip())
						power = int(line_list[0])
						rx_ok_percent = line_list[3]
				if filename_list[0].upper() == 'A':
					print filename_list[2], power, rx_ok_percent
					data_list[index][1][0].append([filename_list[2], power, rx_ok_percent])
				elif filename_list[0].upper() == 'B':
					data_list[index][2][0].append([filename_list[2], power, rx_ok_percent])
				power = -1
				rx_ok_percent = -1
		power_sum = 0
		m = 0
		for data in data_list[index][1][0]:
			if int(data[1]) != -1:
				power_sum = power_sum + int(data[1])
				m = m + 1
		if power_sum != 0:
			data_list[index][1][1] = round(float(power_sum) / float(m), 2)
		else:
			data_list[index][1][1] = 0
		power_sum = 0
		m = 0
		for data in data_list[index][2][0]:
			if int(data[1]) != -1:
				power_sum = power_sum + int(data[1])
				m = m + 1
		if power_sum != 0:
			data_list[index][2][1] = round(float(power_sum) / float(m), 2)
		else:
			data_list[index][2][1] = 0
		index = index + 1
	return index
	
def rx_data_sum_excel_2_4G(log_path, excel_name, pass_standard, model):
	data_list = []
	dir_dirNames = os.listdir(log_path)
	#print dir_dirNames
	index = 0
	#index = get_rate_min_ok(rate_11B, dir_dirNames, log_path, data_list, pass_standard, index)
	index = get_rate_min_ok(rate_11G, dir_dirNames, log_path, data_list, pass_standard, index)
	#index = get_rate_min_ok(rate_11N_20M, dir_dirNames, log_path, data_list, pass_standard, index)
	#index = get_rate_min_ok(rate_11N_40M, dir_dirNames, log_path, data_list, pass_standard, index)
	
	w=Workbook()
	style = XFStyle()
	al = Alignment()
	al.horz = Alignment.HORZ_CENTER
	al.vert = Alignment.VERT_CENTER
	style.alignment = al
	fnt = Font()  
	fnt.height = 200  
	style.font = fnt
	for data_tmp in data_list:
		ws=w.add_sheet(data_tmp[0])
		ws.write(0, 0, 'device', style)
		ws.write(0, 1, 'standard', style)
		ws.write(0, 2, 'channel', style)
		ws.write(0, 3, 'ANT', style)
		ws.write(0, 4, 'power', style)
		ws.write(0, 5, 'Percent', style)
		ws.write(0, 6, 'ANT', style)
		ws.write(0, 7, 'power', style)
		ws.write(0, 8, 'Percent', style)
		if '40' in data_tmp[0]:
			for i in range(3, 12):
				ws.write(i-2, 2, i, style)
			ws.write_merge(1, 10, 0, 0, str(model.upper()), style)
			ws.write_merge(1, 10, 1, 1, str(pass_standard * 100)+'%', style)
			ws.write_merge(1, 10, 3, 3, 'Ant-A', style)
			ws.write_merge(1, 10, 6, 6, 'Ant-B', style)
			ws.write(10, 4, data_tmp[1][1], style)
			ws.write(10, 7, data_tmp[2][1], style)
			for channle_info in data_tmp[1][0]:
				print channle_info
				if int(channle_info[0]) > 2:
					ws.write(int(channle_info[0])-2, 4, int(channle_info[1]), style)
					ws.write(int(channle_info[0])-2, 5, str(channle_info[2]), style)
			for channle_info in data_tmp[2][0]:
				if int(channle_info[0]) > 2:
					ws.write(int(channle_info[0])-2, 7, int(channle_info[1]), style)
					ws.write(int(channle_info[0])-2, 8, str(channle_info[2]), style)
		else:
			for i in range(1, 14):
				ws.write(i, 2, i, style)
			ws.write_merge(1, 14, 0, 0, str(model.upper()), style)
			ws.write_merge(1, 14, 1, 1, str(pass_standard * 100)+'%', style)
			ws.write_merge(1, 14, 3, 3, 'Ant-A', style)
			ws.write_merge(1, 14, 6, 6, 'Ant-B', style)
			ws.write(14, 4, data_tmp[1][1], style)
			ws.write(14, 7, data_tmp[2][1], style)
			for channle_info in data_tmp[1][0]:
				print channle_info
				ws.write(int(channle_info[0]), 4, int(channle_info[1]), style)
				ws.write(int(channle_info[0]), 5, str(channle_info[2]), style)
			for channle_info in data_tmp[2][0]:
				ws.write(int(channle_info[0]), 7, int(channle_info[1]), style)
				ws.write(int(channle_info[0]), 8, str(channle_info[2]), style)
	w.save(os.path.join(log_path,excel_name))
	
	print data_list
 
def rx_data_sum_excel_5G(log_path, excel_name, pass_standard, model):
	data_list = []
	dir_dirNames = os.listdir(log_path)
	#print dir_dirNames
	index = 0
	index = get_rate_min_ok(rate_11G, dir_dirNames, log_path, data_list, pass_standard, index)
	index = get_rate_min_ok(rate_11N_20M, dir_dirNames, log_path, data_list, pass_standard, index)
	index = get_rate_min_ok(rate_11N_40M, dir_dirNames, log_path, data_list, pass_standard, index)
	index = get_rate_min_ok(rate_5G_20M, dir_dirNames, log_path, data_list, pass_standard, index)
	index = get_rate_min_ok(rate_5G_40M, dir_dirNames, log_path, data_list, pass_standard, index)
	index = get_rate_min_ok(rate_5G_80M, dir_dirNames, log_path, data_list, pass_standard, index)

	
	w=Workbook()
	style = XFStyle()
	al = Alignment()
	al.horz = Alignment.HORZ_CENTER
	al.vert = Alignment.VERT_CENTER
	style.alignment = al
	fnt = Font()  
	fnt.height = 200  
	style.font = fnt
	for data_tmp in data_list:
		ws=w.add_sheet(data_tmp[0])
		ws.write(0, 0, 'device', style)
		ws.write(0, 1, 'standard', style)
		ws.write(0, 2, 'channel', style)
		ws.write(0, 3, 'ANT', style)
		ws.write(0, 4, 'power', style)
		ws.write(0, 5, 'Percent', style)
		ws.write(0, 6, 'ANT', style)
		ws.write(0, 7, 'power', style)
		ws.write(0, 8, 'Percent', style)
		if '40' in data_tmp[0]:
			ws.write_merge(1, 7, 0, 0, str(model.upper()), style)
			ws.write_merge(1, 7, 1, 1, str(pass_standard * 100)+'%', style)
			ws.write_merge(1, 7, 3, 3, 'Ant-A', style)
			ws.write_merge(1, 7, 6, 6, 'Ant-B', style)
			ws.write(7, 4, data_tmp[1][1], style)
			ws.write(7, 7, data_tmp[2][1], style)
			ws.write(1, 2, 38, style)
			ws.write(2, 2, 46, style)
			ws.write(3, 2, 54, style)
			ws.write(4, 2, 62, style)
			ws.write(5, 2, 151, style)
			ws.write(6, 2, 159, style)
			for channle_info in data_tmp[1][0]:
				if int(channle_info[0]) < 151:
					ws.write((int(channle_info[0])-38)/8 + 1, 4, int(channle_info[1]), style)
					ws.write((int(channle_info[0])-38)/8 +1, 5, str(channle_info[2]), style)
				else:
					ws.write((int(channle_info[0])-151)/8 + 5, 4, int(channle_info[1]), style)
					ws.write((int(channle_info[0])-151)/8 +5, 5, str(channle_info[2]), style)
			for channle_info in data_tmp[2][0]:
				if int(channle_info[0]) < 151:
					ws.write((int(channle_info[0])-38)/8 + 1, 7, int(channle_info[1]), style)
					ws.write((int(channle_info[0])-38)/8 +1, 8, str(channle_info[2]), style)
				else:
					ws.write((int(channle_info[0])-151)/8 + 5, 7, int(channle_info[1]), style)
					ws.write((int(channle_info[0])-151)/8 +5, 8, str(channle_info[2]), style)
		elif '80' in data_tmp[0]:
			ws.write_merge(1, 4, 0, 0, str(model.upper()), style)
			ws.write_merge(1, 4, 1, 1, str(pass_standard * 100)+'%', style)
			ws.write_merge(1, 4, 3, 3, 'Ant-A', style)
			ws.write_merge(1, 4, 6, 6, 'Ant-B', style)
			ws.write(4, 4, data_tmp[1][1], style)
			ws.write(4, 7, data_tmp[2][1], style)
			ws.write(1, 2, 42, style)
			ws.write(2, 2, 58, style)
			ws.write(3, 2, 155, style)
			for channle_info in data_tmp[1][0]:
				if int(channle_info[0]) < 155:
					ws.write((int(channle_info[0])-42)/16 + 1, 4, int(channle_info[1]), style)
					ws.write((int(channle_info[0])-42)/16 +1, 5, str(channle_info[2]), style)
				else:
					ws.write((int(channle_info[0])-155)/16 + 3, 4, int(channle_info[1]), style)
					ws.write((int(channle_info[0])-155)/16 +3, 5, str(channle_info[2]), style)
			for channle_info in data_tmp[2][0]:
				if int(channle_info[0]) < 151:
					ws.write((int(channle_info[0])-42)/16 + 1, 7, int(channle_info[1]), style)
					ws.write((int(channle_info[0])-42)/16 +1, 8, str(channle_info[2]), style)
				else:
					ws.write((int(channle_info[0])-155)/16 + 3, 7, int(channle_info[1]), style)
					ws.write((int(channle_info[0])-155)/16 +3, 8, str(channle_info[2]), style)
		else:
			ws.write_merge(1, 14, 0, 0, str(model.upper()), style)
			ws.write_merge(1, 14, 1, 1, str(pass_standard * 100)+'%', style)
			ws.write_merge(1, 14, 3, 3, 'Ant-A', style)
			ws.write_merge(1, 14, 6, 6, 'Ant-B', style)
			ws.write(14, 4, data_tmp[1][1], style)
			ws.write(14, 7, data_tmp[2][1], style)
			channel = 36
			for i in range(1, 14):
				ws.write(i, 2, channel, style)
				channel = channel + 4
				if channel == 68:
					channel = 149
			for channle_info in data_tmp[1][0]:
				if int(channle_info[0]) < 149:
					ws.write((int(channle_info[0])-36)/4 + 1, 4, int(channle_info[1]), style)
					ws.write((int(channle_info[0])-36)/4 +1, 5, str(channle_info[2]), style)
				else:
					ws.write((int(channle_info[0])-149)/4 + 9, 4, int(channle_info[1]), style)
					ws.write((int(channle_info[0])-149)/4 +9, 5, str(channle_info[2]), style)
			for channle_info in data_tmp[2][0]:
				if int(channle_info[0]) < 149:
					ws.write((int(channle_info[0])-36)/4 + 1, 7, int(channle_info[1]), style)
					ws.write((int(channle_info[0])-36)/4 +1, 8, str(channle_info[2]), style)
				else:
					ws.write((int(channle_info[0])-149)/4 + 9, 7, int(channle_info[1]), style)
					ws.write((int(channle_info[0])-149)/4 +9, 8, str(channle_info[2]), style)
	w.save(os.path.join(log_path,excel_name))
	
	print data_list

def rx_data_sum_excel(log_path, excel_name, pass_standard, model, band):
	if band.upper() == '2.4G':
		rx_data_sum_excel_2_4G(log_path, excel_name, pass_standard, model)
	else:
		rx_data_sum_excel_5G(log_path, excel_name, pass_standard, model)

	
def mkLoginDir(band_set=band):
	dir=LOGPATH+time.strftime('RX_%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))+'_'+str(band)+'_'+model
	print dir
	if not os.path.exists(dir):
		os.mkdir(dir)
	return dir			
					
def readwireATT_single(file, channel_list):
	with open(file, 'r') as af:
		af_reader = csv.reader(af)
		for line in af_reader:
			for channel in channel_list:
				if line[0].isdigit():
					if int(line[0]) == (channel[0] -1)*5 + freq_base_2_4g:
						channel[1] =  float(line[1])
					if int(line[0]) == (channel[0] -36) / 2 *10 + freq_base_5GLow:
						channel[1] =  float(line[1])
					if int(line[0]) == (channel[0] -149) / 2 *10 + freq_base_5GHigh:
						channel[1] =  float(line[1])				
					
def readwiresATT(afile, bfile):
	readwireATT_single(afile, A_channel_2_4G)
	readwireATT_single(bfile, B_channel_2_4G)
	readwireATT_single(afile, A_channel_2_4G_40M)
	readwireATT_single(bfile, B_channel_2_4G_40M)
	readwireATT_single(afile, A_channel_5G_20M)
	readwireATT_single(bfile, B_channel_5G_20M)
	readwireATT_single(afile, A_channel_5G_40M)
	readwireATT_single(bfile, B_channel_5G_40M)
	readwireATT_single(afile, A_channel_5G_80M)
	readwireATT_single(bfile, B_channel_5G_80M)
	
def readPowerFile_single(file, rate_list):
	with open(file, 'r') as fd:
		lines = fd.readlines()
		for rate in rate_list:
			for line in lines:
				if line.split(',')[0].upper() == rate[0].upper():
					rate[3] = int(line.split(',')[1])
					break
					
def readPowerFile(file):
	readPowerFile_single(file, rate_11B)
	readPowerFile_single(file, rate_11G)
	readPowerFile_single(file, rate_11N_20M)
	readPowerFile_single(file, rate_11N_40M)
	readPowerFile_single(file, rate_5G_20M)
	readPowerFile_single(file, rate_5G_40M)
	readPowerFile_single(file, rate_5G_80M)
	
def connect_WT_server(wt_server=wt_server):
	wt = WT_TestLibrary.WT_TestLibrary()
	wt.init_WT_Test(wt_server)
	ret = wt.WT_Connect()
	if ret != WT_ERR_CODE_OK:
		print 'WT_VSG_Connect set fail: %d' % ret
		sys.exit()
	return wt			

def record_mp_rx_file_RTL_serial(wt, ser, log_dir, channel, bandWidth_set, rate, ant, repeat=1000, waveType=SIG_USERFILE, rfPort=RF_PORT_Default, wave_gap=200):
	rx_success = 1
	rx_ok_percent = 1
	wave = wave_file_base + rate[2]
	power_start = rate[3]
	print 'wave: %s\n' % wave
	print 'power_start: %d\n' % power_start
	print 'channel: %d, channel_external_att: %f\n' % (channel[0], channel[1])
	record_file_name =log_dir + '/'+ant.upper()+'_channel_' + str(channel[0]) + '_' +str(rate[0])+'.txt'
	print record_file_name
	os.system('echo power,	 Rx_OK,	 send_total,  RX_OK_Percent >' +record_file_name)
	ser.set_mp_rx_cfg(channel[0], rate[1], bandWidth_set, ant, interface=mp_iface)
	time.sleep(3)
	while (power_start > power_end) and (rx_ok_percent >= rx_ok_minPer or rx_ok_percent == -1):
		ser.start_mp_rx(interface=mp_iface)
		if  channel[0] < 36:
			vsg_freq_set = ((channel[0] -1)*5 + freq_base_2_4g) * 1e6
		elif channel[0] >= 149:
			vsg_freq_set = ((channel[0] -149) / 2 *10 + freq_base_5GHigh) * 1e6
		else:
			vsg_freq_set = ((channel[0] -36) / 2 *10 + freq_base_5GLow) * 1e6
		print vsg_freq_set
		ret = wt.WT_SetVSG(vsg_freq_set, power_start+channel[1], waveType, wave_gap, rfPort, repeat, wave)
		if ret != WT_ERR_CODE_OK:
			print 'wt_SetVSG set fail: %d' % ret
			sys.exit()
		ret = wt.WT_AsynStartVSG()
		if ret != WT_ERR_CODE_OK:
			print 'WT_AsynStartVSG fail: %d' % ret
			sys.exit() 
		time.sleep(1.5)
		ser.stop_mp_rx(interface=mp_iface)
		ret = wt.WT_StopVSG()
		if ret != WT_ERR_CODE_OK:
			print 'WT_StopVSG fail: %d' % ret
			sys.exit() 
		tx_ok, rx_ok = ser.mp_query(interface=mp_iface)
		if rx_ok.isdigit():
			rx_ok_percent = round(float(float(rx_ok) / float(repeat)), 4)
			print 'rx_ok: %d, rx_ok_percent: %f\n' %(int(rx_ok), rx_ok_percent)
		else:
			rx_ok = -1
			rx_ok_percent = -1
		os.system('echo ' +str(power_start) + '	 '+ str(rx_ok) + '	 '+str(repeat) + '	 ' + str( rx_ok_percent * 100)+ '%' + '>> ' + record_file_name)
		power_start = power_start -1
		
def record_mp_rx_file_MTK_serial(wt, ser, log_dir, channel, bandWidth_set, rate, ant, FREQOFFSET=MTK_2_4G_FREQOFFSET, repeat=1000, waveType=SIG_USERFILE, rfPort=RF_PORT_Default, wave_gap=200):
	rx_success = 1
	rx_ok_percent = 1
	wave = wave_file_base + rate[2]
	power_start = rate[3]
	print 'wave: %s\n' % wave
	print 'power_start: %d\n' % power_start
	print 'channel: %d, channel_external_att: %f\n' % (channel[0], channel[1])
	record_file_name =log_dir + '/'+ant.upper()+'_channel_' + str(channel[0]) + '_' +str(rate[0])+'.txt'
	print record_file_name
	os.system('echo power,	 Rx_OK,	 send_total,  RX_OK_Percent >' +record_file_name)
	ser.set_mp_rx_cfg(channel[0], rate[1], bandWidth_set, ant, FREQOFFSET, interface=mp_iface)
	time.sleep(3)
	while (power_start > power_end) and (rx_ok_percent >= rx_ok_minPer or rx_ok_percent == -1):
		if  channel[0] < 36:
			vsg_freq_set = ((channel[0] -1)*5 + freq_base_2_4g) * 1e6
		elif channel[0] >= 149:
			vsg_freq_set = ((channel[0] -149) / 2 *10 + freq_base_5GHigh) * 1e6
		else:
			vsg_freq_set = ((channel[0] -36) / 2 *10 + freq_base_5GLow) * 1e6
		ret = wt.WT_SetVSG(vsg_freq_set, power_start+round(channel[1], 1), waveType, wave_gap, rfPort, repeat, wave)
		if ret != WT_ERR_CODE_OK:
			print 'wt_SetVSG set fail: %d' % ret
			sys.exit() 
		ret = wt.WT_AsynStartVSG()
		if ret != WT_ERR_CODE_OK:
			print 'WT_AsynStartVSG fail: %d' % ret
			sys.exit() 
		time.sleep(1.5)
		ret = wt.WT_StopVSG()
		if ret != WT_ERR_CODE_OK:
			print 'WT_StopVSG fail: %d' % ret
			sys.exit()
		rx_ok = ser.mp_query(interface=mp_iface)
		if band.upper() == '2.4G':
			ser.reset_mp_rx_2_4G(interface=mp_iface)
		elif band.upper() == '5G':
			ser.reset_mp_rx_5G(interface=mp_iface)
		else:
			raise Exception("band error %s") % band
		if str(rx_ok).isdigit():
			rx_ok_percent = round(float(float(rx_ok) / float(repeat)), 4)
			print 'rx_ok: %d, rx_ok_percent: %f\n' %(int(rx_ok), rx_ok_percent)
		else:
			rx_ok = -1
			rx_ok_percent = -1
		os.system('echo ' +str(power_start) + '	 '+ str(rx_ok) + '	 '+str(repeat) + '	 ' + str( rx_ok_percent * 100)+ '%' + '>> ' + record_file_name)
		power_start = power_start -1

def mp_rx_RTL_serial(channel_list, rate_list, wt, ser, log_dir, bandWidth_set, ant, repeat=1000, waveType=SIG_USERFILE, rfPort=RF_PORT_Default, wave_gap=200):
	for channel in channel_list:
		for rate in rate_list:
			record_mp_rx_file_RTL_serial(wt, ser, log_dir, channel, bandWidth_set, rate, ant, repeat, waveType, rfPort,wave_gap)
			
def mp_rx_MTK_serial(channel_list, rate_list, wt, ser, log_dir, bandWidth_set, ant, FREQOFFSET, repeat=1000, waveType=SIG_USERFILE, rfPort=RF_PORT_Default, wave_gap=200):
	for channel in channel_list:
		for rate in rate_list:
			record_mp_rx_file_MTK_serial(wt, ser, log_dir, channel, bandWidth_set, rate, ant, FREQOFFSET, repeat, waveType, rfPort,wave_gap)			
			
if __name__ == '__main__':
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hP:c:a:b:m:u:p:s:f:i:e:C:r:B:S:", ["help","Power_file=","mode=", "client_ip=", "username=", "password=", "server=", "finish=", "interface=", "external_att=", "COM=", "rate=", "Band=", "fa=", "fb=", "Standard="])
	except getopt.GetoptError:
		print "getopt error!"
	if len(opts) == 0:
		usage()
		sys.exit()
	for o,a in opts:
		if o in ("-h","--help"):
			usage()
			sys.exit()
		elif o in ("-P","--Power_file"):
			power_start_file=a
			print 'power_start_file: %s\n' % power_start_file
		elif o in ("-m","--mode"):
			model=a.upper()
			print 'mode: %s\n' % model
		elif o in ("-s","--server"):
			wt_server=a
			print 'wt_server: %s\n' % wt_server
		elif o in ("-c","--client_ip"):
			client_ip=a
			print 'client_ip: %s\n' % client_ip
		elif o in ("-u","--username"):
			username=a
			print 'username: %s\n' % username
		elif o in ("-p","--password"):
			password=a
			print 'password: %s\n' % password
		elif o in ("-f","--finish"):
			finish=a
			print 'finish: %s\n' % finish	
		elif o in ("-i","--interface"):
			mp_iface=a
			print 'mp_iface: %s\n' % mp_iface
		elif o in ("-e","--external_att"):
			external_att=float(a)
			print 'external_att: %f\n' % external_att
		elif o in ("-C","--COM"):
			COM=str(a)
			print 'COM: %s\n' % COM
		elif o in ("-B","--Band"):
			band=a.upper()
			print 'Band: %s\n' % band
		elif o in ("-r","--rate"):
			bps=int(a)
			print 'bps: %d\n' % bps
		elif o in ("-a", "--fa"):
			a_wireAtt_file=a
			print 'a_wireAtt_file: %s\n' % a_wireAtt_file
		elif o in ("-b", "--fb"):
			b_wireAtt_file=a
			print 'b_wireAtt_file: %s\n' % b_wireAtt_file
		elif o in ("-S", "--Standard"):
			pass_standard=float(a)
			print 'pass_standard: %f\n' % pass_standard
		else:
			usage()
			sys.exit()
	print 'mp_iface: %s\n' % mp_iface
	
	#wt = connect_WT_server()
	#log_dir = mkLoginDir()
	log_dir = './log/RX_2017-01-09-11-26-29_2.4G_97F-7358/'

	readwiresATT(a_wireAtt_file, b_wireAtt_file)
	print A_channel_2_4G
	print B_channel_2_4G
	print '------------5G_20M-----------'
	print A_channel_5G_20M
	print B_channel_5G_20M
	print '------------5G_40M-----------'
	print A_channel_5G_40M
	print B_channel_5G_40M
	print '------------5G_80M-----------'
	print A_channel_5G_80M
	print B_channel_5G_80M	
	readPowerFile(power_start_file)
	print rate_11B
	print rate_11G
	print rate_11N_20M
	print rate_11N_40M
	print rate_5G_20M
	print rate_5G_40M
	print rate_5G_80M
	'''
	if band.upper() == '2.4G':
		if model in RTL_model:
			ser = RTL_MP_Serial.RTL_MP_Serial(COM, bps, finish)
			ser.mp_start(interface=mp_iface)
			#ANTA_A_11B
			mp_rx_RTL_serial(A_channel_2_4G, rate_11B, wt, ser, log_dir, bandWidth_20M_RTL, 'A')
			#ANTA_A_11G
			mp_rx_RTL_serial(A_channel_2_4G, rate_11G, wt, ser, log_dir, bandWidth_20M_RTL, 'A')
			#ANTA_A_11N_20M
			mp_rx_RTL_serial(A_channel_2_4G, rate_11N_20M , wt, ser, log_dir, bandWidth_20M_RTL, 'A')
			#ANTA_A_11N_40M
			mp_rx_RTL_serial(A_channel_2_4G_40M, rate_11N_40M, wt, ser, log_dir, bandWidth_40M_RTL,'A')
			
			mp_rx_RTL_serial(B_channel_2_4G, rate_11B, wt, ser, log_dir, bandWidth_20M_RTL, 'B')
			#ANTA_A_11G
			mp_rx_RTL_serial(B_channel_2_4G, rate_11G, wt, ser, log_dir, bandWidth_20M_RTL, 'B')
			#ANTA_A_11N_20M
			mp_rx_RTL_serial(B_channel_2_4G, rate_11N_20M, wt, ser, log_dir, bandWidth_20M_RTL, 'B')
			#ANTA_A_11N_40M
			mp_rx_RTL_serial(B_channel_2_4G_40M, rate_11N_40M, wt, ser, log_dir, bandWidth_40M_RTL, 'B')
			
			ser.ser.serial_close()
		elif model.upper() in MTK_model:
			print 'MTK_model\n'
			if model.upper() == 'R1':
				print 'R1 RX test---------------'
				#ANTA_A_11B
				ser = MTK_MP_Serial.MTK_MP_Serial(COM, bps, finish)
				mp_rx_MTK_serial(A_channel_2_4G, rate_11B, wt, ser, log_dir, bandWidth_20M_MTK, 'A', MTK_2_4G_FREQOFFSET)
				#ANTA_A_11G
				mp_rx_MTK_serial(A_channel_2_4G, rate_11G, wt, ser, log_dir, bandWidth_20M_MTK, 'A', MTK_2_4G_FREQOFFSET)
				#ANTA_A_11N_20M
				mp_rx_MTK_serial(A_channel_2_4G, rate_11N_20M, wt, ser, log_dir, bandWidth_20M_MTK, 'A', MTK_2_4G_FREQOFFSET)
				#ANTA_A_11N_40M
				mp_rx_MTK_serial(A_channel_2_4G_40M, rate_11N_40M, wt, ser, log_dir, bandWidth_40M_MTK, 'A', MTK_2_4G_FREQOFFSET)
			else:
				#ANTA_A_11B
				ser = MTK_MP_Serial.MTK_MP_Serial(COM, bps, finish)
				mp_rx_MTK_serial(A_channel_2_4G, rate_11B, wt, ser, log_dir, bandWidth_20M_MTK, 'A', MTK_2_4G_FREQOFFSET)
				#ANTA_A_11G
				mp_rx_MTK_serial(A_channel_2_4G, rate_11G, wt, ser, log_dir, bandWidth_20M_MTK, 'A', MTK_2_4G_FREQOFFSET)
				#ANTA_A_11N_20M
				mp_rx_MTK_serial(A_channel_2_4G, rate_11N_20M, wt, ser, log_dir, bandWidth_20M_MTK, 'A', MTK_2_4G_FREQOFFSET)
				#ANTA_A_11N_40M
				mp_rx_MTK_serial(A_channel_2_4G_40M, rate_11N_40M, wt, ser, log_dir, bandWidth_40M_MTK, 'A', MTK_2_4G_FREQOFFSET)
			
				mp_rx_MTK_serial(B_channel_2_4G, rate_11B, wt, ser, log_dir, bandWidth_20M_MTK, 'B', MTK_2_4G_FREQOFFSET)
				#ANTA_A_11G
				mp_rx_MTK_serial(B_channel_2_4G, rate_11G, wt, ser, log_dir, bandWidth_20M_MTK, 'B', MTK_2_4G_FREQOFFSET)
				#ANTA_A_11N_20M
				mp_rx_MTK_serial(B_channel_2_4G, rate_11N_20M, wt, ser, log_dir, bandWidth_20M_MTK, 'B', MTK_2_4G_FREQOFFSET)
				#ANTA_A_11N_40M
				mp_rx_MTK_serial(B_channel_2_4G_40M, rate_11N_40M, wt, ser, log_dir, bandWidth_40M_MTK, 'B', MTK_2_4G_FREQOFFSET)
				ser.ser.serial_close()
	elif band.upper() == '5G':
		if model in RTL_model:
			print 'RTL mode\n'
			#ANTA_A_11B
			ser = RTL_MP_Serial.RTL_MP_Serial(COM, bps, finish)
			ser.mp_start_5g(interface=mp_iface)
			#ANTA_A_OFDM
			mp_rx_RTL_serial(A_channel_5G_20M, rate_11G, wt, ser, log_dir, bandWidth_20M_RTL, 'A')
			#NTA_A_11N_20M
			mp_rx_RTL_serial(A_channel_5G_20M, rate_11N_20M, wt, ser, log_dir, bandWidth_20M_RTL, 'A')
			#NTA_A_11N_40M
			mp_rx_RTL_serial(A_channel_5G_40M, rate_11N_40M, wt, ser, log_dir, bandWidth_40M_RTL, 'A')
			#ANTA_A_VHT20
			mp_rx_RTL_serial(A_channel_5G_20M, rate_5G_20M, wt, ser, log_dir, bandWidth_20M_RTL, 'A')
			#ANTA_A_VHT40
			mp_rx_RTL_serial(A_channel_5G_40M, rate_5G_40M, wt, ser, log_dir, bandWidth_40M_RTL, 'A')
			#ANTA_A_VHT80
			mp_rx_RTL_serial(A_channel_5G_80M, rate_5G_80M, wt, ser, log_dir, bandWidth_80M_RTL, 'A')
			#ANTA_B_OFDM
			mp_rx_RTL_serial(B_channel_5G_20M, rate_11G, wt, ser, log_dir, bandWidth_20M_RTL, 'B')
			#NTA_B_11N_20M
			mp_rx_RTL_serial(B_channel_5G_20M, rate_11N_20M, wt, ser, log_dir, bandWidth_20M_RTL, 'B')
			#NTA_B_11N_40M
			mp_rx_RTL_serial(B_channel_5G_40M, rate_11N_40M, wt, ser, log_dir, bandWidth_40M_RTL, 'B')
			#ANTA_B_VHT20
			mp_rx_RTL_serial(B_channel_5G_20M, rate_5G_20M, wt, ser, log_dir, bandWidth_20M_RTL, 'B')
			#ANTA_B_VHT40
			mp_rx_RTL_serial(B_channel_5G_40M, rate_5G_40M, wt, ser, log_dir, bandWidth_40M_RTL, 'B')
			#ANTA_B_VHT80
			mp_rx_RTL_serial(B_channel_5G_80M, rate_5G_80M, wt, ser, log_dir, bandWidth_80M_RTL, 'B')
			
			ser.ser.serial_close()
		elif model.upper() in MTK_model:
			print 'MTK_model\n'
			#ANTA_A_11B
			ser = MTK_MP_Serial.MTK_MP_Serial(COM, bps, finish)
			#ANTA_A_OFDM
			
			mp_rx_MTK_serial(A_channel_5G_20M, rate_11G, wt, ser, log_dir, bandWidth_20M_MTK, 'A', MTK_5G_FREQOFFSET)
			#NTA_A_11N_20M
			mp_rx_MTK_serial(A_channel_5G_20M, rate_11N_20M, wt, ser, log_dir, bandWidth_20M_MTK, 'A', MTK_5G_FREQOFFSET)
			#NTA_A_11N_40M
			mp_rx_MTK_serial(A_channel_5G_40M, rate_11N_40M, wt, ser, log_dir, bandWidth_40M_MTK, 'A', MTK_5G_FREQOFFSET)	
			#ANTA_A_VHT20
			mp_rx_MTK_serial(A_channel_5G_20M, rate_5G_20M, wt, ser, log_dir, bandWidth_20M_MTK, 'A', MTK_5G_FREQOFFSET)
			#ANTA_A_VHT40
			mp_rx_MTK_serial(A_channel_5G_40M, rate_5G_40M, wt, ser, log_dir, bandWidth_40M_MTK, 'A', MTK_5G_FREQOFFSET)
			#ANTA_A_VHT80
			mp_rx_MTK_serial(A_channel_5G_80M, rate_5G_80M, wt, ser, log_dir, bandWidth_80M_MTK, 'A', MTK_5G_FREQOFFSET)

			#ANTA_B_OFDM
			mp_rx_MTK_serial(B_channel_5G_20M, rate_11G, wt, ser, log_dir, bandWidth_20M_MTK, 'B', MTK_5G_FREQOFFSET)
			#NTA_B_11N_20M
			mp_rx_MTK_serial(B_channel_5G_20M, rate_11N_20M, wt, ser, log_dir, bandWidth_20M_MTK, 'B', MTK_5G_FREQOFFSET)
			#NTA_B_11N_40M
			mp_rx_MTK_serial(B_channel_5G_40M, rate_11N_40M, wt, ser, log_dir, bandWidth_40M_MTK, 'B', MTK_5G_FREQOFFSET)	
			#ANTA_B_VHT20
			mp_rx_MTK_serial(B_channel_5G_20M, rate_5G_20M, wt, ser, log_dir, bandWidth_20M_MTK, 'B', MTK_5G_FREQOFFSET)
			##ANTA_B_VHT40
			mp_rx_MTK_serial(B_channel_5G_40M, rate_5G_40M, wt, ser, log_dir, bandWidth_40M_MTK, 'B', MTK_5G_FREQOFFSET)
			##ANTA_B_VHT80
			mp_rx_MTK_serial(B_channel_5G_80M, rate_5G_80M, wt, ser, log_dir, bandWidth_80M_MTK, 'B', MTK_5G_FREQOFFSET)
			ser.ser.serial_close()
	'''
	excel_name = model+'_'+str(band)+'_'+time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))+'.xls'
	rx_data_sum_excel(log_dir, excel_name, pass_standard, model.upper(), band)
	print "here is :",sys._getframe().f_lineno 
