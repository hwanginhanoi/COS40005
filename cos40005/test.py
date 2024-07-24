
import redis
import json
import requests


r = redis.Redis(host='localhost', port=6379)

def call_api_extract():
    toExtract = r.lpop('extract_queue')
    toExtract = json.loads(toExtract)
    res = requests.get('http://localhost:9966?raw_data=' + toExtract['description'])
    res = res.json()
    # property = Property.objects.get(id=toExtract['id'])
    print('extracttttttt',res)

    try:
        if res['address']['result']:
            print(res['address']['result'])
        if res['real_area']['result']:
            print(res['real_area']['result'])
        if res['number_of_floors']['result']:
            print(res['number_of_floors']['result'])
        if res['number_of_bedrooms']['result']:
            print(res['address']['result'])
        if res['contact_number']['result']:
            print(res['contact_number']['result'])
        if res['number_of_toilets']['result']:
            print(res['number_of_toilets']['result'])
        if res['price']['result']:
            print(res['price']['result'])
        if res['publish_date']['result']:
            print(res['publish_date']['result'])
    except Exception as e:
        print(e)

    # property.save()

call_api_extract()