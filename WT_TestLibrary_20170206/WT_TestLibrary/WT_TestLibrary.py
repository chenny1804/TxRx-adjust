import WT_VSGLibrary
import time
import sys
reload(sys) 
sys.setdefaultencoding('utf8') 

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

#VSG Status
WT_VSG_STATE_DONE = 0
WT_VSG_STATE_RUNNING = 1
WT_VSG_STATE_TIMEOUT = 2
WT_VSG_STATE_ERR_DONE = 3
WT_VSG_STATE_WAITING = 4

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

#WT_TRIG_TYPE_ENUM
WT_TRIG_TYPE_FREE_RUN = 0        
WT_TRIG_TYPE_EXT = 1                      
WT_TRIG_TYPE_IF = 2
WT_TRIG_TYPE_IF_NO_CAL = 3

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

#WT_TRIG_TYPE_ENUM
WT_TRIG_TYPE_FREE_RUN = 0       
WT_TRIG_TYPE_EXT = 1                 
WT_TRIG_TYPE_IF = 2
WT_TRIG_TYPE_IF_NO_CAL = 3


class WT_TestLibrary:
	def __init__(self):
		self.wt = None

	def init_WT_Test(self, server_ip):
		self.wt = WT_VSGLibrary.WT_VSG(str(server_ip))
		return self.wt
		
	def WT_ForceConnect(self):
		ret = self.wt.WT_ForceConnect()
		return ret
	def WT_Connect(self):
		ret = self.wt.WT_Connect()
		return ret		
	def WT_DisConnect(self):
		ret = self.wt.WT_DisConnect()
		return ret	
		
	def WT_SetVSG(self, freq, power, waveType, wave_gap, rfPort, repeat, wave):
		print 'python: freq: %f, power: %f, waveType: %d, wave_gap: %f, rfPort: %d, repeat: %d' % (freq, power, waveType, wave_gap, rfPort, repeat)
		ret = self.wt.WT_SetVSG(freq, power, int(waveType), wave_gap, int(rfPort), int(repeat), str(wave))
		return ret
		
	def WT_SetVSG_local(self, freq, power, wave_gap, rfPort, repeat, wave):
		print 'python: freq: %f, power: %f, waveType: %d, wave_gap: %f, rfPort: %d, repeat: %d' % (freq, power, waveType, wave_gap, rfPort, repeat)
		ret = self.wt.WT_SetVSG(freq, power, 0, wave_gap, int(rfPort), int(repeat), str(wave))
		return ret	
		
	def WT_AsynStartVSG(self):
		ret = self.wt.WT_AsynStartVSG()
		return ret
		
	def WT_GetVSGCurrentState(self):
		ret = self.wt.WT_GetVSGCurrentState()
		return ret
	def WT_GetVSGCurrentState_check(self):
		ret = self.wt.GetVSGCurrentState_check()
		return ret
	def WT_GetVSGCurrentState_return(self):
		ret = self.wt.GetVSGCurrentState_return()
		return ret
		
	def wait_until_state_done(self, count=10):
		ret = -2
		while (count > 0):
			ret = self.wt.GetVSGCurrentState_check()
			if ret == -1:
				return ret
			if (ret != WT_VSG_STATE_RUNNING and ret != WT_VSG_STATE_WAITING):
				break;
			count = count -1
		return ret
		
	def WT_StopVSG(self):
		ret = self.wt.WT_StopVSG()
		return ret	
		
	def WT_DLLTerminate(self):
		ret = self.wt.WT_DLLTerminate()
		return ret
		
	def WT_DataCapture(self):
		ret = self.wt.WT_DataCapture()
		return ret
		
	def WT_StopDataCapture(self):
		ret = self.wt.WT_StopDataCapture()
		return ret	
	def WT_GetResult(self, anaParmString):
		ret = self.wt.WT_GetResult(str(anaParmString))
		return ret, self.wt.anaResult, self.wt.description, self.wt.unit
		
	def WT_SetVSA(self, freq, demod, rf_port, trig_type=WT_TRIG_TYPE_IF, trig_level=-31, smp_time=2000, trig_pretime=20, TimeoutWaiting=5, trig_timeout=5, max_power=0.0, g_external_gain=0.0):
		ret =  self.wt.WT_SetVSA(float(g_external_gain), float(max_power), int(freq), int(demod), int(rf_port), float(smp_time), int(TimeoutWaiting), float(trig_pretime), float(trig_level), int(trig_type), float(trig_timeout))
		return ret
		
	def WT_SetVSA_AutoRange(self, freq, demod, rf_port, trig_type=WT_TRIG_TYPE_IF, trig_level=-31, smp_time=2000, trig_pretime=20, TimeoutWaiting=5, trig_timeout=5, max_power=0.0, g_external_gain=0.0):
		ret =  self.wt.WT_SetVSA_AutoRange(float(g_external_gain), float(max_power), int(freq), int(demod), int(rf_port), float(smp_time), int(TimeoutWaiting), float(trig_pretime), float(trig_level), int(trig_type), float(trig_timeout))
		return ret	
	
	def get_power_evm_FrqEr(self):
		evm_ret = -1
		ret = self.wt.WT_DataCapture()
		if WT_ERR_CODE_OK != ret:
			raise Exception("WT_DataCapture ret: %d\n" % ret)
		ret, POWER_PEAK, description, unit = wt.WT_GetResult(WT_RES_POWER_PEAK_DB)
		evm_ret, EVM_PEAK, description, unit = wt.WT_GetResult(WT_RES_FRAME_EVM_PEAK)
		
		ret, FRAME_FREQ_ERR, description, unit = wt.WT_GetResult(WT_RES_FRAME_FREQ_ERR)
		return evm_ret, POWER_PEAK, EVM_PEAK, FRAME_FREQ_ERR
		
	def get_power(self):
		ret = self.wt.WT_DataCapture()
		if WT_ERR_CODE_OK != ret:
			raise Exception("WT_DataCapture ret: %d\n" % ret)
		ret, POWER_PEAK, description, unit = wt.WT_GetResult(WT_RES_POWER_PEAK_DB)
		
		return POWER_PEAK
		
	def sampling_power_evm(self, path, power, times=20, inter=0.5):
		ret = 0
		POWER_FRAME = ''
		POWER_FRAME_list = []
		POWER_ALL = ''
		POWER_ALL_list = []
		POWER_PEAK = ''
		POWER_PEAK_list = []
		EVM_ALL = ''
		EVM_ALL_list = []
		EVM_PEAK = ''
		EVM_PEAK_list = []
		EVM_ALL_PERCENT = ''
		EVM_ALL_PERCENT_list = []
		FRAME_FREQ_ERR = ''
		FRAME_FREQ_ERR_list = []
		MASK_list = []
		description = ''
		unit = ''
		evm_ok_count = 0
		while times > 0:
			ret = self.wt.WT_DataCapture()
			if WT_ERR_CODE_OK != ret:
				print "WT_DataCapture ret: %d\n" % ret
				time.sleep(inter)
				continue
			#ret, POWER_FRAME, description, unit= wt.WT_GetResult(WT_RES_POWER_FRAME_DB)
			#POWER_FRAME_list.append(POWER_FRAME)
			ret, POWER_ALL, description, unit= wt.WT_GetResult(WT_RES_POWER_ALL_DB)
			POWER_ALL_list.append(POWER_ALL)
			#ret, POWER_PEAK, description, unit = wt.WT_GetResult(WT_RES_POWER_PEAK_DB)
			#POWER_PEAK_list.append(POWER_PEAK)
			ret, EVM_ALL, description, unit = wt.WT_GetResult(WT_RES_FRAME_EVM_ALL)
			EVM_ALL_list.append(EVM_ALL)
			if ret == WT_ERR_CODE_OK:
				evm_ok_count = evm_ok_count + 1
			#ret, EVM_PEAK, description, unit = wt.WT_GetResult(WT_RES_FRAME_EVM_PEAK)
			#EVM_PEAK_list.append(EVM_PEAK)
			#ret, EVM_ALL_PERCENT, description, unit = wt.WT_GetResult(WT_RES_FRAME_EVM_ALL_PERCENT)
			#EVM_ALL_PERCENT_list.append(EVM_ALL_PERCENT)
			ret, FRAME_FREQ_ERR, description, unit = wt.WT_GetResult(WT_RES_FRAME_FREQ_ERR)
			FRAME_FREQ_ERR_list.append(FRAME_FREQ_ERR)
			ret, MASK, description, unit = wt.WT_GetResult(WT_RES_SPECTRUM_MASK_ERR_PERCENT)
			MASK_list.append(MASK)
			
			time.sleep(inter)
			
