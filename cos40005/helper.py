from cffi.backend_ctypes import unicode
import re

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
        for j in range(1, 12):
            if addr[i].__contains__('quan ' + str(j)):
                addr[i] = 'quan ' + str(j)
                is_hcm_ward = True

        if not is_hcm_ward:
            for level in prefixes:
                for prefix in prefixes[level]:
                    addr[i] = addr[i].removeprefix(prefix).strip()


    if len(addr)-1 >= 0:
        res['province'] = addr[len(addr)-1]
    if len(addr)-2 >= 0:
        res['district'] = addr[len(addr)-2]
    if len(addr)-3 >= 0:
        res['ward'] = addr[len(addr)-3]
    if len(addr)-4 >= 0:
        res['street'] = addr[len(addr)-4]
    return res

print(normalise_address("Đường 3 Tháng 2, Phường 12, Quận 10, TPHCM"))

