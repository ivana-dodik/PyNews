import json
import csv
from dateutil import parser
import datetime
from custom_print import custom_print

class NewsFormatter:
    """
    A class for formatting news data into different formats.
    """

    def __init__(self, type):
        """
        Initialize the NewsFormatter object.

        Args:
            type (str): The format type to generate (html, text, csv).
        """

        self.type = type
        custom_print("Initializing News Formatter...")


    def format(self):
        """
        Format news data based on the specified type.
        """

        # Formatting news as HTML or text
        if (self.type == "html"):
            self.format_html()
        elif (self.type == "text"):
            self.format_text()
        elif (self.type == "csv"):
            self.format_csv()
        else:
            custom_print("Unsupported format.")

    def format_html(self):
        """
        Format news data as an HTML file.
        """        
        try:
            with open('news.json') as json_file:
                try:
                    news_json = json.load(json_file)
                except json.JSONDecodeError as e:
                    custom_print("Error decoding JSON file:", str(e))
                    return
                #Generate html file
                html_head = """
                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                        <title>PyNews</title>
                        <meta charset="utf-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
                        <script src="https://cdn.jsdelivr.net/npm/jquery@3.6.3/dist/jquery.slim.min.js"></script>
                        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"></script>
                        <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js"></script>
                        </head>
                        <body>
                        <nav class="navbar navbar-expand-sm bg-dark navbar-dark">
                        <!-- Brand/logo -->
                        <a class="navbar-brand" href="#">PyNews - Vijesti koje su Vama važne</a>
                        </nav>
                        <div class="container-fluid" style="width=100%">
                    """

                html_news_cards = ""
                #Generate cards from JSON news file
                for news_log in news_json:
                    html_card = """
                    <br>
                    <div class="card card-default" style="width: 100%;">
                    <div class="card-body">
                    """
                    html_card += '<h5 class="card-title">'+ news_log.get("title") +'</h5>'
                    html_card += '<h6 class="card-subtitle mb-2 text-muted"><h6>'+ news_log.get("pubDate") +'</h6>'
                    html_card += '<p class="card-text">'+ news_log.get("description") +'</p>'
                    html_card += ''
                    html_card += '</div><div class="card-body"><br><a href="'+ news_log.get("link") +'" class="btn btn-primary">Otvori članak</a></div></div><br>'
                    html_news_cards += html_card

                html_tail = """
                    </div>
                    </body>
                    </html>
                """
                
                #Write html content to a html file
                custom_print("Generating HTML file...")
                try:
                    with open("./output/index.html", "w", encoding='utf-8') as f:
                        f.write(html_head + html_news_cards + html_tail)
                    custom_print("HTML file generation completed.")
                except IOError as e:
                    custom_print("Error writing HTML file:", str(e))
        except IOError as e:
            custom_print("Error opening JSON file:", str(e))

    def format_text(self):
        """
        Format news data as a text file.
        """
        try:
            # Open news JSON file
            with open('news.json') as json_file:
                try:
                    news_json = json.load(json_file)
                except json.JSONDecodeError as e:
                    custom_print("Error decoding JSON file:", str(e))
                    return
            
            # Generate text file
            text_content = ""
            for news_log in news_json:
                text_content += "----------------------------------------------------------\n"
                text_content += "----------------------------------------------------------\n"
                text_content += news_log.get("title") + "\n"
                text_content += "----------------------------------------------------------\n"
                text_content += "----------------------------------------------------------\n"
                text_content += self._format_date(news_log.get("pubDate")) + "\n"
                text_content += "----------------------------------------------------------\n"
                text_content += "----------------------------------------------------------\n"
                text_content += news_log.get("description") + "\n"
                text_content += "----------------------------------------------------------\n"
                text_content += "----------------------------------------------------------\n"
                text_content += news_log.get("link") + "\n"
                text_content += "----------------------------------------------------------\n"
                text_content += "----------------------------------------------------------\n\n"
            
            # Write text content to a text file
            custom_print("Generating text file...")
            try:
                with open("./output/news.txt", "w", encoding="utf-8") as file:
                    file.write(text_content)
                custom_print("Text file generation completed.")
            except IOError as e:
                custom_print("Error writing text file:", str(e))
        except IOError as e:
            custom_print("Error opening JSON file:", str(e))
        finally:
            custom_print("News Formatter - done.")



    def format_csv(self):
        """
        Format news data as a CSV file.
        """

        try:
            # Open news JSON file
            with open('news.json') as json_file:
                try:
                    news_json = json.load(json_file)
                except json.JSONDecodeError as e:
                    print("Error decoding JSON file:", str(e))
                    return
            
            # Generate CSV file
            print("Generating CSV file...")
            csv_file = "./output/news.csv"
            try:
                with open(csv_file, "w", encoding="utf-8", newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["title", "description", "link", "date"])  # Header row
                    for news_log in news_json:
                        title = news_log.get("title")
                        description = news_log.get("description")
                        link = news_log.get("link")
                        date = news_log.get("pubDate")
                        writer.writerow([title, description, link, date])
                print("CSV file generation completed.")
            except IOError as e:
                print("Error writing CSV file:", str(e))
        except IOError as e:
            print("Error opening JSON file:", str(e))
        finally:
            print("News Formatter - done.")
    
    def _format_date(self, date_string):
        """
        Format date according to specification.

        Parameters:
        - date_string (str): The original date string to be formatted.

        Returns:
        - formatted_date_string (str): The formatted date string in the desired format '%d.%m.%Y %H:%M:%S',
                                    or the original date string if the format is unknown.

        Raises:
        - None.

        Example:
            formatter = NewsFormatter('html')
            date_string = 'Mon, 22 May 2023 14:49:14 +0200'
            formatted_date = formatter._format_date(date_string)
            print(formatted_date)
            # Output: '22.05.2023 14:49:14'
        """

        desired_date_format = '%d.%m.%Y %H:%M:%S'

        # Parse the original date string
        try:
            parsed_date = parser.parse(date_string)

            # Format the parsed date into the desired format
            formatted_date_string = parsed_date.strftime(desired_date_format)
            return formatted_date_string
        except parser.ParserError:
            custom_print("Unknown date format:" + date_string)
            return date_string