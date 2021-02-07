import requests
import json
from so import get_so_jobs
from wework import get_wework_jobs
from remoteok import get_remoteok_jobs

SO = "so"
WEWORD = "weword"
REMOTEOK = "remoteok"

def getData(word):
  return filterData(SO, word) + filterData(WEWORD, word) + filterData(REMOTEOK, word)

def setData(dbName, key, data):
  db = getDB(dbName)
  db[key] = data
  setDB(dbName, db)

def filterData(dbName, word):
  # try:
  db = getDB(dbName)
  data = db.get(word)
  if(data == None):
    if(dbName == SO):
      data = get_so_jobs(word)
    elif(dbName == WEWORD):
      data = get_wework_jobs(word)
    elif(dbName == REMOTEOK):
      data = get_remoteok_jobs(word)
    setData(dbName, word, data)
  return data
  # except:
  #   print("filter Data error")
  #   return []

def getDB(dbName):
  try:
    f = open(f"./db/{dbName}.json")
    data = json.load(f)
    return data
  except IOError:
    setDB(dbName, {})
    return {}

def setDB(dbName, data):
  with open(f"./db/{dbName}.json", "w+") as outfile:
    json.dump(data, outfile)