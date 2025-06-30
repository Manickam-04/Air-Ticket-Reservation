import mysql.connector
from mysql.connector import Error

def create_connection():
    """Create a database connection."""
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Replace with your MySQL host
            user='root',       # Replace with your MySQL username
            password='',  # Replace with your MySQL password
            database='airline_reservation'  # Replace with your database name
        )
        if connection.is_connected():
            print("Connection to MySQL database is successful.")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def create_table(connection):
    """Create a table for reservations if it doesn't exist."""
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS reservations (
        id INT AUTO_INCREMENT PRIMARY KEY,
        passenger_name VARCHAR(100) NOT NULL,
        from_where VARCHAR(100) NOT NULL,
        to_where VARCHAR(100) NOT NULL,
        departure_date DATE NOT NULL,
        seat_number VARCHAR(10) NOT NULL
    );
    '''
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        print("Table 'reservations' is ready.")
    except Error as e:
        print(f"Error: {e}")

def add_reservation(connection, passenger_name, from_where, to_where, departure_date, seat_number):
    """Add a new reservation."""
    add_query = '''
    INSERT INTO reservations (passenger_name, from_where, to_where, departure_date, seat_number)
    VALUES (%s, %s, %s, %s, %s);
    '''
    try:
        cursor = connection.cursor()
        cursor.execute(add_query, (passenger_name, from_where, to_where, departure_date, seat_number))
        connection.commit()
        print("Reservation added successfully.")
    except Error as e:
        print(f"Error: {e}")

def view_reservations(connection):
    """View all reservations."""
    view_query = "SELECT * FROM reservations;"
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM reservations")
        rows = cursor.fetchall()
        if not rows:
            print("No reservations found.")
            return None
        else:
            print("\n--- Reservations ---")
            for row in rows:
                print(f"Reservation_ID: {row[0]}, Passenger_name: {row[1]}, From: {row[2]}, To: {row[3]}, Date: {row[4]}, Seat: {row[5]}")
    except Error as e:
        print(f"Error: {e}")

def update_reservation(connection, reservation_id, new_seat_number):
    """Update a reservation's seat number."""
    update_query = """
    UPDATE reservations
    SET seat_number = %s
    WHERE id = %s;
    """
    try:
        cursor = connection.cursor()
        cursor.execute(update_query, (new_seat_number, reservation_id))
        connection.commit()
        print("Reservation updated successfully.")
    except Error as e:
        print(f"Error: {e}")

def delete_reservation(connection, reservation_id):
    """Delete a reservation by ID."""
    delete_query = "DELETE FROM reservations WHERE id = %s;"
    try:
        cursor = connection.cursor()
        cursor.execute(delete_query, (reservation_id,))
        connection.commit()
        print("Reservation deleted successfully.")
    except Error as e:
        print(f"Error: {e}")

def main():
    connection = create_connection()
    if connection:
        create_table(connection)

        while True:
            print("\nAir Ticket Reservation System")
            print("1. Add Reservation")
            print("2. View Reservations")
            print("3. Update Reservation")
            print("4. Delete Reservation")
            print("5. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                name = input("Enter passenger name: ")
                from_where = input("Enter departure location: ")
                to_where = input("Enter destination location: ")
                date = input("Enter departure date (YYYY-MM-DD): ")
                seat = input("Enter seat number which you want to book: ")
                add_reservation(connection, name, from_where, to_where, date, seat)

            elif choice == '2':
                    view_reservations(connection)

            elif choice == '3':
                rid = int(input("Enter reservation ID to update: "))
                new_seat = input("Enter new seat number: ")
                update_reservation(connection, rid, new_seat)

            elif choice == '4':
                rid = int(input("Enter reservation ID to delete: "))
                delete_reservation(connection, rid)

            elif choice == '5':
                print("Exiting system.")
                break

            else:
                print("Invalid choice. Please try again.")

        connection.close()

main()
