import datetime

class Flight:
    def __init__(self, flight_id, destination, date, price, seats_available):

        self.flight_id = flight_id
        self.destination = destination
        self.date = date
        self.price = price
        self.seats_available = seats_available
    
    def book_seat(self):
        if self.seats_available > 0:
            self.seats_available -= 1
            return True
        else:
            return False
        
    def __str__(self):
        return f"Flight ID : {self.flight_id} | Destination : {self.destination} | Date : {self.date} | Price : Rs.{self.price} | Seats Available : {self.seats_available}"
    

class Booking:
    def __init__(self, booking_id, flight, passenger_name):

        self.booking_id = booking_id
        self.flight = flight
        self.passenger_name = passenger_name
        self.date_booked = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return f"Booking ID : {self.booking_id} | Passenger Name : {self.passenger_name} | Flight : {self.flight.destination} On {self.flight.date} | Date Booked : {self.date_booked}"


class FlightBookingApp:
    
    def __init__(self):
        self.flights = []
        self.bookings = []
        self.booking_id_counter = 1

    def add_sample_flights(self):
        self.flights.append(Flight(1,"New York","2024-12-01",300,5))
        self.flights.append(Flight(2,"London","2024-12-02",450,3))
        self.flights.append(Flight(3,"Canada","2024-12-03",500,2))

    def display_flights(self):
        print("\nAvailable Flights:\n")

        for flight in self.flights:
            print(flight)

    def book_flight(self):

        self.display_flights()

        try:
            flight_id = int(input("Enter Flight ID to Book: "))
            passenger_name = input("Enter your Name: ")

            flight = next((f for f in self.flights if f.flight_id == flight_id), None)

            if flight and flight.book_seat():

                booking = Booking(self.booking_id_counter, flight, passenger_name)
                self.bookings.append(booking)
                self.booking_id_counter += 1

                print(f"\nBooking Successful! Your Booking ID is {booking.booking_id}")

            else:
                print("\nBooking failed. Flight full or invalid Flight ID.")

        except ValueError:
            print("Invalid input. Please enter numeric Flight ID.")

    def view_bookings(self):

        if not self.bookings:
            print("\nNo bookings found.")

        else:
            print("\nYour Bookings:\n")

            for booking in self.bookings:
                print(booking)

    def start(self):

        self.add_sample_flights()

        while True:

            print("\n---- Flight Booking System ----")
            print("1. View Flights")
            print("2. Book a Flight")
            print("3. View My Bookings")
            print("4. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.display_flights()

            elif choice == '2':
                self.book_flight()

            elif choice == '3':
                self.view_bookings()

            elif choice == '4':
                print("Exiting the Flight Booking System. Thank you.")
                break

            else:
                print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    app = FlightBookingApp()
    app.start()