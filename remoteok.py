import requests, re
from bs4 import BeautifulSoup

USER_AGENT_VALUE = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36"

def extract_job(html):
  if(html.find("span", {"class": "closed"})):
    return
  title = html.find("h2", {"itemprop":"title"}).get_text(strip=True)
  company = html.find("h3", {"itemprop": "name"}).get_text(strip=True)
  locationBox = html.find("div", {"class": "location tooltip"})
  location = locationBox.get_text(strip=True) if locationBox else ""
  linkBox = html.find("td", {"class", "source"})
  linkBox = linkBox.find("a")
  link = linkBox["href"] if linkBox else ""

  return {'title':title, 'company':company, 'location':location, 'link': link if("mailto" in link) else f"https://remoteok.io{link}"}

def extract_jobs(url):
  jobs = []
  headers = {'User-Agent': USER_AGENT_VALUE}
  result = requests.get(url, headers=headers)
  soup = BeautifulSoup(result.text, "html.parser")
  table = soup.find("table", {"id": "jobsboard"})
  results = table.find_all("tr", {"class":"job"})

  for result in results:
    job = extract_job(result)
    if(job):
      jobs.append(job)

  return jobs

def get_remoteok_jobs(word):
  words = re.split('[-()\"#/@;:<>{}`+=~|!?]',word)
  jobs = []
  for w in words:
    print(f"Scraping remoteok page by {w}...")
    URL = f"https://remoteok.io/remote-dev+{w}-jobs"
    jobs += extract_jobs(URL)
  return jobs