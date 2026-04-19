import json
import requests
while True:
    url = 'https://api.exchangerate.host/latest'
    result =requests.get(url)
    result = json.loads(result.text)
    ed= result['rates']
    euro_birim = ed["EUR"]
    try_birim = ed["TRY"]
    dolar_birim= ed["USD"]
    print("TRY/euro birim:")
    print(try_birim/euro_birim)
    print("try/dolar birim :")
    print(try_birim/dolar_birim)
    bozulan_doviz = input("bozulan_doviz türü: ")
    #alinan_doviz = input("alinan_doviz türü: ")
    edi= result['rates'][bozulan_doviz]    
    miktar = input(f' Kur : 1 {bozulan_doviz} : {edi*try_birim} TRY dir.\nNe kadar bozdurmak istiyorsun. :')
    sonuc = float(miktar)*float(edi)*float(try_birim)
    print(f"{sonuc} TRY eder.")
    print('bitt'.center(50,'-'))
