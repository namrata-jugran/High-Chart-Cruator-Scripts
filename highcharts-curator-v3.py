import mammoth
import ntpath
import tkinter.filedialog

from datetime import datetime
import json
import os
import re
from os import getcwd

root = tkinter.Tk()
root.withdraw()

chart = ""
divId = ""
scripts = '<script src="https://code.highcharts.com/highcharts.js"></script> <script src="https://code.highcharts.com/highcharts-more.js"></script> <script src="https://code.highcharts.com/modules/dumbbell.js"></script> <script src="https://code.highcharts.com/modules/exporting.js"></script> <script src="https://code.highcharts.com/modules/export-data.js"></script> <script src="https://code.highcharts.com/modules/accessibility.js"></script> <script src="https://code.highcharts.com/modules/annotations.js"></script>'

def main():
	print('Processing start')	
	process_files(file_path)
	print(chart)
	print(divId)
	with open(divId + "-chart-"+datetime.now().strftime("%Y%m%d%H%M%S")+".html", "w") as file:
		file.write(scripts)
		div = '<div id="' + divId + '"></div>'
		file.write(div)
		file.write('<script type="text/javascript">')
		file.write(chart)
		file.write('</script>')
	print('Processing end')

def extend_dict(primary_dict, secondary_dict):
    result_dict = {}
    for k in set(primary_dict.keys()).union(set(secondary_dict.keys())):
        if (k in primary_dict.keys() and k in secondary_dict.keys()) and (isinstance(primary_dict[k], dict) and isinstance(secondary_dict[k], dict)):
            result_dict.update({k: extend_dict(primary_dict[k], secondary_dict[k])})
        elif k in primary_dict.keys():
            result_dict.update({k: primary_dict[k]})
        elif k in secondary_dict.keys():
            result_dict.update({k: secondary_dict[k]})
    return result_dict

def get_json(file, chartname):
	print(chartname)
	with open(file) as chart:
		chart = json.load(chart)
	print(chart['options'])
	options = chart['options']
	template = chart['template']
	options = extend_dict(options,template)	
	options = json.dumps(options)
	return options

def div_id(chartname):
	d = re.compile(r'figure (\d+) .+')
	divId = d.sub(r'fig\1',chartname)
	return divId

def path_leaf(file_path):
    rootdir, file = ntpath.split(file_path)
    return file or ntpath.basename(rootdir)

def process_files(file_path):
	print(file_path)
	file = path_leaf(file_path)
	print(file)
			
	ext = os.path.splitext(file)[-1].lower()
	chartname = os.path.splitext(file)[0].lower()
	if ext == '.json':		
		options = get_json(file_path, chartname)
		global divId
		divId = div_id(chartname)
		global chart
		chart = 'Highcharts.chart("' + divId + '",' + options + ');\r\n\r\n'
		#print('Highcharts.chart("' + chartname + '",' + options + ');\r\n\r\n')
	
# Default function is main()
if __name__ == '__main__':
    file_path = tkinter.filedialog.askopenfilename()    
    print(file_path)
    extension = os.path.splitext(file_path)[-1].lower()
    print(extension)
    if file_path != '' and extension == '.json':
    	main()
    elif extension != '.json':
        	print('Error: Please re-run the script and select JSON file type.')
    else:
        print('Sorry! File not found')
