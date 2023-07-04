import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

def get_website_info(url):
    # Send a GET request to the website
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for unsuccessful requests
    
    # Extract HTML content
    html_content = response.text
    
    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Get website information
    title = soup.title.text.strip()
    meta_tags = soup.find_all('meta')
    links = soup.find_all('a')
    
    # Print website information
    print(f"Website: {url}")
    print(f"Title: {title}")
    
    print("Meta tags:")
    for meta in meta_tags:
        print(meta.attrs)
    
    print("Links:")
    for link in links:
        print(link.get('href'))
    
    print("\n")

def extract_code_snippets(url):
    # Send a GET request to the website
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for unsuccessful requests
    
    # Extract code snippets
    code_snippets = re.findall(r'<script.*?</script>|<style.*?</style>', response.text, flags=re.DOTALL)
    
    # Print code snippets
    print(f"Website: {url}")
    print("Code Snippets:")
    for code in code_snippets:
        print(code)
    
    print("\n")

def extract_server_info(url):
    # Send a HEAD request to retrieve server and other headers
    response = requests.head(url)
    response.raise_for_status()  # Raise an exception for unsuccessful requests
    
    # Get server information
    server = response.headers.get('Server')
    firewall = response.headers.get('X-Firewall')
    # Extract other headers as needed
    
    # Print server information
    print(f"Website: {url}")
    print(f"Server: {server}")
    print(f"Firewall: {firewall}")
    # Print other headers as needed
    
    print("\n")

def compare_websites(url1, url2):
    print(f"Comparing websites: {url1} and {url2}\n")
    
    get_website_info(url1)
    extract_code_snippets(url1)
    extract_server_info(url1)
    
    get_website_info(url2)
    extract_code_snippets(url2)
    extract_server_info(url2)

def crawl_website(url):
    try:
        # Send a GET request to the website
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for unsuccessful requests
        
        # Extract HTML content
        html_content = response.text
        
        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all anchor tags
        links = soup.find_all('a')
        
        # Crawl all paths and sub-paths
        for link in links:
            path = link.get('href')
            if path and not path.startswith('#'):
                absolute_url = urljoin(url, path)
                crawl_website(absolute_url)
    except requests.exceptions.RequestException as e:
        print(f"Error crawling URL: {url}")
        print(f"Error message: {e}\n")

def validate_url(url):
    # Validate the URL format
    return re.match(r'^https?://(?:www\.)?[^\s/$.?#].[^\s]*$', url) is not None

# URLs of the websites to differentiate
website1_url = 'https://www.example1.com'
website2_url = 'https://www.example2.com'

# Validate the URLs
if not validate_url(website1_url) or not validate_url(website2_url):
    print("Invalid URL format. Please provide valid URLs.")
    exit(1)

# Compare the websites
compare_websites(website1_url, website2_url)
  
