import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urlparse, urljoin

# Set the starting URL
base_url = 'https://www.pipasha-restaurant.co.uk'

# Initialize the set of visited URLs and add the base URL
visited_urls = set()
visited_urls.add(base_url)

# Initialize the set of URLs to be visited and add the base URL
urls_to_visit = set()
urls_to_visit.add(base_url)

# Parse the base URL to get the domain name
base_domain = urlparse(base_url).netloc

# Initialize the CSV writer
csv_file = open('links.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
# Loop through the URLs to be visited
while urls_to_visit:

    # Get the next URL from the set of URLs to be visited
    current_url = urls_to_visit.pop()

    try:
        # Make a GET request to the URL
        response = requests.get(current_url)

        # Check if the response was successful (status code 200)
        if response.status_code == 200:

            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all the links on the page
            for link in soup.find_all('a'):

                # Get the URL from the link
                link_url = link.get('href')

                # Make sure the link URL is not None and is not an empty string
                if link_url is not None and link_url != '':
                    print(link_url)
                    # Normalize the link URL by joining it with the base URL
                    link_url = urljoin(current_url, link_url)

                    # Parse the domain name from the link URL
                    link_domain = urlparse(link_url).netloc

                    # Check if the link domain matches the base domain
                    if link_domain == base_domain:

                        # Add the link URL to the set of URLs to be visited if it hasn't been visited yet
                        if link_url not in visited_urls:
                            urls_to_visit.add(link_url)

                        # Add the link URL to the set of visited URLs
                        visited_urls.add(link_url)

                        # Write the link URL to the CSV file
                        csv_writer.writerow([link_url])

        # Print an error message if the response was not successful
        else:
            print('Error: ' + str(response.status_code))

    # Print an error message if there was an error making the GET request
    except requests.exceptions.RequestException as e:
        print('Error: ' + str(e))

# Close the CSV file
csv_file.close()