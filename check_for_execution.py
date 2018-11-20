import sys
import json
import requests

def parse_guids(activity_response):
    '''Parse response response from Activity endpoint
       return a unique set of GUIDs
    '''
    return {entry['connector_guid'] for entry in activity_response['data']}

def main():
    '''The main logic of the script
    '''
    client_id = 'a1b2c3d4e5f6g7h8i9j0'
    api_key = 'a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6'

    try:
        sha256 = sys.argv[1]
    except IndexError:
        sha256 = input('Enter a SHA256: ')

    # Instantiate requestions session object
    amp_session = requests.session()
    amp_session.auth = (client_id, api_key)

    # Containers for data
    output_json = {'executed':False, 'sha256':sha256, 'hosts':[]}
    guids = set()

    # Activity URL
    activity_url = 'https://api.amp.cisco.com/v1/computers/activity?q={}'.format(sha256)

    # Query the Activity API endpoint
    response_json = amp_session.get(activity_url).json()

    # Print the number of computers that have seen the file
    total_guids = response_json['metadata']['results']['total']
    print('\nComputers that have seen the file: {}'.format(total_guids))

    # Extract GUIDs from JSON
    guids = guids.union(parse_guids(response_json))

    # Check if there are more pages and repeat
    while 'next' in response_json['metadata']['links']:
        next_url = response_json['metadata']['links']['next']
        response_json = amp_session.get(next_url).json()
        index = response_json['metadata']['results']['index']
        print('Processing index: {}'.format(index))
        guids = guids.union(parse_guids(response_json))

    # Get GUID trajectory
    for guid in guids:
        trajectory_url = 'https://api.amp.cisco.com/v1/computers/{}/trajectory?q={}'.format(guid, sha256)
        trajectory_response_json = amp_session.get(trajectory_url).json()
        data = trajectory_response_json.get('data')
        computer = data.get('computer', {'hostname':'Hostname not found'})
        hostname = computer.get('hostname')
        events = data.get('events')

        guid_json = {'guid':guid, 'hostname':hostname, 'seen':True, 'executed':False, 'executed_file':None}

        if events is not None:
            for event in events:
                event_type = event.get('event_type')
                # Verify the event type and the executed SHA256 is not the parent
                if event_type == 'Executed by' and sha256 == event['file']['identity']['sha256']:
                    file_name = event['file']['file_name']
                    file_path = event['file']['file_path']
                    if guid_json['executed_file'] is None:
                        guid_json['executed_file'] = set()
                    guid_json['executed_file'].add((file_name, file_path))
                    guid_json['executed'] = True
                    output_json['executed'] = True

        # Convert set to list so it is serializable for JSON output
        if guid_json['executed_file'] is not None:
            guid_json['executed_file'] = list(guid_json['executed_file'])

        # Append to hosts list
        output_json['hosts'].append(guid_json)

    # Parse output_json and print computers that executed the SHA256
    print('\nHosts observed executing the file:')
    for host in output_json['hosts']:
        if host['executed']:
            print('{} - {}'.format(host['guid'], host['hostname']))
            for file in host['executed_file']:
                print('  File: {}\n  Path: {}\n'.format(file[0], file[1]))

    # Write output to a file
    with open('output.json', 'w') as file:
        file.write(json.dumps(output_json))

if __name__ == "__main__":
    main()
