# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on Fri May 31 15:52:37 2019
Safe Rating Calculator for Game Automobilista's LOG Files.
This script is under the MIT License - 2019.

@author: Ramon Pinto de Barros
"""
import os
from datetime import date, datetime, timedelta
from .helpers import xmlreader, createdb

def calculator():
	PATH_CONFIG = {
	        'logs': 'LOGS\\',
	        'database': 'DB\\',
	        'backup': 'DB\\BACKUP\\',
	        'output': 'DB\\OUTPUT\\',}
	result_file = ''
	open_db = ''
	backup = False

	while True: #start loop
	    while True:
	        print('WELCOME')
	        print('The result files below are ready for use')
	        print('----------')
	        try:
	        	oslist =  os.listdir(PATH_CONFIG['logs'])
	        	logfiles = [(oslist[i], i+1) for i in range(len(os.listdir(PATH_CONFIG['logs']))) if oslist[i].endswith('.xml')]
	        	if len(logfiles) > 0:
		        	print([('FILENAME', 'FILENUMBER')] + logfiles)
		        	print('----------')
		        	print('The result files above are ready for use')
		        else:
		        	print("There's no LOGS in the LOGS folder.")
		        	print("Please, add a copy of a AMS .xml log file to the folder")
		        	print("So we can continue")
		        	break
	        except Exception as e:
	        	print('PLEASE, CREATE THE DIRECTORIES:')
	        	print('\\LOGS')
	        	print('\\DB')
	        	print('\\DB\\BACKUP')
	        	print('\\DB\\OUTPUT')
	        	print("SO WE CAN CONTINUE")
	        
	        if result_file == '':
	            result_file = input('Input Filename or filenumber: ')
	            try:
	                filenumber = int(result_file)
	                if filenumber < 1:
	                    filenumber = None
	                try: #check if the file is in the correct folder
	                    result_file = oslist[filenumber-1]
	                    with open(PATH_CONFIG['logs']+result_file) as f:
	                        print('The file ' + result_file + ' has been found')
	                    break
	                except:
	                    print('The filenumber ' + str(filenumber) + " is not correct")
	                    print('')
	                    result_file = ''
	            except:
	                if result_file.endswith('.xml') == False:
	                    result_file = result_file + '.xml'
	                try: #check if the file is in the correct folder
	                    with open(PATH_CONFIG['logs']+result_file) as f:
	                        print('The file ' + result_file + ' has been found')
	                    break
	                except:
	                    print('The file ' + result_file + " coudn't be found in the LOGS directory")
	                    result_file = ''
	        else:
	            continue
	            
	    
	    while True: #loop that checks if the track dificulty was inputed correctly
	        track_dificulty = input('Track dificulty level (1-5): ')
	        try:
	            track_dificulty = int(track_dificulty)
	            if track_dificulty > 0 and track_dificulty < 6:
	                print('The track dificulty level was set to: ' + str(track_dificulty))
	                break
	            else:
	                print('Choose a valid number (1-5)')
	        except:
	            print("You didn't choose a number")
	            
	    
	    while True: #Loop that checks if there is a DB on the DB folder
	        files = [f for f in os.listdir(PATH_CONFIG['database']) if f.endswith('.csv')]
	        files.sort()
	        backup_files = [f for f in os.listdir(PATH_CONFIG['backup']) if f.endswith('.csv')]
	        backup_files.sort()
	        
	        #Checks if there's csv files in the database directory
	        if len(files) == 0: #NO CSVFILE
	            print('NO DATABASE FOUND IN THE DB DIRECTORY.')
	            open_db = createdb(PATH_CONFIG['database'])
	            
	            
	            
	        elif len(files) > 0: #MANY DB FILES
	            open_db = ''
	            print('You can create a new DB file, or use an existing one.')
	            y_n = ''
	            while True:
	                if y_n == '':
	                    y_n = input('Do you want to create a new DB?? ')
	                    if y_n.startswith('N') or y_n.startswith('n'):
	                        continue
	                    elif y_n.startswith('Y') or y_n.startswith('y'):
	                        print('You choose to create a new database')
	                        open_db =createdb(PATH_CONFIG['database'])
	                        break
	                    else:
	                        print('Please answer Y for yes and N for no!')
	                        y_n = ''
	                if open_db == '':
	                    number_dbs = len(files)
	                    print('There are ' + str(number_dbs) + ' csv files on the directory')
	                    print('Please, input the name of what csv file you want to open')
	                    print(files)
	                    open_db = input('Open:')
	                    if open_db.endswith('.csv') == False:
	                        open_db = open_db + '.csv'
	                    try:
	                        with open(PATH_CONFIG['database'] + open_db, 'r') as f:
	                            print('Database "' + open_db + '" was found')
	                        break
	                    except:
	                        print('The file '+ open_db + " couldn't be found in the DB directory")
	                        open_db = ''
	            
	        
	        '''if len(backup_files) > 0: #There are/is file(s) in the backup folder
	            for bkp in backup_files:
	                if bkp.startswith(open_db.replace('.csv','')):
	                    print('DATABASE BACKUPs WERE FOUND IN THE BACKUP FOLDER')
	                    print('-----------')
	                    print([f for f in backup_files if f.startswith(open_db.replace('.csv',''))])
	                    print('-----------')
	                    print("IF YOU WANT TO RECOVER A BACKUP, YOU MAY INPUT IT'S NAME,")
	                    print("LEAVE BLANK IF YOU DO NOT WANT TO RECOVER A BACKUP")
	                    answer = input('Backup Filename: ')
	                    if answer == '':
	                        answer = ' '
	                    if answer[0] != ' ':
	                        if answer in backup_files
	                        backup = True
	                        open_db = answer
	                    else:
	                        if answer.endswith('.csv') == False:
	                            answer = answer + '.csv'
	                        break
	                else:1
	                
	                    print('No backup file was found for '+ open_db + '.')'''
	        
	        if open_db != '':
	            break
	    
	    print('adding data to the Database')
	    result = xmlreader(PATH_CONFIG['database'], result_file, open_db, track_dificulty)
	    
	    break