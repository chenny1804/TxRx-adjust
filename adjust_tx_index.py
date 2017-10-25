# -*- coding: cp936 -*-
import time
import WT_TestLibrary
import Read_TXCFG
import string
import getopt
import os
import sys
import MTK_MP_Serial
import RTL_MP_Serial
import re
import csv
from adjust_xls_report import adjust_xls_report
reload(sys) 
sys.setdefaultencoding('utf8')
from pyExcelerator import *

#校准index，开始、结束和步长
power_index_start=40
power_index_end=63
power_index_step=1

power_start = -10
power_end = -110
rx_ok_minPer = 0.8
ANTA = 'A'
model = 'P1'
MTK_2_4G_FREQOFFSET = 48
MTK_5G_FREQOFFSET = 17
#WT200的地址
wt_server = '192.168.10.254'
#WT200的Tx校准口
RF_PORT_Default = 1
SIG_USERFILE = 0
COM = None
bps = 38400
#串口命令结束符
finish = '$'
mp_iface = 'wlan1'
band = '2.4G'
#日志路径
LOGPATH='./log/'

#wave_file_base = 'C:/Program Files (x86)/xgiga/WT200.wave/'
wave_file_base = 'C:/Program Files/xgiga/WT200.wave/'
Txconfig_file=  './Txconfig_RTL.txt'
#通过标准文件路径
pass_standard_file = './WiFi(B).cfg'
#速率IndexFile
RateIndexFile='RTL_mp_rate.txt'
external_att = 1.45
EVM_min_limit = -60.0
mask_min_limit = 0.0

a_wireAtt_file = None
b_wireAtt_file = None
power_start_file = None
#被测设备型号列表
RTL_model = ['P0', 'P1', 'P2S', '97F', '97F-7357', '97F-7358', '97F-7384','96D']
MTK_model = ['P2', 'R1']

#线材的衰减
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


#基础信道频率值
freq_base_2_4g = 2412
freq_base_5GLow = 5180
freq_base_5GHigh= 5745

#不同模式下的速率对应的A,B两路天线的power index、power的最大最小值、EVM的最大最小值、PPM的最大最小值、以及Mask的最大最小值
#[rate_name, mp_rate_index, [A_mp_power_index, B_mp_power_index], [power_min, power_max], [evm_min, evm_max], [ppm_min, ppm_max], [mask_min, mask_max]]
rate_11B = [['1M', 2, [33, 32], [18, 21], [-60.00, -29.00], [], []], ['2M', 4, [33, 32], [18, 21], [], [], []], ['5.5M', 11, [33, 32], [18, 21], [], [], []], ['11M', 22, [33, 32], [18, 21], [], [], []]]
rate_11G = [['6M', 12, [33, 32], [18, 21], [-60.00, -29.00], [], []], ['9M', 18, [33, 32], [18, 21], [-60.00, -29.00], [], []], ['12M', 24, [33, 32], [18, 21], [-60.00, -29.00], [], []], ['18M', 36, [33, 32], [18, 21], [], [], []], ['24M', 48, [33, 32], [18, 21], [], [], []], ['36M', 72, [33, 32], [18, 21], [], [], []], ['48M', 96, [33, 32], [18, 21], [], [], []], ['54M', 108, [33, 32], [18, 21], [], [], []]]
rate_11N_base = 128
rate_11N_20M = [['HT20-MCS0', 128, [33, 32], [18, 21], [], [], []], ['HT20-MCS1', 129, [33, 32], [18, 21], [], [], []], ['HT20-MCS2', 130, [33, 32], [18, 21], [], [], []], ['HT20-MCS3', 131, [33, 32], [18, 21], [], [], []],['HT20-MCS4', 132, [33, 32], [18, 21], [], [], []],['HT20-MCS5', 133, [33, 32], [18, 21], [], [], []],['HT20-MCS6', 134, [33, 32], [18, 21], [], [], []],['HT20-MCS7', 135, [33, 32], [18, 21], [], [], []]]
rate_11N_40M = [['HT40-MCS0', 128, [33, 32], [18, 21], [], [], []], ['HT40-MCS1', 129, [33, 32], [18, 21], [], [], []], ['HT40-MCS2', 130, [33, 32], [18, 21], [], [], []], ['HT40-MCS3', 131, [33, 32], [18, 21], [], [], []],['HT40-MCS4', 132, [33, 32], [18, 21], [], [], []],['HT40-MCS5', 133, [33, 32], [18, 21], [], [], []],['HT40-MCS6', 134, [33, 32], [18, 21], [], [], []],['HT40-MCS7', 135, [33, 32], [18, 21], [], [], []]]

rate_5G_20M = [['VHT20-MCS0', 128, [33, 32], [18, 21], [], [], []], ['VHT20-MCS1', 129, [33, 32], [18, 21], [], [], []], ['VHT20-MCS2', 130, [33, 32], [18, 21], [], [], []], ['VHT20-MCS3', 131, [33, 32], [18, 21], [], [], []],['VHT20-MCS4', 132, [33, 32], [18, 21], [], [], []],['VHT20-MCS5', 133, [33, 32], [18, 21], [], [], []],['VHT20-MCS6', 134, [33, 32], [18, 21], [], [], []],['VHT20-MCS7', 135, [33, 32], [18, 21], [], [], []],['VHT20-MCS8', 136, [33, 32], [18, 21], [], [], []]]
rate_5G_40M = [['VHT40-MCS0', 128, [33, 32], [18, 21], [], [], []], ['VHT40-MCS1', 129, [33, 32], [18, 21], [], [], []], ['VHT40-MCS2', 130, [33, 32], [18, 21], [], [], []], ['VHT40-MCS3', 131, [33, 32], [18, 21], [], [], []],['VHT40-MCS4', 132, [33, 32], [18, 21], [], [], []],['VHT40-MCS5', 133, [33, 32], [18, 21], [], [], []],['VHT40-MCS6', 134, [33, 32], [18, 21], [], [], []],['VHT40-MCS7', 135, [33, 32], [18, 21], [], [], []],['VHT40-MCS8', 136, [33, 32], [18, 21], [], [], []],['VHT40-MCS9', 137, [33, 32], [18, 21], [], [], []]]
rate_5G_80M = [['VHT80-MCS0', 128, [33, 32], [18, 21], [], [], []], ['VHT80-MCS1', 129, [33, 32], [18, 21], [], [], []], ['VHT80-MCS2', 130, [33, 32], [18, 21], [], [], []], ['VHT80-MCS3', 131, [33, 32], [18, 21], [], [], []],['VHT80-MCS4', 132, [33, 32], [18, 21], [], [], []],['VHT80-MCS5', 133, [33, 32], [18, 21], [], [], []],['VHT80-MCS6', 134, [33, 32], [18, 21], [], [], []],['VHT80-MCS7', 135, [33, 32], [18, 21], [], [], []],['VHT80-MCS8', 136, [33, 32], [18, 21], [], [], []],['VHT80-MCS9', 137, [33, 32], [18, 21], [], [], []]]

channelRate_dict_2_4G = {}
channelRate_dict_5G = {}
channelRate_dict_all = {}


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

#WT_TRIG_TYPE_ENUM
WT_TRIG_TYPE_FREE_RUN = 0       
WT_TRIG_TYPE_EXT = 1                 
WT_TRIG_TYPE_IF = 2
WT_TRIG_TYPE_IF_NO_CAL = 3
#SPECTRUM  
WT_RES_SPECTRUM_CARR_LEAKAGE     =  "Spec_carrier_leakage"
WT_RES_SPECTRUM_OBW_99           =  "Spec_Obw"
WT_RES_SPECTRUM_MASK_ERR_PERCENT =  "Spec_mask_err"
WT_RES_SPECTRUM_PEAK_POW_FREQ    =  "Spec_peak_freq"
WT_RES_SPECTRUM_DATA             =  "Spec_data"
WT_RES_SPECTRUM_MARGIN			 =  "Spec_margin"
WT_RES_CW_FREQ_OFFSET            =  "CW_spec_freq_offset"

#IQ 
WT_RES_RAW_DATA                  =  "Raw_data"

#POWER
WT_RES_POWER_FRAME_CNT           =  "Pow_frame_count"   
WT_RES_POWER_FRAME_DB            =  "Pow_frame"           
WT_RES_POWER_ALL_DB              =  "Pow_all"    
WT_RES_POWER_PEAK_DB             =  "Pow_peak"    


#WIFI Frame
WT_RES_FRAME_EVM_ALL              = "evm.all"   
WT_RES_FRAME_EVM_ALL_PERCENT      = "evm.all(%)"   
WT_RES_FRAME_EVM_PEAK             = "evm.pk"   
WT_RES_FRAME_EVM_PEAK_PERCENT     = "evm.pk(%)"
WT_RES_FRAME_FREQ_ERR             = "signal.freqerr"
WT_RES_FRAME_SYMBOL_CLOCK_ERR     = "signal.symclockerr"
WT_RES_FRAME_IQ_MATCH_AMP         = "iqmatch.amp"  
WT_RES_FRAME_IQ_MATCH_PHASE       = "iqmatch.phase"  
WT_RES_FRAME_PHASE_ERROR 		  = "phase.error"
WT_RES_FRAME_DATA_RATE_MBPS       = "Data_rate_Mbps"
WT_RES_FRAME_RAMP_ON_TIME         = "ramp.on_time"       
WT_RES_FRAME_RAMP_OFF_TIME        = "ramp.off_time"    
WT_RES_FRAME_OFDM_NUMBER_SYMBOLS  = "ofdm.more_res.PLCP.Nspp"
WT_RES_FRAME_EVM_DATA_DB          = "evm.data"          
WT_RES_FRAME_EVM_PILOT_DB         = "evm.pilot"
WT_RES_SPECTRUM_FLATNESS_PASSED   = "flatness.passed"
WT_RES_SPECTRUM_FLATNESS_SECTION_VALUE  =  "flatness.section.value"
WT_RES_SPECTRUM_FLATNESS_SECTION_MARGIN =  "flatness.section.margin"
WT_RES_FRAME_IQ_OFFSET_11B			=	  "iq.offset"
WT_RES_FRAME_CARRIER_SUPPRESSION_11B	=  "carrier.suppression"

