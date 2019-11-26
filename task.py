import csv
import datetime
import json
import re
import signal
import time
from datetime import timedelta

import requests

from job import Job
from stop_program import ProgramKilled


def find_patterns(content, pattern):
    match = re.findall(pattern, content)
    if not match:
        return "No match"
    return ";".join(match)


def save_results(url, duration, error="", result=""):
    with open("results.csv", "a+") as results:
        results_writer = csv.writer(results, delimiter=",", lineterminator="\n")
        timestamp = str(datetime.datetime.now()).split(".")[0]
        results_writer.writerow([url, result, timestamp, duration, error])


def download_site(url, session):
    try:
        with session.get(url) as response:
            return response.content.decode("utf-8")
    except requests.exceptions.ConnectionError:
        return "URL Not found"
    except requests.exceptions.HTTPError as http_error:
        print(http_error)


def analyze_sites(data):
    with requests.Session() as session:
        for resource in data["urls"]:
            start_time = time.time()
            url = resource["url"]
            site_content = download_site(url, session)
            if site_content == "URL Not found":
                error = site_content
                duration = time.time() - start_time            
                save_results(url, duration, error)
            else:
                regex_patterns = resource["regex"]
                for pattern in regex_patterns:
                    result = find_patterns(site_content, pattern)
                    duration = time.time() - start_time
                    save_results(url, duration, result=result)
            

def get_matches():
    try:
        with open("urs.json", "r") as urls:
            analyze_sites(json.load(urls))
    except FileNotFoundError as fnf_error:
        return fnf_error


def signal_handler(signum, frame):
    raise ProgramKilled


signal.signal(signal.SIGTERM, signal_handler)
# Intercept SIGINT signal when CTRL+C is pressed
signal.signal(signal.SIGINT, signal_handler)
job = Job(interval=timedelta(seconds=5), execute=get_matches)
job.start()

while True:
    try:
        time.sleep(1)
    except ProgramKilled:
        print("Killing program")
        job.stop()
        break
