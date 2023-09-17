from flask import Flask, jsonify, request, send_file, render_template
import os
import json
from supabase import create_client, Client
from dotenv import load_dotenv
load_dotenv()


application = Flask(__name__)
@app.route('/')
def start():
    return "API IS RUNNING!"


@app.route('/accessDB/<event>')
def accessDB(event):
    url: str = os.environ.get('SUPABASE_URL')
    key: str = os.environ.get('SUPABASE_KEY')
    supabase: Client = create_client(url, key)
    event_drivers_response = supabase.table('Event').select("*, Driver(*)").eq('name', event).execute()
    event_riders_response = supabase.table('Event').select("*, Rider(*)").eq('name', event).execute()
    drivers_data = json.loads(event_drivers_response.json())
    riders_data = json.loads(event_riders_response.json())
    print(type(drivers_data))
    print(type(riders_data))


    event_values = [drivers_data, riders_data]
    return event_values

# API endpoint
@app.route('/api/dummy', methods=['GET'])
def hello():
    event = request.args.get('event')
    #print(event)

    event_values = accessDB(event)
    #print(event_values)

    #print(eventData)
    #event_values[0] contains the event and the drivers Data

    #event_values[1] contains the event and the riders Data

def organize_event_data(event_values):
    event_data = event_values[0]['data'][0]
    event_latitude = event_data['latitude']
    event_longitude = event_data['longitude']

    drivers = event_data['Driver']
    passengers = event_values[1]['data'][0]['Rider']

    formatted_data = {
        "Event": {
            "EventPin": [event_latitude, event_longitude],
            "Drivers": [
                {"DriverID": driver['id'], "Capacity": driver['capacity'], "DriverPin": [driver['latitude'], driver['longitude']]}
                for driver in drivers
            ],
            "Passengers": [
                {"PassengerID": rider['id'], "PassengerPin": [rider['latitude'], rider['longitude']]}
                for rider in passengers
            ]
        }
    }
    return formatted_data
    
@app.route('/api/endpoint', methods=['GET'])
def format_event():
    event = request.args.get('event')
    event_values = accessDB(event)  # Assuming this function is defined elsewhere
    formatted_data = organize_event_data(event_values)
    return formatted_data




if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8000)