#BT   Frame     
WT_RES_BT_FRAME_CARR_FREQ_DRIFT  = "BT_CARR_FREQ_DRIFT" 
WT_RES_BT_FRAME_CARR_FREQ_BUF    = "BT_CARR_FREQ_BUF"     
WT_RES_BT_FRAME_MAX_CARR_FREQ    = "BT_MAX_CARR_FREQ"     
WT_RES_BT_FRAME_DELTA_F1_VALID   = "BT_DELTA_F1_VALID"     
WT_RES_BT_FRAME_DELTA_F1_AVG     = "BT_DELTA_F1_AVG" 
WT_RES_BT_FRAME_DELTA_F2_VALID   = "BT_DELTA_F2_VALID" 
WT_RES_BT_FRAME_DELTA_F2_AVG     = "BT_DELTA_F2_AVG"
WT_RES_BT_FRAME_DELTA_F2_MAX     = "BT_DELTA_F2_MAX" 
WT_RES_BT_FRAME_BT_DEVM_VALID    = "BT_DEVM_VALID" 
WT_RES_BT_FRAME_BT_DEVM          = "BT_DEVM"     
WT_RES_BT_FRAME_BT_DEVM_PEAK     = "BT_DEVM_PEAK" 
WT_RES_BT_FRAME_BT_POW_DIFF      = "BT_POW_DIFF"     
WT_RES_BT_FRAME_BT_99PCT         = "BT_99PCT" 	     
WT_RES_BT_FRAME_EDR_Omega_I      = "BT_Omega_I"     
WT_RES_BT_FRAME_EDR_Omega_O      = "BT_Omega_O"
WT_RES_BT_FRAME_EDR_Omega_IO     = "BT_Omega_IO" 
WT_RES_BT_FRAME_BW20dB_Passed    = "BT_BW20dB_Passed"
WT_RES_BT_FRAME_BW20dB           = "BT_BW20dB_Value"

#Zigbee   Frame     
WT_RES_ZIGBEE_FRAME_EVM_PSDU           = "Zigbee.evm(psdu)"
WT_RES_ZIGBEE_FRAME_EVM_PSDU_PERCENT   = "Zigbee.evm(psdu).percent"
WT_RES_ZIGBEE_FRAME_EVM_SHRPHR         = "Zigbee.evm(shr+phr)"
WT_RES_ZIGBEE_FRAME_EVM_SHRPHR_PERCENT = "Zigbee.evm(shr+phr).percent"



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

def get_tx_result(rate_list, file_list, log_path, data_list, index=0):
    #将文件夹中的数据整理到data_list中
	power = -1
	rx_ok_percent = -1

	for rate in rate_list:
		# ['6M', [[antA all channel data], [all channel avg]], [[antb all channel data], [all channel avg]]]
		#[3, power_avg, evm_avg, ppm_avg, mask_avg]
		data_list.append([rate[0], [[], []], [[], []]])	
		for dirName in file_list:
			if 'channel' not in dirName:
				continue
			txt_list = dirName.split('.txt')
			if txt_list[0] == dirName:
				continue
			filename_list = txt_list[0].split('_')
			power_avg = 0
			power_sum = 0
			evm_avg = 0
			evm_sum = 0
			ppm_avg = 0
			ppm_sum = 0
			mask_avg = 0
			mask_sum = 0
			#status = ''
			count = 0
			if filename_list[3] == rate[0]:
				with open( os.path.join(log_path, dirName), 'r') as fd:
					lines = fd.readlines()
					for line in lines[1:]:
						line_list = re.split('\s+', line.strip())
						power_sum += float(line_list[0])
						evm_sum += float(line_list[1])
						ppm_sum += float(line_list[2])
						mask_sum += float(line_list[3])
						count += 1
				power_avg = round(power_sum/count, 2)
				evm_avg = round(evm_sum/count, 2)
				ppm_avg = round(ppm_sum/count, 2)
				mask_avg = round(mask_sum/count, 2)
				if filename_list[0].upper() == 'A':
					data_list[index][1][0].append([filename_list[2], power_avg, evm_avg, ppm_avg, mask_avg])
				elif filename_list[0].upper() == 'B':
					data_list[index][2][0].append([filename_list[2], power_avg, evm_avg, ppm_avg, mask_avg])
		power_avg = 0
		power_sum = 0
		evm_avg = 0
		evm_sum = 0
		ppm_avg = 0
		ppm_sum = 0
		mask_avg = 0
		mask_sum = 0
		#status = ''
		count = 0
		for data in data_list[index][1][0]:
			power_sum += data[1]
			evm_sum += data[2]
			ppm_sum += data[3]
			mask_sum += data[4]
			count += 1
		if count != 0:
			power_avg = round(power_sum/count, 2)
			evm_avg = round(evm_sum/count, 2)
			ppm_avg = round(ppm_sum/count, 2)
			mask_avg = round(mask_sum/count, 2)
			data_list[index][1][1] = [power_avg, evm_avg, ppm_avg, mask_avg]
		else:
			data_list[index][1][1] = []
		power_avg = 0
		power_sum = 0
		evm_avg = 0
		evm_sum = 0
		ppm_avg = 0
		ppm_sum = 0
		mask_avg = 0
		mask_sum = 0
		#status = ''
		count = 0
		for data in data_list[index][2][0]:
			power_sum += data[1]
			evm_sum += data[2]
			ppm_sum += data[3]
			mask_sum += data[4]
			count += 1
		if count != 0:
			power_avg = round(power_sum/count, 2)
			evm_avg = round(evm_sum/count, 2)
			ppm_avg = round(ppm_sum/count, 2)
			mask_avg = round(mask_sum/count, 2)
			data_list[index][2][1] = [power_avg, evm_avg, ppm_avg, mask_avg]
		else:
			data_list[index][2][1] = []
		index = index + 1
	print 'index: %d' % index
	return index

	
