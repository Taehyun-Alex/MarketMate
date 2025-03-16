import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request

app = Flask(__name__)

def scrape_supermarket(search_query):
    url = f"https://www.woolworths.com.au/shop/search/products?searchTerm={search_query}"
    headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
}
    
    response = requests.get(url, headers=headers)

    print(response.text) 

    soup = BeautifulSoup(response.text, "html.parser")

    products = []

    for item in soup.select(".ng-tns-c865356747-6 product-grid-v2--tile ng-star-inserted"):
        name = item.select_one(".title").text.strip()
        price_text = item.select_one(".primary").text.strip()
        price = float(price_text.replace("$", ""))
        supermarket = "Woolworths"

        products.append({"name": name, "price": price, "supermarket": supermarket})

    return products

@app.route("/scrape", methods=["GET"])
def scrape():
    search_query = request.args.get("query")
    if not search_query:
        return jsonify({"error": "Missing search query"}), 400
    
    data = scrape_supermarket(search_query)
    sorted_data = sorted(data, key=lambda x: x["price"])
    return jsonify(sorted_data)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
