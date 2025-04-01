import requests
import json
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

# API Configuration
API_KEY = "cm5ppmxs30001js032fsnet77"
HEADERS = {'x-magicapi-key': API_KEY}
API_URL = "https://api.magicapi.dev/api/v1/aedbx/aerodatabox/flights/CallSign/{callsign}?withAircraftImage=false&withLocation=false"

# AI Configuration
DEEPSEEK_MODEL = "deepseek-r1-distill-llama-70b"
groq_client = ChatGroq(api_key="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", model_name=DEEPSEEK_MODEL)
parser = StrOutputParser()
ai_chain = groq_client | parser

def index(request):
    return render(request, 'index.html')

def search_flight(request):
    if request.method == 'GET':
        flight_callsign = request.GET.get('flight', '').upper()
        if not flight_callsign:
            return JsonResponse({'error': 'Please enter a flight number!'}, status=400)
        try:
            flight_data = get_flight_data(flight_callsign)
            if 'error' in flight_data:
                return JsonResponse({'error': flight_data['error']}, status=404)
            
            formatted_data = {
                'number': flight_data.get('number', 'N/A'),
                'status': flight_data.get('status', 'Unknown'),
                'aircraft': flight_data.get('aircraft', {}).get('model', 'N/A'),
                'departure': {
                    'airport': f"{flight_data.get('departure', {}).get('airport', {}).get('name', 'N/A')} ({flight_data.get('departure', {}).get('airport', {}).get('icao', 'N/A')})",
                    'time': flight_data.get('departure', {}).get('scheduledTime', {}).get('local', 'N/A')
                },
                'arrival': {
                    'airport': f"{flight_data.get('arrival', {}).get('airport', {}).get('name', 'N/A')} ({flight_data.get('arrival', {}).get('airport', {}).get('icao', 'N/A')})",
                    'time': flight_data.get('arrival', {}).get('predictedTime', {}).get('local', 'N/A')
                },
                'progress': flight_data.get('completionPercent', 0),
                'remaining': flight_data.get('timeRemaining', 'N/A')
            }
            return JsonResponse({'flights': [formatted_data]})
        except Exception as e:
            return JsonResponse({'error': f'System error: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def chat_assistant(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            callsign = data.get('callsign', '').upper()
            question = data.get('message', '').strip()
            if not callsign:
                return JsonResponse({'error': 'Flight number is required!'}, status=400)
            if not question:
                return JsonResponse({'error': 'Question field cannot be empty!'}, status=400)
            flight_data = get_flight_data(callsign)
            if 'error' in flight_data:
                return JsonResponse({'error': flight_data['error']}, status=404)
            response = generate_ai_response(flight_data, question)
            return JsonResponse({'response': response})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Internal server error: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Only POST requests are accepted'}, status=405)

def get_flight_data(callsign: str) -> dict:
    """Enhanced flight data retrieval function with custom timeRemaining calculation"""
    try:
        response = requests.get(
            API_URL.format(callsign=callsign),
            headers=HEADERS,
            timeout=15
        )
        response.raise_for_status()
        flights = response.json()
        if not flights or not isinstance(flights, list):
            return {'error': 'No data found for this flight number'}

        now_local = datetime.now()
        valid_flights = []
        for flight in flights:
            if not isinstance(flight, dict):
                continue
            try:
                dep_info = flight.get('departure', {})
                scheduled = dep_info.get('scheduledTime', {})
                dep_time_str = scheduled.get('local', '')
                if dep_time_str:
                    dep_clean = dep_time_str.replace('Z', '').split('+')[0]
                    dep_dt = datetime.fromisoformat(dep_clean)
                else:
                    dep_dt = None
                valid_flights.append({
                    'flight': flight,
                    'departure_dt': dep_dt,
                    'is_future': dep_dt and dep_dt >= now_local
                })
            except Exception:
                continue

        if not valid_flights:
            return {'error': 'No valid flight data available'}

        future_flights = [f for f in valid_flights if f['is_future']]
        if future_flights:
            selected = min(future_flights, key=lambda x: x['departure_dt'])['flight']
        else:
            selected = max(valid_flights, key=lambda x: x['departure_dt'])['flight']

        # Process departure time
        departure = selected.get('departure', {})
        sched = departure.get('scheduledTime', {})
        dep_time_str = sched.get('local', '')
        if dep_time_str:
            dep_clean = dep_time_str.replace('Z', '').split('+')[0]
            dep_dt = datetime.fromisoformat(dep_clean)
            sched['local'] = dep_dt.strftime('%d/%m/%Y %H:%M')
        else:
            sched['local'] = 'N/A'
            dep_dt = None

        # Process arrival time
        arrival = selected.get('arrival', {})
        pred = arrival.get('predictedTime', {})
        arr_time_str = pred.get('local', '')
        if arr_time_str:
            arr_clean = arr_time_str.replace('Z', '').split('+')[0]
            arr_dt = datetime.fromisoformat(arr_clean)
            pred['local'] = arr_dt.strftime('%d/%m/%Y %H:%M')
        else:
            pred['local'] = 'N/A'
            arr_dt = None

        # Calculate remaining time based on flight duration and current time
        if dep_dt and arr_dt:
            flight_duration = arr_dt - dep_dt
            elapsed = now_local - dep_dt
            remaining = flight_duration - elapsed
            if remaining.total_seconds() > 0:
                hours = remaining.seconds // 3600
                minutes = (remaining.seconds % 3600) // 60
                selected['timeRemaining'] = f"{hours}h {minutes}min"
            else:
                selected['timeRemaining'] = "0h 0min"
            total_seconds = flight_duration.total_seconds()
            selected['completionPercent'] = min(100, max(0, int((elapsed.total_seconds() / total_seconds) * 100)) if total_seconds > 0 else 0)

        number = selected.get('number', {})
        if isinstance(number, dict):
            selected['number'] = number.get('callSign', 'N/A')
        else:
            selected['number'] = 'N/A'

        selected['status'] = 'En Route' if selected.get('status') == 'EnRoute' else selected.get('status', 'Unknown')
        return selected

    except requests.exceptions.RequestException as e:
        return {'error': f'API connection error: {str(e)}'}
    except Exception as e:
        return {'error': f'Data processing error: {str(e)}'}


def generate_ai_response(flight_data: dict, question: str) -> str:
    try:
        prompt = f"""Use the following flight data to answer the user's question:
        {{
            "Flight No": "{flight_data.get('number', 'N/A')}",
            "Status": "{flight_data.get('status', 'Unknown')}",
            "Departure": "{flight_data.get('departure', {}).get('airport', {}).get('name', 'N/A')} ({flight_data.get('departure', {}).get('airport', {}).get('icao', 'N/A')})",
            "Arrival": "{flight_data.get('arrival', {}).get('airport', {}).get('name', 'N/A')} ({flight_data.get('arrival', {}).get('airport', {}).get('icao', 'N/A')})",
            "Departure Time": "{flight_data.get('departure', {}).get('scheduledTime', {}).get('local', 'N/A')}",
            "Estimated Arrival": "{flight_data.get('arrival', {}).get('predictedTime', {}).get('local', 'N/A')}",
            "Progress": "%{flight_data.get('completionPercent', 0)}",
            "Remaining Time": "{flight_data.get('timeRemaining', 'N/A')}"
        }}

        Rules:
        1. Answer only in English
        2. Maximum 2 sentences
        3. Use metric system
        4. Date format: DD/MM/YYYY HH:MM
        5. Current time: {datetime.now().strftime('%d/%m/%Y %H:%M')}

        Question: {question}
        """
        raw_response = ai_chain.invoke(prompt)
        return raw_response.split('</think>')[-1].strip() if '<think>' in raw_response else raw_response
    except Exception as e:
        return f"Could not generate response: {str(e)}"
