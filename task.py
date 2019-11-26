import csv
import datetime
import re
import signal
import time
from datetime import timedelta
import requests
import json

from job import Job
from stop_program import ProgramKilled


def find_patterns(content, pattern):
    if content is not None:
        if len(pattern) > 1:
            for i in range(len(pattern)):
                matches = re.findall(pattern[i], content)
                if matches:
                    return ";".join(matches)
                return "No match"
        match = ";".join(re.findall(pattern[0], content))
        if not match:
            return "No match"
        return match
    else:
        return "No such URL"


def save_results(url, result):
    with open("results.csv", "a") as results:
        results_writer = csv.writer(results, delimiter=",", lineterminator="\n")
        timestamp = str(datetime.datetime.now()).split(".")[0]
        error = ""
        if result == "No such URL":
            error = result
            result = "No match"
        results_writer.writerow([url, result, timestamp, "1", error])


def download_site(url, session):
    try:
        with session.get(url) as response:
            return response.content.decode("utf-8")
    except requests.exceptions.ConnectionError as connection_error:
        print(connection_error)
    except requests.exceptions.HTTPError as http_error:
        print(http_error)


def analyze_sites(data):
    with requests.Session() as session:
        for resource in data["urls"]:
            site_content = download_site(resource["url"], session)
            regex_patterns = resource["regex"]
            result = find_patterns(site_content, regex_patterns)
            save_results(resource["url"], result)


def get_urls():
    with open("urls.json", "r") as urls:
        return json.load(urls)


def signal_handler(signum, frame):
    raise ProgramKilled


resource_objects = get_urls()
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)
job = Job(interval=timedelta(seconds=10), execute=analyze_sites(resource_objects))
job.start()

while True:
    try:
        time.sleep(1)
    except ProgramKilled:
        print("Killing program")
        job.stop()
        break

