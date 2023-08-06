from django.test import TestCase

# Create your tests here.


import requests


if __name__ == "__main__":
    requests.get('http://localhost:8000/post/ip/?esp_ip=dfkghj,')
    print(requests.get('http://localhost:8000/get/ip/').json())