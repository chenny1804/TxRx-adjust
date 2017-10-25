import csv
import time
import os
import sys
import string
import re
reload(sys) 
sys.setdefaultencoding('utf8')

from pyExcelerator import *
rate_11B = [['1M', 2, '1 Mbps(DSSS).csv'], ['2M', 4, '2 Mbps(DSSS).csv'], ['5.5M', 11, '5.5 Mbps(DSSS).csv'], ['11M', 22, '11 Mbps(DSSS).csv']]
rate_11G = [['6M', 12, '6 Mbps(OFDM).csv'], ['9M', 18, '9 Mbps(OFDM).csv'], ['12M', 24, '12 Mbps(OFDM).csv'], ['18M', 36, '18 Mbps(OFDM).csv'], ['24M', 48, '24 Mbps(OFDM).csv'], ['36M', 72, '36 Mbps(OFDM).csv'], ['48M', 96, '48 Mbps(OFDM).csv'], ['54M', 108, '54 Mbps(OFDM).csv']]
rate_11N_base = 128
rate_11N_20M = [['HT20-MCS0', 128, 'HT20-MCS0.CSV'], ['HT20-MCS1', 129, 'HT20-MCS1.CSV'], ['HT20-MCS2', 130, 'HT20-MCS2.CSV'], ['HT20-MCS3', 131, 'HT20-MCS3.CSV'],['HT20-MCS4', 132, 'HT20-MCS4.CSV'],['HT20-MCS5', 133, 'HT20-MCS5.CSV'],['HT20-MCS6', 134, 'HT20-MCS6.CSV'],['HT20-MCS7', 135, 'HT20-MCS7.CSV']]
rate_11N_40M = [['HT40-MCS0', 128, 'HT40-MCS0.CSV'], ['HT40-MCS1', 129, 'HT40-MCS1.CSV'], ['HT40-MCS2', 130, 'HT40-MCS2.CSV'], ['HT40-MCS3', 131, 'HT40-MCS3.CSV'],['HT40-MCS4', 132, 'HT40-MCS4.CSV'],['HT40-MCS5', 133, 'HT40-MCS5.CSV'],['HT40-MCS6', 134, 'HT40-MCS6.CSV'],['HT40-MCS7', 135, 'HT40-MCS7.CSV']]

rate_5G_20M = [['VHT20-MCS0', 128, 'VHT20-MCS0.CSV'], ['VHT20-MCS1', 129, 'VHT20-MCS1.CSV'], ['VHT20-MCS2', 130, 'VHT20-MCS2.CSV'], ['VHT20-MCS3', 131, 'VHT20-MCS3.CSV'],['VHT20-MCS4', 132, 'VHT20-MCS4.CSV'],['VHT20-MCS5', 133, 'VHT20-MCS5.CSV'],['VHT20-MCS6', 134, 'VHT20-MCS6.CSV'],['VHT20-MCS7', 135, 'VHT20-MCS7.CSV'],['VHT20-MCS8', 135, 'VHT20-MCS8.CSV']]
rate_5G_40M = [['VHT40-MCS0', 128, 'VHT40-MCS0.CSV'], ['VHT40-MCS1', 129, 'VHT40-MCS1.CSV'], ['VHT40-MCS2', 130, 'VHT40-MCS2.CSV'], ['VHT40-MCS3', 131, 'VHT40-MCS3.CSV'],['VHT40-MCS4', 132, 'VHT40-MCS4.CSV'],['VHT40-MCS5', 133, 'VHT40-MCS5.CSV'],['VHT40-MCS6', 134, 'VHT40-MCS6.CSV'],['VHT40-MCS7', 135, 'VHT40-MCS7.CSV'],['VHT40-MCS8', 135, 'VHT40-MCS8.CSV'],['VHT40-MCS9', 135, 'VHT40-MCS9.CSV']]
rate_5G_80M = [['VHT80-MCS0', 128, 'VHT80-MCS0.CSV'], ['VHT80-MCS1', 129, 'VHT80-MCS1.CSV'], ['VHT80-MCS2', 130, 'VHT80-MCS2.CSV'], ['VHT80-MCS3', 131, 'VHT80-MCS3.CSV'],['VHT80-MCS4', 132, 'VHT80-MCS4.CSV'],['VHT80-MCS5', 133, 'VHT80-MCS5.CSV'],['VHT80-MCS6', 134, 'VHT80-MCS6.CSV'],['VHT80-MCS7', 135, 'VHT80-MCS7.CSV'],['VHT80-MCS8', 135, 'VHT80-MCS8.CSV'],['VHT80-MCS9', 135, 'VHT80-MCS9.CSV']]

