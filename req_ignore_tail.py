#!python 3.6.2 or greater
# import all necessary packages
import datetime
import csv
import os
import shutil
import time
import fnmatch
import sys
import json
import re
import json
from pathlib import Path
from collections import OrderedDict
# current directory
currentDirectory = Path(os.getcwd())

# all const
stg1DropLocation = Path('//cuaisilon/socappstgfile01/SOC_Share/Stg1/QA_MVC/adh_receive')
stg1ReceiveLocation = Path('//cuaisilon/socappstgfile01/SOC_Share/Stg1/QA_MVC/adh_send')
stg2DropLocation = Path('//gscfile01/SharedFile/QA_MVC/STG2/adh_receive')
stg2ReceiveLocation = Path('//gscfile01/SharedFile/QA_MVC/STG2/adh_send')
stg3DropLocation = Path('//gscfile01/SharedFile/QA_MVC/STG3/adh_receive')
stg3ReceiveLocation = Path('//gscfile01/SharedFile/QA_MVC/STG3/adh_send')

# get the target date and drop location
with open('config.json') as json_file:
    data = json.load(json_file)
    env = data['env']
    tDateString = data['targetDate']
    if env != 'stg1' and env != 'stg2' and env != 'stg3':
        print(f'Make sure "env" is set to "stg1" or "stg2" or "stg3"')
        print(f'Invalid "env" data on config.json')
        sys.exit("Stopping script .......")
    pattern = r'(([0-2]\d{1})|([3][01]{1}))(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)(\d)(\d)'
    datePattern = re.compile(pattern)
    if not datePattern.match(tDateString):
        print(f'Make sure "targetDate" is set using format "DDMMMYY". Month should be uppercase!! ex: 02JUN18')
        print(f'Invalid "targetDate" data on config.json')
        sys.exit("Stopping script .......")
    tDate = datetime.datetime.strptime(tDateString, '%d%b%y')
    currentDate = tDate.strftime('%d%b%y').upper()
    preveousDate = (tDate + datetime.timedelta(days=-1)
                    ).strftime('%d%b%y').upper()
    # ignore these tail numbers
    ignoreTail = data['ignoreTail']
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
def call_adhoc_4_and_get_filtered_tail_num_untouched_flight_data_csv(receive_folder, send_folder, local_directory, current_date, outputFileName='filtered_data/filtered'):
    # note that repeat is needed since the adhoc processor sometimes does not return csv.
    # get current timestamp
    sendPattern = f'MCEG_DATA*.txt'
    timeStamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    sentFiles = os.listdir(send_folder)
    if fnmatch.filter(sentFiles, sendPattern):
        print('There are request files waiting on que, adhoc processor may be down')
    else:
        request_file = open(
            f'{send_folder}/MCEG_DATA_ADHOC4_{timeStamp}.txt', 'w')
        request_file.write(f'ADH004_{current_date}')
        adh004String = f'ADH004_{current_date}'
        request_file.close()
        print(
            f' Sending adhoc 4 request using: {adh004String} and waiting for file....')
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
        shutil.copy(
            f'{receive_folder}/{file_name[0]}', f'{local_directory}/DATA/data.csv')
        print("csv file copied to local folder for parsing")
        # remove all files that was generated by this script.
        for csvfile in os.listdir(receive_folder):
            if fnmatch.fnmatch(csvfile, 'MCEG_DATA_ADHOC4*.csv'):
                os.remove(f'{receive_folder}/{csvfile}')

        # add header row
        with open(f'{local_directory}/DATA/data.csv', newline='') as f:
            r = csv.reader(f)
            data = [line for line in r]
        with open(f'{local_directory}/DATA/data.csv', 'w', newline='') as f:
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
                if (x['sequence'].strip() == '10'
                    and x['tailNumber'].strip() not in ignoreTail
                        and x['tailNumber'].strip().startswith('-') == False):
                    filteredData.append(x)

            with open(f'{outputFileName}.csv', 'w+', newline='') as csvfile:
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
                print(
                    f'Finished filtering flights. Check {outputFileName}.csv')
                with open(f'{outputFileName}.csv') as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)

                with open(f'{outputFileName}.json', 'w') as f:
                    json.dump(rows, f)
    else:
        # if file is not available abort the script
        print(f'Did not find csv file for adhoc 4')
        print('Check if the adhoc processor is down')
        pass


check_if_folder_exist(stageReceive)

# taking data for day before the target date
call_adhoc_4_and_get_filtered_tail_num_untouched_flight_data_csv(
    stageReceive, stageSend, currentDirectory, preveousDate, 'DATA/dayBefore')

# create OOOI for all the flights except ignored tails
print(f'Making all flights arrive for previous day: {preveousDate} of target date')
timeStamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
print(f'This will take 1hr and 20 min from now. Starting at: {timeStamp} ...........')

