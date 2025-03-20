import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter/material.dart';

class SearchPage extends StatefulWidget {
  @override
  State<SearchPage> createState() => _SearchPageState();
}

class _SearchPageState extends State<SearchPage> {
  List<dynamic> products = [];
  TextEditingController searchController = TextEditingController();

  Future<void> fetchData(String query) async {
    try {
      final response = await http.get(Uri.parse("http://10.0.2.2:5000/scrape?query=$query")); // Use 10.0.2.2 for Emulator
      if (response.statusCode == 200) {
        setState(() {
          products = json.decode(response.body);
        });
      } else {
        print("Error: ${response.statusCode}");
      }
    } catch (e) {
      print("Failed to load data: $e");
    }
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
              controller: searchController,
              decoration: InputDecoration(
                labelText: "Search Product",
                suffixIcon: IconButton(
                  icon: Icon(Icons.search),
                  onPressed: () {
                    fetchData(searchController.text); // Fetch products
                  },
                ),
              ),
            ),

            // Search Results List
            Expanded(
              child: products.isEmpty
                  ? Center(child: Text("No products found"))
                  : ListView.builder(
                      itemCount: products.length,
                      itemBuilder: (context, index) {
                        return ListTile(
                          title: Text(products[index]['name']),
                          subtitle: Text("${products[index]['supermarket']} - \$${products[index]['price']}"),
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
