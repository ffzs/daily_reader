import os
import numpy as np

dir_list = os.listdir()
day_list = []
for item in dir_list:
    if not '.' in item:
        day_list.append(item)
# print(day_list)

for day in day_list[:-1]:
    html_head = '<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">'
    html_title = '<title>{}</title>'.format(day)
    html_h1 = '</head><body><h1>{}</h1>'.format(day)
    html_p = '<dl><p></p>'
    html_end = '</dl></body></html>'
    path = day + '/info.txt'
    variable_name = ''
    with open(day + '/index.html', 'w', encoding='utf-8') as f:
        f.write(html_head)
        f.write(html_title)
        f.write(html_h1)
        f.write(html_p)
        for line in open(path, 'r', encoding='utf-8'):
            name, title, url, file = line.split('$')
            if name != variable_name:
                variable_name = name
                f.write('<h2>{}</h2>'.format(name))
            f.write('<dt><a href="{}" target="_blank">{}</a></dt>\n'.format(url, title))
            f.write('<dt><a href="{}" target="_blank">{}</a></dt>\n'.format(file, 'pdf版本'))
        f.write(html_end)

        # print(name, title, url, day, file )