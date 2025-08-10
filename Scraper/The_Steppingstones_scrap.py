from bs4 import BeautifulSoup
import csv
import requests

headers = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    'page': '187',
}

response = requests.get('https://jobs.thesteppingstonesgroup.com/jobs', params=params, headers=headers)
"""web scriping of job website to grab the information about heading """


#List use in code

url_list = []
income_list = []
heading_list = []
venue_list = []
category_list = []
summery_list = []

# Url collector 

def url_finder(url,link_list):
    response = requests.get(url)
    source = BeautifulSoup(response.text,"lxml")
    web_col = source.find_all("div",class_="col-md-6 col-12")
    for col in web_col:
         a_tag = col.find("a")
         if a_tag and a_tag.get("href"):
            link_list.append(a_tag["href"])

# text finder from website for income

def text_finder_income(url,income_list):

    response = requests.get(url)
    source = BeautifulSoup(response.text,"lxml")
    web_col = source.find_all("div",class_="col-md-6 col-12")
    for col in web_col:
        job_box = col.find("div", class_="job-box")
        if job_box:
                job_text_div = job_box.find("div", class_="job-text")
                if job_text_div.get_text(strip=True) == 'Media,Pennsylvania,USA':
                    income_list.append("No Data Given")
                else:
                    income_list.append(job_text_div.get_text(strip=True))

# Heading finder from website for heading

def text_finder_heading(url,heading_list):
    response = requests.get(url)
    source = BeautifulSoup(response.text,"lxml")
    web_col = source.find_all("div",class_="col-md-6 col-12")
    for col in web_col:
         a_tag = col.find("a")
         if a_tag:
             heading_list.append(a_tag.get_text(strip=True))

# this function made for scrap the summery 

def text_finder_summery(url,summery_list):
    response = requests.get(url)
    source = BeautifulSoup(response.text,"lxml")
    summery_data = source.find_all("div",class_="fade-text")
    for summery in summery_data:
        if summery:
            summery_list.append(summery.get_text(strip=True))

#Making a csv file 

csv_file = open("Jobs.csv","w",newline = "",encoding="utf-8")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Job Name","Job URL","Job Pay rate","Job summery"])

#final result of scraping 

for i in range(1,51):
    url = "https://jobs.thesteppingstonesgroup.com/jobs"
    text_finder_heading(url,heading_list)
    text_finder_income(url,income_list)
    text_finder_summery(url,summery_list)
    url_finder(url,url_list)
    url = url+f"?page={i+1}"


for name,url,pay,summery in zip(heading_list,url_list,income_list,summery_list):
    csv_writer.writerow([name,url,pay,summery])  
status = response.status_code
print(status) 
