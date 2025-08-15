import requests 
import requests

cookies = {
    '_ga': 'GA1.1.630444198.1755266525',
    '_ga_JJ7G51SZ42': 'GS2.1.s1755266525$o1$g1$t1755266605$j60$l0$h0',
    '_ga_VM62FXQ912': 'GS2.1.s1755266526$o1$g1$t1755266605$j60$l0$h0',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'referer': 'https://bdgwin.one/',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',

}

response = requests.get('https://bdgby.com/', cookies=cookies, headers=headers)

print(f"Status : {response.status_code}")