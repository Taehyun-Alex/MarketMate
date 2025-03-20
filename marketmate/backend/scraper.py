from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, jsonify, request
import time

app = Flask(__name__)

def scrape_supermarket(search_query):
    url = f"https://www.coles.com.au/search/products?q={search_query}"
    
    # Set up Selenium WebDriver
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.78 Safari/537.36")


    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    
    # Wait for JavaScript to load
    time.sleep(5)

    print(driver.page_source) 
    products = []

    # Find product elements (Fixed CSS selector)
    product_elements = driver.find_elements(By.CSS_SELECTOR, ".sc-6831e1f3-8.cppZxr.coles-targeting-ProductTileProductTileWrapper")

    for item in product_elements:
        try:
            name = item.find_element(By.CSS_SELECTOR, ".LinesEllipsis.product__title").text.strip()
            price_text = item.find_element(By.CSS_SELECTOR, ".price__value").text.strip()
            price = float(price_text.replace("$", "").replace(",", ""))
            supermarket = "Coles"

            products.append({"name": name, "price": price, "supermarket": supermarket})
        except Exception as e:
            print(f"Skipping item due to error: {e}")

    driver.quit()  # Close the browser

    return products

@app.route("/scrape", methods=["GET"])
def scrape():
    search_query = request.args.get("query")
    if not search_query:
        return jsonify({"error": "Missing search query"}), 400

    data = scrape_supermarket(search_query)
    
    print("Scraped Data:", data)  # Debugging
    

    return jsonify(data if data else [])

if __name__ == "__main__":
    app.run(debug=True, port=5000)
