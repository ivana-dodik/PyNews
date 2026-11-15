import json
import urllib.request
import ssl
from custom_print import custom_print


class WebCrawler:

    ssl._create_default_https_context = ssl._create_unverified_context
    """
    This class encapsulates data and functionalities for fetching raw
    data from the internet.
    """
    def __init__(self):
        """
        Construct a new WebCrawler object.

        :return: no return value
        """
        custom_print("Initializing Web Crawler...")

    def getAllRawData(self):
        """
        Get raw content from the internet and store data from sources into
        separate files.

        :return: no return value
        """
        try:
            # Open sources.json to read all of the sources to be parsed
            with open('sources.json') as json_file:
                sources_data = json.load(json_file)
                custom_print("Parsing sources...")
            
            # Loop through all sources and store raw data to separate files.
            for source_record in sources_data:
                custom_print("Parsing source: " + source_record.get("tag") + " ...")
                file = urllib.request.urlopen(source_record.get("address"))
                content_bytes = file.read()
                content_txt = content_bytes.decode("utf8")
                file.close()
                
                # Write content to a temp file
                custom_print("Writing fetched content to file...")
                f = open("./temp_files/" + source_record.get("tag") + ".txt", "w", encoding='utf-8')
                f.write(content_txt)
                f.close()
            
            custom_print("Web Crawler - done.")
        finally:
            # Ensure that the file is closed even if an exception occurs
            if 'f' in locals() and not f.closed:
                f.close()