with open('DATA/dayBefore.json') as f:
    data = json.load(f)

    ###########################################
    # Sending OUT request for all flight
    ###########################################
    for x in data:
        flightNum = x['identifier'].strip().rjust(4, '0')
        utcOriginDate = x['numGMTDate'].strip()
        origin = x['origin'].strip()
        destination = x['destination'].strip()
        stdUTC = x['STDudt'].strip()
        outUTC = stdUTC
        outAdhocString = f'ADH016_{flightNum}{utcOriginDate}{origin}{destination}{stdUTC}OUT{outUTC}'
        timeStamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        request_file = open(
            f'{stageSend}/MCEG_BE_TEST_DATA_ADHOC16_OUT_{flightNum}_{timeStamp}.txt', 'w')
        request_file.write(outAdhocString)
        request_file.close()
    time.sleep(1200)

    ###########################################
    # Sending OFF request for all flight
    ###########################################
    for x in data:
        flightNum = x['identifier'].strip().rjust(4, '0')
        utcOriginDate = x['numGMTDate'].strip()
        origin = x['origin'].strip()
        destination = x['destination'].strip()
        stdUTC = x['STDudt'].strip()
        outUTC = stdUTC
        offUTC = (datetime.datetime.strptime(stdUTC, '%H%M') +
                  datetime.timedelta(minutes=5)).strftime(format='%H%M')
        offAdhocString = f'ADH016_{flightNum}{utcOriginDate}{origin}{destination}{stdUTC}OFF{outUTC}{offUTC}'
        timeStamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        request_file = open(
            f'{stageSend}/MCEG_BE_TEST_DATA_ADHOC16_OFF_{flightNum}_{timeStamp}.txt', 'w')
        request_file.write(offAdhocString)
        request_file.close()
    time.sleep(1200)

    ###########################################
    # Sending ON request for all flight
    ###########################################
    for x in data:
        flightNum = x['identifier'].strip().rjust(4, '0')
        utcOriginDate = x['numGMTDate'].strip()
        origin = x['origin'].strip()
        destination = x['destination'].strip()
        stdUTC = x['STDudt'].strip()
        staUTC = x['STAudt'].strip()
        onUTC = (datetime.datetime.strptime(staUTC, '%H%M') +
                  datetime.timedelta(minutes=-5)).strftime(format='%H%M')
        onAdhocString = f'ADH016_{flightNum}{utcOriginDate}{origin}{destination}{stdUTC}ON_{onUTC}'
        timeStamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        request_file = open(
            f'{stageSend}/MCEG_BE_TEST_DATA_ADHOC16_ON_{flightNum}_{timeStamp}.txt', 'w')
        request_file.write(onAdhocString)
        request_file.close()
    time.sleep(1200)

    
    ###########################################
    # Sending IN request for all flight
    ###########################################
    for x in data:
        flightNum = x['identifier'].strip().rjust(4, '0')
        utcOriginDate = x['numGMTDate'].strip()
        origin = x['origin'].strip()
        destination = x['destination'].strip()
        stdUTC = x['STDudt'].strip()
        onUTC = (datetime.datetime.strptime(staUTC, '%H%M') +
                  datetime.timedelta(minutes=-5)).strftime(format='%H%M')
        inUTC = (datetime.datetime.strptime(staUTC, '%H%M') +
                  datetime.timedelta(minutes=0)).strftime(format='%H%M')
        inAdhocString = f'ADH016_{flightNum}{utcOriginDate}{origin}{destination}{stdUTC}IN_{onUTC}{inUTC}'
        timeStamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        request_file = open(
            f'{stageSend}/MCEG_BE_TEST_DATA_ADHOC16_IN_{flightNum}_{timeStamp}.txt', 'w')
        request_file.write(inAdhocString)
        request_file.close()
    time.sleep(1200)


# taking data for day before the target date
call_adhoc_4_and_get_filtered_tail_num_untouched_flight_data_csv(
    stageReceive, stageSend, currentDirectory, currentDate, 'DATA/targetDay')

