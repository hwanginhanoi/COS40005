import json
import os

from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import string
import re
from elasticsearch import Elasticsearch
import pandas as pd
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

prefixes = {
    'street': ['pho', 'duong'],
    'ward': ['xa','phuong','thi tran'],
    'district': ['quan','huyen','thi xa'],
    'province': ['tinh','thanh pho']
}

INTAB = "ạảãàáâậầấẩẫăắằặẳẵóòọõỏôộổỗồốơờớợởỡéèẻẹẽêếềệểễúùụủũưựữửừứíìịỉĩýỳỷỵỹđẠẢÃÀÁÂẬẦẤẨẪĂẮẰẶẲẴÓÒỌÕỎÔỘỔỖỒỐƠỜỚỢỞỠÉÈẺẸẼÊẾỀỆỂỄÚÙỤỦŨƯỰỮỬỪỨÍÌỊỈĨÝỲỶỴỸĐ"

OUTTAB = "a" * 17 + "o" * 17 + "e" * 11 + "u" * 11 + "i" * 5 + "y" * 5 + "d" + \
         "A" * 17 + "O" * 17 + "E" * 11 + "U" * 11 + "I" * 5 + "Y" * 5 + "D"

r = re.compile("|".join(INTAB))
replaces_dict = dict(zip(INTAB, OUTTAB))

def normalize_vietnamese(text):
    return r.sub(lambda m: replaces_dict[m.group(0)], text).lower()

def search(index, query, client):
    resp = client.search(
        index=index,
        query={
            "multi_match": {
                "query": query,
                "fields": ["parent_code", "name", "slug", "name_with_type", "path_with_type", "abbreviation"]
            }
        },
    )

    return resp["hits"]["hits"]

def normalise_address(addr, client):
    res = {
        'street': None,
        'ward': None,
        'district': None,
        'province': None
    }
    addr = normalize_vietnamese(addr).split(',')
    for i in range(len(addr)-1,-1,-1):
        addr[i] = addr[i].strip().lstrip()

        is_hcm_ward = False
        for j in range(12, -1, -1):
            if addr[i].__contains__('quan ' + str(j)):
                addr[i] = 'quan ' + str(j)
                is_hcm_ward = True
                break

    if len(addr)-1 >= 0:
        raw = addr[len(addr)-1]
        search_res = search("tinh_tp", raw, client)
        if len(search_res) > 0:
            res['province'] = search_res[0]["_source"]["id"]
    if len(addr)-2 >= 0:
        raw = addr[len(addr)-2] + ', ' + addr[len(addr)-1]
        search_res = search("quan_huyen", raw, client)
        for r in search_res:
            if r["_source"]["parent_code"] == res['province']:
                res['district'] = r["_source"]["id"]
                break
    if len(addr)-3 >= 0:
        raw = addr[len(addr)-3] + ', ' + addr[len(addr)-2] + ', ' + addr[len(addr)-1]
        search_res = search("xa_phuong", raw, client)
        for r in search_res:
            if r["_source"]["parent_code"] == res['district']:
                res['ward'] = r["_source"]["id"]
                break
    if len(addr)-4 >= 0:
        res['street'] = addr[len(addr)-4]
    return res

def normalise_price(price_str):
    price_str = normalize_vietnamese(price_str)
    res = {
        "price": -1,
        "isRent": False
    }
    if "/thang" in price_str:
        price_str = price_str.replace("/thang","")
        res['isRent'] = True
    price = 0
    price_str = price_str.split(' ')
    for i in range(0,len(price_str),2):
        if i + 1 < len(price_str) and price_str[i].isnumeric():
            if price_str[i+1] in ["ti", "ty"]:
                price += int(price_str[i]) * 1000000000
            elif price_str[i+1] == "trieu":
                price += int(price_str[i]) * 1000000
            elif price_str[i+1] == "nghin":
                price += int(price_str[i]) * 1000

    if not res['isRent']:
        res['isRent'] = price < 700000000

    res['price'] = price
    return res

def normalise_area(area_str):
    res = -1
    area_str = area_str.split(" ")
    try:
        if area_str[0].isnumeric():
            res = float(area_str[0])
        elif ',m2' in area_str[0]:
            res = float(area_str[0].replace(',m2',''))
        elif 'm2' in area_str[0]:
            res = float(area_str[0].replace('m2',''))
    except Exception as e:
        print(e)
    return res

def normalise_floor(floor_str):
    res = -1
    if floor_str.isnumeric():
        res = int(floor_str)
    else:
        res = 0
        floor_split = floor_str.split(' ')
        for f in floor_split:
            if f.isnumeric():
                res = res + int(f)

    return res

