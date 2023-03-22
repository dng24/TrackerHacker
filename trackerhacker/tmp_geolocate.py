import dns.resolver
import requests
import json

def get_dns(url):
    url_ips = []
    answers = dns.resolver.resolve(url, 'A')
    for a in answers:
        url_ips.append(str(a))

    return url_ips


def geolocate(urls):
    for ip in urls:
        request_url = 'https://geolocation-db.com/jsonp/' + ip
        response = requests.get(request_url)
        result = response.content.decode()
        result = result.split("(")[1].strip(")")
        result  = json.loads(result)
        print(f"Geolocation for {ip}: \n\n  {result}")

x = get_dns('www.cnn.com')
print(x)

geolocate(x)
