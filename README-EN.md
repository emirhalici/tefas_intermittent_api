# tefas_intermittent_api

> Türkçe versiyonu için [README](README.md)'a gidin.

Pulls basic fund info from TEFAS periodically using Github Workflow Actions. This is done via a Python script by scraping the specific TEFAS page for each fund.

# How to Use

[scraper.yml](.github/workflows/scraper.yml) action has been set to run every day at 12PM Türkiye time. Each fund with code defined inside `INPUTS` variable is automatically fetched through [scraper.py](scraper.py) and written/committed to `data` branch on the workflow action. At any point, you can read the data in json or csv format. 

See the [file](https://raw.githubusercontent.com/emirhalici/tefas_intermittent_api/data/fund_data.csv) in CSV format.

See the [file](https://raw.githubusercontent.com/emirhalici/tefas_intermittent_api/data/fund_data.json) in JSON format.


# How to Customize

To change fund codes defined in the script, you must clone/fork the project.

### 1. Clone project

### 2. Modify script

Adjust `INPUTS` variable by adding/removing other fund codes based on your preference. 

> Warning: Too many fund codes may result in hitting the rate limit and unreliable results.

### 2. Modify Workflow Action

To commit file changes after each run workflow action requires commit permissions. Create a token called `GH_TOKEN` in repository settings and give it permission for the repository.
