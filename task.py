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


def save_results(url, result, duration):
    with open("results.csv", "a+") as results:
        results_writer = csv.writer(results, delimiter=",", lineterminator="\n")
        timestamp = str(datetime.datetime.now()).split(".")[0]
        results_writer.writerow([url, result, timestamp, duration])


def download_site(url, session):
    try:
        with session.get(url) as response:
            return response.content.decode("utf-8")
    except requests.exceptions.ConnectionError:
        return "Not found"
    except requests.exceptions.HTTPError as http_error:
        print(http_error)


def analyze_sites(data):
    with requests.Session() as session:
        for resource in data["urls"]:
            start_time = time.time()
            url = resource["url"]
            site_content = download_site(url, session)
            if site_content == "Not found":
                duration = time.time() - start_time
                save_results(url, site_content, duration)
            else:
                regex_patterns = resource["regex"]
                if not isinstance(regex_patterns, list):
                    duration = time.time() - start_time
                    save_results(url, "Incorrect regex input", duration)
                else:
                    for i in range(len(regex_patterns)):
                        result = find_patterns(site_content, regex_patterns[i])
                        duration = time.time() - start_time
                        save_results(url, result, duration)


def get_urls():
    try:
        with open("urls.json", "r") as urls:
            return json.load(urls)
    except FileNotFoundError as fnf_error:
        print(fnf_error)


def signal_handler(signum, frame):
    raise ProgramKilled


resource_objects = get_urls()
signal.signal(signal.SIGTERM, signal_handler)
# Intercept SIGINT signal when CTRL+C is pressed
signal.signal(signal.SIGINT, signal_handler)
job = Job(interval=timedelta(seconds=60), execute=analyze_sites(resource_objects))
job.start()

while True:
    try:
        time.sleep(1)
    except ProgramKilled:
        print("Killing program")
        job.stop()
        break
