from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Set up Selenium WebDriver with headless mode (no browser window)
options = Options()
options.add_argument("--headless")  # Run in the background without a browser window
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scrape_woolworths(query):
    url = f"https://www.woolworths.com.au/shop/search/products?searchTerm={query}"

    # Open the page
    driver.get(url)
    time.sleep(5)  # Give time for JavaScript to load content

    # Find product elements (adjust class names if needed)
    products = driver.find_elements(By.CLASS_NAME, "ng-star-inserted")
    
    # Extract product details
    product_list = []
    for product in products:
        try:
            name = product.find_element(By.CLASS_NAME, "title").text
            price = product.find_element(By.CLASS_NAME, "primary").text
            link = product.find_element(By.CLASS_NAME, "product-title-link").get_attribute("href")
            
            product_list.append({
                "name": name,
                "price": price,
                "link": link
            })
        except Exception as e:
            print(f"Skipping product due to error: {e}")

    # Close the browser after scraping
    driver.quit()

    return product_list

# Scrape products based on the search query
products = scrape_woolworths("chocolate")

# Print results
if products:
    for p in products:
        print(f"Name: {p['name']}\nPrice: {p['price']}\nLink: {p['link']}\n{'-'*50}")
else:
    print("No products found.")