def rx_data_sum_excel_2_4G(log_path, excel_name, model):
	rate_all_list = rate_11B + rate_11G + rate_11N_20M + rate_11N_40M
	data_list = []
	dir_dirNames = os.listdir(log_path)
	#print dir_dirNames
	index = 0
	index = get_tx_result(rate_11B, dir_dirNames, log_path, data_list, index)
	index = get_tx_result(rate_11G, dir_dirNames, log_path, data_list, index)
	index = get_tx_result(rate_11N_20M, dir_dirNames, log_path, data_list, index)
	index = get_tx_result(rate_11N_40M, dir_dirNames, log_path, data_list, index)

	w=Workbook()
	style = XFStyle()
	al = Alignment()
	al.horz = Alignment.HORZ_CENTER
	al.vert = Alignment.VERT_CENTER
	style.alignment = al
	fnt = Font()  
	fnt.height = 200  
	style.font = fnt
	
	fail_style = XFStyle()
	fail_style.alignment = al
	red_fnt = Font()
	red_fnt.colour_index = 2
	red_fnt.height = 200	
	fail_style.font = red_fnt
	power_min = 0
	power_max = 0
	evm_min = -60
	evm_max = 0
	ppm_max = 0
	ppm_min = 0 
	mask_min = 0
	mask_max = 0
	power_avg_excel = 0
	evm_avg_excel = 0
	ppm_avg_excel = 0
	mask_avg_excel = 0
	A_power_idx_col = 3
	A_power_col = 4
	A_evm_col = 5
	A_ppm_col = 6
	A_mask_col = 7
	B_power_idx_col = 9
	B_power_col = 10
	B_evm_col = 11
	B_ppm_col = 12
	B_mask_col = 13
	for data_tmp in data_list:
		ws=w.add_sheet(data_tmp[0])
		for rate in rate_all_list:
			if rate[0] == data_tmp[0]:
				#print rate
				power_min = rate[3][0]
				power_max = rate[3][1]
				evm_min = rate[4][0]
				evm_max = rate[4][1]
				ppm_max = rate[5][1]
				ppm_min = -ppm_max
				mask_min = rate[6][0]
				mask_max = rate[6][1]
				rate_all_list.remove(rate)
				#print 'power_min: %lf, power_max: %1f, evm_min: %1f, evm_max: %1f, ppm_min: %1f, ppm_max: %1f, mask_min: %1f, mask_max: %1f' %(power_min, power_max, evm_min, evm_max, ppm_min, ppm_max,mask_min, mask_max)
				break
		ws.write(0, 0, 'device', style)
		ws.write(0, 1, 'channel', style)
		ws.write(0, 2, 'ANT', style)
		ws.write(0, A_power_idx_col, 'power_idx', style)
		ws.write(0, A_power_col, 'power', style)
		ws.write(0, A_evm_col, 'evm', style)
		ws.write(0, A_ppm_col, 'ppm', style)
		ws.write(0, A_mask_col, 'mask', style)
		ws.write(0, 8, 'ANT', style)
		ws.write(0, B_power_idx_col, 'power_idx', style)
		ws.write(0, B_power_col, 'power', style)
		ws.write(0, B_evm_col, 'evm', style)
		ws.write(0, B_ppm_col, 'ppm', style)
		ws.write(0, B_mask_col, 'mask', style)
		if '40' in data_tmp[0]:
			for i in range(3, 12):
				ws.write(i-2, 1, i, style)
			ws.write_merge(1, 10, 0, 0, str(model.upper()), style)
			ws.write_merge(1, 10, 2, 2, 'Ant-A', style)
			ws.write_merge(1, 10, 8, 8, 'Ant-B', style)
			if data_tmp[1][1][0] < power_min:
				ws.write(10, A_power_col, data_tmp[1][1][0], fail_style)
			else:
				ws.write(10, A_power_col, data_tmp[1][1][0], style)
			if data_tmp[1][1][1] > evm_max or data_tmp[1][1][1] < evm_min:
				ws.write(10, A_evm_col, data_tmp[1][1][1], fail_style)
			else:
				ws.write(10, A_evm_col, data_tmp[1][1][1], style)
			if data_tmp[1][1][2] > ppm_max or data_tmp[1][1][2] < ppm_min:
				ws.write(10, A_ppm_col, data_tmp[1][1][2], fail_style)
			else:
				ws.write(10, A_ppm_col, data_tmp[1][1][2], style)
			if data_tmp[1][1][3] > mask_max or data_tmp[1][1][3] < mask_min:
				ws.write(10, A_mask_col, data_tmp[1][1][3], fail_style)
			else:
				ws.write(10, A_mask_col, data_tmp[1][1][3], style)
				
			if data_tmp[2][1][0] < power_min:
				ws.write(10, B_power_col, data_tmp[2][1][0], fail_style)
			else:
				ws.write(10, B_power_col, data_tmp[2][1][0], style)
			if data_tmp[2][1][1] > evm_max or data_tmp[2][1][1] < evm_min:
				ws.write(10, B_evm_col, data_tmp[2][1][1], fail_style)
			else:
				ws.write(10, B_evm_col, data_tmp[2][1][1], style)
			if data_tmp[2][1][2] > ppm_max or data_tmp[2][1][2] < ppm_min:
				ws.write(10, B_ppm_col, data_tmp[2][1][2], fail_style)
			else:
				ws.write(10, B_ppm_col, data_tmp[2][1][2], style)
			if data_tmp[2][1][3] > mask_max or data_tmp[2][1][3] < mask_min:
				ws.write(10, B_mask_col, data_tmp[2][1][3], fail_style)
			else:
				ws.write(10, B_mask_col, data_tmp[2][1][3], style)

			for channle_info in data_tmp[1][0]:
				print channle_info
				power_avg_excel = float(channle_info[1])
				evm_avg_excel = float(channle_info[2])
				ppm_avg_excel = float(channle_info[3])
				mask_avg_excel = float(channle_info[4])
				if int(channle_info[0]) > 2:
					channel_excel = int(channle_info[0])-2
					power_idx = channelRate_dict_all[str(channle_info[0])][data_tmp[0]][0]
					if power_idx.isdigit():
						ws.write(channel_excel, A_power_idx_col, int(power_idx), style)
					else:
						ws.write(channel_excel, A_power_idx_col, power_idx, style)
					if power_avg_excel < power_min:
						ws.write(channel_excel, A_power_col, power_avg_excel, fail_style)
					else:
						ws.write(channel_excel, A_power_col, power_avg_excel, style)
					if evm_avg_excel > evm_max or evm_avg_excel < evm_min:
						ws.write(channel_excel, A_evm_col, evm_avg_excel, fail_style)
					else:
						ws.write(channel_excel, A_evm_col, evm_avg_excel, style)
					if ppm_avg_excel > ppm_max or ppm_avg_excel < ppm_min:
						ws.write(channel_excel, A_ppm_col, ppm_avg_excel, fail_style)
					else:
						ws.write(channel_excel, A_ppm_col, ppm_avg_excel, style)
					if mask_avg_excel > mask_max or mask_avg_excel < mask_min:
						ws.write(channel_excel, A_mask_col, mask_avg_excel, fail_style)
					else:
						ws.write(channel_excel, A_mask_col, mask_avg_excel, style)
					
			for channle_info in data_tmp[2][0]:
				power_avg_excel = float(channle_info[1])
				evm_avg_excel = float(channle_info[2])
				ppm_avg_excel = float(channle_info[3])
				mask_avg_excel = float(channle_info[4])
				if int(channle_info[0]) > 2:
					channel_excel = int(channle_info[0])-2
					power_idx = channelRate_dict_all[str(channle_info[0])][data_tmp[0]][1]
					if power_idx.isdigit():
						ws.write(channel_excel, B_power_idx_col, int(power_idx), style)
					else:
						ws.write(channel_excel, B_power_idx_col, power_idx, style)
					if power_avg_excel < power_min:
						ws.write(channel_excel, B_power_col, power_avg_excel, fail_style)
					else:
						ws.write(channel_excel, B_power_col, power_avg_excel, style)
					if evm_avg_excel > evm_max or evm_avg_excel < evm_min:
						ws.write(channel_excel, B_evm_col, evm_avg_excel, fail_style)
					else:
						ws.write(channel_excel, B_evm_col, evm_avg_excel, style)
					if ppm_avg_excel > ppm_max or ppm_avg_excel < ppm_min:
						ws.write(channel_excel, B_ppm_col, ppm_avg_excel, fail_style)
					else:
						ws.write(channel_excel, B_ppm_col, ppm_avg_excel, style)
					if mask_avg_excel > mask_max or mask_avg_excel < mask_min:
						ws.write(channel_excel, B_mask_col, mask_avg_excel, fail_style)
					else:
						ws.write(channel_excel, B_mask_col, mask_avg_excel, style)
		else:
			for i in range(1, 14):
				ws.write(i, 1, i, style)
			ws.write_merge(1, 14, 0, 0, str(model.upper()), style)
			ws.write_merge(1, 14, 2, 2, 'Ant-A', style)
			ws.write_merge(1, 14, 8, 8, 'Ant-B', style)
			
			print data_tmp
			if data_tmp[1][1][0] < power_min:
				ws.write(14, A_power_col, data_tmp[1][1][0], fail_style)
			else:
				ws.write(14, A_power_col, data_tmp[1][1][0], style)
			if data_tmp[1][1][1] > evm_max or data_tmp[1][1][1] < evm_min:
				ws.write(14, A_evm_col, data_tmp[1][1][1], fail_style)
			else:
				ws.write(14, A_evm_col, data_tmp[1][1][1], style)
			if data_tmp[1][1][2] > ppm_max or data_tmp[1][1][2] < ppm_min:
				ws.write(14, A_ppm_col, data_tmp[1][1][2], fail_style)
			else:
				ws.write(14, A_ppm_col, data_tmp[1][1][2], style)
			if data_tmp[1][1][3] > mask_max or data_tmp[1][1][3] < mask_min:
				ws.write(14, A_mask_col, data_tmp[1][1][3], fail_style)
			else:
				ws.write(14, A_mask_col, data_tmp[1][1][3], style)
				
			if data_tmp[2][1][0] < power_min:
				ws.write(14, B_power_col, data_tmp[2][1][0], fail_style)
			else:
				ws.write(14, B_power_col, data_tmp[2][1][0], style)
			if data_tmp[2][1][1] > evm_max or data_tmp[2][1][1] < evm_min:
				ws.write(14, B_evm_col, data_tmp[2][1][1], fail_style)
			else:
				ws.write(14, B_evm_col, data_tmp[2][1][1], style)
			if data_tmp[2][1][2] > ppm_max or data_tmp[2][1][2] < ppm_min:
				ws.write(14, B_ppm_col, data_tmp[2][1][2], fail_style)
			else:
				ws.write(14, B_ppm_col, data_tmp[2][1][2], style)
			if data_tmp[2][1][3] > mask_max or data_tmp[2][1][3] < mask_min:
				ws.write(14, B_mask_col, data_tmp[2][1][3], fail_style)
			else:
				ws.write(14, B_mask_col, data_tmp[2][1][3], style)
			for channle_info in data_tmp[1][0]:
				power_avg_excel = float(channle_info[1])
				evm_avg_excel = float(channle_info[2])
				ppm_avg_excel = float(channle_info[3])
				mask_avg_excel = float(channle_info[4])
				channel_excel = int(channle_info[0])
				power_idx = channelRate_dict_all[str(channle_info[0])][data_tmp[0]][0]
				if power_idx.isdigit():
					ws.write(channel_excel, A_power_idx_col, int(power_idx), style)
				else:
					ws.write(channel_excel, A_power_idx_col, power_idx, style)
				if power_avg_excel < power_min:
					ws.write(channel_excel, A_power_col, power_avg_excel, fail_style)
				else:
					ws.write(channel_excel, A_power_col, power_avg_excel, style)
				if evm_avg_excel > evm_max or evm_avg_excel < evm_min:
					ws.write(channel_excel, A_evm_col, evm_avg_excel, fail_style)
				else:
					ws.write(channel_excel, A_evm_col, evm_avg_excel, style)
				if ppm_avg_excel > ppm_max or ppm_avg_excel < ppm_min:
					ws.write(channel_excel, A_ppm_col, ppm_avg_excel, fail_style)
				else:
					ws.write(channel_excel, A_ppm_col, ppm_avg_excel, style)
				if mask_avg_excel > mask_max or mask_avg_excel < mask_min:
					ws.write(channel_excel, A_mask_col, mask_avg_excel, fail_style)
				else:
					ws.write(channel_excel, A_mask_col, mask_avg_excel, style)
			for channle_info in data_tmp[2][0]:
				power_avg_excel = float(channle_info[1])
				evm_avg_excel = float(channle_info[2])
				ppm_avg_excel = float(channle_info[3])
				mask_avg_excel = float(channle_info[4])
				channel_excel = int(channle_info[0])
				power_idx = channelRate_dict_all[str(channle_info[0])][data_tmp[0]][1]
				if power_idx.isdigit():
					ws.write(channel_excel, B_power_idx_col, int(power_idx), style)
				else:
					ws.write(channel_excel, B_power_idx_col, power_idx, style)
				if power_avg_excel < power_min:
					ws.write(channel_excel, B_power_col, power_avg_excel, fail_style)
				else:
					ws.write(channel_excel, B_power_col, power_avg_excel, style)
				if evm_avg_excel > evm_max or evm_avg_excel < evm_min:
					ws.write(channel_excel, B_evm_col, evm_avg_excel, fail_style)
				else:
					ws.write(channel_excel, B_evm_col, evm_avg_excel, style)
				if ppm_avg_excel > ppm_max or ppm_avg_excel < ppm_min:
					ws.write(channel_excel, B_ppm_col, ppm_avg_excel, fail_style)
				else:
					ws.write(channel_excel, B_ppm_col, ppm_avg_excel, style)
				if mask_avg_excel > mask_max or mask_avg_excel < mask_min:
					ws.write(channel_excel, B_mask_col, mask_avg_excel, fail_style)
				else:
					ws.write(channel_excel, B_mask_col, mask_avg_excel, style)
	w.save(os.path.join(log_path,excel_name))
	
	print data_list
 
