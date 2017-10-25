# -*- coding: cp936 -*-
import xlwt,re
import xlrd,os
import sys
from xlutils.copy import copy
reload(sys) 
sys.setdefaultencoding('utf8')

#POWERFAIL��style:��׺���
styleRedbk_blackFont=xlwt.easyxf("pattern:pattern solid,fore_colour red; font:color black;align:horz center;")
##EVMFAIL��style:�ҵ׺���
styleGreybk_blackFont=xlwt.easyxf("pattern:pattern solid,fore_colour gray25; font:color black;align:horz center;")
#PPMFAIL��style:��ɫ�׺���
styleOrangebk_blackFont=xlwt.easyxf("pattern:pattern solid,fore_colour light_orange; font:color black;align:horz center;")
#MASKFAIL��style:��ɫ�׺���
styleYellowbk_blackFont=xlwt.easyxf("pattern:pattern solid,fore_colour yellow; font:color black;align:horz center;")
#PASS��style:�׵�����
styleWhitebk_greenFont=xlwt.easyxf("pattern:pattern solid,fore_colour white; font:color green,bold on;align:horz center;")
#����״̬��style:�׵׺���
styleDefault=xlwt.easyxf("pattern:pattern solid,fore_colour white; font:color black;align:horz center;")

def write_data(sheet,row,col,values,style):
	sheet.write(row,col,values,style)
	
	
def read_and_copy(filename,sheetname):
#�����������ݵ�xls�������Ƶ���д��xls
	with xlrd.open_workbook(filename,formatting_info=True) as read_xls:
		rows=0
		if sheetname in read_xls.sheet_names():
			read_sheet=read_xls.sheet_by_name(sheetname)
			sheet_index=read_sheet.number
			rows=read_sheet.nrows
			write_xls_workbook=copy(read_xls)
			sheet_write=write_xls_workbook.get_sheet(sheet_index)
		else:
			write_xls_workbook=copy(read_xls)
			sheet_write=add_sheet(write_xls_workbook,sheetname)
	return write_xls_workbook,sheet_write,rows
	
	
def add_sheet(write_xls_workbook,sheetname):
	new_sheet=write_xls_workbook.add_sheet(sheetname,cell_overwrite_ok=True)
	return new_sheet
	
	
def get_log_name_list(path):
	#�����ĵ�����ʱ�����򣬷����ļ���
	new_filename_list=[]
	file_list= os.listdir(path)
	file_dict={}
	for file_name in file_list:
		filestat=os.stat(path+"/"+file_name)
		file_dict[file_name]=filestat.st_ctime
	#print file_dict
	sort_file_name=sorted(file_dict.items(),key=lambda file_dict:file_dict[1])
	#print sort_file_name
	for filename in sort_file_name:
		if 'channel' in filename[0]:
			new_filename_list.append(filename[0])
	print new_filename_list
	return new_filename_list
	
def mkxlsfile(filename):
	#����һ��xls�ĵ�
	#make a new xls 
	newworkbook=xlwt.Workbook()
	newsheet=newworkbook.add_sheet('Introdue')
	row=0
	col=0
	newsheet.write(row,col,"Result",styleDefault)
	newsheet.write(row,col+1,"STYLE",styleDefault)
	newsheet.write(row+1,col,"Power Fail",styleDefault)
	newsheet.write(row+1,col+1,"Power Fail",styleRedbk_blackFont)
	newsheet.write(row+2,col,"EVM Fail",styleDefault)
	newsheet.write(row+2,col+1,"EVM Fail",styleGreybk_blackFont)
	newsheet.write(row+3,col,"PPM Fail",styleDefault)
	newsheet.write(row+3,col+1,"PPM Fail",styleOrangebk_blackFont)
	newsheet.write(row+4,col,"MASK Fail",styleDefault)
	newsheet.write(row+4,col+1,"MASK Fail",styleYellowbk_blackFont)
	newsheet.write(row+5,col,"PASS",styleDefault)
	newsheet.write(row+5,col+1,"PASS",styleWhitebk_greenFont)
	newworkbook.save(filename)
	
	
def analysisResult(filename,testtime):
#������־�ļ�����
	with open(filename,'r') as fd:
		lines=fd.readlines()
	fd.close()
	count=testtime
	result_list=[]
	flags=True
	for line in lines[1:]:
		result=re.split('\s+', line.strip())
		if count > 1:
			if result[-1] != 'PASS':
				flags=False
			flags=flags and True
			count=count-1
			continue
		else:
			result_list.append(result)
			count=testtime
	
	return result_list
	
def adjust_xls_report(path,excel_filename,testtime,total_index_num):
#����xls����
#����:
#	1����ȡ��־�ļ����б�
#	2�������µ�xls�ĵ�
#	3��������־�ļ�����ÿһ����־���д��xls�ĵ�
	log_files_list=get_log_name_list(path)
	#print "log file :",log_files_list
	
	mkxlsfile(path+'\\'+excel_filename)
	
	for filename in log_files_list:
		result_list=analysisResult(path+'\\'+filename,testtime)
		#print result_list
		split_filename=filename.split('.txt')[0].split('_')
		print split_filename
		sheet_name=split_filename[-1]
		col=int(split_filename[2])
		
		ant=split_filename[0]
		print "ANT:",ant,"sheet_name",sheet_name,"channel:",col
		
		#�����е�xls�ĵ����ݱ�������д��������
		write_xls_workbook,sheet_write,nrows=read_and_copy(path+'\\'+excel_filename,sheet_name)
		
		if nrows == 0:
			#�ĵ�û������ʱ����д����������
			write_data(sheet_write,0,0,"ANT",styleDefault)
			write_data(sheet_write,0,1,"index\\ch",styleDefault)
			for i in range(2,15,1):
				write_data(sheet_write,0,i,i-1,styleDefault)
			nrows=1
		i=0
		#�ĵ�������ʱ���ڶ�Ӧ�������е�����д������
		for result in result_list:
			#����result���
			if result[-1].upper()=="POWERFAIL":
				style=styleRedbk_blackFont
			elif result[-1].upper() == "EVMFAIL":
				style=styleGreybk_blackFont
			elif result[-1].upper() == "PPMFAIL":
				style=styleOrangebk_blackFont
			elif result[-1].upper() == "MASKFAIL":
				style=styleYellowbk_blackFont
			elif result[-1].upper() == "PASS":
				style=styleWhitebk_greenFont
			else:
				style=styleDefault
			#print result
			if ant == 'A':
				nrows=1
				#write ant
				write_data(sheet_write,nrows+i,0,ant,styleDefault)
				#write power index
				write_data(sheet_write,nrows+i,1,int(result[0]),styleDefault)
				#write power				
				write_data(sheet_write,nrows+i,col+1,float(result[1]),style)
			elif ant == 'B':
				nrows=total_index_num+2
				write_data(sheet_write,nrows+i,0,ant,styleDefault)
				#write power index
				write_data(sheet_write,nrows+i,1,int(result[0]),styleDefault)
				#write power
				write_data(sheet_write,nrows+i,col+1,float(result[1]),style)
			else:
				raise("ANT Error")
			i=i+1
		write_xls_workbook.save(path+'\\'+excel_filename)
	
if __name__ == '__main__':
	adjust_xls_report('.\log\Adjust_TX_2017-01-10-15-16-28_2.4G_96D','adjust_96d_2.4G.xls',3,len(range(40,64,1)))
	#get_log_name_list('')
	pass
