from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import mysql.connector
from mysql.connector import Error
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Для flash повідомлень

# --- Параметри підключення до MySQL ---
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "HBr</24t",  # ЗАМІНИ на свій пароль
    "database": "transport_company"
}

def get_db_connection():
    """Створює підключення до БД"""
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"Помилка підключення до БД: {e}")
        return None

# ==================== ГОЛОВНА СТОРІНКА ====================
@app.route("/")
def index():
    conn = get_db_connection()
    if not conn:
        flash("Помилка підключення до бази даних", "error")
        return render_template("index.html", orders=[], stats={})
    
    cursor = conn.cursor()
    
    # Отримання замовлень
    cursor.execute("""
        SELECT o.order_id, c.name, c.phone, v.plate_number, d.name,
               r.start_location, r.end_location, r.distance_km,
               o.status, o.created_at
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN vehicles v ON o.vehicle_id = v.vehicle_id
        JOIN routes r ON o.route_id = r.route_id
        JOIN drivers d ON v.driver_id = d.driver_id
        ORDER BY o.created_at DESC
    """)
    orders = cursor.fetchall()
    
    # Статистика
    cursor.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN status = 'нове' THEN 1 ELSE 0 END) as new_orders,
            SUM(CASE WHEN status = 'в дорозі' THEN 1 ELSE 0 END) as in_progress,
            SUM(CASE WHEN status = 'доставлено' THEN 1 ELSE 0 END) as delivered
        FROM orders
    """)
    stats = cursor.fetchone()
    stats_dict = {
    'total': stats[0] if stats[0] is not None else '0',
    'new': stats[1] if stats[1] is not None else '0',
    'in_progress': stats[2] if stats[2] is not None else '0',
    'delivered': stats[3] if stats[3] is not None else '0'
    }
    
    conn.close()
    return render_template("index.html", orders=orders, stats=stats_dict)

# ==================== КЛІЄНТИ ====================
@app.route("/customers")
def customers():
    conn = get_db_connection()
    if not conn:
        flash("Помилка підключення до бази даних", "error")
        return render_template("customers.html", customers=[])
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.customer_id, c.name, c.phone, c.email,
               COUNT(o.order_id) as orders_count
        FROM customers c
        LEFT JOIN orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id
    """)
    customers_list = cursor.fetchall()
    conn.close()
    return render_template("customers.html", customers=customers_list)

@app.route("/customers/add", methods=["POST"])
def add_customer():
    name = request.form["name"]
    phone = request.form["phone"]
    email = request.form["email"]
    
    conn = get_db_connection()
    if not conn:
        flash("Помилка підключення до бази даних", "error")
        return redirect(url_for('customers'))
    
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO customers (name, phone, email)
            VALUES (%s, %s, %s)
        """, (name, phone, email))
        conn.commit()
        flash("Клієнта успішно додано!", "success")
    except Error as e:
        flash(f"Помилка: {e}", "error")
    finally:
        conn.close()
    
    return redirect(url_for('customers'))

@app.route("/customers/delete/<int:customer_id>")
def delete_customer(customer_id):
    conn = get_db_connection()
    if not conn:
        flash("Помилка підключення до бази даних", "error")
        return redirect(url_for('customers'))
    
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
        conn.commit()
        flash("Клієнта успішно видалено!", "success")
    except Error as e:
        flash(f"Помилка: не можна видалити клієнта з активними замовленнями", "error")
    finally:
        conn.close()
    
    return redirect(url_for('customers'))

# ==================== ВОДІЇ ====================
@app.route("/drivers")
def drivers():
    conn = get_db_connection()
    if not conn:
        flash("Помилка підключення до бази даних", "error")
        return render_template("drivers.html", drivers=[])
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT d.driver_id, d.name, d.license_number,
               COUNT(v.vehicle_id) as vehicles_count
        FROM drivers d
        LEFT JOIN vehicles v ON d.driver_id = v.driver_id
        GROUP BY d.driver_id
    """)
    drivers_list = cursor.fetchall()
    conn.close()
    return render_template("drivers.html", drivers=drivers_list)

