
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "bookstore-secret-key-2026"

# Data buku
books = [
    {
        "id": 1,
        "title": "Laut Bercerita",
        "author": "Leila S. Chudori",
        "price": 95000,
        "category": "Novel",
        "image": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500"
    },
    {
        "id": 2,
        "title": "Atomic Habits",
        "author": "James Clear",
        "price": 120000,
        "category": "Pengembangan Diri",
        "image": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=500"
    },
    {
        "id": 3,
        "title": "Filosofi Teras",
        "author": "Henry Manampiring",
        "price": 85000,
        "category": "Filsafat",
        "image": "https://images.unsplash.com/photo-1519682337058-a94d519337bc?w=500"
    },
    {
        "id": 4,
        "title": "Bumi",
        "author": "Tere Liye",
        "price": 90000,
        "category": "Novel",
        "image": "https://images.unsplash.com/photo-1513001900722-370f803f498d?w=500"
    },
    {
        "id": 5,
        "title": "Rich Dad Poor Dad",
        "author": "Robert Kiyosaki",
        "price": 110000,
        "category": "Bisnis",
        "image": "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=500"
    },
    {
        "id": 6,
        "title": "The Psychology of Money",
        "author": "Morgan Housel",
        "price": 105000,
        "category": "Bisnis",
        "image": "https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=500"
    }
]


@app.route("/")
def index():

    search = request.args.get("search", "").strip()
    category = request.args.get("category", "")

    filtered_books = books

    # Fitur pencarian
    if search:
        filtered_books = [
            book for book in filtered_books
            if search.lower() in book["title"].lower()
            or search.lower() in book["author"].lower()
        ]

    # Filter kategori
    if category:
        filtered_books = [
            book for book in filtered_books
            if book["category"] == category
        ]

    # Mengambil data keranjang
    cart = session.get("cart", {})

    cart_items = []
    total = 0

    for book_id, quantity in cart.items():
        book = next(
            (b for b in books if b["id"] == int(book_id)),
            None
        )

        if book:
            item = book.copy()
            item["quantity"] = quantity
            item["subtotal"] = book["price"] * quantity

            cart_items.append(item)
            total += item["subtotal"]

    cart_count = sum(cart.values())

    categories = sorted(set(book["category"] for book in books))

    return render_template(
        "index.html",
        books=filtered_books,
        categories=categories,
        selected_category=category,
        search=search,
        cart_items=cart_items,
        cart_count=cart_count,
        total=total
    )


# Menambahkan buku ke keranjang
@app.route("/add/<int:book_id>", methods=["POST"])
def add_to_cart(book_id):

    if not any(book["id"] == book_id for book in books):
        return redirect(url_for("index"))

    cart = session.get("cart", {})

    key = str(book_id)
    cart[key] = cart.get(key, 0) + 1

    session["cart"] = cart

    return redirect(url_for("index"))


# Menghapus buku dari keranjang
@app.route("/remove/<int:book_id>", methods=["POST"])
def remove_from_cart(book_id):

    cart = session.get("cart", {})

    cart.pop(str(book_id), None)

    session["cart"] = cart

    return redirect(url_for("index"))


# Mengosongkan keranjang
@app.route("/clear", methods=["POST"])
def clear_cart():

    session["cart"] = {}

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5001,
        debug=True
    )
