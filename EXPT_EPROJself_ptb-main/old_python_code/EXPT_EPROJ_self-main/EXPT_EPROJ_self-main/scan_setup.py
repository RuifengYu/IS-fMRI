import pandas as pd
participant = input('Participant: ')
session = input('Session: ')
session_num=input('Session_Num: ')

import csv
f = open('exp_info.csv', 'w')
writer = csv.writer(f)
writer.writerow(['participant', 'session', 'mriMode', 'offset_x', 'offset_y', 'NBACK_run','EPROJ_run','LANG_run','FIXATION_run','NBACK_PRACTICE_run'])


if session_num=='1':
	writer.writerow([participant, session, 'scan', 0, 0, 1, 1, 1, 1, 1])
elif session_num=='2': 
	writer.writerow([participant, session, 'scan', 0, 0, 5, 4, 3, 4, 2])