pass_standard = 0.5

def get_rate_min_ok(rate_list, file_list, log_path, data_list, pass_standard=pass_standard, index=0):
	power = -1
	rx_ok_percent = -1
	for rate in rate_list:
		data_list.append([rate[0], [[], []], [[], []]])
		for dirName in file_list:
			filename_list = dirName.split('.txt')[0].split('_')
			if filename_list[3] == rate[0]:
				with open( os.path.join(log_path, dirName), 'r') as fd:
					lines = fd.readlines()
					j = 1
					for line in lines[1:]:
						line_list = re.split('\s+', line.strip())
						if line_list[0] != line and float(line_list[3][0:-1]) < pass_standard * 100:
							#print 'break: %d\n' % j
							break
						j = j + 1
					if j != 1:
						j = j -1
						line_list = re.split('\s+', lines[j].strip())
						power = int(line_list[0])
						rx_ok_percent = line_list[3]
				if filename_list[0].upper() == 'A':
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
	
def rx_data_sum_excel(log_path, excel_name, pass_standard, model):
	data_list = []
	dir_dirNames = os.listdir(log_path)
	#print dir_dirNames
	index = 0
	index = get_rate_min_ok(rate_11B, dir_dirNames, log_path, data_list, pass_standard, index)
	index = get_rate_min_ok(rate_11G, dir_dirNames, log_path, data_list, pass_standard, index)
	index = get_rate_min_ok(rate_11N_20M, dir_dirNames, log_path, data_list, pass_standard, index)
	index = get_rate_min_ok(rate_11N_40M, dir_dirNames, log_path, data_list, pass_standard, index)
	
	w=Workbook()
	for data_tmp in data_list:
		ws=w.add_sheet(data_tmp[0])
		ws.write(0, 0, 'device')
		ws.write(0, 1, 'standard')
		ws.write(0, 2, 'channel')
		ws.write(0, 3, 'ANT')
		ws.write(0, 4, 'power')
		ws.write(0, 5, 'Percent')
		ws.write(0, 6, 'ANT')
		ws.write(0, 7, 'power')
		ws.write(0, 8, 'Percent')
		for i in range(1, 14):
			ws.write(i, 2, i)
		ws.write_merge(1, 14, 0, 0, str(model.upper()))
		ws.write_merge(1, 14, 1, 1, str(pass_standard * 100)+'%')
		ws.write_merge(1, 14, 3, 3, 'Ant-A')
		ws.write_merge(1, 14, 6, 6, 'Ant-B')
		ws.write(14, 4, data_tmp[1][1])
		ws.write(14, 7, data_tmp[2][1])
		for channle_info in data_tmp[1][0]:
			print channle_info
			ws.write(int(channle_info[0]), 4, int(channle_info[1]))
			ws.write(int(channle_info[0]), 5, str(channle_info[2]))
		for channle_info in data_tmp[2][0]:
			ws.write(int(channle_info[0]), 7, int(channle_info[1]))
			ws.write(int(channle_info[0]), 8, str(channle_info[2]))
	w.save(excel_name)
	
	os.system('echo ' + str(data_list) + '> temp.txt')
	print data_list
	
if __name__ == '__main__':
	'''
	w=Workbook()
	ws=w.add_sheet('hello')
	ws.write_merge(0, 0, 0, 1, 'Long Cell')
	ws.write(1, 0, 1)
	ws.write(1, 1, 2)
	ws1=w.add_sheet('hello2')
	ws1.write_merge(0, 2, 0, 0, 'Long Cell')
	ws1.write(0, 1, 1)
	ws1.write(1, 1, 2)
	w.save('test.xls')
	'''
	rx_data_sum_excel('./log/2016-08-01-20-29-04_2.4G_P0', 'P0_rx.xls', 0.92, 'P0')