import requests, json, csv
from JabberCreator import *

#Target CUCM server details
CUCM_IP = '<your_cucm_ip>'
CUCM_USERNAME = '<your_cucm_username_AXL_enabled>'
CUCM_PASSWORD = '<your_cucm_password_AXL_enabled>'

#Webex Teams room details
TARGET_ROOM_NAME = '<your_room_name>'
GET_ROOMS_API_URL = 'https://webexapis.com/v1/rooms?max=200'
POST_MESSAGE_API_URL = 'https://webexapis.com/v1/messages'
WEBEX_ACCESS_TOKEN = '<your_access_token>'

'''
Posting of message in specified Webex Teams room
'''
def notify_teams(message):
    #Get Teams chat id of interest
    room_collection = requests.get(
        url = GET_ROOMS_API_URL,
        headers = {
            "Authorization": f'Bearer {WEBEX_ACCESS_TOKEN}',
            "Content-Type": "application/json"
            }
    )
    print(room_collection.status_code)
    ROOM_ID = list(filter(lambda x: TARGET_ROOM_NAME in x["title"],json.loads(room_collection.text)['items']))[0]['id']
    print(ROOM_ID)

    #Post message
    requests.post(
        POST_MESSAGE_API_URL,
        data = json.dumps({
            "roomId": ROOM_ID,
            "text": message
        }),
        headers = {
            "Authorization": f'Bearer {WEBEX_ACCESS_TOKEN}',
            "Content-Type": "application/json"
        },
    )

'''
Provisioning of jabber devices
'''
def main():
    #Connection to the target CUCM node
    TARGET_CUCM = JabberCreator(CUCM_IP,CUCM_USERNAME,CUCM_PASSWORD,debug=False)

    #If the connection is successful, proceed with the provisioning
    if(TARGET_CUCM.isValid()):

        #Dummy data collection and parsing
        with open('mock_data_users_provisioning.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            PROVISIONING_LOGS = ''
            for row in csv_reader: 
                DEVICE_NAME = f'CSF{row[0].upper()}'         
                DEVICE_LINES = [
                    {
                        'index':'1',
                        'dirn':{
                            'pattern':row[1],
                            'routePartitionName':'INTERNAL_PT'
                        }
                    },
                    {
                        'index':'2',
                        'dirn':{
                            'pattern':'810010',
                            'routePartitionName':'Shared-PT'
                        }
                    }
                ]

                #Provisioning of the jabber device
                result = TARGET_CUCM.add_jabber_device(DEVICE_NAME,DEVICE_LINES,row[3],row[2],row[0])

                #Reporting of the provisioning results
                if 'ERROR' in result:
                    print(f'💥 CSF{row[0].upper()} - {result}')
                    PROVISIONING_LOGS += f'💥 CSF{row[0].upper()} - {result}\n'
                else:
                    print(f'✅ CSF{row[0].upper()}')
                    PROVISIONING_LOGS += f'✅ CSF{row[0].upper()}\n'

            #Posting of results in Teams
            notify_teams(PROVISIONING_LOGS)

if __name__ == "__main__":
    main()