import time
import WT_TestLibrary
import string
import getopt
import telnetlib
import sys
reload(sys) 
sys.setdefaultencoding('utf8')

power_min = 18
power_max = 24
power_index_min = 0
power_index_max = 63
ANTA = 'A'
model = 'P1'
RTL_model = ['P0', 'P1', 'P2S']
MTK_model = ['P2', 'R1']
channel_2_4G = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
freq_base = 2412*1e6
rate_11B = [['1M', 1], ['2M', 2], ['5.5M', 4], ['11M', 8]]
rate_11AG = []
bandWidth_20M = 'mp_bandwidth 40M=0'
bandWidth_40M = 'mp_bandwidth 40M=1'
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
mp_iface = 'wlan0'
LOGPATH='./log/'
RF_PORT_Default = 1


def usage():
	print '''usage:
	python nonSignaling_test.py -l 18 -r 24 -a A -m P2 -s 192.168.10.254
	'''

   
def mkLoginDir():
	dir=LOGPATH+time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
	print dir
	if not os.path.exists(dir):
		os.mkdir(dir)

			
def login_router(host=client_ip, username=username, password=password, promt=finish):
	tn = telnetlib.Telnet(host=Host, timeout=5)  
	print 'open success'
	tn.read_until('login')  
	tn.write(username + '\n')  
	print 'input login success'
	
	tn.read_until('Password')  
	tn.write(password + '\n')  
	print 'input password success'
	tn.read_until(finish, 5)
	return tn
def stop_mp_ctx_RTL(tn, interface=mp_iface):
	cmd = 'iwpriv ' + interface +' mp_ctx stop'
	tn.write(cmd + '\n')  
	tn.read_until(finish, 5)
	
def mp_start_RTL(tn, interface=mp_iface):
	tn.write('ifconfig ' +interface +' down\n')  
	tn.read_until(finish, 5)
	tn.write('iwpriv ' +interface +' set_mib mp_specific=1\n')  
	tn.read_until(finish, 5)
	tn.write('ifconfig ' +interface +' up\n')  
	tn.read_until(finish, 5)
	tn.write('iwpriv ' +interface +' mp_start\n')  
	tn.read_until(finish, 5)
	
def start_mp_ctx_RTL(tn, channel, rate, power, bandWidth_set, interface=mp_iface):	
	tn.write('iwpriv ' +interface +' mp_channel ' +channel+ '\n')  
	tn.read_until(finish, 5)
	tn.write('iwpriv ' +interface +' mp_rate ' +rate+ '\n')  
	tn.read_until(finish, 5)
	tn.write('iwpriv ' +interface +'  mp_txpower patha=' +power+ ' pathb=' + power+'\n')  
	tn.read_until(finish, 5)
	tn.write('iwpriv ' +interface +'  mp_bandwidth ' +bandWidth_set+ ',shortGI=0\n')  
	tn.read_until(finish, 5)	
	tn.write('iwpriv ' +interface +'  mp_ant_tx ' +ant+'\n')  
	tn.read_until(finish, 5)	
	tn.write('iwpriv ' +interface +'  mp_ctx pkt,background\n')  
	tn.read_until(finish, 5)
	
def mp_query_RTL(tn, interface=mp_iface):
	tn.write('iwpriv ' +interface +' mp_query\n')  
	out = tn.read_until(finish, 5)
	
def connect_WT_server(wt_server=wt_server):
	wt = WT_TestLibrary()
	wt.init_WT_Test('192.168.10.254')
	ret = wt.WT_Connect()
	if ret != WT_ERR_CODE_OK:
		print 'WT_VSG_Connect set fail: %d' % ret
		sys.exit()
	return wt
	
def find_suitable_start_index(wt, wt_mode, tn, channel, rate, bandWidth_set, interface=mp_iface):
	power_index_suitable = 0
	ret = wt.WT_SetVSA_AutoRange(((channel -1)*5 + 1) *freq_base, wt_mode, RF_PORT_Default)
	if ret != WT_ERR_CODE_OK:
		print 'WT_SetVSA_AutoRange set fail: %d' % ret
		sys.exit() 
	for power_index in range(power_index_min, power_index_max+1):
		start_mp_ctx_RTL(tn, channel, rate[1], power_index, bandWidth_set, interface)
		time.sleep(1)
		power_ret = wt.get_power()
		if power_ret >= power_min:
			power_index_suitable = power_index
			break
	if power_index_suitable == 0:
		raise Exception("find suit start error: %d\n" % power_index_suitable)
	return power_index_suitable

def record_mp_file(wt, wt_mode, tn, channel, rate, power_index_start, bandWidth_set, interface=mp_iface):
	ret = wt.WT_SetVSA_AutoRange(((channel -1)*5 + 1) * freq_base, wt_mode, RF_PORT_Default)
	if ret != WT_ERR_CODE_OK:
		print 'WT_SetVSA_AutoRange set fail: %d' % ret
		sys.exit() 
	for power_index in range(power_index_start, power_index_max+1):
		start_mp_ctx_RTL(tn, channel, rate[1], power_index, bandWidth_set, interface)
		time.sleep(1)
		evm_ret, POWER_PEAK, EVM_PEAK, FRAME_FREQ_ERR = wt.get_power_evm_FrqEr()
		if power_peak > power_max:
			print 'loop to power_max: %f\n' % power_max
			break
		else:
			os.system('echo ANTA' +ANTA+'/'+ channel+'/'+rate[0]+'/'+'Power: '+POWER_PEAK+' EVM: ' + EVM_PEAK+' FrqEr: '+FRAME_FREQ_ERR > './power_evm_frqer.txt')
		
if __name__ == '__main__':
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hl:r:c:a:m:u:p:s:f:i", ["help","power_left=","power_right=","anta=","mode=", "client_ip=", "username=", "password=", "server=", "finish=", "interface="])
	except getopt.GetoptError:
		print "getopt error!"
	if len(opts) == 0:
		usage()
		sys.exit()
	for o,a in opts:
		if o in ("-h","--help"):
			usage()
			sys.exit()
		elif o in ("-l","--power_left"):
			power_min=string.atoi(a)
			print 'power_min: %d\n' % power_min
		elif o in ("-r","--power_right"):
			power_max=string.atoi(a)
			print 'power_min: %d\n' % power_max
		elif o in ("-a","--anta"):
			ANTA=a
			print 'ANTA: %s\n' % ANTA
		elif o in ("-m","--mode"):
			model_detail=a
			print 'mode: %s\n' % model_detail
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
		else:
			usage()
			sys.exit()
	#tn = login_router()
	#wt = connect_WT_server()
	if mode.upercase() in RTL_model:
		#11B mode
		for channel in range(1, 14):
			for rate in rate_11B:
				start_index = find_suitable_start_index(wt, WT_DEMOD_11B, tn, channel, rate, bandWidth_set, mp_iface)
				record_mp_file(wt, wt_mode, tn, channel, rate, start_index, bandWidth_20M, mp_iface)
		#11AG mode
		for channel in range(1, 14):
			for rate in rate_11AG:
				start_index = find_suitable_start_index(wt, WT_DEMOD_11AG, tn, channel, rate, bandWidth_set, mp_iface)
				record_mp_file(wt, wt_mode, tn, channel, rate, start_index, bandWidth_20M, mp_iface)
	elif mode.uppercase() in MTK_model:
		print 'MTK_model\n'
		
	
	
	