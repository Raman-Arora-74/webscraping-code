from lxml import html
import requests 
import asyncio
from export import * 
import httpx 
semaphore = asyncio.Semaphore(6)
csvFileName = "aequor.csv"

import requests
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'If-None-Match': 'W/"82a64-0P7xoS4Qofa+WKBIKbWP1I53G9s-gzip"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    'discipline-group': 'Education',
}
source = requests.Session()
source.headers.update(headers)
response = source.get("https://work.aequor.com/browse-jobs?discipline-group=Education&within=50&jobAlertsName=My%20saved%20alert&job-alert-frequency=01")
print(f"Status Code: {response.status_code}")

open("aeqour.html", "w",encoding="utf-8").write(response.text)
tree = html.fromstring(response.text)
lastPage = tree.xpath('//a[@class = "page-link"]')
total_pages = int(lastPage[-1].text_content().strip())

baseUrl = "https://work.aequor.com/browse-jobs?discipline-group=Education&within=50&jobAlertsName=My%20saved%20alert&job-alert-frequency=01"

async def fetch_page(client, page, retries = 10):
    url = f"{baseUrl}&page{page}"
    for attempt in range(1, retries + 1):
        try:
            print(f"Fetching page {page}...{url}")
            response = await client.get(url)
            tree = html.fromstring(response.text)
            urls = tree.xpath('//p[@class = "job-search__jobs-list__job-name single-row"]')
            print(f"Fetched page {page} with {len(urls)} jobs")
            return urls
        except Exception as e:
            print(f"Attempt {attempt} failed to fetch page {page}: {e}")
            await asyncio.sleep(1) 
    print(f"❌ Failed to fetch page {page} after {retries} attempts.")
    return []

JOB_URLS = []

async def fetch_job_details(client, job_url):
    for attempt in range(1, 6):
        try:
            resp = await client.get(job_url, timeout=10)
            print(f"Fetching job details from {job_url} - Status Code: {resp.status_code}")
            tree = html.fromstring(resp.text)
            data  = {
                "title": tree.xpath('//p[@class = "job-search__jobs-list__job-name single-row"]/a/text()'),
                "salary": tree.xpath('//*[@id="jobs-list__list"]/li/div[2]/div[2]/div[2]/text()'),
                "location":tree.xpath('//*[@id="jobs-list__list"]/li/div[2]/div[2]/div[1]/text()'),
                "duration": tree.xpath('//*[@id="jobs-list__list"]/li/div[2]/div[2]/div[3]/text()'),
                "joburl": job_url
            }

            return data
        except Exception as e:
            print(f"Attempt {attempt} failed to fetch job details from {job_url}: {e}")
            await asyncio.sleep(1)

async def fetch_and_save_job(client, job_url):
    job_data = await fetch_job_details(client, job_url)  
    
    if job_data:
        append_to_csv([job_data], csvFileName)  
        append_url_to_log(job_url)  
        print(f"Saved job: {job_data['JobTitle']}")

async def fetch_and_save_job_limited(client, job_url):
    async with semaphore:
        return await fetch_and_save_job(client, job_url)
    
async def fetch_page_limited(client, page):
    async with semaphore:
        return await fetch_page(client, page)
async def main():
    print(f"Total pages: {total_pages}")
    
    async with httpx.AsyncClient(headers=headers) as client:
        tasks = [fetch_page_limited(client, page) for page in range(1, total_pages + 1)]
        results = await asyncio.gather(*tasks)

    JobURLS = [url for sublist in results for url in sublist]
   
    JobURLS = list(set(JobURLS) - set(read_log_file('log.txt')))
    print(f"{len(JobURLS)} new job URLs to scrape (excluding already scraped)")
    print(f"Collected {len(JobURLS)} job URLs")

    async with httpx.AsyncClient(headers=headers) as client:
        tasks = [fetch_and_save_job_limited(client, url) for url in JobURLS]
        results = await asyncio.gather(*tasks)

    jobs_data = [job for job in results if job]

    print(f"Scraped {len(jobs_data)} job details")
    if jobs_data:
        print(jobs_data[0])


asyncio.run(main())




    