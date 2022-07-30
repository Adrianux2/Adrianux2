# This macro would receive a CSV with a list of URL that would be test for a 200 response connection.
import pandas as pd
import requests
from alive_progress import alive_bar

ImageCount = 0

data = pd.read_csv("remaining-missing-assets.csv")

urls = data.assets

with alive_bar(len(urls), length=150, spinner='dots_waves') as bar:
    for url in urls:
        try:
            ImageCount = (ImageCount + 1)
            response = requests.get(url, stream=True)
            if response.status_code != 200:
                print(url + " is broken.")

        except requests.exceptions.MissingSchema:
            print("Encountered MissingSchema Exception in " + url)
        except requests.exceptions.InvalidSchema:
            print("Encountered InvalidSchema Exception in " + url)
        except requests.exceptions.Timeout:
            print("Encountered Timeout Exception in " + url)
        except requests.exceptions.ConnectionError:
            print("Encountered Connection Exception in " + url)
        except:
            print("Encountered Some other Exception in " + url)

        bar()

print("Successfully terminated the review")
