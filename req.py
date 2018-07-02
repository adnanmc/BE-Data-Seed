import json, datetime, time
from pathlib import Path

# all const
stg1DropLocation = Path('//gscfile01/SharedFile/QA_MVC/STG1/adh_receive')
stg1ReceiveLocation = Path('//gscfile01/SharedFile/QA_MVC/STG1/adh_send')
stg2DropLocation = Path('//gscfile01/SharedFile/QA_MVC/STG2/adh_receive')
stg2ReceiveLocation = Path('//gscfile01/SharedFile/QA_MVC/STG2/adh_send')
stg3DropLocation = Path('//gscfile01/SharedFile/QA_MVC/STG3/adh_receive')
stg3ReceiveLocation = Path('//gscfile01/SharedFile/QA_MVC/STG3/adh_send')
testLocation = Path('test')

# functions
def step1_OOOI_previous_day(environment, fDate):
    if environment == 'stg1':
        location = stg1DropLocation
    elif environment == 'stg2':
        location = stg2DropLocation
    elif environment == 'stg3':
        location = stg3DropLocation
    # location = testLocation # this is only for testing purpose
    data = f'ADH015_{fDate}TIMP0100000'
    
    # pick location based on env

    request_file = open(f'{location}/step1_OOOI_previous_day.txt', 'w')
    request_file.write(data)
    request_file.close()
    
def step2_ETD_target_day(environment, fDate):
    if environment == 'stg1':
        location = stg1DropLocation
    elif environment == 'stg2':
        location = stg2DropLocation
    elif environment == 'stg3':
        location = stg3DropLocation
    # location = testLocation # this is only for testing purpose
    data = f'ADH015_{fDate}ETDP0100015'
    
    # pick location based on env

    request_file = open(f'{location}/step2_ETD_target_day.txt', 'w')
    request_file.write(data)
    request_file.close()

def step3_OOOI_target_day(environment, fDate):
    if environment == 'stg1':
        location = stg1DropLocation
    elif environment == 'stg2':
        location = stg2DropLocation
    elif environment == 'stg3':
        location = stg3DropLocation
    # location = testLocation # this is only for testing purpose
    data = f'ADH015_{fDate}TIMP0100000'
    
    # pick location based on env

    request_file = open(f'{location}/step3_OOOI_target_day.txt', 'w')
    request_file.write(data)
    request_file.close()


with open('config.json') as json_file:  
    data = json.load(json_file)
    env = data['env']
    tDateString = data['targetDate']
    tDate = datetime.datetime.strptime(tDateString,'%d%b%y')
    targetDate = tDate.strftime('%d%b%y').upper()
    preveousDate = (tDate + datetime.timedelta(days=-1)).strftime('%d%b%y').upper()

# print(targetDate)
# print(preveousDate)

step1_OOOI_previous_day(env, preveousDate)
nextStepTime = (datetime.datetime.now() + datetime.timedelta(minutes=30)).strftime('%b-%d-%Y | %I:%M %p')
print(f'Waiting 30 min for all previous day: {preveousDate} flights to have OOOI times added')
print(f'Next step will start on {nextStepTime}')
time.sleep(1800)


step2_ETD_target_day(env, preveousDate)
nextStepTime = (datetime.datetime.now() + datetime.timedelta(minutes=30)).strftime('%b-%d-%Y | %I:%M %p')
print(f'Waiting 30 min for all target day: {targetDate} flights to have 15 min ETD delay added')
print(f'Next step will start on {nextStepTime}')
time.sleep(1800)


step3_OOOI_target_day(env, preveousDate)
nextStepTime = (datetime.datetime.now() + datetime.timedelta(minutes=30)).strftime('%b-%d-%Y | %I:%M %p')
print(f'Waiting 30 min for all target day: {targetDate} flights to have OOOI times added')
print(f'This step will finish on {nextStepTime}')
time.sleep(1800)
print('Finished sending requests.')
print('Important!! Please login to Movement Control to manually add OOOI values to any flight that may be missed!')


