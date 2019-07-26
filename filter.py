#!python 3.6.2 or greater
# import all necessary packages
import datetime, csv, os, shutil, time, fnmatch, sys, json, re
from pathlib import Path
from collections import OrderedDict

# current directory
currentDirectory = Path(os.getcwd())

# all const
stg1DropLocation = Path('//cuaisilon/socappstgfile01/SOC_Share/Stg1/QA_MVC/adh_receive')
stg1ReceiveLocation = Path('//cuaisilon/socappstgfile01/SOC_Share/Stg1/QA_MVC/adh_send')
stg2DropLocation = Path('//cuaisilon/socappstgfile01/SOC_Share/Stg2/QA_MVC/adh_receive')
stg2ReceiveLocation = Path('//cuaisilon/socappstgfile01/SOC_Share/Stg2/QA_MVC/adh_send')
stg3DropLocation = Path('//cuaisilon/socappstgfile01/SOC_Share/Stg3/QA_MVC/adh_receive')
stg3ReceiveLocation = Path('//cuaisilon/socappstgfile01/SOC_Share/Stg3/QA_MVC/adh_send')

# get the target date and drop location
with open('config.json') as json_file:  
    data = json.load(json_file)
    env = data['env']
    tDateString = data['targetDate']
    if env != 'stg1' and env != 'stg2' and env != 'stg3':
        print(f'Make sure "env" is set to "stg1" or "stg2" or "stg3"')
        print(f'Invalid "env" data on config.json')
        sys.exit("Stopping script .......")
    pattern=r'(([0-2]\d{1})|([3][01]{1}))(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)(\d)(\d)'
    datePattern = re.compile(pattern)
    if not datePattern.match(tDateString):
        print(f'Make sure "targetDate" is set using format "DDMMMYY". Month should be uppercase!! ex: 02JUN18')
        print(f'Invalid "targetDate" data on config.json')
        sys.exit("Stopping script .......")
    tDate = datetime.datetime.strptime(tDateString,'%d%b%y')
    currentDate = tDate.strftime('%d%b%y').upper()
    if env == 'stg1':
        stageSend = stg1DropLocation
        stageReceive = stg1ReceiveLocation
    elif env == 'stg2':
        stageSend = stg2DropLocation
        stageReceive = stg2ReceiveLocation
    elif env == 'stg3':
        stageSend = stg3DropLocation
        stageReceive = stg3ReceiveLocation

# ############################## functions ##########################

# Check if adhoc folders are visible from the current machine
def check_if_folder_exist(location):
    if os.path.exists(location):
        print(f'[ {location} ] folder found')
    else:
        print(f'Could not find [ {location} ] folder!')
        print(f'make sure [ {location} ] is available from this machine!')
        sys.exit("Stopping script .......")