@app.route("/drivers/add", methods=["POST"])
def add_driver():
    name = request.form["name"]
    license_number = request.form["license_number"]
    
    conn = get_db_connection()
    if not conn:
        flash("Помилка підключення до бази даних", "error")
        return redirect(url_for('drivers'))
    
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO drivers (name, license_number)
            VALUES (%s, %s)
        """, (name, license_number))
        conn.commit()
        flash("Водія успішно додано!", "success")
    except Error as e:
        flash(f"Помилка: {e}", "error")
    finally:
        conn.close()
    
    return redirect(url_for('drivers'))

@app.route("/drivers/delete/<int:driver_id>")
def delete_driver(driver_id):
    conn = get_db_connection()
    if not conn:
        flash("Помилка підключення до бази даних", "error")
        return redirect(url_for('drivers'))
    
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM drivers WHERE driver_id = %s", (driver_id,))
        conn.commit()
        flash("Водія успішно видалено!", "success")
    except Error as e:
        flash(f"Помилка: не можна видалити водія з прив'язаними авто", "error")
    finally:
        conn.close()
    
    return redirect(url_for('drivers'))

# ==================== ТРАНСПОРТ ====================
@app.route("/vehicles")
def vehicles():
    conn = get_db_connection()
    if not conn:
        flash("Помилка підключення до бази даних", "error")
        return render_template("vehicles.html", vehicles=[], drivers=[])
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT v.vehicle_id, v.plate_number, v.capacity, d.name
        FROM vehicles v
        LEFT JOIN drivers d ON v.driver_id = d.driver_id
    """)
    vehicles_list = cursor.fetchall()
    
    cursor.execute("SELECT driver_id, name FROM drivers")
    drivers_list = cursor.fetchall()
    
    conn.close()
    return render_template("vehicles.html", vehicles=vehicles_list, drivers=drivers_list)

@app.route("/vehicles/add", methods=["POST"])
def add_vehicle():
    plate_number = request.form["plate_number"]
    capacity = request.form["capacity"]
    driver_id = request.form["driver_id"]
    
    conn = get_db_connection()
    if not conn:
        flash("Помилка підключення до бази даних", "error")
        return redirect(url_for('vehicles'))
    
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO vehicles (plate_number, capacity, driver_id)
            VALUES (%s, %s, %s)
        """, (plate_number, capacity, driver_id))
        conn.commit()
        flash("Транспорт успішно додано!", "success")
    except Error as e:
        flash(f"Помилка: {e}", "error")
    finally:
        conn.close()
    
    return redirect(url_for('vehicles'))

@app.route("/vehicles/delete/<int:vehicle_id>")
def delete_vehicle(vehicle_id):
    conn = get_db_connection()
    if not conn:
        flash("Помилка підключення до бази даних", "error")
        return redirect(url_for('vehicles'))
    
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM vehicles WHERE vehicle_id = %s", (vehicle_id,))
        conn.commit()
        flash("Транспорт успішно видалено!", "success")
    except Error as e:
        flash(f"Помилка: не можна видалити авто з активними замовленнями", "error")
    finally:
        conn.close()
    
    return redirect(url_for('vehicles'))

# ==================== МАРШРУТИ ====================
@app.route("/routes")
def routes():
    conn = get_db_connection()
    if not conn:
        flash("Помилка підключення до бази даних", "error")
        return render_template("routes.html", routes=[])
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.route_id, r.start_location, r.end_location, r.distance_km,
               COUNT(o.order_id) as usage_count
        FROM routes r
        LEFT JOIN orders o ON r.route_id = o.route_id
        GROUP BY r.route_id
    """)
    routes_list = cursor.fetchall()
    conn.close()
    return render_template("routes.html", routes=routes_list)

