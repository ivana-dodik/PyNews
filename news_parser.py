import xml.etree.ElementTree as ET
import feedparser
import json
import requests
import ssl
from bs4 import BeautifulSoup
from custom_print import custom_print

class NewsParser:
    """
    A class for parsing news data from different sources.
    """
    ssl._create_default_https_context = ssl._create_unverified_context

    def __init__(self, config):
        """
        Initialize the NewsParser object.

        Parameters:
        - config (dict): Configuration settings for the parser.

        Returns:
        - None.

        Raises:
        - None.
        """
        #Web crawler will use this date to fetch news
        self.config = config
        custom_print("Initializing parser...")

    def parse(self):
        """
        Parse news from various sources and save them to a JSON file.

        Parameters:
        - None.

        Returns:
        - None.

        Raises:
        - None.
        """
        # Open sources.json to read all of the sources to be parsed
        try:
            with open('sources.json') as json_file:
                sources_data = json.load(json_file)
        except Exception as e:
            custom_print("Error reading sources.json:", str(e))
            sources_data = []

        # Create an array of news logs (dictionaries)
        news = []

        # Loop through raw content files and extract and format data
        for source_record in sources_data:
            source_tag = source_record.get("tag")
            try:
                with open("./temp_files/" + source_tag + ".txt", "r", encoding='utf-8') as f:
                    source_txt = f.read()
            except Exception as e:
                custom_print("Error opening source file:", str(e))
                continue

            # Source-specific parsing
            if source_tag == "rtrs":
                custom_print("Parsing news from " + source_record.get("description"))
                try:
                    # Parsing XML file type
                    tree = ET.parse("./temp_files/" + source_tag + ".txt")
                    root = tree.getroot()
                    # Parsing desired number of news
                    number_of_news = self.config.get("number_of_news_per_source") + 5
                    for index in range(5, number_of_news):
                        news_log = {}
                        for x in root[0][index]:
                            if x.tag != "guid":
                                # Add record to news_log dictionary
                                news_log[x.tag] = x.text
                        # Add news_log dictionary to an array of all news
                        news.append(news_log)
                except Exception as e:
                    custom_print("Error parsing XML:", str(e))

            elif source_tag == "rts" or source_tag == "hrt":
                try:
                    feed = feedparser.parse(source_txt)
                    number_of_news = self.config.get("number_of_news_per_source")
                    limited_entries = feed.entries[:number_of_news]

                    # Access the entries in the feed
                    for entry in limited_entries:
                        news_log = {}
                        news_log["title"] = entry.title
                        news_log["description"] = entry.description
                        news_log["pubDate"] = entry.published
                        news_log["link"] = entry.link

                        news.append(news_log)
                except Exception as e:
                    custom_print("Error parsing feed:", str(e))


            elif source_tag == "bntv":
                custom_print("Parsing news from " + source_record.get("description"))
                try:
                    # Create a BeautifulSoup object to parse the HTML
                    soup = BeautifulSoup(source_txt, 'html.parser')

                    # Find all news articles
                    news_articles = soup.find_all('article', class_='news-article')

                    number_of_news = self.config.get("number_of_news_per_source")
                    news_articles = news_articles[:number_of_news]

                    # Iterate over each news article
                    for article in news_articles:
                        try:
                            news_log = {}
                            # Get the date
                            date = article.find('span', class_='date').text.strip()

                            # Get the link and text
                            link = article.find('a', class_='showNewsDetail')['href']
                            title = article.find('h2').text.strip()
                            description = self._get_description(link)

                            news_log["title"] = title
                            news_log["description"] = description
                            news_log["pubDate"] = date
                            news_log["link"] = link

                            news.append(news_log)
                        except Exception as e:
                            custom_print("Error parsing news article:", str(e))
                except Exception as e:
                    custom_print("Error parsing HTML:", str(e))

    
        # Save all news array to a JSON file
        try:
            custom_print("Creating news.json ...")
            with open("news.json", "w") as f:
                f.write(json.dumps(news, indent=2))
            custom_print("News Parser - done.")
        except Exception as e:
            custom_print("Error saving news to JSON file:", str(e))



    def _get_description(self, link):
        """
        Retrieve the description of a news article from a given link.

        Parameters:
        - link (str): The URL of the news article.

        Returns:
        - description (str): The description of the news article, or "No description available" if not found.

        Raises:
        - None.
        """

        description = "No description available."

        try:
            # Optionally - BEGIN
            article_response = requests.get(link, verify=False)
            # Create a BeautifulSoup object for the article detail page
            article_soup = BeautifulSoup(article_response.text, 'html.parser')
            # Find the news article details
            article_details = article_soup.find('div', class_='news-detail-txt')
            # Get the first paragraph tag from the article details
            article_paragraph = article_details.find('p')
            # Extract the text from the paragraph tag
            if article_paragraph:
                description = article_paragraph.text.strip()
            # Optionally - END
        except Exception as e:
            custom_print("Error retrieving news article description:", str(e))
        finally:
            if article_response:
                article_response.close()

        return description



    