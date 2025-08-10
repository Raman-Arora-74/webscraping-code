import requests
from bs4 import BeautifulSoup
import csv
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
}
urls = []
titles = []
summarys = []
locations = []
csv_file = open("csv_file.csv","w",newline ="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Job Title","Job URL","Job Location","Pay rate discription"])
for page in range(1,9):
    url = "https://staffez.org/job-search/"
    response = requests.get(url).text
    soup = BeautifulSoup(response,"lxml")
    link = soup.find("div",class_="bh-job-list")
    job_url= link.find_all("div","job-result")
    for job in job_url:
        job_link = job.find("h2").find("a")["href"]
        urls.append(job_link)
        for job in job_url :
            title = (job.find("h2").find("a").text)
            titles.append(title)
    job_summery = link.find_all("div",class_="job-result-teaser")
    for discription in job_summery:
        for p in discription.find_all("p"):
            text = p.get_text(strip=True)
            if text:
                summarys.append(text)
    job_location = link.find_all("div","job-result-customer")
    for location in job_location:
        job_loc = location.p.text
        locations.append(job_loc)
    url = url+f"?sf_paged={page+1}"
print(urls)
print(titles)
for title,url,location,summary in zip(titles,urls,locations,summarys):
    csv_writer.writerow([title,url,location,summary])

    
        
