ROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS vehicles CASCADE;
DROP TABLE IF EXISTS routes CASCADE;
DROP TABLE IF EXISTS drivers CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TYPE IF EXISTS order_status CASCADE;

CREATE TABLE customers (
  customer_id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  phone VARCHAR(20),
  email VARCHAR(100) UNIQUE
);

CREATE TABLE drivers (
  driver_id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  license_number VARCHAR(50) UNIQUE
);

CREATE TABLE routes (
  route_id SERIAL PRIMARY KEY,
  start_location VARCHAR(100),
  end_location VARCHAR(100),
  distance_km DECIMAL(6,2)
);

CREATE TABLE vehicles (
  vehicle_id SERIAL PRIMARY KEY,
  plate_number VARCHAR(20) UNIQUE,
  capacity INT,
  driver_id INT REFERENCES drivers(driver_id)
);

CREATE TABLE orders (
  order_id SERIAL PRIMARY KEY,
  customer_id INT REFERENCES customers(customer_id),
  vehicle_id INT REFERENCES vehicles(vehicle_id),
  route_id INT REFERENCES routes(route_id),
  status VARCHAR(50) DEFAULT 'нове',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
