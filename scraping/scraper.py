import json
import requests

from bs4 import BeautifulSoup
from utils.country import Country

class Scraper:
    def __init__(self, language="en"):
        self.base_url = f"https://{language}.wikipedia.org/wiki/"

    def get_country_article(self, country_name):
        country_slug = country_name.replace(" ", "_")
        url = self.base_url + country_slug

        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all("p")

            content = "\n".join(p.get_text() for p in paragraphs[:20])
            return {
                "country": country_name,
                "url": url,
                "content": content
            }
        except requests.exceptions.HTTPError:
            return {"error": f"Could not retrieve page for {country_name}", "url": url}
        except Exception as e:
            return {"error": str(e), "url": url}


    def get_country_info(self):
        country = Country()
        countries = country.get_country_list()
        country_list = []
        error_log = []

        for country in countries:
            article_info = self.get_country_article(country['name'])

            if "content" in article_info:
                country_info = {
                    "country": country['name'],
                    "content": article_info['content']
                }
                country_list.append(country_info)
            else:
                msg = f"Error fetching data for {country['name']}: {article_info['error']}"
                print(msg)
                error_log.append(msg)

        try:
            with open('country_list.json', 'w', encoding='utf-8') as f:
                json.dump(country_list, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Failed to write JSON: {e}")

        if error_log:
            with open('scraper_errors.log', 'w', encoding='utf-8') as log_file:
                log_file.write("\n".join(error_log))

        return {
            "success": len(country_list),
            "failed": len(error_log)
        }
    