def rx_data_sum_excel_5G(log_path, excel_name, model):
	data_list = []
	rate_all_list = rate_11G + rate_11N_20M + rate_11N_40M + rate_5G_20M + rate_5G_40M + rate_5G_80M
	print rate_all_list
	print rate_11G
	dir_dirNames = os.listdir(log_path)
	#print dir_dirNames
	index = 0
	index = get_tx_result(rate_11G, dir_dirNames, log_path, data_list, index)
	index = get_tx_result(rate_11N_20M, dir_dirNames, log_path, data_list, index)
	index = get_tx_result(rate_11N_40M, dir_dirNames, log_path, data_list, index)
	index = get_tx_result(rate_5G_20M, dir_dirNames, log_path, data_list, index)
	index = get_tx_result(rate_5G_40M, dir_dirNames, log_path, data_list, index)
	index = get_tx_result(rate_5G_80M, dir_dirNames, log_path, data_list, index)
	print 'index_ end'
	
	w=Workbook()
	style = XFStyle()
	al = Alignment()
	al.horz = Alignment.HORZ_CENTER
	al.vert = Alignment.VERT_CENTER
	style.alignment = al
	fnt = Font()  
	fnt.height = 200
	style.font = fnt
	
	fail_style = XFStyle()
	fail_style.alignment = al
	red_fnt = Font()
	red_fnt.colour_index = 2
	red_fnt.height = 200	
	fail_style.font = red_fnt
	power_min = 0
	power_max = 0
	evm_min = -60
	evm_max = 0
	ppm_max = 0
	ppm_min = 0 
	mask_min = 0
	mask_max = 0
	power_avg_excel = 0
	evm_avg_excel = 0
	ppm_avg_excel = 0
	mask_avg_excel = 0
	A_power_idx_col = 3
	A_power_col = 4
	A_evm_col = 5
	A_ppm_col = 6
	A_mask_col = 7
	B_power_idx_col = 9
	B_power_col = 10
	B_evm_col = 11
	B_ppm_col = 12
	B_mask_col = 13
	channel_excel = 0

	for data_tmp in data_list:
		if data_tmp[1] == [[], []] or data_tmp[2] ==  [[], []]:
			print '%s not in file' % rate[0]
			continue
		ws=w.add_sheet(data_tmp[0])
		for rate in rate_all_list:
			if rate[0] == data_tmp[0]:
				#print rate
				power_min = rate[3][0]
				power_max = rate[3][1]
				evm_min = rate[4][0]
				evm_max = rate[4][1]
				ppm_max = rate[5][1]
				ppm_min = -ppm_max
				mask_min = rate[6][0]
				mask_max = rate[6][1]
				rate_all_list.remove(rate)
				#print 'power_min: %lf, power_max: %1f, evm_min: %1f, evm_max: %1f, ppm_min: %1f, ppm_max: %1f, mask_min: %1f, mask_max: %1f' %(power_min, power_max, evm_min, evm_max, ppm_min, ppm_max,mask_min, mask_max)
				break
		ws.write(0, 0, 'device', style)
		ws.write(0, 1, 'channel', style)
		ws.write(0, 2, 'ANT', style)
		ws.write(0, A_power_idx_col, 'power_idx', style)
		ws.write(0, A_power_col, 'power', style)
		ws.write(0, A_evm_col, 'evm', style)
		ws.write(0, A_ppm_col, 'ppm', style)
		ws.write(0, A_mask_col, 'mask', style)
		ws.write(0, 8, 'ANT', style)
		ws.write(0, B_power_idx_col, 'power_idx', style)
		ws.write(0, B_power_col, 'power', style)
		ws.write(0, B_evm_col, 'evm', style)
		ws.write(0, B_ppm_col, 'ppm', style)
		ws.write(0, B_mask_col, 'mask', style)
		if '40' in data_tmp[0]:
			print 'data_tmp: %s' % str(data_tmp)
			ws.write_merge(1, 7, 0, 0, str(model.upper()), style)
			ws.write_merge(1, 7, 2, 2, 'Ant-A', style)
			ws.write_merge(1, 7, 8, 8, 'Ant-B', style)
			if data_tmp[1][1][0] < power_min:
				ws.write(7, A_power_col, data_tmp[1][1][0], fail_style)
			else:
				ws.write(7, A_power_col, data_tmp[1][1][0], style)
			if data_tmp[1][1][1] > evm_max or data_tmp[1][1][1] < evm_min:
				ws.write(7, A_evm_col, data_tmp[1][1][1], fail_style)
			else:
				ws.write(7, A_evm_col, data_tmp[1][1][1], style)
			if data_tmp[1][1][2] > ppm_max or data_tmp[1][1][2] < ppm_min:
				ws.write(7, A_ppm_col, data_tmp[1][1][2], fail_style)
			else:
				ws.write(7, A_ppm_col, data_tmp[1][1][2], style)
			if data_tmp[1][1][3] > mask_max or data_tmp[1][1][3] < mask_min:
				ws.write(7, A_mask_col, data_tmp[1][1][3], fail_style)
			else:
				ws.write(7, A_mask_col, data_tmp[1][1][3], style)
				
			if data_tmp[2][1][0] < power_min:
				ws.write(7, B_power_col, data_tmp[2][1][0], fail_style)
			else:
				ws.write(7, B_power_col, data_tmp[2][1][0], style)
			if data_tmp[2][1][1] > evm_max or data_tmp[2][1][1] < evm_min:
				ws.write(7, B_evm_col, data_tmp[2][1][1], fail_style)
			else:
				ws.write(7, B_evm_col, data_tmp[2][1][1], style)
			if data_tmp[2][1][2] > ppm_max or data_tmp[2][1][2] < ppm_min:
				ws.write(7, B_ppm_col, data_tmp[2][1][2], fail_style)
			else:
				ws.write(7, B_ppm_col, data_tmp[2][1][2], style)
			if data_tmp[2][1][3] > mask_max or data_tmp[2][1][3] < mask_min:
				ws.write(7, B_mask_col, data_tmp[2][1][3], fail_style)
			else:
				ws.write(7, B_mask_col, data_tmp[2][1][3], style)	
			ws.write(1, 1, 38, style)
			ws.write(2, 1, 46, style)
			ws.write(3, 1, 54, style)
			ws.write(4, 1, 62, style)
			ws.write(5, 1, 151, style)
			ws.write(6, 1, 159, style)
			for channle_info in data_tmp[1][0]:
				power_avg_excel = float(channle_info[1])
				evm_avg_excel = float(channle_info[2])
				ppm_avg_excel = float(channle_info[3])
				mask_avg_excel = float(channle_info[4])
				if int(channle_info[0]) < 151:
					channel_excel = (int(channle_info[0])-38)/8+1
				else:
					channel_excel = (int(channle_info[0])-151)/8 + 5
				power_idx = channelRate_dict_all[str(channle_info[0])][data_tmp[0]][0]
				#ws.write(channel_excel, A_power_idx_col, str(power_idx), style)
				if power_idx.isdigit():
					ws.write(channel_excel, A_power_idx_col, int(power_idx), style)
				else:
					ws.write(channel_excel, A_power_idx_col, power_idx, style)
				if power_avg_excel < power_min:
					ws.write(channel_excel, A_power_col, power_avg_excel, fail_style)
				else:
					ws.write(channel_excel, A_power_col, power_avg_excel, style)
				if evm_avg_excel > evm_max or evm_avg_excel < evm_min:
					ws.write(channel_excel, A_evm_col, evm_avg_excel, fail_style)
				else:
					ws.write(channel_excel, A_evm_col, evm_avg_excel, style)
				if ppm_avg_excel > ppm_max or ppm_avg_excel < ppm_min:
					ws.write(channel_excel, A_ppm_col, ppm_avg_excel, fail_style)
				else:
					ws.write(channel_excel, A_ppm_col, ppm_avg_excel, style)
				if mask_avg_excel > mask_max or mask_avg_excel < mask_min:
					ws.write(channel_excel, A_mask_col, mask_avg_excel, fail_style)
				else:
					ws.write(channel_excel, A_mask_col, mask_avg_excel, style)

			for channle_info in data_tmp[2][0]:
				power_avg_excel = float(channle_info[1])
				evm_avg_excel = float(channle_info[2])
				ppm_avg_excel = float(channle_info[3])
				mask_avg_excel = float(channle_info[4])
				if int(channle_info[0]) < 151:
					channel_excel = (int(channle_info[0])-38)/8+1
				else:
					channel_excel = (int(channle_info[0])-151)/8 + 5
				power_idx = channelRate_dict_all[str(channle_info[0])][data_tmp[0]][1]
				#ws.write(channel_excel, B_power_idx_col, str(power_idx), style)
				if power_idx.isdigit():
					ws.write(channel_excel, B_power_idx_col, int(power_idx), style)
				else:
					ws.write(channel_excel, B_power_idx_col, power_idx, style)
				if power_avg_excel < power_min:
					ws.write(channel_excel, B_power_col, power_avg_excel, fail_style)
				else:
					ws.write(channel_excel, B_power_col, power_avg_excel, style)
				if evm_avg_excel > evm_max or evm_avg_excel < evm_min:
					ws.write(channel_excel, B_evm_col, evm_avg_excel, fail_style)
				else:
					ws.write(channel_excel, B_evm_col, evm_avg_excel, style)
				if ppm_avg_excel > ppm_max or ppm_avg_excel < ppm_min:
					ws.write(channel_excel, B_ppm_col, ppm_avg_excel, fail_style)
				else:
					ws.write(channel_excel, B_ppm_col, ppm_avg_excel, style)
				if mask_avg_excel > mask_max or mask_avg_excel < mask_min:
					ws.write(channel_excel, B_mask_col, mask_avg_excel, fail_style)
				else:
					ws.write(channel_excel, B_mask_col, mask_avg_excel, style)
		elif '80' in data_tmp[0]:
			ws.write_merge(1, 4, 0, 0, str(model.upper()), style)
			ws.write_merge(1, 4, 2, 2, 'Ant-A', style)
			ws.write_merge(1, 4, 8, 8, 'Ant-B', style)
			if data_tmp[1][1][0] < power_min:
				ws.write(4, A_power_col, data_tmp[1][1][0], fail_style)
			else:
				ws.write(4, A_power_col, data_tmp[1][1][0], style)
			if data_tmp[1][1][1] > evm_max or data_tmp[1][1][1] < evm_min:
				ws.write(4, A_evm_col, data_tmp[1][1][1], fail_style)
			else:
				ws.write(4, A_evm_col, data_tmp[1][1][1], style)
			if data_tmp[1][1][2] > ppm_max or data_tmp[1][1][2] < ppm_min:
				ws.write(4, A_ppm_col, data_tmp[1][1][2], fail_style)
			else:
				ws.write(4, A_ppm_col, data_tmp[1][1][2], style)
			if data_tmp[1][1][3] > mask_max or data_tmp[1][1][3] < mask_min:
				ws.write(4, A_mask_col, data_tmp[1][1][3], fail_style)
			else:
				ws.write(4, A_mask_col, data_tmp[1][1][3], style)
				
			if data_tmp[2][1][0] < power_min:
				ws.write(4, B_power_col, data_tmp[2][1][0], fail_style)
			else:
				ws.write(4, B_power_col, data_tmp[2][1][0], style)
			if data_tmp[2][1][1] > evm_max or data_tmp[2][1][1] < evm_min:
				ws.write(4, B_evm_col, data_tmp[2][1][1], fail_style)
			else:
				ws.write(4, B_evm_col, data_tmp[2][1][1], style)
			if data_tmp[2][1][2] > ppm_max or data_tmp[2][1][2] < ppm_min:
				ws.write(4, B_ppm_col, data_tmp[2][1][2], fail_style)
			else:
				ws.write(4, B_ppm_col, data_tmp[2][1][2], style)
			if data_tmp[2][1][3] > mask_max or data_tmp[2][1][3] < mask_min:
				ws.write(4, B_mask_col, data_tmp[2][1][3], fail_style)
			else:
				ws.write(4, B_mask_col, data_tmp[2][1][3], style)	
			ws.write(1, 1, 42, style)
			ws.write(2, 1, 58, style)
			ws.write(3, 1, 155, style)
			for channle_info in data_tmp[1][0]:
				power_avg_excel = float(channle_info[1])
				evm_avg_excel = float(channle_info[2])
				ppm_avg_excel = float(channle_info[3])
				mask_avg_excel = float(channle_info[4])
				if int(channle_info[0]) < 155:
					channel_excel = (int(channle_info[0])-42)/16 + 1
				else:
					channel_excel = (int(channle_info[0])-155)/16 + 3
				power_idx = channelRate_dict_all[str(channle_info[0])][data_tmp[0]][0]
				#ws.write(channel_excel, A_power_idx_col, str(power_idx), style)
				if power_idx.isdigit():
					ws.write(channel_excel, A_power_idx_col, int(power_idx), style)
				else:
					ws.write(channel_excel, A_power_idx_col, power_idx, style)
				if power_avg_excel < power_min:
					ws.write(channel_excel, A_power_col, power_avg_excel, fail_style)
				else:
					ws.write(channel_excel, A_power_col, power_avg_excel, style)
				if evm_avg_excel > evm_max or evm_avg_excel < evm_min:
					ws.write(channel_excel, A_evm_col, evm_avg_excel, fail_style)
				else:
					ws.write(channel_excel, A_evm_col, evm_avg_excel, style)
				if ppm_avg_excel > ppm_max or ppm_avg_excel < ppm_min:
					ws.write(channel_excel, A_ppm_col, ppm_avg_excel, fail_style)
				else:
					ws.write(channel_excel, A_ppm_col, ppm_avg_excel, style)
				if mask_avg_excel > mask_max or mask_avg_excel < mask_min:
					ws.write(channel_excel, A_mask_col, mask_avg_excel, fail_style)
				else:
					ws.write(channel_excel, A_mask_col, mask_avg_excel, style)
			for channle_info in data_tmp[2][0]:
				power_avg_excel = float(channle_info[1])
				evm_avg_excel = float(channle_info[2])
				ppm_avg_excel = float(channle_info[3])
				mask_avg_excel = float(channle_info[4])
				if int(channle_info[0]) < 155:
					channel_excel = (int(channle_info[0])-42)/16 + 1
				else:
					channel_excel = (int(channle_info[0])-155)/16 + 3
				power_idx = channelRate_dict_all[str(channle_info[0])][data_tmp[0]][1]
				#ws.write(channel_excel, B_power_idx_col, str(power_idx), style)
				if power_idx.isdigit():
					ws.write(channel_excel, B_power_idx_col, int(power_idx), style)
				else:
					ws.write(channel_excel, B_power_idx_col, power_idx, style)
				if power_avg_excel < power_min:
					ws.write(channel_excel, B_power_col, power_avg_excel, fail_style)
				else:
					ws.write(channel_excel, B_power_col, power_avg_excel, style)
				if evm_avg_excel > evm_max or evm_avg_excel < evm_min:
					ws.write(channel_excel, B_evm_col, evm_avg_excel, fail_style)
				else:
					ws.write(channel_excel, B_evm_col, evm_avg_excel, style)
				if ppm_avg_excel > ppm_max or ppm_avg_excel < ppm_min:
					ws.write(channel_excel, B_ppm_col, ppm_avg_excel, fail_style)
				else:
					ws.write(channel_excel, B_ppm_col, ppm_avg_excel, style)
				if mask_avg_excel > mask_max or mask_avg_excel < mask_min:
					ws.write(channel_excel, B_mask_col, mask_avg_excel, fail_style)
				else:
					ws.write(channel_excel, B_mask_col, mask_avg_excel, style)
		else:
			#print '20M %s' % str(data_tmp)
			ws.write_merge(1, 14, 0, 0, str(model.upper()), style)
			ws.write_merge(1, 14, 2, 2, 'Ant-A', style)
			ws.write_merge(1, 14, 8, 8, 'Ant-B', style)
			if data_tmp[1][1][0] < power_min:
				ws.write(14, A_power_col, data_tmp[1][1][0], fail_style)
			else:
				ws.write(14, A_power_col, data_tmp[1][1][0], style)
			if data_tmp[1][1][1] > evm_max or data_tmp[1][1][1] < evm_min:
				ws.write(14, A_evm_col, data_tmp[1][1][1], fail_style)
			else:
				ws.write(14, A_evm_col, data_tmp[1][1][1], style)
			if data_tmp[1][1][2] > ppm_max or data_tmp[1][1][2] < ppm_min:
				ws.write(14, A_ppm_col, data_tmp[1][1][2], fail_style)
			else:
				ws.write(14, A_ppm_col, data_tmp[1][1][2], style)
			if data_tmp[1][1][3] > mask_max or data_tmp[1][1][3] < mask_min:
				ws.write(14, A_mask_col, data_tmp[1][1][3], fail_style)
			else:
				ws.write(14, A_mask_col, data_tmp[1][1][3], style)
				
			if data_tmp[2][1][0] < power_min:
				ws.write(14, B_power_col, data_tmp[2][1][0], fail_style)
			else:
				ws.write(14, B_power_col, data_tmp[2][1][0], style)
			if data_tmp[2][1][1] > evm_max or data_tmp[2][1][1] < evm_min:
				ws.write(14, B_evm_col, data_tmp[2][1][1], fail_style)
			else:
				ws.write(14, B_evm_col, data_tmp[2][1][1], style)
			if data_tmp[2][1][2] > ppm_max or data_tmp[2][1][2] < ppm_min:
				ws.write(14, B_ppm_col, data_tmp[2][1][2], fail_style)
			else:
				ws.write(14, B_ppm_col, data_tmp[2][1][2], style)
			if data_tmp[2][1][3] > mask_max or data_tmp[2][1][3] < mask_min:
				ws.write(14, B_mask_col, data_tmp[2][1][3], fail_style)
			else:
				ws.write(14, B_mask_col, data_tmp[2][1][3], style)	
			channel = 36
			for i in range(1, 14):
				ws.write(i, 1, channel, style)
				channel = channel + 4
				if channel == 68:
					channel = 149
			for channle_info in data_tmp[1][0]:
				power_avg_excel = float(channle_info[1])
				evm_avg_excel = float(channle_info[2])
				ppm_avg_excel = float(channle_info[3])
				mask_avg_excel = float(channle_info[4])
				if int(channle_info[0]) < 149:
					channel_excel = (int(channle_info[0])-36)/4 + 1
				else:
					channel_excel = (int(channle_info[0])-149)/4 + 9
				power_idx = channelRate_dict_all[str(channle_info[0])][data_tmp[0]][0]
				#print 'power_idx: %s' % power_idx
				if power_idx.isdigit():
					ws.write(channel_excel, A_power_idx_col, int(power_idx), style)
				else:
					ws.write(channel_excel, A_power_idx_col, power_idx, style)
				if power_avg_excel < power_min:
					ws.write(channel_excel, A_power_col, power_avg_excel, fail_style)
				else:
					ws.write(channel_excel, A_power_col, power_avg_excel, style)
				if evm_avg_excel > evm_max or evm_avg_excel < evm_min:
					ws.write(channel_excel, A_evm_col, evm_avg_excel, fail_style)
				else:
					ws.write(channel_excel, A_evm_col, evm_avg_excel, style)
				if ppm_avg_excel > ppm_max or ppm_avg_excel < ppm_min:
					ws.write(channel_excel, A_ppm_col, ppm_avg_excel, fail_style)
				else:
					ws.write(channel_excel, A_ppm_col, ppm_avg_excel, style)
				if mask_avg_excel > mask_max or mask_avg_excel < mask_min:
					ws.write(channel_excel, A_mask_col, mask_avg_excel, fail_style)
				else:
					ws.write(channel_excel, A_mask_col, mask_avg_excel, style)
			for channle_info in data_tmp[2][0]:
				power_avg_excel = float(channle_info[1])
				evm_avg_excel = float(channle_info[2])
				ppm_avg_excel = float(channle_info[3])
				mask_avg_excel = float(channle_info[4])
				if int(channle_info[0]) < 149:
					channel_excel = (int(channle_info[0])-36)/4 + 1
				else:
					channel_excel = (int(channle_info[0])-149)/4 + 9
				power_idx = channelRate_dict_all[str(channle_info[0])][data_tmp[0]][1]
				#ws.write(channel_excel, B_power_idx_col, str(power_idx), style)
				if power_idx.isdigit():
					ws.write(channel_excel, B_power_idx_col, int(power_idx), style)
				else:
					ws.write(channel_excel, B_power_idx_col, power_idx, style)
				if power_avg_excel < power_min:
					ws.write(channel_excel, B_power_col, power_avg_excel, fail_style)
				else:
					ws.write(channel_excel, B_power_col, power_avg_excel, style)
				if evm_avg_excel > evm_max or evm_avg_excel < evm_min:
					ws.write(channel_excel, B_evm_col, evm_avg_excel, fail_style)
				else:
					ws.write(channel_excel, B_evm_col, evm_avg_excel, style)
				if ppm_avg_excel > ppm_max or ppm_avg_excel < ppm_min:
					ws.write(channel_excel, B_ppm_col, ppm_avg_excel, fail_style)
				else:
					ws.write(channel_excel, B_ppm_col, ppm_avg_excel, style)
				if mask_avg_excel > mask_max or mask_avg_excel < mask_min:
					ws.write(channel_excel, B_mask_col, mask_avg_excel, fail_style)
				else:
					ws.write(channel_excel, B_mask_col, mask_avg_excel, style)	
	w.save(os.path.join(log_path,excel_name))
	
	#print data_list

