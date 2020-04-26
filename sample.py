import requests
import csv
import json

def make_request(url):
    r = requests.get('http://samplecsvs.s3.amazonaws.com/Sacramentorealestatetransactions.csv')
    return r

if __name__ == "__main__":
    res = make_request('hello')
    decoded = res.content.decode('utf-8')
    cr = csv.reader(decoded.splitlines(), delimiter=',')
    data = []
    my_list = list(cr)
    for row in my_list[:2]:
        data.append(row) 
    json_data = json.dumps(data)
    #print(f"json_data = {json_data}")
    print(json_data)

