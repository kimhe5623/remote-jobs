"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""
from flask import Flask, render_template, request, redirect, send_file
from exporter import save_to_file
from dataService import getData
import re, os

app = Flask("JobScrapper")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/report")
def report():
    word = request.args.get("word")
    if word:
        word = word.lower()
        jobs = getData(word)
    else:
        return redirect("/")
    return render_template(
        "report.html", resultNumber=len(jobs), searchingBy=word, jobs=jobs)

@app.route("/export")
def export():
  try:
    word = request.args.get("word")
    if not word:
      raise Exception()

    word = word.lower()
    jobs = getData(word)
    if not jobs:
      raise Exception()
    print("OK")
    word = re.sub(r'[-()\"#/@;:<>{}`+=~|.!?,]', "_", word)
    print(word)
    
    if not os.path.isfile("files/{word}_jobs.csv"):
      save_to_file(word, jobs)
      
    return send_file(
      f"files/{word}_jobs.csv",
      as_attachment=True,
      attachment_filename=f"{word}_jobs.csv"
      )

  except:
    return redirect("/")

app.run(host="0.0.0.0")