with open('DATA/targetDay.json') as f:
    data = json.load(f)

    # create ETD delay + OOOI for all the flights except ignored tails
    print(f'Making all flights delayed by 15 min and OOOI for target day: {currentDate}')
    timeStamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    print(f'This will take 1hr and 40 min from now. Starting at: {timeStamp} ...........')

    ###########################################
    # Sending ETD request for all flight
    ###########################################
    for x in data:
        flightNum = x['identifier'].strip().rjust(4, '0')
        utcOriginDate = x['numGMTDate'].strip()
        origin = x['origin'].strip()
        destination = x['destination'].strip()
        stdUTC = x['STDudt'].strip()
        etdUTC = (datetime.datetime.strptime(stdUTC, '%H%M') +
                  datetime.timedelta(minutes=15)).strftime(format='%H%M')
        etdAdhocString = f'ADH016_{flightNum}{utcOriginDate}{origin}{destination}{stdUTC}ETD{etdUTC}'
        timeStamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        request_file = open(
            f'{stageSend}/MCEG_BE_TEST_DATA_ADHOC16_ETD_{flightNum}_{timeStamp}.txt', 'w')
        request_file.write(etdAdhocString)
        request_file.close()
    time.sleep(1200)

    ###########################################
    # Sending OUT request for all flight
    ###########################################
    for x in data:
        flightNum = x['identifier'].strip().rjust(4, '0')
        utcOriginDate = x['numGMTDate'].strip()
        origin = x['origin'].strip()
        destination = x['destination'].strip()
        stdUTC = x['STDudt'].strip()
        outUTC = (datetime.datetime.strptime(stdUTC, '%H%M') +
                  datetime.timedelta(minutes=15)).strftime(format='%H%M')
        outAdhocString = f'ADH016_{flightNum}{utcOriginDate}{origin}{destination}{stdUTC}OUT{outUTC}'
        timeStamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        request_file = open(
            f'{stageSend}/MCEG_BE_TEST_DATA_ADHOC16_OUT_{flightNum}_{timeStamp}.txt', 'w')
        request_file.write(outAdhocString)
        request_file.close()
    time.sleep(1200)

    ###########################################
    # Sending OFF request for all flight
    ###########################################
    for x in data:
        flightNum = x['identifier'].strip().rjust(4, '0')
        utcOriginDate = x['numGMTDate'].strip()
        origin = x['origin'].strip()
        destination = x['destination'].strip()
        stdUTC = x['STDudt'].strip()
        outUTC = (datetime.datetime.strptime(stdUTC, '%H%M') +
                  datetime.timedelta(minutes=15)).strftime(format='%H%M')
        offUTC = (datetime.datetime.strptime(stdUTC, '%H%M') +
                  datetime.timedelta(minutes=20)).strftime(format='%H%M')
        offAdhocString = f'ADH016_{flightNum}{utcOriginDate}{origin}{destination}{stdUTC}OFF{outUTC}{offUTC}'
        timeStamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        request_file = open(
            f'{stageSend}/MCEG_BE_TEST_DATA_ADHOC16_OFF_{flightNum}_{timeStamp}.txt', 'w')
        request_file.write(offAdhocString)
        request_file.close()
    time.sleep(1200)

    ###########################################
    # Sending ON request for all flight
    ###########################################
    for x in data:
        flightNum = x['identifier'].strip().rjust(4, '0')
        utcOriginDate = x['numGMTDate'].strip()
        origin = x['origin'].strip()
        destination = x['destination'].strip()
        stdUTC = x['STDudt'].strip()
        staUTC = x['STAudt'].strip()
        onUTC = (datetime.datetime.strptime(staUTC, '%H%M') +
                  datetime.timedelta(minutes=10)).strftime(format='%H%M')
        onAdhocString = f'ADH016_{flightNum}{utcOriginDate}{origin}{destination}{stdUTC}ON_{onUTC}'
        timeStamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        request_file = open(
            f'{stageSend}/MCEG_BE_TEST_DATA_ADHOC16_ON_{flightNum}_{timeStamp}.txt', 'w')
        request_file.write(onAdhocString)
        request_file.close()
    time.sleep(1200)

    
    ###########################################
    # Sending IN request for all flight
    ###########################################
    for x in data:
        flightNum = x['identifier'].strip().rjust(4, '0')
        utcOriginDate = x['numGMTDate'].strip()
        origin = x['origin'].strip()
        destination = x['destination'].strip()
        stdUTC = x['STDudt'].strip()
        onUTC = (datetime.datetime.strptime(staUTC, '%H%M') +
                  datetime.timedelta(minutes=10)).strftime(format='%H%M')
        inUTC = (datetime.datetime.strptime(staUTC, '%H%M') +
                  datetime.timedelta(minutes=15)).strftime(format='%H%M')
        inAdhocString = f'ADH016_{flightNum}{utcOriginDate}{origin}{destination}{stdUTC}IN_{onUTC}{inUTC}'
        timeStamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        request_file = open(
            f'{stageSend}/MCEG_BE_TEST_DATA_ADHOC16_IN_{flightNum}_{timeStamp}.txt', 'w')
        request_file.write(inAdhocString)
        request_file.close()
    time.sleep(1200)

# cleanup csv folder after the script run where adhocprocessor could not find the flight.
for csvfile in os.listdir(stageReceive):
    if fnmatch.fnmatch(csvfile, 'MCEG_BE_TEST_DATA_ADHOC16*.csv'):
        os.remove(f'{stageReceive}/{csvfile}')
print('Finished sending requests.')
print('Important!! Please login to Movement Control to manually add OOOI values to any flight that may be missed!')
