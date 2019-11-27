# py-task
Python script to find regex patterns in the given URLs.

## Installation guide

* Download or clone the files in the repository
* Create your project directory
* Set up Python virtual environtment in your directory
  * Win: `py -3 -m venv venv`
  * Linux: `python3 -m venv venv`
* Activate Python venv:
  * Win: `venv\Scripts\activate`
  * Linux: `. venv/bin/activate`
* `pip install requests` since it's the only external dependency or `pip install -r requirements.txt` in the venv


## Running the script

* Provide your URLs and regular expressions for the url respectively (example can be found in urls.json)
  	* Format: key "urls" has a list of objects. You can put one regular expression in the "regex" list or multiple
   ```
   {
     "urls": [
       {
        "url": ...,
        "regex": 
          [
            ...
          ]
      },
      { 
       etc...
      }
    ]
  }
  ```
  
* Run script `python task.py`
* Script will run continuously checking URLs after certain period (can be changed on line 76 of task.py, interval argument, set 5 sec for now)
* Scripts output will be saved in results.csv
  * CSV headers: url, result, timestamp, duration, error
  * If the check was successful the result column contains semicolon separated string of the found matches, otherwise it will be left empty
  * In case something went wrong, there is a error message in the error column
