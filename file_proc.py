import json, csv, os
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

if not os.path.exists('out'):
    os.mkdir('out')


def task_1(x, y, f_in='test_payload1.xml', f_out='out/Task1.xml'):
    """Takes arguments int X and int Y, and updates DEPART and RETURN fields in test_payload1.xml"""
    
    def calc_date(days): # https://stackoverflow.com/a/28154159/17246406
        """Takes the number of days then get the future date in yyyymmdd format"""
        new_date = datetime.now() + timedelta(days=days)
        return str(10000*new_date.year + 100*new_date.month + new_date.day)
    # end calc_date

    # open and parse
    tree = ET.parse(f_in)
    # get the root
    root = tree.getroot()
    
    # find the 'DEPART' tag
    dep = root.find('.//TP/DEPART')
    # change its value
    dep.text = calc_date(x)
    
    # find the 'RETURN' tag
    ret = root.find('.//TP/RETURN')
    # change its value
    ret.text = calc_date(y)

    # write new file
    tree.write(f_out)
# end task_1

def task_2(del_key, f_in='test_payload.json', f_out='out/Task2.json'):
    """Takes a json element as an argument, and removes that element from test_payload.json."""
    
    def remove_el(js):
        """Remove the element from the json using recursion"""

        for key, val in js.copy().items():
            if key == del_key:
                # remove element
                js.pop(key)
            
            # if nested check it too
            elif isinstance(val, dict):
                js[key] = remove_el(val)
        
        return js
    # end remove_el 
    
    # open json file in read mode
    with open(f_in, 'r') as f:
        js = json.load(f)

    # remove the element
    new_js = remove_el(js)
    
    # write json file
    with open(f_out, 'w') as f:
        json.dump(new_js, f, indent=2)
# end task_2

def task_3(files_in=['Jmeter_log1.jtl', 'Jmeter_log2.jtl']):
    """Parse jmeter log files in CSV format, if non-successful endpoint responses prints"""

    def print_line(line_data):
        """format print list"""
        print(
            line_data[0].ljust(33), line_data[1].ljust(12), line_data[2].ljust(16),
            line_data[3].ljust(14), line_data[4], sep= ' | '
        )
    # end print_line

    # empty list to save the csv rows in 
    all_rows = []

    # reaad csv files
    for f_in in files_in:
        with open(f_in, 'r') as f:
            all_rows.extend(csv.DictReader(f))

    print_line(['label', 'responseCode', 'responseMessage', 'failureMessage', 'time'])

    for row in all_rows:
        if row['success'] != 'true': # non-successful
            print_line([
                row['label'], row['responseCode'], row['responseMessage'], row['failureMessage'],
                # https://stackoverflow.com/a/31548402/17246406
                datetime.fromtimestamp(float(row['timeStamp'])/1000).strftime("%Y-%m-%d %H:%M:%S")
            ])
# end task_3

# test
if __name__ == '__main__':
    task_1(5, 10)
    task_2('appdate', f_out='out/Task2-1.json')
    task_2('outParams', f_out='out/Task2-2.json')
    task_3()