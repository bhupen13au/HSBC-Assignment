from django.shortcuts import render, redirect
from django.contrib import messages
import requests


def home(request):
    """
    Redirects to the search page
    """
    return redirect('search')


def search(request):
    """
    View for searching cities which starts with the given letter
    """
    if request.method == 'POST':
        letter = request.POST['letter']
        cities = []
        if letter.isalpha():
            try:
                # making get request to the end-point
                response = requests.get('https://samples.openweathermap.org/data/2.5/box/city?bbox=12,32,15,37,10&appid=b6907d289e10d714a6e88b30761fae22')
                # extracting data from the response from end-point
                data = response.json()
                # filtering city names from the data whose name starts with the letter provided by user
                cities = [city['name'] for city in data['list'] if city['name'][0].lower() == letter.lower()]
            except:
                messages.info(request, 'Faced error while getting cities')
                return render(request, 'search.html')

        # counting the no. of cities filtered
        count = len(cities)
        if cities:
            return render(request, 'search.html', {'cities': cities, 'count': count})
        else:
            messages.info(request, 'No data found')
            return render(request, 'search.html')

    else:
        return render(request, 'search.html')
