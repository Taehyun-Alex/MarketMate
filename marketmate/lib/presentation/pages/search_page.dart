import 'package:flutter/material.dart';

class SearchPage extends StatefulWidget {
  const SearchPage({super.key, required String title});

  @override
  State<SearchPage> createState() => _SearchPageState();
}

class _SearchPageState extends State<SearchPage> {
  final TextEditingController _searchController = TextEditingController();

  List<Map<String, dynamic>> allProducts = [
    {"name": "Milk", "supermarket": "Coles", "price": 3.50},
    {"name": "Milk", "supermarket": "Woolworths", "price": 3.20},
    {"name": "Milk", "supermarket": "Aldi", "price": 2.90},
    {"name": "Eggs", "supermarket": "Coles", "price": 5.00},
    {"name": "Eggs", "supermarket": "Woolworths", "price": 4.80},
    {"name": "Eggs", "supermarket": "Aldi", "price": 4.20},
  ];

  List<Map<String, dynamic>> filteredProducts = [];

  void _searchProducts(String query) {
    setState(() {
      filteredProducts = allProducts
          .where((product) =>
              product["name"].toLowerCase().contains(query.toLowerCase()))
          .toList();

      // Sort by price (cheapest first)
      filteredProducts.sort((a, b) => a["price"].compareTo(b["price"]));
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("MarketMate"),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            // Search Bar
            TextField(
              controller: _searchController,
              decoration: InputDecoration(
                hintText: "Search for groceries...",
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                prefixIcon: const Icon(Icons.search),
              ),
              onChanged: _searchProducts, // Calls function on typing
            ),
            const SizedBox(height: 16),

            // Search Results List
            Expanded(
              child: ListView.builder(
                itemCount: filteredProducts.length,
                itemBuilder: (context, index) {
                  final product = filteredProducts[index];
                  final bool isCheapest = (index == 0); // First item is cheapest

                  return ListTile(
                    title: Text(
                      "${product["name"]} - ${product["supermarket"]}",
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        color: isCheapest ? Colors.green : Colors.black, // Highlight cheapest
                      ),
                    ),
                    subtitle: Text("\$${product["price"].toStringAsFixed(2)}"),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}