@app.route("/routes/add", methods=["POST"])
def add_route():
    start_location = request.form["start_location"]
    end_location = request.form["end_location"]
    distance_km = request.form["distance_km"]
    
    conn = get_db_connection()
    if not conn:
        flash("Помилка підключення до бази даних", "error")
        return redirect(url_for('routes'))
    
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO routes (start_location, end_location, distance_km)
            VALUES (%s, %s, %s)
        """, (start_location, end_location, distance_km))
        conn.commit()
        flash("Маршрут успішно додано!", "success")
    except Error as e:
        flash(f"Помилка: {e}", "error")
    finally:
        conn.close()
    
    return redirect(url_for('routes'))

@app.route("/routes/delete/<int:route_id>")
def delete_route(route_id):
    conn = get_db_connection()
    if not conn:
        flash("Помилка підключення до бази даних", "error")
        return redirect(url_for('routes'))
    
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM routes WHERE route_id = %s", (route_id,))
        conn.commit()
        flash("Маршрут успішно видалено!", "success")
    except Error as e:
        flash(f"Помилка: не можна видалити маршрут з активними замовленнями", "error")
    finally:
        conn.close()
    
    return redirect(url_for('routes'))

# ==================== ЗАМОВЛЕННЯ ====================
@app.route("/orders")
def orders():
    conn = get_db_connection()
    if not conn:
        flash("Помилка підключення до бази даних", "error")
        return render_template("orders.html", orders=[], customers=[], vehicles=[], routes=[])
    
    cursor = conn.cursor()
    
    # Отримання всіх замовлень
    cursor.execute("""
        SELECT o.order_id, c.name, v.plate_number, 
               r.start_location, r.end_location, o.status, o.created_at
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN vehicles v ON o.vehicle_id = v.vehicle_id
        JOIN routes r ON o.route_id = r.route_id
        ORDER BY o.created_at DESC
    """)
    orders_list = cursor.fetchall()
    
    # Списки для форми додавання
    cursor.execute("SELECT customer_id, name FROM customers")
    customers_list = cursor.fetchall()
    
    cursor.execute("SELECT vehicle_id, plate_number FROM vehicles")
    vehicles_list = cursor.fetchall()
    
    cursor.execute("SELECT route_id, start_location, end_location FROM routes")
    routes_list = cursor.fetchall()
    
    conn.close()
    return render_template("orders.html", orders=orders_list, 
                         customers=customers_list, 
                         vehicles=vehicles_list, 
                         routes=routes_list)

@app.route("/orders/add", methods=["POST"])
def add_order():
    customer_id = request.form["customer_id"]
    vehicle_id = request.form["vehicle_id"]
    route_id = request.form["route_id"]
    
    conn = get_db_connection()
    if not conn:
        flash("Помилка підключення до бази даних", "error")
        return redirect(url_for('orders'))
    
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO orders (customer_id, vehicle_id, route_id, status)
            VALUES (%s, %s, %s, 'нове')
        """, (customer_id, vehicle_id, route_id))
        conn.commit()
        flash("Замовлення успішно створено!", "success")
    except Error as e:
        flash(f"Помилка: {e}", "error")
    finally:
        conn.close()
    
    return redirect(url_for('index'))

@app.route("/orders/update/<int:order_id>", methods=["POST"])
def update_order(order_id):
    new_status = request.form["status"]
    
    conn = get_db_connection()
    if not conn:
        flash("Помилка підключення до бази даних", "error")
        return redirect(url_for('index'))
    
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status=%s WHERE order_id=%s", (new_status, order_id))
    conn.commit()
    conn.close()
    
    flash("Статус замовлення оновлено!", "success")
    return redirect(url_for('index'))

@app.route("/orders/delete/<int:order_id>")
def delete_order(order_id):
    conn = get_db_connection()
    if not conn:
        flash("Помилка підключення до бази даних", "error")
        return redirect(url_for('orders'))
    
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
        conn.commit()
        flash("Замовлення успішно видалено!", "success")
    except Error as e:
        flash(f"Помилка: {e}", "error")
    finally:
        conn.close()
    
    return redirect(url_for('orders'))

# ==================== ПОШУК ====================
@app.route("/search")
def search():
    query = request.args.get('q', '')
    status_filter = request.args.get('status', '')
    
    if not query and not status_filter:
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    if not conn:
        flash("Помилка підключення до бази даних", "error")
        return redirect(url_for('index'))
    
    cursor = conn.cursor()
    
    sql = """
        SELECT o.order_id, c.name, c.phone, v.plate_number, d.name,
               r.start_location, r.end_location, r.distance_km,
               o.status, o.created_at
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN vehicles v ON o.vehicle_id = v.vehicle_id
        JOIN routes r ON o.route_id = r.route_id
        JOIN drivers d ON v.driver_id = d.driver_id
        WHERE 1=1
    """
    params = []
    
    if query:
        sql += """ AND (c.name LIKE %s OR v.plate_number LIKE %s 
                       OR r.start_location LIKE %s OR r.end_location LIKE %s)"""
        search_term = f"%{query}%"
        params.extend([search_term, search_term, search_term, search_term])
    
    if status_filter:
        sql += " AND o.status = %s"
        params.append(status_filter)
    
    sql += " ORDER BY o.created_at DESC"
    
    cursor.execute(sql, params)
    orders = cursor.fetchall()
    conn.close()
    
    return render_template("search_results.html", orders=orders, query=query, status=status_filter)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)