def rx_data_sum_excel(log_path, excel_name, model, band):
	if band.upper() == '2.4G':
		rx_data_sum_excel_2_4G(log_path, excel_name, model)
	else:
		rx_data_sum_excel_5G(log_path, excel_name, model)

	
def mkLoginDir(band_set=band):
	dir=LOGPATH+time.strftime('Adjust_TX_%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))+'_'+str(band)+'_'+model
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

def readChannelRatePowerIndex(file):
	with open(file, 'r') as fd:
		lines = fd.readlines()
		channelRate_dict_2_4G = eval(lines[0])
		channelRate_dict_5G = eval(lines[1])
		channelRate_dict_all = dict(channelRate_dict_2_4G, **channelRate_dict_5G)
		print 'channelRate_dict_all#############################################'
		print channelRate_dict_all
		print 'channelRate_dict_end@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
	return channelRate_dict_all
		#for channel in A_channel_2_4G:
		#	print channelRate_dict_2_4G[str(channel[0])]
		#	channel.append(channelRate_dict_2_4G[str(channel[0])])
		#for channel in B_channel_2_4G:
		#	channel.append(channelRate_dict_2_4G[str(channel[0])])
		#for channel in A_channel_2_4G_40M:
		#	channel.append(channelRate_dict_2_4G[str(channel[0])])
		#for channel in B_channel_2_4G_40M:
		#	channel.append(channelRate_dict_2_4G[str(channel[0])])	
		#for channel in A_channel_5G_20M:
		#	channel.append(channelRate_dict_5G[str(channel[0])])
		#for channel in B_channel_5G_20M:
		#	channel.append(channelRate_dict_5G[str(channel[0])])
		#for channel in A_channel_5G_40M:
		#	channel.append(channelRate_dict_5G[str(channel[0])])
		#for channel in B_channel_5G_40M:
		#	channel.append(channelRate_dict_5G[str(channel[0])])
		#for channel in A_channel_5G_80M:
		#	channel.append(channelRate_dict_5G[str(channel[0])])
		#for channel in B_channel_5G_80M:
		#	channel.append(channelRate_dict_5G[str(channel[0])])
	
def readMPRateIndex(file):
	with open(file, 'r') as fd:
		lines = fd.readlines()
		rate_list = eval(lines[0])
		print rate_list
		for rate in rate_11B:
			rate[1] = rate_list[rate[0]]
		for rate in rate_11G:
			rate[1] = rate_list[rate[0]]
		for rate in rate_11N_20M:
			rate[1] = rate_list[rate[0]]
		for rate in rate_11N_40M:
			rate[1] = rate_list[rate[0]]
		for rate in rate_5G_20M:
			rate[1] = rate_list[rate[0]]
		for rate in rate_5G_40M:
			rate[1] = rate_list[rate[0]]
		for rate in rate_5G_80M:
			rate[1] = rate_list[rate[0]]
			
def readTXwifiCFG(cfg_file):
	rt = Read_TXCFG.Read_TXCFG(cfg_file)
	power_list = rt.read_power_stand()
	print 'power_list_2.4G'
	print power_list[0]
	print 'power_list_5G'
	print power_list[1]

	evm_list = rt.read_evm_stand()
	print "evm_list"
	print evm_list
	ppm_list = rt.read_ppm_stand()
	print "ppm_list"
	print ppm_list
	mask_list = rt.read_mask_stand()
	print "mask_list"
	print mask_list
	rt.close_file()
	#set power
	if band.upper() == '2.4G':
		for rate in rate_11B:
			rate[3] = power_list[0][0]
		for rate in rate_11G:
			rate[3] = power_list[0][1]
		for rate in rate_11N_20M:
			rate[3] = power_list[0][2]
		for rate in rate_11N_40M:
			rate[3] = power_list[0][3]
	elif band.upper() == '5G':
		for rate in rate_11G:
			rate[3] = power_list[1][1]
		for rate in rate_11N_20M:
			rate[3] = power_list[1][2]
		for rate in rate_11N_40M:
			rate[3] = power_list[1][3]
		for rate in rate_5G_20M:
			rate[3] = power_list[1][4]
		for rate in rate_5G_40M:
			rate[3] = power_list[1][5]
		for rate in rate_5G_80M:
			rate[3] = power_list[1][6]
	else:
		raise Exception("ANT error %s") % ant
		
	#set evm
	test_len = len(rate_11B)
	for i in range(test_len):
		rate_11B[i][4] = [EVM_min_limit, evm_list[0][i]]
	test_len = len(rate_11G)
	for i in range(test_len):
		rate_11G[i][4] = [EVM_min_limit, evm_list[1][i]]
	test_len = len(rate_11N_20M)
	for i in range(test_len):
		rate_11N_20M[i][4] = [EVM_min_limit, evm_list[2][i]]	
	test_len = len(rate_11N_40M)
	for i in range(test_len):
		rate_11N_40M[i][4] = [EVM_min_limit, evm_list[3][i]]	
	test_len = len(rate_5G_20M)
	for i in range(test_len):
		rate_5G_20M[i][4] = [EVM_min_limit, evm_list[4][i]]
	test_len = len(rate_5G_40M)
	for i in range(test_len):
		rate_5G_40M[i][4] = [EVM_min_limit, evm_list[5][i]]	
	test_len = len(rate_5G_80M)
	for i in range(test_len):
		rate_5G_80M[i][4] = [EVM_min_limit, evm_list[6][i]]	
		
	#set ppm
	for rate in rate_11B:
		rate[5] = ppm_list[0]
	for rate in rate_11G:
		rate[5] = ppm_list[1]
	for rate in rate_11N_20M:
		rate[5] = ppm_list[2]
	for rate in rate_11N_40M:
		rate[5] = ppm_list[3]
	for rate in rate_5G_20M:
		rate[5] = ppm_list[4]
	for rate in rate_5G_40M:
		rate[5] = ppm_list[5]
	for rate in rate_5G_80M:
		rate[5] = ppm_list[6]
		
	#set mask
	for rate in rate_11B:
		rate[6] = [mask_min_limit, mask_list[0]]
	for rate in rate_11G:
		rate[6] = [mask_min_limit, mask_list[1]]
	for rate in rate_11N_20M:
		rate[6] = [mask_min_limit, mask_list[2]]
	for rate in rate_11N_40M:
		rate[6] = [mask_min_limit, mask_list[3]]
	for rate in rate_5G_20M:
		rate[6] = [mask_min_limit, mask_list[4]]
	for rate in rate_5G_40M:
		rate[6] = [mask_min_limit, mask_list[5]]
	for rate in rate_5G_80M:
		rate[6] = [mask_min_limit, mask_list[6]]
		
	print '***************11B*******************'	
	print rate_11B
	print '***************11G*******************'
	print rate_11G
	print '***************rate_11N_20M*******************'	
	print rate_11N_20M
	print '***************rate_11N_40M*******************'
	print rate_11N_40M
	print '***************rate_5G_20M*******************'
	print rate_5G_20M
	print '***************rate_5G_40M*******************'
	print rate_5G_40M
	print '***************rate_5G_80M*******************'	
	print rate_5G_80M		
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

def adjust_mp_tx_file_RTL_serial(wt, ser, log_dir, wt_demod, channel, bandWidth_set, rate, ant, rfPort=RF_PORT_Default, trig_type=WT_TRIG_TYPE_IF, trig_level=-31, smp_time=2000, trig_pretime=20, TimeoutWaiting=5, trig_timeout=5, max_power=0.0, g_external_gain=0.0, test_time=3):
	#rate=['1M', 2, [33, 32], [18, 21], [-60.00, -29.00], [], []
	#power_start_index = 0
	power_min = float(rate[3][0])
	power_max = float(rate[3][1])
	evm_min = float(rate[4][0])
	evm_max = float(rate[4][1])
	ppm_max = float(rate[5][1])
	#ppm_min = float(rate[5][0])
	ppm_min = 0 - ppm_max
	mask_min = float(rate[6][0])
	mask_max = float(rate[6][1])
	print 'power_min: %lf, power_max: %1f, evm_min: %1f, evm_max: %1f, ppm_min: %1f, ppm_max: %1f, mask_min: %1f, mask_max: %1f' %(power_min, power_max, evm_min, evm_max, ppm_min, ppm_max,mask_min, mask_max)
	ppm = 0
	rate_key = None
	status = 'Fail'
	retry_time_max = 10
	retry_time = 0
	print rate
	rate_key = rate[0]
	print 'rate_key: %s\n' % rate_key
	print channel
	
	#if ant.upper() == 'A':
	#	power_start_index = int(channel[2][str(rate_key)][0], 16)
	#elif ant.upper() == 'B':
	#	power_start_index = int(channel[2][str(rate_key)][1], 16)
	#else:
	#	raise Exception("ANT error %s") % ant
	#if ant.upper() == 'A':
	#	power_start_index = int(channelRate_dict_all[str(channel[0])][rate_key][0], 16)
	#elif ant.upper() == 'B':
	#	power_start_index = int(channelRate_dict_all[str(channel[0])][rate_key][1], 16)
	#else:
	#	raise Exception("ANT error %s") % ant	
	record_file_name =log_dir + '/'+ant.upper()+'_channel_' + str(channel[0]) + '_' +str(rate[0])+'.txt'
	print record_file_name
	os.system('echo powerindex	  power	  evm	  ppm 	  mask 	  result >' +record_file_name)
	for i in range(power_index_start,power_index_end+1,power_index_step):
		print "=============power_index:",i,"============================"
		power_index=i
		print 'channel: %d, channel_external_att: %f, power_idx: %d\n' % (channel[0], channel[1], power_index)
		ser.start_mp_ctx(channel[0], rate[1], power_index, bandWidth_set, ant.lower(), interface=mp_iface)	
		time.sleep(3)
		if  channel[0] < 36:
			vsa_freq_set = ((channel[0] -1)*5 + freq_base_2_4g) * 1e6
		elif channel[0] >= 149:
			vsa_freq_set = ((channel[0] -149) / 2 *10 + freq_base_5GHigh) * 1e6
		else:
			vsa_freq_set = ((channel[0] -36) / 2 *10 + freq_base_5GLow) * 1e6
		print vsa_freq_set
		ret = wt.WT_SetVSA_AutoRange(vsa_freq_set, wt_demod, rfPort, trig_type, trig_level, smp_time, trig_pretime, TimeoutWaiting, trig_timeout, max_power, g_external_gain)
		if ret != WT_ERR_CODE_OK:
			print 'WT_SetVSA_AutoRange set fail: %d' % ret
			sys.exit()
		while (test_time > 0):
			if retry_time >= retry_time_max:
				print 'retry_time end: %d, now break\n' % retry_time
				sys.exit()
			ret = wt.WT_DataCapture()
			if WT_ERR_CODE_OK != ret:
				raise Exception("WT_DataCapture ret: %s\n") % str(ret)
			ret, power_all, description, unit= wt.WT_GetResult(WT_RES_POWER_ALL_DB)
			print "power all ret: %d\n"  % ret
			if WT_ERR_CODE_OK != ret:
				print "get power_all error %d" % ret
				retry_time = retry_time + 1
				continue
			print "power all: %lf dBm\n"  % power_all
			ret, power_frame, description, unit= wt.WT_GetResult(WT_RES_POWER_FRAME_DB)
			print "power_frame ret: %d\n"  % ret
			print "power_frame: %lf dBm\n"  % power_frame
			#print "power all description: %s\n"  % description
			#print "power all unit: %s\n"  % unit
			power_frame = power_frame + channel[1]
			print "power frame add wireATT: %lf dBm\n"  % power_frame
			ret, evm_all, description, unit = wt.WT_GetResult(WT_RES_FRAME_EVM_ALL)
			print "EVM_ALL ret: %d\n" % ret
			if WT_ERR_CODE_OK != ret:
				print ("get evm_all error %d") % ret
				retry_time = retry_time + 1
				continue
			print "EVM_ALL: %lf dBm\n"  % evm_all
			#print "EVM_ALL description: %s\n"  % description
			#print "EVM_ALL unit: %s\n"  % unit
			ret, freq_err, description, unit = wt.WT_GetResult(WT_RES_FRAME_FREQ_ERR)
			print "freq_err ret: %d\n"  % ret
			if WT_ERR_CODE_OK != ret:
				print ("get freq_err error %d") % ret
				retry_time = retry_time + 1
				continue
			print "FREQ_ERR ret: %d\n" % ret
			print "FREQ_ERR: %lf Hz\n"  % freq_err
			#print "FREQ_ERR description: %s\n"  % description
			#print "FREQ_ERR unit: %s\n"  % unit
			ppm = round(float(freq_err) / float(vsa_freq_set/1e6), 2)
			print "ppm: %lf\n"  % ppm
			ret, mask, description, unit = wt.WT_GetResult(WT_RES_SPECTRUM_MASK_ERR_PERCENT)
			print "mask ret: %d\n"  % ret
			if WT_ERR_CODE_OK != ret:
				print ("get mask error %d") % ret
				retry_time = retry_time + 1
				continue
			print "mask: %lf\n"  % mask
			#print "mask description: %s\n"  % description
			#print "mask unit: %s\n"  % unit
			#if evm_all > evm_max or  ppm > ppm_max or ppm < ppm_min or mask > mask_max or mask < mask_min:
			#if power_frame < power_min or evm_all > evm_max or  abs(ppm) > ppm_max  or abs(ppm) < ppm_min or mask > mask_max or mask < mask_min:
			#	status = 'Fail'
			if power_frame < power_min:
				status ="POWERFAIL"
			elif evm_all > evm_max:
				status = "EVMFAIL"
			elif abs(ppm) > ppm_max  or abs(ppm) < ppm_min:
				status="PPMFAIL"
			elif mask > mask_max or mask < mask_min:
				status ="MASKFAIL"
			else:
				status = 'PASS'
			os.system('echo '+str(power_index)+'	' +str(round(power_frame, 2)) + '	'+ str(round(evm_all, 2)) + '	' + str(ppm)+ '	'+ str(round(mask, 2)) + '	' +str(status) +'>> ' + record_file_name)		
			time.sleep(1)
			test_time = test_time - 1
		test_time=3
	ser.stop_mp_tx(mp_iface)
	#time.sleep(1)
	#wt.WT_StopDataCapture()
def adjust_mp_tx_RTL_serial(wt_demod, channel_list, rate_list, wt, ser, log_dir, bandWidth_set, ant, rfPort=RF_PORT_Default, trig_type=WT_TRIG_TYPE_IF, trig_level=-31, smp_time=2000, trig_pretime=20, TimeoutWaiting=5, trig_timeout=5, max_power=0.0, g_external_gain=0.0, test_time=3):
		print channel_list
		for channel in channel_list:
			print "channel:\n",channel
			print "rate_list\n",rate_list
			for rate in rate_list:
				print "rate:\n",rate
				adjust_mp_tx_file_RTL_serial(wt, ser, log_dir, wt_demod, channel, bandWidth_set, rate, ant, rfPort, trig_type, trig_level, smp_time, trig_pretime, TimeoutWaiting, trig_timeout, max_power, g_external_gain, test_time)

def record_mp_tx_file_RTL_serial(wt, ser, log_dir, wt_demod, channel, bandWidth_set, rate, ant, rfPort=RF_PORT_Default, trig_type=WT_TRIG_TYPE_IF, trig_level=-31, smp_time=2000, trig_pretime=20, TimeoutWaiting=5, trig_timeout=5, max_power=0.0, g_external_gain=0.0, test_time=3):
	#['1M', 2, [33, 32], [18, 21], [-60.00, -29.00], [], []
	power_start_index = 0
	power_min = float(rate[3][0])
	power_max = float(rate[3][1])
	evm_min = float(rate[4][0])
	evm_max = float(rate[4][1])
	ppm_max = float(rate[5][1])
	#ppm_min = float(rate[5][0])
	ppm_min = 0 - ppm_max
	mask_min = float(rate[6][0])
	mask_max = float(rate[6][1])
	print 'power_min: %lf, power_max: %1f, evm_min: %1f, evm_max: %1f, ppm_min: %1f, ppm_max: %1f, mask_min: %1f, mask_max: %1f' %(power_min, power_max, evm_min, evm_max, ppm_min, ppm_max,mask_min, mask_max)
	ppm = 0
	rate_key = None
	status = 'Fail'
	retry_time_max = 10
	retry_time = 0
	print rate
	rate_key = rate[0]
	print 'rate_key: %s\n' % rate_key
	print channel
	
	#if ant.upper() == 'A':
	#	power_start_index = int(channel[2][str(rate_key)][0], 16)
	#elif ant.upper() == 'B':
	#	power_start_index = int(channel[2][str(rate_key)][1], 16)
	#else:
	#	raise Exception("ANT error %s") % ant
	if ant.upper() == 'A':
		power_start_index = int(channelRate_dict_all[str(channel[0])][rate_key][0], 16)
	elif ant.upper() == 'B':
		power_start_index = int(channelRate_dict_all[str(channel[0])][rate_key][1], 16)
	else:
		raise Exception("ANT error %s") % ant	
	
	print 'channel: %d, channel_external_att: %f, power_idx: %d\n' % (channel[0], channel[1], power_start_index)
	record_file_name =log_dir + '/'+ant.upper()+'_channel_' + str(channel[0]) + '_' +str(rate[0])+'.txt'
	print record_file_name
	os.system('echo power	  evm	  ppm 	  mask 	  result >' +record_file_name)
	ser.start_mp_ctx(channel[0], rate[1], power_start_index, bandWidth_set, ant.lower(), interface=mp_iface)	
	time.sleep(3)

	if  channel[0] < 36:
		vsa_freq_set = ((channel[0] -1)*5 + freq_base_2_4g) * 1e6
	elif channel[0] >= 149:
		vsa_freq_set = ((channel[0] -149) / 2 *10 + freq_base_5GHigh) * 1e6
	else:
		vsa_freq_set = ((channel[0] -36) / 2 *10 + freq_base_5GLow) * 1e6
	print vsa_freq_set
	ret = wt.WT_SetVSA_AutoRange(vsa_freq_set, wt_demod, rfPort, trig_type, trig_level, smp_time, trig_pretime, TimeoutWaiting, trig_timeout, max_power, g_external_gain)
	if ret != WT_ERR_CODE_OK:
		print 'WT_SetVSA_AutoRange set fail: %d' % ret
		sys.exit()
	#time.sleep(1)
	while (test_time > 0):
		if retry_time >= retry_time_max:
			print 'retry_time end: %d, now break\n' % retry_time
			sys.exit()
		ret = wt.WT_DataCapture()
		if WT_ERR_CODE_OK != ret:
			raise Exception("WT_DataCapture ret: %d\n") % ret	
		ret, power_all, description, unit= wt.WT_GetResult(WT_RES_POWER_ALL_DB)
		print "power all ret: %d\n"  % ret
		if WT_ERR_CODE_OK != ret:
			print "get power_all error %d" % ret
			retry_time = retry_time + 1
			continue
		print "power all: %lf dBm\n"  % power_all
		ret, power_frame, description, unit= wt.WT_GetResult(WT_RES_POWER_FRAME_DB)
		print "power_frame ret: %d\n"  % ret
		print "power_frame: %lf dBm\n"  % power_frame
		#print "power all description: %s\n"  % description
		#print "power all unit: %s\n"  % unit
		power_frame = power_frame + channel[1]
		print "power frame add wireATT: %lf dBm\n"  % power_frame
		ret, evm_all, description, unit = wt.WT_GetResult(WT_RES_FRAME_EVM_ALL)
		print "EVM_ALL ret: %d\n" % ret
		if WT_ERR_CODE_OK != ret:
			print ("get evm_all error %d") % ret
			retry_time = retry_time + 1
			continue
		print "EVM_ALL: %lf dBm\n"  % evm_all
		#print "EVM_ALL description: %s\n"  % description
		#print "EVM_ALL unit: %s\n"  % unit
		ret, freq_err, description, unit = wt.WT_GetResult(WT_RES_FRAME_FREQ_ERR)
		print "freq_err ret: %d\n"  % ret
		if WT_ERR_CODE_OK != ret:
			print ("get freq_err error %d") % ret
			retry_time = retry_time + 1
			continue
		print "FREQ_ERR ret: %d\n" % ret
		print "FREQ_ERR: %lf Hz\n"  % freq_err
		#print "FREQ_ERR description: %s\n"  % description
		#print "FREQ_ERR unit: %s\n"  % unit
		ppm = round(float(freq_err) / float(vsa_freq_set/1e6), 2)
		print "ppm: %lf\n"  % ppm
		ret, mask, description, unit = wt.WT_GetResult(WT_RES_SPECTRUM_MASK_ERR_PERCENT)
		print "mask ret: %d\n"  % ret
		if WT_ERR_CODE_OK != ret:
			print ("get mask error %d") % ret
			retry_time = retry_time + 1
			continue
		print "mask: %lf\n"  % mask
		#print "mask description: %s\n"  % description
		#print "mask unit: %s\n"  % unit
		#if evm_all > evm_max or  ppm > ppm_max or ppm < ppm_min or mask > mask_max or mask < mask_min:
		if power_frame < power_min or evm_all > evm_max or  abs(ppm) > ppm_max  or abs(ppm) < ppm_min or mask > mask_max or mask < mask_min:
			status = 'Fail'
		else:
			status = 'Pass'
		os.system('echo ' +str(round(power_frame, 2)) + '	'+ str(round(evm_all, 2)) + '	' + str(ppm)+ '	'+ str(round(mask, 2)) + '	' +str(status) +'>> ' + record_file_name)		
		time.sleep(0.6)
		test_time = test_time - 1
	ser.stop_mp_tx(mp_iface)
	#time.sleep(1)
	#wt.WT_StopDataCapture()
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

def mp_tx_RTL_serial(wt_demod, channel_list, rate_list, wt, ser, log_dir, bandWidth_set, ant, rfPort=RF_PORT_Default, trig_type=WT_TRIG_TYPE_IF, trig_level=-31, smp_time=2000, trig_pretime=20, TimeoutWaiting=5, trig_timeout=5, max_power=0.0, g_external_gain=0.0, test_time=3):
	for channel in channel_list:
		for rate in rate_list:
			record_mp_tx_file_RTL_serial(wt, ser, log_dir, wt_demod, channel, bandWidth_set, rate, ant, rfPort, trig_type, trig_level, smp_time, trig_pretime, TimeoutWaiting, trig_timeout, max_power, g_external_gain, test_time)
			
def mp_rx_MTK_serial(channel_list, rate_list, wt, ser, log_dir, bandWidth_set, ant, FREQOFFSET, repeat=1000, waveType=SIG_USERFILE, rfPort=RF_PORT_Default, wave_gap=200):
	for channel in channel_list:
		for rate in rate_list:
			record_mp_rx_file_MTK_serial(wt, ser, log_dir, channel, bandWidth_set, rate, ant, FREQOFFSET, repeat, waveType, rfPort,wave_gap)			
			
if __name__ == '__main__':

	try:
		opts, args = getopt.getopt(sys.argv[1:], "hT:c:a:b:m:u:p:s:f:i:e:C:r:B:S:P:R:l:", ["help","Txconfig=","mode=", "server=", "finish=", "interface=", "external_att=", "COM=", "rate=", "Band=", "fa=", "fb=", "Standard=", "PowerRateFile=", "RateIndexFile=", "logdir="])
	except getopt.GetoptError:
		print "getopt error!"
	if len(opts) == 0:
		usage()
		sys.exit()
	for o,a in opts:
		if o in ("-h","--help"):
			usage()
			sys.exit()
		elif o in ("-T","--Txconfig"):
			Txconfig_file=a
			print 'Txconfig_file: %s\n' % Txconfig_file
		elif o in ("-P","--PowerRateFile"):
			PowerRateFile=str(a)
			print 'PowerRateFile: %s\n' % PowerRateFile		
		elif o in ("-m","--mode"):
			model=a.upper()
			print 'mode: %s\n' % model
		elif o in ("-s","--server"):
			wt_server=a
			print 'wt_server: %s\n' % wt_server
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
			pass_standard_file=str(a)
			print 'pass_standard_file: %s\n' % pass_standard_file
		elif o in ("-R", "--RateIndexFile"):
			RateIndexFile=str(a)
			print 'RateIndexFile: %s\n' % RateIndexFile
		elif o in ("-l", "--logdir"):
			log_dir=str(a)
			print 'RateIndexFile: %s\n' % RateIndexFile			
		else:
			usage()
			sys.exit()
	print 'mp_iface: %s\n' % mp_iface
	
	wt = connect_WT_server()
	log_dir = mkLoginDir()
	#log_dir = './log/TX_2016-12-08-15-22-55_5G_97F-7384-NO.1212-nfjrom161130/'
	#log_dir = './log/TX_2016-12-14-21-12-01_5G_97F-7384No.1212-nfjrom161212.7384_L2/'

	readwiresATT(a_wireAtt_file, b_wireAtt_file)
	#channelRate_dict_all = readChannelRatePowerIndex(PowerRateFile)
	#cmd = 'xcopy '+PowerRateFile + ' ' +log_dir
	#print cmd
	#os.system(cmd)
	#print A_channel_2_4G
	#print B_channel_2_4G
	#print '------------5G_20M-----------'
	#print A_channel_5G_20M
	#print B_channel_5G_20M
	#print '------------5G_40M-----------'
	#print A_channel_5G_40M
	#print B_channel_5G_40M
	#print '------------5G_80M-----------'
	#print A_channel_5G_80M
	#print B_channel_5G_80M	
	#readMPRateIndex(RateIndexFile)
	
	readTXwifiCFG(pass_standard_file)
	#print rate_11B
	#print rate_11G
	#print rate_11N_20M
	#print rate_11N_40M
	#print rate_5G_20M
	#print rate_5G_40M
	#print rate_5G_80M
	
	if band.upper() == '2.4G':
		if model in RTL_model:
			ser = RTL_MP_Serial.RTL_MP_Serial(COM, bps, finish)
			ser.mp_start(interface=mp_iface)
			#ANTA_A_11B
			#adjust_mp_tx_RTL_serial(WT_DEMOD_11B, A_channel_2_4G, rate_11B, wt, ser, log_dir, bandWidth_20M_RTL, 'A')
			#mp_tx_RTL_serial(WT_DEMOD_11B, A_channel_2_4G, rate_11B, wt, ser, log_dir, bandWidth_20M_RTL, 'A')
			#ANTA_A_11G
			adjust_mp_tx_RTL_serial(WT_DEMOD_11AG, A_channel_2_4G[-3:], rate_11G, wt, ser, log_dir, bandWidth_20M_RTL, 'A')
			#mp_tx_RTL_serial(WT_DEMOD_11AG, A_channel_2_4G, rate_11G, wt, ser, log_dir, bandWidth_20M_RTL, 'A')
			#ANTA_A_11N_20M
			adjust_mp_tx_RTL_serial(WT_DEMOD_11N_20M, A_channel_2_4G, rate_11N_20M , wt, ser, log_dir, bandWidth_20M_RTL, 'A')
			#mp_tx_RTL_serial(WT_DEMOD_11N_20M, A_channel_2_4G, rate_11N_20M , wt, ser, log_dir, bandWidth_20M_RTL, 'A')
			#ANTA_A_11N_40M
			adjust_mp_tx_RTL_serial(WT_DEMOD_11N_40M, A_channel_2_4G_40M, rate_11N_40M, wt, ser, log_dir, bandWidth_40M_RTL,'A')
			#mp_tx_RTL_serial(WT_DEMOD_11N_40M, A_channel_2_4G_40M, rate_11N_40M, wt, ser, log_dir, bandWidth_40M_RTL,'A')

			#ANTA_B_11B
			adjust_mp_tx_RTL_serial(WT_DEMOD_11B, B_channel_2_4G, rate_11B, wt, ser, log_dir, bandWidth_20M_RTL, 'B')
			#mp_tx_RTL_serial(WT_DEMOD_11B, B_channel_2_4G, rate_11B, wt, ser, log_dir, bandWidth_20M_RTL, 'B')
			#ANTA_B_11G
			adjust_mp_tx_RTL_serial(WT_DEMOD_11AG, B_channel_2_4G, rate_11G, wt, ser, log_dir, bandWidth_20M_RTL, 'B')
			#mp_tx_RTL_serial(WT_DEMOD_11AG, B_channel_2_4G, rate_11G, wt, ser, log_dir, bandWidth_20M_RTL, 'B')
			#ANTA_B_11N_20M
			adjust_mp_tx_RTL_serial(WT_DEMOD_11N_20M, B_channel_2_4G, rate_11N_20M, wt, ser, log_dir, bandWidth_20M_RTL, 'B')
			#mp_tx_RTL_serial(WT_DEMOD_11N_20M, B_channel_2_4G, rate_11N_20M, wt, ser, log_dir, bandWidth_20M_RTL, 'B')
			#ANTA_B_11N_40M
			adjust_mp_tx_RTL_serial(WT_DEMOD_11N_40M, B_channel_2_4G_40M, rate_11N_40M, wt, ser, log_dir, bandWidth_40M_RTL, 'B')
			#mp_tx_RTL_serial(WT_DEMOD_11N_40M, B_channel_2_4G_40M, rate_11N_40M, wt, ser, log_dir, bandWidth_40M_RTL, 'B')
			
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
			adjust_mp_tx_RTL_serial(WT_DEMOD_11AG, A_channel_5G_20M, rate_11G, wt, ser, log_dir, bandWidth_20M_RTL, 'A')
			#mp_tx_RTL_serial(WT_DEMOD_11AG, A_channel_5G_20M, rate_11G, wt, ser, log_dir, bandWidth_20M_RTL, 'A')
			#NTA_A_11N_20M
			adjust_mp_tx_RTL_serial(WT_DEMOD_11N_20M, A_channel_5G_20M, rate_11N_20M, wt, ser, log_dir, bandWidth_20M_RTL, 'A')
			#mp_tx_RTL_serial(WT_DEMOD_11N_20M, A_channel_5G_20M, rate_11N_20M, wt, ser, log_dir, bandWidth_20M_RTL, 'A')
			#NTA_A_11N_40M
			#mp_tx_RTL_serial(WT_DEMOD_11N_40M, A_channel_5G_40M, rate_11N_40M, wt, ser, log_dir, bandWidth_40M_RTL, 'A')
			#ANTA_A_VHT20
			#mp_tx_RTL_serial(WT_DEMOD_11AC_20M, A_channel_5G_20M, rate_5G_20M, wt, ser, log_dir, bandWidth_20M_RTL, 'A')
			#ANTA_A_VHT40
			#mp_tx_RTL_serial(WT_DEMOD_11AC_40M, A_channel_5G_40M, rate_5G_40M, wt, ser, log_dir, bandWidth_40M_RTL, 'A')
			##ANTA_A_VHT80
			#mp_tx_RTL_serial(WT_DEMOD_11AC_80M, A_channel_5G_80M, rate_5G_80M, wt, ser, log_dir, bandWidth_80M_RTL, 'A')
			#ANTA_B_OFDM
			adjust_mp_tx_RTL_serial(WT_DEMOD_11AG, B_channel_5G_20M, rate_11G, wt, ser, log_dir, bandWidth_20M_RTL, 'B')
			mp_tx_RTL_serial(WT_DEMOD_11AG, B_channel_5G_20M, rate_11G, wt, ser, log_dir, bandWidth_20M_RTL, 'B')
			#NTA_B_11N_20M
			adjust_mp_tx_RTL_serial(WT_DEMOD_11N_20M, B_channel_5G_20M, rate_11N_20M, wt, ser, log_dir, bandWidth_20M_RTL, 'B')
			mp_tx_RTL_serial(WT_DEMOD_11N_20M, B_channel_5G_20M, rate_11N_20M, wt, ser, log_dir, bandWidth_20M_RTL, 'B')
			#NTA_B_11N_40M
			#mp_tx_RTL_serial(WT_DEMOD_11N_40M, B_channel_5G_40M, rate_11N_40M, wt, ser, log_dir, bandWidth_40M_RTL, 'B')
			#ANTA_B_VHT20
			adjust_mp_tx_RTL_serial(WT_DEMOD_11AC_20M, B_channel_5G_20M, rate_5G_20M, wt, ser, log_dir, bandWidth_20M_RTL, 'B')
			#mp_tx_RTL_serial(WT_DEMOD_11AC_20M, B_channel_5G_20M, rate_5G_20M, wt, ser, log_dir, bandWidth_20M_RTL, 'B')
			#ANTA_B_VHT40
			#mp_tx_RTL_serial(WT_DEMOD_11AC_40M, B_channel_5G_40M, rate_5G_40M, wt, ser, log_dir, bandWidth_40M_RTL, 'B')
			##ANTA_B_VHT80
			#mp_tx_RTL_serial(WT_DEMOD_11AC_80M, B_channel_5G_80M, rate_5G_80M, wt, ser, log_dir, bandWidth_80M_RTL, 'B')
			
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
			#ANTA_B_VHT40
			mp_rx_MTK_serial(B_channel_5G_40M, rate_5G_40M, wt, ser, log_dir, bandWidth_40M_MTK, 'B', MTK_5G_FREQOFFSET)
			#ANTA_B_VHT80
			mp_rx_MTK_serial(B_channel_5G_80M, rate_5G_80M, wt, ser, log_dir, bandWidth_80M_MTK, 'B', MTK_5G_FREQOFFSET)
			ser.ser.serial_close()
	wt.WT_StopDataCapture()
	wt.WT_DLLTerminate()

	excel_name = model+'_'+str(band)+'_'+time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))+'.xls'
	#rx_data_sum_excel(log_dir, excel_name, model.upper(), band)
	adjust_xls_report(log_dir,excel_name,3,len(range(power_index_start,power_index_end,power_index_step)))