# -*- coding: utf-8 -*-
"""
Created on Fri May 31 15:52:37 2019
Safe Rating Calculator for Game Automobilista's LOG Files.
This script is under the MIT License - 2019.

@author: Ramon Pinto de Barros
"""
from bs4 import BeautifulSoup as BS
from datetime import date, datetime, timedelta
import re
import pandas as pd
import time

def xmlreader(database_path, result_file, db_file, track_dificulty):
    incident_sum = [] 
    steamidlist = [[],[]]   
    incident_list = [[],[],[]]
    inc_dict_list= []
    
    f = open('LOGS\\' + result_file)
    filename = result_file
    #print(filename)
    soup = BS(f, 'xml')
    tableDict = {}
    finalresultlist = []
    timestamp = soup.find("DateTime").contents[0]
    tableDict['timestamp'] = timestamp #timestamp
    tableDict['racedate'] = datetime.fromtimestamp(int
         (timestamp)).strftime('%Y-%m-%d %I:%M %p %Z') #human_date
    
    if result_file.endswith('P1.xml'):
        tableDict['practicefilename'] = filename #Nome do arquivo
    elif result_file.endswith('Q1.xml'):
        tableDict['qualifyfilename'] = filename #Nome do arquivo
    elif result_file.endswith('R1.xml'):
        tableDict['racefilename'] = filename #Nome do arquivo
    else:
        tableDict['TBDfilename'] = filename
    
    
    name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content = [
            [],[],[],[],[],[],[],[],[],[]
            ]
    playnum = 0
    for item in soup.find_all('SteamID'):
        if int(item.contents[0]) != 0:
            playnum += 1
    print('The session had ' + str(playnum) + ' total players')
    
        
      
    ##############################
    #Saves [[],[Pos]]
    print('Reading the XML...')
    for Position in soup.find_all('Position'):
        pos_cont = Position.contents
        if int(pos_cont[0]) == -1:
            name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[2].append('DNF')
        elif int(pos_cont[0]) < 10:
            name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[2].append('0'+pos_cont[0])
        else:
            name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[2].append(pos_cont[0])
    print('Reading Positions....Done!')        
    ##############################
    #Saves [[Drivername],[]]
    for Name in soup.find_all('Name'):
        name_cont = Name.contents
        name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[0].append(name_cont[0])
        steamidlist[1].append(name_cont[0].upper().title())
    print('Reading Drivers names, Done!')
    #############################
    #Getting STEAM_ID, USERID, END POSITION Values and ALL LAPS for each driver
    for SteamID in soup.find_all('SteamID'):
        steamid_cont = SteamID.contents
        user = steamid_cont[0]
        name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[1].append(steamid_cont[0])
        try:
            name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[6].append(user['_id'])
        except:
            name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[6].append('')
        steamidlist[0].append(steamid_cont[0])
    print('Reading drivers ID......Done!')
    if soup.find_all('GridPos') == []:
        pass
    else:
        for gridpos in soup.find_all('GridPos'):
            st_position = gridpos.contents
            if int(st_position[0]) < 10:
                name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[3].append('0'+st_position[0])
            else:
                name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[3].append(st_position[0])
    print('Starting to Read Drivers Laps!')             
    for driver in soup.find_all('Driver'):
        laplist = []
           
    
        for lap in driver.find_all('Lap'):
            lapdict = {}
            laptime = lap.contents[0]
            fuel = float(lap['fuel']) * 100
            position = lap['p']
            
            
            
            if int(lap['p']) < 10:
                position = '0' + position

            lapdict['position'] = position
            lapdict['fuel'] = str(round(fuel, 2)) + '%'
            
            try:
                lap_s1 = float(lap['s1']) * 1000
                s, ms = divmod(lap_s1, 1000)
                m, s= divmod(s, 60)
                h, m = divmod(m, 60)
                lapdict['s1'] = ("%d:%02d:%02d:%03d" % (h, m, s, ms))
            except:
                lapdict['s1'] = '--:--:--:---'

            try:
                lap_s2 = float(lap['s2']) * 1000
                s, ms = divmod(lap_s2, 1000)
                m, s= divmod(s, 60)
                h, m = divmod(m, 60)
                lapdict['s2'] = ("%d:%02d:%02d:%03d" % (h, m, s, ms))
            except:
                lapdict['s2'] = '--:--:--:---'
            try:
                lap_s3 = float(lap['s3']) * 1000
                s, ms = divmod(lap_s3, 1000)
                m, s= divmod(s, 60)
                h, m = divmod(m, 60)
                lapdict['s3'] = ("%d:%02d:%02d:%03d" % (h, m, s, ms))
            except:
                lapdict['s3'] = '--:--:--:---'

            try:
                laptime = float(lap.contents[0]) * 1000
                s, ms = divmod(laptime, 1000)
                m, s= divmod(s, 60)
                h, m = divmod(m, 60)
                lapdict['laptime'] = ("%d:%02d:%02d:%03d" % (h, m, s, ms))
            except:
                if str(laptime) == '--.----':
                    lapdict['laptime'] = 'ALERTA - Corte de Pista ou Volta não Completada'


            laplist.append(lapdict)
        for j in range(len(laplist)):
            if j == 0:
                s1_index = j
                s2_index = j
                s3_index = j
                bl_index = j
                if laplist[j]['s1'] == '--:--:--:---' :
                    laplist[j]['bests1'] = False
                else:
                    laplist[j]['bests1'] = True
                    
                if laplist[j]['s2'] == '--:--:--:---' :
                    laplist[j]['bests2'] = False
                else:
                    laplist[j]['bests2'] = True
                    
                if laplist[j]['s3'] == '--:--:--:---' :
                    laplist[j]['bests3'] = False
                else:
                    laplist[j]['bests3'] = True
                    
                if laplist[j]['laptime'] == 'ALERTA - Corte de Pista ou Volta não Completada' :
                    laplist[j]['bestlap'] = False
                else:
                    laplist[j]['bestlap'] = True
                    
                
                
            else:
                if laplist[j]['s1'] == '--:--:--:---' :
                    laplist[j]['bests1'] = False
                elif (laplist[j]['s1'] < laplist[s1_index]['s1'] ) or (laplist[s1_index]['s1'] == '--:--:--:---'):
                    laplist[j]['bests1'] = True
                    laplist[s1_index]['bests1'] = False
                    s1_index = j
                else:
                    laplist[j]['bests1'] = False

                if laplist[j]['s2'] == '--:--:--:---' :
                    laplist[j]['bests2'] = False
                elif (laplist[j]['s2'] < laplist[s2_index]['s2']) or (laplist[s2_index]['s2'] == '--:--:--:---'):
                    laplist[j]['bests2'] = True
                    laplist[s2_index]['bests2'] = False
                    s2_index = j
                else:
                    laplist[j]['bests2'] = False

                if laplist[j]['s3'] == '--:--:--:---' :
                    laplist[j]['bests3'] = False
                elif (laplist[j]['s3'] < laplist[s3_index]['s3']) or (laplist[s3_index]['s3'] == '--:--:--:---'):
                    laplist[j]['bests3'] = True
                    laplist[s3_index]['bests3'] = False
                    s3_index = j
                else:
                    laplist[j]['bests3'] = False

                if laplist[j]['laptime'] == 'ALERT - Cut track or uncomplete lap' :
                    laplist[j]['bestlap'] = False
                elif (laplist[j]['laptime'] < laplist[bl_index]['laptime'] or (laplist[bl_index]['laptime'] == 'ALERT - Cut track or uncomplete lap')):
                    laplist[j]['bestlap'] = True
                    laplist[bl_index]['bestlap'] = False
                    bl_index = j
                else:
                    laplist[j]['bestlap'] = False


            
        name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[4].append(laplist)
        try:
            bestlap = driver.find_all('BestLapTime')
            bestlaptime = float(bestlap[0].contents[0]) * 1000
            s, ms = divmod(bestlaptime, 1000)
            m, s= divmod(s, 60)
            h, m = divmod(m, 60)
            fulltime = "%d:%02d:%02d:%03d" % (h, m, s, ms)
            name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[7].append(fulltime)
        except:
            name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[7].append('-:--:--:---')

            
       
        
        if result_file.endswith('R1.xml'):
            finishtime = driver.find_all('FinishTime')
            try:
                finishtime = float(finishtime[0].contents[0]) * 1000
                s, ms = divmod(finishtime, 1000)
                m, s= divmod(s, 60)
                h, m = divmod(m, 60)
                finishtime = "%d:%02d:%02d:%03d" % (h, m, s, ms)
            except:
                status = driver.find_all('FinishStatus')
                finishtime = status[0].contents[0]
            
            name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[5].append(finishtime)
            
            lapsled = driver.find_all('LapsLed')
            name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[8].append(lapsled[0].contents[0])

        

        
        finishstatus = driver.find_all('FinishStatus')
        if finishstatus[0].contents[0] == 'Finished Normally':
            name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[9].append('Finished Normally')
        elif finishstatus[0].contents[0] == 'DNF':
            name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[9].append('DNF')
        else:
            name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[9].append('Unknow?')
    
    print('Reading Drivers laps.........Done!')
    print('Race Session, driver Status, Done!')

        
            
        

    
    ##############################
    #START RETRIEVE RACE'S INCIDENTS
    print('Retrieving Session incidents...')
    for incident in soup.find_all('Incident'):
        incident_cont = incident.contents[0]
        et = incident['et']
        

        try:
            m = re.match(r'(?P<driver1>.*) reported contact (?P<value>.*) with another vehicle (?P<driver2>.*)', incident_cont)
            incident_list[0].append(m.group('driver1').split('(')[0])
            incident_list[1].append(m.group('driver2').split('(')[0])
            if float(et) < 250:
                incvalue = float(m.group('value').split('(')[1].split(')')[0]) * 2
                incident_list[2].append(incvalue)
            else:
                incident_list[2].append(float(m.group('value').split('(')[1].split(')')[0]))
        except:
            m = re.match(r'(?P<driver1>.*) reported contact (?P<value>.*) with (?P<driver2>.*)', incident_cont)
            incident_list[0].append(m.group('driver1').split('(')[0])
            incident_list[1].append(m.group('driver2').split('(')[0])
            if float(et) < 250:
                incvalue = float(m.group('value').split('(')[1].split(')')[0]) * 2
                incident_list[2].append(incvalue)
            else:
                incident_list[2].append(float(m.group('value').split('(')[1].split(')')[0]))


    names_list = []
    #LIST UNIQUE DRIVER NAMES INSIDE THE INCIDENTS_LIST
    for driver1 in incident_list[0]:
        names_list.append(driver1) #adiciona o nome do piloto
    for driver2 in incident_list[1]:
        names_list.append(driver2)
    names_set = set(names_list)


    #########################################################
    #Start defining the sum of incidents values for a driver
    #Summing the Incident values into driver's object in database
    #It's important to set up the parameters before running the code
    if track_dificulty == 1:
        QR_regen = 0.5
    elif track_dificulty == 2:
        QR_regen = 0.75
    elif track_dificulty == 3:
        QR_regen = 1.0
    elif track_dificulty == 4:
        QR_regen = 1.2
    elif track_dificulty == 5:
        QR_regen = 1.3
    ###########--------PARAMETERS---------#############
    max_incidents = float(16) #Max log value for penalization
    startQR = float(10) #Start value of QualityRating. The value goes down
    rate_for_incidents = startQR/max_incidents #parameter that changes log values to QR values
    ###########--------PARAMETERS---------#############

    incident = float(0)
    print('...')
    #print(incident_list)
    #print(name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[0])
    for j in range(len(name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[0])):
        for i in range(len(incident_list[1])):

            if (name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[0][j] == incident_list[0][i]):
                if (incident_list[1][i] == 'Wing' or
                    incident_list[1][i] == 'Part' or
                    incident_list[1][i] == 'Wheel' or
                    incident_list[1][i] == 'Cone' or
                    incident_list[1][i] == 'Sign' or
                    incident_list[1][i] == 'Post'):
                    incident += 0
                elif incident_list[1][i] == 'Immovable':
                    incident += (incident_list[2][i]*0.7)
                else:
                    incident += incident_list[2][i]
                    
            if (name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[0][j] == incident_list[1][i]):
                incident += incident_list[2][i]
            #print(incident)
        st_id = name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[1][j]
        rated_incident = rate_for_incidents * incident
        #print(rated_incident, incident)
        inc_dict_list.append({'steamID':st_id, 'incidents': round(rated_incident, 2)})
        incident_sum.append(incident)
        incident = float(0)
    
            
        
    print('Putting all together into the Race Result...')
    for i in range(len(name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[0])):
        if not name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[3]:
            finalresult = {'position': name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[2][i],
                           'driver': name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[0][i],
                           'laps': name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[4][i],
                           'steamID': name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[1][i],
                           'userid': name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[6][i],
                           'incidents': float(0),
                           'finishstatus': name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[9][i],
                           'bestlap': name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[7][i]
                           }
        else:
            finalresult = {'position': name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[2][i],
                           'driver': name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[0][i],
                           'laps': name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[4][i],
                           'fulltime': name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[5][i],
                           'steamID': name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[1][i],
                           'userid': name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[6][i],
                           'incidents': float(0),
                           'st_position': name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[3][i],
                           'lapsled' : name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[8][i],
                           'finishstatus': name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[9][i],
                           'bestlap': name_id_pos_stpos_laplist_fulltime_userid_bestlap_lapsled_finishstat_content[7][i]
                           }
        for incident_dict in inc_dict_list:
            if (finalresult['steamID'] == incident_dict['steamID']):
                finalresult['incidents'] = incident_dict['incidents']
        finalresultlist.append(finalresult)
    
    #-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    #UPDATING THE DATABASE

    timestr = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    #mkdir(PATH_CONFIG['output']+timestr+'\\')
    
    try: #THE DATABASE HAS ANY DATA!??!?!
        df = pd.read_csv(database_path + db_file,index_col=[0] )
        df = df.transpose()
        df.to_csv('DB\\BACKUP\\' + db_file.replace('.csv','') + '_' + timestr + '.csv')
        print('BACKUP FILE WITH NAME' + db_file + '_' + timestr + ' HAS BEEN CREATED')
        print('Database "' + db_file + '" is being updated')
        data = {}
        for item in list(df):
            data[item] = list(df[item])
        
        data['dificulty'].append(track_dificulty)
        
        # ITERATES THROUGH THE DRIVERS, INCIDENTS and FINISHSTATUS IN THE RESULT XML FILE
        drivers = [finalresultlist[i]['driver']+','+finalresultlist[i]['steamID'] for i in range(len(finalresultlist))] #Driver Name, SteamID
        incidents = [finalresultlist[i]['incidents'] for i in range(len(finalresultlist))]
        finish_status = [finalresultlist[i]['finishstatus'] for i in range(len(finalresultlist))]
        
        for driver in drivers:
            if driver not in data:  #CHECK IF THE DRIVER IS NOT IN THE CSV FILE ALREADY.
            
                #ADD THE DRIVER TO THE DATA IF IT'S NOT IN THE CSV FILE.
                data[driver] = [10 for j in range(len(data['dificulty'])-1)] 
                data[driver+' delta'] =  [0 for j in range(len(data['dificulty'])-1)]
                print('This is driver ' + driver + ' first race!')
        
        for d in data: #CHECK IF THE DRIVER HAS RACE BEFORE AND MISSED THE RACE
            if d == 'dificulty':
                continue
            try:
                index = drivers.index(d.replace(' delta',''))
            except:
                pass
            if d not in drivers and d.endswith('delta') == False: #AN OBJECT OF A DRIVER THAT MISS A RACE IS NOT UPDATED! 
                #print(d, data[d])
                data[d].append(data[d][-1]) 
                #print(d, data[d])
                print('Driver ' + d.split(',')[0] + ' missed this race')
            elif d.replace(' delta','') in drivers and d.endswith('delta') == False: #AN OBJECT OF A DRIVER THAT ATTEND THE RACE IS UPDATED
                if finish_status[index] == 'Unknow?':
                    #print(d, data[d])
                    data[d].append(float(data[d][-1]))
                    #print(d, data[d])
                else:    
                    #print(d, data[d])
                    data[d].append(float(data[d][-1]) - incidents[index] + QR_regen) 
                    #print(d, data[d])
                    print('Driver ' + d.split(',')[0] + ' attended race')
            
            elif d.replace(' delta','') not in drivers and d.endswith('delta'):
                #print(d, data[d])
                data[d].append(0)
                #print(d, data[d])    
            elif d.replace(' delta','')in drivers and d.endswith('delta'):
                #print(d, data[d])
                data[d].append(float(data[d.replace(' delta','')][-1])-float(data[d.replace(' delta','')][-2]))
                #print(d, data[d])
                    
        
    except: #THE DATABASE IS BLANK
        print('Database "' + db_file + '" is being defined')
        data = {
                'dificulty': [0],
                }
        data['dificulty'].append(track_dificulty)
        for i in range(len(finalresultlist)):
            if finalresultlist[i]['finishstatus'] == 'Unknow?':
                data[finalresultlist[i]['driver']+','+finalresultlist[i]['steamID']] = [startQR, startQR - finalresultlist[i]['incidents']]
            else:
                data[finalresultlist[i]['driver']+','+finalresultlist[i]['steamID']] = [startQR, startQR - finalresultlist[i]['incidents'] + QR_regen]
            data[finalresultlist[i]['driver']+','+finalresultlist[i]['steamID'] +' delta'] = [0, data[finalresultlist[i]['driver']+','+finalresultlist[i]['steamID']][1] - data[finalresultlist[i]['driver']+','+finalresultlist[i]['steamID']][0]]
    
    df = pd.DataFrame(data, index = ['Start'] + ['Race '+ str(i+1) for i in range(len(data['dificulty'])-1)])    
    df = df.transpose()
    print('Incidents, Done!')
    print('------------------------')
    df.to_csv(database_path + db_file)
    return df
    #return finalresultlist
###################################################################################################################

def createdb(db_path):
    db_name = ''
    while True:
        if db_name == '':
            print('CREATING NEW DB:')
            db_name = input('Select the name for your DB: ')
            if db_name.endswith('.csv') == False:
                db_name = db_name + '.csv'
            with open(db_path + db_name, 'wb') as f:
                print('Database "' + db_name + '" was correctly created')
                break
    return db_name