import requests
from lxml import html
import csv

base_url = "https://jobs.spurstaffing.com/jobs/show_more"

cookies = {
    '_tt_session': '4f8af4fc8d8862d5303e813d44fc548b',
    '_ttCookiePermissions': 'analytics%2Cmarketing%2Cpreferences',
    '_ttAnalytics': 'Ur2%2Bc9KV6sO9djmDoWngrtfPhRluTXq1XdEudgVSBvEt9P3cfz1wObqnsjg%2FO4Ic%2F8AXP8DPC4eSwSdyWmktCAcM4q1lILAIS7B4mSFI%2BA%3D%3D--yKZT4nMGXqVgmc3K--l9%2Fuk8Q75en1svKXBvH2fA%3D%3D',
}

headers = {
    'accept': 'text/vnd.turbo-stream.html, text/html, application/xhtml+xml',
    'accept-language': 'en-US,en;q=0.9',
    'referer': 'https://jobs.spurstaffing.com/jobs',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'turbo-frame': 'jobs_list',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
}

all_jobs = []

for page in range(1, 7): 
    params = {'page': page}
    resp = requests.get(base_url, headers=headers, cookies=cookies, params=params)
    print(f"Page {page} -> Status: {resp.status_code}")
    if resp.status_code != 200:
        print(f"Stoping due to server Status :{resp.status_code}")
        break 
    if resp.status_code == 200:
        tree = html.fromstring(resp.content)
        location_city = tree.xpath('//div[@class = "mt-1 text-md"]/span[1]/text()')
        location_state = tree.xpath('//div[@class = "mt-1 text-md"]/span[3]/text()')
        titles = tree.xpath('//span[@class = "text-block-base-link sm:min-w-[25%] sm:truncate company-link-style hyphens-auto"]/text()')
        links = tree.xpath('//a[@class = "flex flex-col py-6 text-center sm:px-6 hover:bg-gradient-block-base-bg"]/@href')
        for title_of_job , location_city ,location_state,link in zip(titles, location_city,location_state, links):
            all_jobs.append({
                "title": title_of_job.strip(),
                "location": (location_city + ", " + location_state).strip(),
                "link": link
            })

with open("JobsSpurstaffing.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Title", "location", "link"])
    writer.writeheader()
    writer.writerows(all_jobs)

print(f"Scraping complete! Saved {len(all_jobs)} jobs to JobsSpurstaffing.csv")