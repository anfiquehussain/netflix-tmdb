from django.shortcuts import render
from django.conf import settings
import requests

api_key = settings.TMDB_API_KEY
base_url = "https://api.themoviedb.org/3"
language = 'en-US'

def Index(request):
    query_key = request.GET.get('query_name')
    if query_key:
        endpoint_popular = f"/search/multi?query={query_key}"
    else:
        endpoint_popular = f"/trending/all/week?api_key={api_key}&language={language}"

    

    url = f"{base_url}{endpoint_popular}"
    params = {"api_key": api_key}

    response = requests.get(url, params=params)
    data = {}
    if response.status_code == 200:
        data = response.json()
        for movie in data["results"]:
            v_url = f"{base_url}/movie/{movie['id']}/videos?api_key={api_key}&language=en-US"
            v_response = requests.get(v_url)
            videos = []

            if v_response.status_code == 200:
                video_data = v_response.json()
                videos = video_data.get('results', [])

            movie['videos'] = videos
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

    context = {
        'data': data.get("results", []),
        'base_url': base_url,
        'endpoint_popular': endpoint_popular,
        'imageUrl': 'https://image.tmdb.org/t/p/original',
        'language': language,
        'v_response': v_response,
    }

    return render(request, 'index.html', context)



