import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from bs4.element import Comment
import json
import traceback


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    found = []
    try:
        if resp.status != 200:
            print(resp.error)
            return []
        # Parse html response
        soup = BeautifulSoup(resp.raw_response.content, "html.parser")

        # Text data in response
        all_texts = soup.get_text()

        # Save data to json file
        # Try to load previous json file if exists
        try:
            with open("url_responses.json", "r") as outfile:
                data = json.load(outfile)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = {}
        # update dictionary with new url data
        data[url] = all_texts
        if url != resp.url:
            data[resp.url] = ""
        # write back to json file
        with open("url_responses.json", "w") as outfile:
            json.dump(data, outfile, indent=4)

        # Get links in response
        for anchor in soup.find_all("a"):
            try:
                found.append(anchor['href'])
            except KeyError:
                pass

    except FileNotFoundError as e:
        print(f"Error: File {e} not found")
    except UnicodeDecodeError as e:
        print(f"Error: File {e} contains invalid characters")
    except Exception as e:
        print(f"ERROR: {e}")
        traceback.print_exc()
        return []
    print(f"Found {len(found)} links")
    return found


def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False

        # Check if url has already been scraped
        with open("url_responses.json", 'r') as json_file:
            data = json.load(json_file)
            keys = data.keys()
            if url in keys:
                return False

        # Check if in valid domain
        if not re.match(r"ics\.uci\.edu|\.cs\.uci\.edu|informatics\.uci\.edu|stat\.uci\.edu",
                        parsed.hostname):
            return False
        # today.uci.edu/department/information_computer_sciences/ formatting
        if parsed.hostname == "today.uci.edu" and parsed.path.startswith("/department/information_computer_sciences"):
            return True

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print("TypeError for ", parsed)
        raise


if __name__ == "__main__":
    print(is_valid(input()))
