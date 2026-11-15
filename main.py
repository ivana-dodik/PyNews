import web_crawler 
import news_parser as np
import news_formatter as nf
from datetime import date
import json
import urllib3
from custom_print import custom_print

# Da ne smara za BN
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Get current date
today = date.today()
# dd/mm/YY
formatted_date = today.strftime("%d.%m.%Y")

#Open sources.json to read all of the sources to be parsed
try:
    with open('settings.json') as json_file:
        config = json.load(json_file)

except Exception as e:
    # Handle any exceptions that occur during the file reading operation
    custom_print("An error occurred while reading the JSON file:", str(e))

finally:
    # Add a finally block to ensure that the file is closed properly
    if 'json_file' in locals() and not json_file.closed:
        json_file.close()

custom_print("============= PyNews " + formatted_date + " =============")
webCrawler = web_crawler.WebCrawler()
webCrawler.getAllRawData()
newsParser = np.NewsParser(config)
newsParser.parse()
newsFormatter1 = nf.NewsFormatter("html")
newsFormatter1.format()
newsFormatter2 = nf.NewsFormatter("text")
newsFormatter2.format()
newsFormatter3 = nf.NewsFormatter("csv")
newsFormatter3.format()
custom_print("==================== Done! ==================")