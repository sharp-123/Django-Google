import os
import re
import sys

import requests
from fake_useragent import UserAgent
from googlesearch import search


def store_urls(search_term: str, total_urls: int, platform: str) -> str:
    """Store the urls from Google search results"""
    print("getting urls....")

    try:
        urls = set(search(f"{search_term+' '+platform}", tld="com", num=int(total_urls), stop=10, pause=2))
        print("--------------------------------------------")
        print(urls)
        # with open(fpath, "w", encoding="utf-8") as fn:
        #     for url in urls:
        #         fn.write(url)
        #         fn.write("\n")
        #     print(f"{file_name}_url.txt created!")
        #     return fpath
        return urls

    except Exception as e:
        print(e)


def extract_emails(html_text: str) -> list:
    """Regex to extract email from html text"""

    pattern = r"[\w.+-]+@[\w-]+\.[\w.-]+"
    matches = re.findall(pattern, html_text)
    return matches


def get_emails(url: str, user_agent: UserAgent) -> tuple[list, str]:
    """Download html content from the url and scrapes and returns emails from it"""

    headers = {"User-Agent": f"{user_agent}"}
    emails = []
    try:
        res = requests.get(url, headers=headers, timeout=8)
        if res.status_code == 200:
            html_text = str(res.text)
            emails = extract_emails(html_text)
            return emails, "Successful"

        if res.status_code == 429:  # Too Many Requests
            return emails, "break"

        else:
            return emails, "Unsuccessful"

    except KeyboardInterrupt:
        sys.exit()

    except Exception as e:
        return emails, f"Unsuccessful Error: {e}"


def take_input():
    """Take input from user"""

    print("Enter the search term (comma separated if more than one values): ")
    count = 10
    search_keyword = input("> ")
    search_list = search_keyword.split(",")
    search_list = [s.strip() for s in search_list]
    delay = 1
    if len(search_list) > 1:
        print("Delay between each keyword search (seconds): ")
        delay = int(input("> "))
    print('Delay between each request: (leave empty for no delay)')
    ask_req_delay = input('> ')
    req_delay = None
    if ask_req_delay:
        req_delay = float(ask_req_delay)

    while True:
        try:
            count = int(input("Enter the total number of urls to scrape: "))
            break
        except ValueError:
            print("Please enter a number")
            continue
    return search_list, count, delay, req_delay


def emails_to_file(search_term: str, emails: list) -> None:
    """Create an absolute file path from the search term and dump emails into it"""

    file_name = re.sub(r"\s", "_", search_term)
    output_file_path = os.path.join(os.getcwd(), "output", f"{file_name}_emails.txt")

    with open(output_file_path, "w", encoding="utf-8") as file_write:
        for email in emails:
            file_write.write(email)
            file_write.write("\n")
    print(f"{file_name}_emails.txt Created!")
