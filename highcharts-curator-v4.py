import mammoth
import tkinter.filedialog

from datetime import datetime
import json
import os
import re
from os import getcwd

root = tkinter.Tk()
root.withdraw()

charts = []
divIds = []
scripts = '<script src="https://code.highcharts.com/highcharts.js"></script> <script src="https://code.highcharts.com/highcharts-more.js"></script> <script src="https://code.highcharts.com/modules/dumbbell.js"></script> <script src="https://code.highcharts.com/modules/exporting.js"></script> <script src="https://code.highcharts.com/modules/export-data.js"></script> <script src="https://code.highcharts.com/modules/accessibility.js"></script> <script src="https://code.highcharts.com/modules/annotations.js"></script>'

def main():
	print('Processing start')
	#print(rootdir)
	process_files(rootdir)
	#print(charts)
	print(divIds)
	with open("charts-"+datetime.now().strftime("%Y%m%d%H%M%S")+".html", "w") as file:
		file.write(scripts)
		for divId in divIds:
			div = '<div id="' + divId + '"></div>'
			file.write(div)
		file.write('<script type="text/javascript">')
		for chart in charts:
			file.write(chart)
		file.write('</script>')
	print('Processing end')

def get_all_values(pkey, nested_dictionary):
    for key, value in nested_dictionary.items():
        if type(value) is dict:
            print(key, ":", value)
            get_all_values(key, value)
        else:
            print(key, ":", value)

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
	#print(chartname)
	with open(file) as chart:
		chart = json.load(chart)
	#print(chart['options'])
	options = chart['options']
	template = chart['template']
	options = extend_dict(options,template)
	options = json.dumps(options)
	return options

def div_id(chartname):
	d = re.compile(r'figure (\d+) .+')
	chartname = d.sub(r'fig\1',chartname)
	return chartname

def process_files(rootdir):
	for subdir, dirs, files in os.walk(rootdir):
		for file in files:
			#print(rootdir + '/' + file)
			ext = os.path.splitext(file)[-1].lower()
			chartname = os.path.splitext(file)[0].lower()
			if ext == '.json':
				#print(file)
				options = get_json(rootdir + '/' + file, chartname)
				chartname = div_id(chartname)
				chart = 'Highcharts.chart("' + chartname + '",' + options + ');\r\n\r\n'
				global charts
				charts.append(chart)
				global divIds
				divIds.append(chartname)
				#print('Highcharts.chart("' + chartname + '",' + options + ');\r\n\r\n')
	
				


# Default function is main()
if __name__ == '__main__':
    rootdir = tkinter.filedialog.askdirectory()
    print(rootdir)
    if rootdir != '':
        main()
    else:
        print('Sorry! File not found')
