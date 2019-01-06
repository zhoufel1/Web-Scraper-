import requests
from bs4 import BeautifulSoup


def web_scraper(pages: int):
    f = open('data/titles.csv', 'w')
    page = 0
    # For testing
    print("writing to file...")
    while page < pages:
        # Initialize the request to the page, and retrieve the html.
        url = "https://www.policeauctionscanada.com/Browse?page=" + str(page)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Gathers the information of all items on one page.
        items = soup.findAll("section")
        # Writes the information from one page onto data file in CSV format.
        for item in items:
            write_title(item, f)
            write_price(item, f)
            write_current_bids(item, f)
            f.write('\n')
        page += 1
    f.close()
    # For testing
    print("done!")


# Helper function to retrieve the id of a specific item
def get_id(title: str):
    return title[-8:-1]


def write_title(item, file):
    if ',' in item.h1.text:
        file.write(get_id(item.h1.text.strip()) + ',')
        file.write(item.h1.text.strip()[:-10] + ',')
    else:
        file.write(get_id(item.h1.text.strip()) + ',')
        file.write(item.h1.text.strip()[:-10] + ',' + ',')


def write_price(item, file):
    file.write(item.find('span', {'class': 'awe-rt-CurrentPrice price'}).text + ',')


def write_current_bids(item, file):
    file.write(item.find('span', {'class': 'awe-rt-AcceptedListingActionCount'}).text.strip() + ' Bids')


if __name__ == '__main__':
    web_scraper(3)
