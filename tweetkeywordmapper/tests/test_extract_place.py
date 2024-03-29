import time
import re
from tweetkeywordmapper.core import extract_place as ex
from tweetkeywordmapper.core import constants as cons

states = cons.states
cities = cons.cities
areas = cons.area_codes

pls = ['NYC via ME', 'Boston -> Washington, D.C.', '848 from 716', 'Morgantown, West Virginia', '716 West Dr.', 'ÜT: 38.890550,-77.009017', '38.890550, -77.009017', '388905, -770090', '43°12′51″N,77°56′22″W', '43°12′51″N, 77°56′22″W']

for pl in pls:
    print(f'Place: {pl}\n')

    time.sleep(0.5)
    
    if len(pl.split(', ')) > 1:
        elements = pl.split(', ')
    
    elif len(pl.split(',')) > 1:
        elements = pl.split(',')
    
    elif len(pl.split(' ')) > 1:
        elements = pl.split(' ')
    
    else:
        elements = []
    
    if (pl.find('ÜT: ') != -1 or pl.find('°') != -1) or (len(elements) == 2 and ('.' in elements[0] and re.sub('\.|\-', '', elements[0]).isnumeric()) and ('.' in elements[1] and re.sub('\.|\-', '', elements[1]).isnumeric())):
        print('State:', ex.determine_state_from_coordinates(pl, states, elements))
    
    elif pl.find('via') != -1 or pl.find('from') != -1:
        print('State:', ex.find_state_in_place_value(pl, states, cities, areas, word='via'))
    
    else: 
        print('State:', ex.find_state_in_place_value(pl, states, cities, areas))
    
    print()
    
    time.sleep(0.25)