import time
import string
import os
import re
import sys
reload(sys) 
sys.setdefaultencoding('utf8')

TX_PASS_POWER_2_4G = 'TX_PASS_POWER_2_4G'
TX_LIMIT_POWER_2_4G = 'TX_LIMIT_POWER_2_4G'
TX_PASS_POWER_5_0G = 'TX_PASS_POWER_5_0G'
TX_LIMIT_POWER_5_0G = 'TX_LIMIT_POWER_5_0G'
TX_EVM_11B_LIMIT = 'TX_EVM_11B_LIMIT'
TX_EVM_11G_LIMIT = 'TX_EVM_11G_LIMIT'
TX_EVM_HT20_LIMIT = 'TX_EVM_HT20_LIMIT'
TX_EVM_HT40_LIMIT = 'TX_EVM_HT40_LIMIT'
TX_EVM_VHT20_LIMIT = 'TX_EVM_VHT20_LIMIT'
TX_EVM_VHT40_LIMIT = 'TX_EVM_VHT40_LIMIT'
TX_EVM_VHT80_LIMIT = 'TX_EVM_VHT80_LIMIT'
TX_EVM_VHT160_LIMIT = 'TX_EVM_VHT160_LIMIT'
FREQ_ERR_PASS_LIMIT = 'FREQ_ERR_PASS_LIMIT'
FREQ_ERR_FINE_LIMIT = 'FREQ_ERR_FINE_LIMIT'
MASK_ERR_LIMIT = 'MASK_ERR_LIMIT'
EVM_min_limit = -60.0
mask_min_limit = 0.0

class Read_TXCFG:
	fb = None
	all_text =  None
	def __init__(self, fileName):
		self.fb = open(fileName, 'r')
		try:
			self.all_text = self.fb.read( )
			print self.all_text
		except IOError, e:  
			print e
			self.fb.close()

	def close_file(self):
		self.fb.close()
	def read_power_stand(self):
		power_2_4G_list = []
		power_5G_list = []
		power_min_2_4G = re.split(TX_PASS_POWER_2_4G+'\s+=\s+', self.all_text)[1].split('\n')[0].split('\t')
		power_max_2_4G = re.split(TX_LIMIT_POWER_2_4G+'\s+=\s+', self.all_text)[1].split('\n')[0].split('\t')
		power_min_5G = re.split(TX_PASS_POWER_5_0G+'\s+=\s+', self.all_text)[1].split('\n')[0].split('\t')
		power_max_5G = re.split(TX_LIMIT_POWER_5_0G+'\s+=\s+', self.all_text)[1].split('\n')[0].split('\t')
		power_2_4G_len = len(power_min_2_4G)
		power_5G_len = len(power_min_5G)
		for i in range(power_2_4G_len):
			power_2_4G_list.append([float(power_min_2_4G[i]), float(power_max_2_4G[i])])
		for i in range(power_5G_len):
			power_5G_list.append([float(power_min_5G[i]), float(power_max_5G[i])])
		return [power_2_4G_list, power_5G_list]
	
	def read_evm_stand(self):
		TX_EVM_11B_list = map(eval, re.split(TX_EVM_11B_LIMIT+'\s+=\s+', self.all_text)[1].split('\n')[0].split('\t'))
		TX_EVM_11G_list = map(eval, re.split(TX_EVM_11G_LIMIT+'\s+=\s+', self.all_text)[1].split('\n')[0].split('\t'))
		TX_EVM_HT20_list = map(eval, re.split(TX_EVM_HT20_LIMIT+'\s+=\s+', self.all_text)[1].split('\n')[0].split('\t'))
		TX_EVM_HT40_list = map(eval, re.split(TX_EVM_HT40_LIMIT+'\s+=\s+', self.all_text)[1].split('\n')[0].split('\t'))
		TX_EVM_VHT20_list = map(eval, re.split(TX_EVM_VHT20_LIMIT+'\s+=\s+', self.all_text)[1].split('\n')[0].split('\t'))
		TX_EVM_VHT40_list = map(eval, re.split(TX_EVM_VHT40_LIMIT+'\s+=\s+', self.all_text)[1].split('\n')[0].split('\t'))
		TX_EVM_VHT80_list = map(eval, re.split(TX_EVM_VHT80_LIMIT+'\s+=\s+', self.all_text)[1].split('\n')[0].split('\t'))
		TX_EVM_VHT160_list = map(eval, re.split(TX_EVM_VHT160_LIMIT+'\s+=\s+', self.all_text)[1].split('\n')[0].split('\t'))
		return [TX_EVM_11B_list, TX_EVM_11G_list, TX_EVM_HT20_list, TX_EVM_HT40_list, TX_EVM_VHT20_list, TX_EVM_VHT40_list, TX_EVM_VHT80_list, TX_EVM_VHT160_list]
	
	def read_ppm_stand(self):
		ppm_list = []
		FREQ_ERR_PASS_list = re.split(FREQ_ERR_PASS_LIMIT+'\s+=\s+', self.all_text)[1].split('\n')[0].split('\t')
		FREQ_ERR_FINE_list = re.split(FREQ_ERR_FINE_LIMIT+'\s+=\s+', self.all_text)[1].split('\n')[0].split('\t')	
		FREQ_ERR_PASS_len = len(FREQ_ERR_PASS_list)
		FREQ_ERR_FINE_len = len(FREQ_ERR_FINE_list)
		for i in range(FREQ_ERR_PASS_len):
			ppm_list.append([float(FREQ_ERR_FINE_list[i]), float(FREQ_ERR_PASS_list[i])])
		return ppm_list
		
	def read_mask_stand(self):
		mask_list = map(eval, re.split(MASK_ERR_LIMIT+'\s+=\s+', self.all_text)[1].split('\n')[0].split('\t'))
		return mask_list	
if __name__ == '__main__':
	rt = Read_TXCFG('WiFi(B).cfg')
	power_list = rt.read_power_stand()
	print power_list
	evm_list = rt.read_evm_stand()
	print evm_list
	ppm_list = rt.read_ppm_stand()
	print ppm_list
	mask_list = rt.read_mask_stand()
	print mask_list
	rt.close_file()