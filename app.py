from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ooh@ 429",
        database="ecommerce"
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/products", methods=["GET", "POST", "DELETE"])
def manage_products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        data = request.json
        cursor.execute("INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)", 
                       (data["name"], data["price"], data["stock"]))
        conn.commit()
        return jsonify({"message": "Product added successfully!"})

    elif request.method == "DELETE":
        product_id = request.args.get("id")
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()
        return jsonify({"message": "Product deleted successfully!"})

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return render_template("products.html", products=products)

@app.route("/users", methods=["GET", "POST", "DELETE"])
def manage_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        data = request.json
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", 
                       (data["name"], data["email"], data["password"]))
        conn.commit()
        return jsonify({"message": "User added successfully!"})

    elif request.method == "DELETE":
        user_id = request.args.get("id")
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        return jsonify({"message": "User deleted successfully!"})

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return render_template("users.html", users=users)

@app.route("/orders", methods=["GET", "POST", "DELETE"])
def manage_orders():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        data = request.json
        cursor.execute("INSERT INTO orders (user_id, product_id, quantity) VALUES (%s, %s, %s)", 
                       (data["user_id"], data["product_id"], data["quantity"]))
        conn.commit()
        return jsonify({"message": "Order added successfully!"})

    elif request.method == "DELETE":
        order_id = request.args.get("id")
        cursor.execute("DELETE FROM orders WHERE id = %s", (order_id,))
        conn.commit()
        return jsonify({"message": "Order deleted successfully!"})

    cursor.execute("""
        SELECT orders.id, users.name as user_name, products.name as product_name, orders.quantity
        FROM orders
        JOIN users ON orders.user_id = users.id
        JOIN products ON orders.product_id = products.id
    """)
    orders = cursor.fetchall()
    conn.close()
    return render_template("orders.html", orders=orders)

@app.route('/products')
def products():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    return render_template('products.html', products=products)


if __name__ == "__main__":
    app.run(debug=True)