# check for response csv, if exist copy to current directory for parsing
def call_adhoc_4_and_check_for_response_csv(receive_folder, send_folder, local_directory, current_date):
    # note that repeat is needed since the adhoc processor sometimes does not return csv.
    # get current timestamp
    sendPattern = f'MCEG_DATA*.txt'
    timeStamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    sentFiles = os.listdir(send_folder)
    if fnmatch.filter(sentFiles, sendPattern):
      print('There are request files waiting on que, adhoc processor may be down')
    else:
      request_file = open(f'{send_folder}/MCEG_DATA_ADHOC4_{timeStamp}.txt', 'w')
      request_file.write(f'ADH004_{current_date}')
      adh004String = f'ADH004_{current_date}'
      request_file.close()
      print(f' Sending adhoc 4 request using: {adh004String} and waiting for file....')
      time.sleep(20)
    # check if the file exist
    receivedFiles = os.listdir(receive_folder)
    receivePattern = f'MCEG_DATA_ADHOC4_{timeStamp}*.csv'
    # for file in os.listdir(receive_folder):
    # if fnmatch.fnmatch(file, pattern) == True:
    if fnmatch.filter(receivedFiles, receivePattern):
        file_name = fnmatch.filter(receivedFiles, receivePattern)
        print(f'csv file for adhoc 4 found')
        # Copy file
        shutil.copy(f'{receive_folder}/{file_name[0]}', f'{local_directory}/DATA/data.csv')
        print("csv file copied to local folder for parsing")
        # remove all files that was generated by this script.
        for csvfile in os.listdir(receive_folder):
          if fnmatch.fnmatch(csvfile, 'MCEG_DATA_ADHOC4*.csv'):
              os.remove(f'{receive_folder}/{csvfile}')


        # add header row
        with open(f'{local_directory}/DATA/data.csv',newline='') as f:
            r = csv.reader(f)
            data = [line for line in r]
        with open(f'{local_directory}/DATA/data.csv','w',newline='') as f:
            w = csv.writer(f)
            w.writerow(['recordStatus',
                        'lastDateModified',
                        'lastTimeModified',
                        'lastUserToModify',
                        'legDepartureDate',
                        'airlineCode',
                        'identifier',
                        'sequence',
                        'flightOriginDay',
                        'numericFlightDate',
                        'numGMTDate',
                        'STDudt',
                        'STAudt',
                        'tailNumber',
                        'numLastDateModified',
                        'flightStatus',
                        'origin',
                        'STDLocal',
                        'dispatchDesk',
                        'STDGMTVariance',
                        'destination',
                        'STALocal',
                        'STAGMTVariance',
                        'OAGEquipmentType',
                        'ACConfiguration',
                        'serviceType',
                        'originGate',
                        'ETDlocal',
                        'ETDudt',
                        'TAXIutc',
                        'OUTudt',
                        'OFFudt',
                        'destinationGate',
                        'ETAlocal',
                        'ETAudt',
                        'ONudt',
                        'INudt',
                        'previousTailNumber',
                        'ETE',
                        'DCNutc',
                        'ETOutc',
                        'EONutc',
                        'EDTCutc',
                        'flightType',
                        'newDepartureCity',
                        'newArrivalCity',
                        'SchedOAGEquipType',
                        'OAGEquipSubType',
                        'csvFSDailyID',
                        'tailNumBeforeCancel',
                        'CTAUTC',
                        'cancelled',
                        'replaced',
                        'ATCStatus',
                        'scheduledFlightType',
                        'aircraftRouting',
                        'mealService',
                        'hub',
                        'landingRestriction',
                        'headStartFlight',
                        'actualDeparture',
                        'specialFlight',
                        'actualArrival',
                        'scheduledTaxiOut',
                        'scheduledTaxiIn',
                        'STOSetByUser',
                        'STISetByUser',
                        'CTFlightNumber'])
            w.writerows(data)
        with open(f'{local_directory}/DATA/data.csv') as f:
          reader = csv.DictReader(f)
          rows = list(reader)

        with open(f'{local_directory}/DATA/data.json', 'w') as f:
            json.dump(rows, f)

        with open('DATA/data.json') as f:
            data = json.load(f)
            filteredData = []
            for x in data:
                if (x['STDudt'].strip() < x['ETDudt'].strip() 
                and x['OUTudt'].strip() != '' 
                and x['OFFudt'].strip() != ''
                and x['ONudt'].strip() != ''
                and x['INudt'].strip() != ''
                and x['tailNumber'].strip().startswith('-') == False):
                    filteredData.append(x)


            with open('filtered_data/filtered.csv', 'w+', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['recordStatus',
                                'lastDateModified',
                                'lastTimeModified',
                                'lastUserToModify',
                                'legDepartureDate',
                                'airlineCode',
                                'identifier',
                                'sequence',
                                'flightOriginDay',
                                'numericFlightDate',
                                'numGMTDate',
                                'STDudt',
                                'STAudt',
                                'tailNumber',
                                'numLastDateModified',
                                'flightStatus',
                                'origin',
                                'STDLocal',
                                'dispatchDesk',
                                'STDGMTVariance',
                                'destination',
                                'STALocal',
                                'STAGMTVariance',
                                'OAGEquipmentType',
                                'ACConfiguration',
                                'serviceType',
                                'originGate',
                                'ETDlocal',
                                'ETDudt',
                                'TAXIutc',
                                'OUTudt',
                                'OFFudt',
                                'destinationGate',
                                'ETAlocal',
                                'ETAudt',
                                'ONudt',
                                'INudt',
                                'previousTailNumber',
                                'ETE',
                                'DCNutc',
                                'ETOutc',
                                'EONutc',
                                'EDTCutc',
                                'flightType',
                                'newDepartureCity',
                                'newArrivalCity',
                                'SchedOAGEquipType',
                                'OAGEquipSubType',
                                'csvFSDailyID',
                                'tailNumBeforeCancel',
                                'CTAUTC',
                                'cancelled',
                                'replaced',
                                'ATCStatus',
                                'scheduledFlightType',
                                'aircraftRouting',
                                'mealService',
                                'hub',
                                'landingRestriction',
                                'headStartFlight',
                                'actualDeparture',
                                'specialFlight',
                                'actualArrival',
                                'scheduledTaxiOut',
                                'scheduledTaxiIn',
                                'STOSetByUser',
                                'STISetByUser',
                                'CTFlightNumber'])
                for flight in filteredData:
                    writer.writerow([flight['recordStatus'],
                                    flight['lastDateModified'],
                                    flight['lastTimeModified'],
                                    flight['lastUserToModify'],
                                    flight['legDepartureDate'],
                                    flight['airlineCode'],
                                    flight['identifier'],
                                    flight['sequence'],
                                    flight['flightOriginDay'],
                                    flight['numericFlightDate'],
                                    flight['numGMTDate'],
                                    flight['STDudt'],
                                    flight['STAudt'],
                                    flight['tailNumber'],
                                    flight['numLastDateModified'],
                                    flight['flightStatus'],
                                    flight['origin'],
                                    flight['STDLocal'],
                                    flight['dispatchDesk'],
                                    flight['STDGMTVariance'],
                                    flight['destination'],
                                    flight['STALocal'],
                                    flight['STAGMTVariance'],
                                    flight['OAGEquipmentType'],
                                    flight['ACConfiguration'],
                                    flight['serviceType'],
                                    flight['originGate'],
                                    flight['ETDlocal'],
                                    flight['ETDudt'],
                                    flight['TAXIutc'],
                                    flight['OUTudt'],
                                    flight['OFFudt'],
                                    flight['destinationGate'],
                                    flight['ETAlocal'],
                                    flight['ETAudt'],
                                    flight['ONudt'],
                                    flight['INudt'],
                                    flight['previousTailNumber'],
                                    flight['ETE'],
                                    flight['DCNutc'],
                                    flight['ETOutc'],
                                    flight['EONutc'],
                                    flight['EDTCutc'],
                                    flight['flightType'],
                                    flight['newDepartureCity'],
                                    flight['newArrivalCity'],
                                    flight['SchedOAGEquipType'],
                                    flight['OAGEquipSubType'],
                                    flight['csvFSDailyID'],
                                    flight['tailNumBeforeCancel'],
                                    flight['CTAUTC'],
                                    flight['cancelled'],
                                    flight['replaced'],
                                    flight['ATCStatus'],
                                    flight['scheduledFlightType'],
                                    flight['aircraftRouting'],
                                    flight['mealService'],
                                    flight['hub'],
                                    flight['landingRestriction'],
                                    flight['headStartFlight'],
                                    flight['actualDeparture'],
                                    flight['specialFlight'],
                                    flight['actualArrival'],
                                    flight['scheduledTaxiOut'],
                                    flight['scheduledTaxiIn'],
                                    flight['STOSetByUser'],
                                    flight['STISetByUser'],
                                    flight['CTFlightNumber']])
                print('Finished filtering flights. Check filtered.csv')

    else:
        # if file is not available abort the script
        print(f'Did not find csv file for adhoc 4')
        print('Check if the adhoc processor is down')
        pass

check_if_folder_exist(stageReceive)

call_adhoc_4_and_check_for_response_csv(stageReceive,stageSend,currentDirectory,currentDate)



