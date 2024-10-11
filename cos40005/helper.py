from cffi.backend_ctypes import unicode
import re
from elasticsearch import Elasticsearch
ES_USER = "elastic"
ES_PASS = "_YnyYSU1F5mv9esOU70a"
client = Elasticsearch("https://localhost:9200/", basic_auth=(ES_USER, ES_PASS), ca_certs="./http_ca.crt")

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

def search(index, query):
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

def normalise_address(addr):
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
        search_res = search("tinh_tp", raw)
        if len(search_res) > 0:
            res['province'] = search_res[0]["_source"]["id"]
    if len(addr)-2 >= 0:
        raw = addr[len(addr)-2] + ', ' + addr[len(addr)-1]
        search_res = search("quan_huyen", raw)
        for r in search_res:
            if r["_source"]["parent_code"] == res['province']:
                res['district'] = r["_source"]["id"]
                break
    if len(addr)-3 >= 0:
        raw = addr[len(addr)-3] + ', ' + addr[len(addr)-2] + ', ' + addr[len(addr)-1]
        search_res = search("xa_phuong", raw)
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
    if area_str[0].isnumeric():
        res = float(area_str[0])
    return res

import psycopg2
def create_data():
    conn = psycopg2.connect(database="postgres",
                            user="postgres.iteuczlaiijtvkpplsms",
                            host='aws-0-ap-southeast-1.pooler.supabase.com',
                            password="aUbEUkOgw23zCDdc",
                            port=6543)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM cos40005_property 
        WHERE id IS NOT NULL
            AND title IS NOT NULL AND title <> ''
            AND address IS NOT NULL AND address <> ''
            AND price IS NOT NULL AND price <> ''
            AND area IS NOT NULL AND area <> '';
        """)
    rows = cur.fetchall()
    conn.commit()
    cur.close()
    f = open("./output.csv", "w")
    f.write("id,price,is_rent,area,province,district,ward,floor,bedroom,toilet\n")
    for row in rows:
        id = str(row[0])
        norm_price = normalise_price(row[3])
        price = str(norm_price["price"])
        is_rent = '1' if norm_price["isRent"] else '0'
        area = str(normalise_area(row[4]))
        norm_addr = normalise_address(row[2])
        province = norm_addr["province"]
        district = norm_addr["district"]
        ward = norm_addr["ward"]
        floor = str(row[5]) if row[5] is not None else '0'
        bedroom = str(row[6]) if row[6] is not None else '0'
        toilet = str(row[7]) if row[7] is not None else '0'
        if province is not None and district is not None and ward is not None:
            row_data = ','.join([id, price, is_rent, area, province, district, ward, floor, bedroom, toilet]) + "\n"
            print(row_data)
            f.write(row_data)
    f.close()
    conn.close()

create_data()

__all__ = ['normalise_price', 'normalise_address', 'normalise_area']