import psycopg2
def create_data(username, password):
    client = Elasticsearch("https://localhost:9200/", basic_auth=(username, password), ca_certs='./http_ca.crt',
                           verify_certs=False)
    conn = psycopg2.connect(database="postgres",
                            user="postgres.iteuczlaiijtvkpplsms",
                            host='aws-0-ap-southeast-1.pooler.supabase.com',
                            password="aUbEUkOgw23zCDdc",
                            port=6543,
                            sslmode='require',
                            keepalives=1,
                            keepalives_idle=30,
                            keepalives_interval=10,
                            keepalives_count=5,
                            )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("SET statement_timeout = 0")
    cur.execute(
        """
        SELECT * FROM cos40005_property 
        WHERE id IS NOT NULL
            AND title IS NOT NULL AND title <> ''
            AND address IS NOT NULL AND address <> ''
            AND price IS NOT NULL AND price <> ''
            AND area IS NOT NULL AND area <> ''
            LIMIT 10;
        """)
    rows = cur.fetchall()
    conn.commit()
    cur.close()
    f = open("./output.csv", "w", encoding="utf-8")
    f.write("id,title,price,is_rent,area,province,district,ward,floor,bedroom,toilet\n")
    for row in rows:
        id = str(row[0])
        title = normalize_vietnamese(str(row[1])).translate(str.maketrans('', '',string.punctuation))
        norm_price = normalise_price(row[3])
        price = str(norm_price["price"])
        is_rent = '1' if norm_price["isRent"] else '0'
        area = str(normalise_area(row[4]))
        norm_addr = normalise_address(row[2], client)
        province = norm_addr["province"]
        district = norm_addr["district"]
        ward = norm_addr["ward"]
        floor = str(normalise_floor(row[5])) if row[5] is not None else '0'
        bedroom = str(row[6]) if row[6] is not None and str(row[6]).isnumeric() else '0'
        toilet = str(row[7]) if row[7] is not None and str(row[7]).isnumeric() else '0'
        if province is not None and district is not None and ward is not None:
            row_data = ','.join([id, title, price, is_rent, area, province, district, ward, floor, bedroom, toilet]) + "\n"
            print(row_data)
            f.write(row_data)
    f.close()
    conn.close()

def clean_data():
    df = pd.DataFrame(pd.read_csv("./output.csv"))
    df_no_duplicates = df.drop_duplicates(subset=df.columns.difference(['id']))
    df_no_duplicates.drop('title', axis=1, inplace=True)
    df_filtered = df_no_duplicates[df_no_duplicates['province'].isin([1, 79])]
    df_filtered = df_filtered[df_filtered['is_rent'] == 0]
    df_filtered.to_csv('./output_cleaned.csv', index=False)


def load_data_address(username, password):
    client = Elasticsearch("https://localhost:9200/", basic_auth=(username, password), ca_certs='./http_ca.crt', verify_certs=False)


    with open('./data_address/tinh_tp.json', 'r', encoding="utf") as file:
        data = json.load(file)

    for i in data:
        data[i]["id"] = i
        data[i]["abbreviation"] = ' '.join([''.join([c.lower()[0] for c in data[i]["name_with_type"].split(' ')]),
                                            ''.join([c.lower()[0] for c in data[i]["name"].split(' ')])])
        resp = client.index(index="tinh_tp", id=i, document=data[i])
        print(resp["result"])

    # %%
    # Load data quan_huyen
    with open('./data_address/quan_huyen.json', 'r', encoding="utf") as file:
        data = json.load(file)

    for i in data:
        data[i]["id"] = i
        data[i]["abbreviation"] = ' '.join(
            [''.join([c.lower()[0] if len(c) > 0 else '' for c in data[i]["name_with_type"].split(' ')]),
             ''.join([c.lower()[0] if len(c) > 0 else '' for c in data[i]["name"].split(' ')])])
        resp = client.index(index="quan_huyen", id=i, document=data[i])
        print(resp["result"])
    # %%
    # Load data xa_phuong
    with open('./data_address/xa_phuong.json', 'r', encoding="utf") as file:
        data = json.load(file)

    for i in data:
        data[i]["id"] = i
        data[i]["abbreviation"] = ' '.join(
            [''.join([c.lower()[0] if len(c) > 0 else '' for c in data[i]["name_with_type"].split(' ')]),
             ''.join([c.lower()[0] if len(c) > 0 else '' for c in data[i]["name"].split(' ')])])
        resp = client.index(index="xa_phuong", id=i, document=data[i])
        print(resp["result"])
    resp = client.search(
        index="tinh_tp",
        query={
            "multi_match": {
                "query": "tphcm",
                "fields": ["parent_code", "name", "slug", "name_with_type", "path_with_type", "abbreviation"]
            }
        },
    )
    resp["hits"]["hits"]


class API(APIView):
    def post(self, request):
        flag = request.data.get('flag')
        username = request.data.get('username')
        password = request.data.get('password')

        if flag == 'normalize':
            create_data(username, password)
            clean_data()
            file_path = './output_cleaned.csv'
            if os.path.exists(file_path):
                return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='output_cleaned.csv')
            else:
                data = {"message": "File not found"}
                return Response(data, status=status.HTTP_404_NOT_FOUND)
        elif flag == 'load':
            load_data_address(username, password)
            data = {"message": "Data loaded"}
        else:
            data = {"message": "Invalid flag"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        return Response(data, status=status.HTTP_200_OK)