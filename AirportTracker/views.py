import requests
from django.shortcuts import render
from datetime import datetime, timezone

def index(request):
    """Anasayfa için şablonu döndürür."""
    return render(request, 'index.html')

def search_flight(request):
    """CallSign'e göre uçuş bilgilerini arar ve sonuçları döndürür."""
    flight_callsign = request.GET.get('flight')
    if not flight_callsign:
        return render(request, 'index.html', {'error': 'Flight CallSign is required!'})

    # API isteği
    flight_url = (
        f"https://api.magicapi.dev/api/v1/aedbx/aerodatabox/flights/CallSign/"
        f"{flight_callsign}?withAircraftImage=false&withLocation=false"
    )
    headers = {'x-magicapi-key': 'cm5ppmxs30001js032fsnet77'}
    response = requests.get(flight_url, headers=headers)

    if response.status_code != 200:
        return render(request, 'index.html', {'error': 'Flight not found!'})

    flights_data = response.json()
    if not flights_data:
        return render(request, 'index.html', {'error': 'No data available for this flight!'})

    # 1) API'den dönen tüm uçuş kayıtlarını parse edip departure zamanlarına göre sıralayalım
    flight_items = []
    for raw_flight in flights_data:
        dep_local_str = raw_flight.get('departure', {}).get('scheduledTime', {}).get('local')
        
        # Uçuşu bir listeye eklerken parse edilip edilmediğini kontrol edelim
        if dep_local_str:
            try:
                dep_dt = datetime.fromisoformat(dep_local_str.replace('Z', '+00:00'))
            except ValueError:
                dep_dt = None
        else:
            dep_dt = None
        
        flight_items.append({
            'flight': raw_flight,
            'departure_dt': dep_dt
        })

    # 2) departure_dt değerine göre sıralayalım (tarihe göre)
    #    departure_dt olmayanlar (None) en sona atılacak şekilde
    flight_items.sort(key=lambda x: (x['departure_dt'] is None, x['departure_dt']))

    # 3) Şimdiki UTC zamanını al
    now_utc = datetime.now(timezone.utc)
    future_flights = [f for f in flight_items if f['departure_dt'] and f['departure_dt'] >= now_utc]
    
    # 4) Eğer gelecekte/şu anda olan uçuşlar varsa en yakını alalım.
    #    Yoksa, en son gerçekleşen uçuşu (listede en sonuncu) alalım.
    if future_flights:
        selected_flight_dict = future_flights[0]  # Liste sıralı, en yakını bu
    else:
        # Tümü geçmişteyse en son (en güncel) uçuşu al
        selected_flight_dict = flight_items[-1]

    selected_flight = selected_flight_dict['flight']

    # Aşağıdaki kısım, tek bir kaydı işlemeye uyarlanmıştır.
    STATUS_MAP = {
        'EnRoute': 'On the Way'
    }

    raw_status = selected_flight.get('status', 'Unknown')
    selected_flight['status'] = STATUS_MAP.get(raw_status, raw_status)

    dep_local_str = selected_flight.get('departure', {}).get('scheduledTime', {}).get('local')
    arr_local_str = (
        selected_flight.get('arrival', {}).get('scheduledTime', {}).get('local')
        or selected_flight.get('arrival', {}).get('predictedTime', {}).get('local')
    )

    # Zaman formatlama
    if dep_local_str:
        try:
            dep_dt = datetime.fromisoformat(dep_local_str.replace('Z', '+00:00'))
            selected_flight['departure']['scheduledTime']['local'] = dep_dt.strftime('%Y-%m-%d %H:%M')
        except:
            pass

    if arr_local_str:
        try:
            arr_dt = datetime.fromisoformat(arr_local_str.replace('Z', '+00:00'))
            if ('scheduledTime' in selected_flight['arrival'] 
                and 'local' in selected_flight['arrival']['scheduledTime']):
                selected_flight['arrival']['scheduledTime']['local'] = arr_dt.strftime('%Y-%m-%d %H:%M')
            elif ('predictedTime' in selected_flight['arrival'] 
                  and 'local' in selected_flight['arrival']['predictedTime']):
                selected_flight['arrival']['predictedTime']['local'] = arr_dt.strftime('%Y-%m-%d %H:%M')
        except:
            pass

    # Uçuşun yüzde kaçının tamamlandığı + kalan süre
    try:
        now_utc = datetime.now(timezone.utc)
        dep_for_calc = datetime.fromisoformat(dep_local_str.replace('Z', '+00:00'))
        arr_for_calc = datetime.fromisoformat(arr_local_str.replace('Z', '+00:00'))

        total_duration = (arr_for_calc - dep_for_calc).total_seconds()
        elapsed = (now_utc - dep_for_calc).total_seconds()
        remaining = (arr_for_calc - now_utc).total_seconds()

        percentage = 0
        if total_duration > 0:
            ratio = elapsed / total_duration
            if ratio < 0:
                percentage = 0
            elif ratio > 1:
                percentage = 100
            else:
                percentage = int(ratio * 100)
        selected_flight['completionPercent'] = percentage

        if remaining > 0:
            hours = int(remaining // 3600)
            minutes = int((remaining % 3600) // 60)
            selected_flight['timeRemaining'] = f"{hours}h {minutes}m"
        else:
            selected_flight['timeRemaining'] = "0h 0m"
    except:
        selected_flight['completionPercent'] = 0
        selected_flight['timeRemaining'] = "Unknown"

    # Artık sadece tek uçuşu 'flights' listesi hâlinde şablona gönderiyoruz
    flights = [selected_flight]

    return render(request, 'search_results.html', {'flights': flights})