if __name__ == '__main__':
	g_wifi_11ag_freq = 2412*1e6
	SIG_802_11_G_6MBS = 101
	wt = WT_TestLibrary()
	wt.init_WT_Test('192.168.10.254')
	ret = wt.WT_Connect()
	#print 'WT_VConnect return: %d' % ret
	#ret = wt.WT_ForceConnect()
	#print 'WT_ForceConnect return: %d' % ret
	if ret != WT_ERR_CODE_OK:
		print 'WT_VSG_Connect set fail: %d' % ret
		sys.exit() 
	
	##int SetVSG(float freq, float power, int waveType, float vave_gap, int  rfPort, int repeat, char *wave)
	#ret = wt.WT_SetVSG(g_wifi_11ag_freq, -10.0, 0, 50, 1, 0, 'C:/Program Files (x86)/xgiga/WT200.wave/1 Mbps(DSSS).csv')
	##ret = wt.WT_SetVSG(g_wifi_11ag_freq, -10.0, 101, 50, 1, 0, None)
	#print 'WT_SetVSG return: %d' % ret
	#'''
	#if ret != WT_ERR_CODE_OK:
	#	print 'WT_SetVSG set fail: %d' % ret
	#	ret = wt.WT_StopVSG()
	#	print 'WT_StopVSG return: %d' % ret
	#	wt.WT_DLLTerminate()
	#	sys.exit() 
	#'''
	#ret = wt.WT_AsynStartVSG()
	#print 'WT_AsynStartVSG return: %d' % ret
	#
	#ret = wt.WT_GetVSGCurrentState()
	#print 'WT_GetVSGCurrentState return: %d' % ret
	#
	#time.sleep(8)
	#
	#ret = wt.WT_SetVSG(g_wifi_11ag_freq, -10.0, 0, 500, 1, 0, 'C:/Program Files (x86)/xgiga/WT200.wave/2 Mbps(DSSS).csv')
	##ret = wt.WT_SetVSG(g_wifi_11ag_freq, -10.0, 101, 500, 1, 0, None)
	#print 'WT_SetVSG return: %d' % ret
	#time.sleep(8)
	#ret = wt.WT_StopVSG()
	#print 'WT_StopVSG return: %d' % ret
	
	ret = wt.WT_SetVSA_AutoRange(g_wifi_11ag_freq, WT_DEMOD_11B, 1)
	if ret != WT_ERR_CODE_OK:
		print 'WT_SetVSA_AutoRange set fail: %d' % ret
		sys.exit() 
		
		
	while True:
		ret = wt.WT_DataCapture()
		if WT_ERR_CODE_OK != ret:
			print "WT_DataCapture ret: %d\n" % ret
	
		ret, data_result, description, unit= wt.WT_GetResult(WT_RES_POWER_FRAME_DB)
		if WT_ERR_CODE_OK == ret:
			print "power frame: %lf dBm\n"  % data_result
			print "power frame description: %s\n"  % description
			print "power frame unit: %s\n"  % unit
			
		ret, data_result, description, unit= wt.WT_GetResult(WT_RES_POWER_ALL_DB)
		if WT_ERR_CODE_OK == ret:
			print "power all: %lf dBm\n"  % data_result
			print "power all description: %s\n"  % description
			print "power all unit: %s\n"  % unit
		ret, data_result, description, unit = wt.WT_GetResult(WT_RES_POWER_PEAK_DB)
		if WT_ERR_CODE_OK == ret:
			print "power peak: %lf dBm\n"  % data_result
			print "power peak description: %s\n"  % description
			print "power peak unit: %s\n"  % unit
			
		ret, data_result, description, unit = wt.WT_GetResult(WT_RES_FRAME_EVM_ALL)
		print "EVM_ALL ret: %d\n" % ret
		print "EVM_ALL: %lf dBm\n"  % data_result
		print "EVM_ALL description: %s\n"  % description
		print "EVM_ALL unit: %s\n"  % unit
			
		ret, data_result, description, unit = wt.WT_GetResult(WT_RES_FRAME_EVM_PEAK)
		print "EVM_PEAK ret: %d\n" % ret
		print "EVM_PEAK: %lf dBm\n"  % data_result
		print "EVM_PEAK description: %s\n"  % description
		print "EVM_PEAK unit: %s\n"  % unit	
		
		ret, data_result, description, unit = wt.WT_GetResult(WT_RES_FRAME_EVM_ALL_PERCENT)
		print "ALL_PERCENT ret: %d\n" % ret
		print "ALL_PERCENT: %lf\n"  % data_result
		print "ALL_PERCENT description: %s\n"  % description
		print "ALL_PERCENT unit: %s\n"  % unit
	
		ret, data_result, description, unit = wt.WT_GetResult(WT_RES_FRAME_FREQ_ERR)
		print "FREQ_ERR ret: %d\n" % ret
		print "FREQ_ERR: %lf Hz\n"  % data_result
		print "FREQ_ERR description: %s\n"  % description
		print "FREQ_ERR unit: %s\n"  % unit		
		ret, data_result, description, unit = wt.WT_GetResult(WT_RES_SPECTRUM_MASK_ERR_PERCENT)
		print "mask ret: %d\n" % ret
		print "mask: %lf Hz\n"  % data_result
		print "mask description: %s\n"  % description
		print "mask unit: %s\n"  % unit		
		time.sleep(1)
	wt.WT_DLLTerminate()
      

		
        
