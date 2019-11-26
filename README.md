# py-task
Python script to find regex patterns in the given URLs.

## Installation guide

* Download the files in the repository
* Create your project directory
* Create Python virtual environtment in your directory
  * Win: py -3 -m venv venv
  * Linux: python3 -m venv venv
* Actiavate Python venv:
  * Win: venv\Scripts\activate
  * Linux: . venv/bin/activate
* pip install requirements or pip install -r requirements.txt in the venv

## How to run the script

* Provide your URLs and regular expressions for the url respectively (can be found in urls.json)
 - Format: key "urls" has a list of objects.
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
* Scripts output will be saved in results.csv
