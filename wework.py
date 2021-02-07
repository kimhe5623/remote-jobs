import requests
from bs4 import BeautifulSoup

def extract_job(html):
  title = html.find("span", {"class":"title"}).get_text(strip=True)
  company = html.find_all("span", {"class": "company"})[0].get_text(strip=True)
  location = html.find("span", {"class": "region"}).get_text(strip=True)
  links = html.find_all("a")
  link = links[0]["href"] if(len(links) == 1) else links[1]["href"]

  return {'title':title, 'company':company, 'location':location, 'link':f"https://weworkremotely.com{link}"}

def extract_jobs(url):
  jobs = []
  print("Scraping weworkremotely page...")
  result = requests.get(f"{url}")
  soup = BeautifulSoup(result.text, "html.parser")
  section = soup.find("section", {"class":"jobs"})
  results = section.find_all("li")

  for idx in range(len(results) - 1):
    job = extract_job(results[idx])
    jobs.append(job)

  return jobs

def get_wework_jobs(word):
  URL = f"https://weworkremotely.com/remote-jobs/search?term={word}"
  jobs = extract_jobs(URL)
  return jobs