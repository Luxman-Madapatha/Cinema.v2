"""Cinema Seat Booking Application Prototype"""

import pandas as pd
import numpy as np

booking_id_dict = {}


def cinema_screen(seat_map):
    """Displays the screen layout."""

    if len(seat_map.columns) < 10:
        text = (len(seat_map.columns) - len("SCREEN") // 2 + 1) * "-"
        print(f"{text}--SCREEN--{text}")

    else:
        text = (((len(seat_map.columns) * 3) - 9) // 2) * "-"
        print(f"{text}----SCREEN----{text}")


def set_booking_id(seat_list):
    """Generates a unique booking ID."""
    booking_id = "GIC" + str(np.random.randint(1000, 9999))
    booking_id_dict[booking_id] = seat_list
    return booking_id


def main_menu(movie_title, seats_taken, total_seat_count, df_):
    """Displays the main menu and handles user choices."""
    # global df

    while True:
        print(
            "Welcome to GIC Cinemas\n"
            "[1] Book tickets for "
            f"{movie_title} ({total_seat_count - seats_taken} seats available)\n"
            "[2] Check bookings\n"
            "[3] Exit\n"
            "Please enter your selection:"
        )

        choice = input()

        if choice == "1":
            try:
                seats_taken, df_ = book_tickets(seats_taken, total_seat_count, df_)
            except ValueError as ve:
                print(str(ve))
        elif choice == "2":
            check_bookings(df_)
        elif choice == "3":
            print("Thank you for using GIC Cinemas system. Bye!")
            break
        else:
            print("Invalid selection. Please try again.")


def update_seat_map(seat_map, seats_required):
    """Updates the seat map DataFrame with new bookings."""
    middle_col = len(seat_map.columns) // 2
    num_seats_booked = 0
    original_seat_map = seat_map.copy(deep=True)
    booked_seats = []

    def book_seats(seat_map, seats_required, num_seats_booked):
        """
        Books a single seat in the seat map.

        This function marks the specified seat as booked in the seat map.

        Args:
            seat_map (pd.DataFrame): The seat map DataFrame.
            row_char (str): The row character of the seat to book.
            col_num (int): The column number of the seat to book.

        Returns:
            None
        """
        for row in seat_map.index:
            for offset in range(len(seat_map.columns) // 2 + 1):
                left_col = middle_col - offset
                right_col = middle_col + offset

                if left_col >= 0 and seat_map.loc[row, seat_map.columns[left_col]] == 0:
                    seat_map.loc[row, seat_map.columns[left_col]] = 1
                    booked_seats.append(str(row) + str(seat_map.columns[left_col]))
                    num_seats_booked += 1
                    if num_seats_booked == seats_required:
                        return

                if (
                    right_col < len(seat_map.columns)
                    and left_col != right_col
                    and seat_map.loc[row, seat_map.columns[right_col]] == 0
                ):
                    seat_map.loc[row, seat_map.columns[right_col]] = 1
                    booked_seats.append(str(row) + str(seat_map.columns[right_col]))
                    num_seats_booked += 1
                    if num_seats_booked == seats_required:
                        return

    def handle_user_input(seat_map):
        """
        Handles user input for booking seats.

        This function prompts the user to enter a seat to start with, and then
        books the seats accordingly. If the user presses Enter without entering
        a seat, it will accept the current seating.

        Args:
            seat_map (pd.DataFrame): The seat map DataFrame.

        Returns:
            None
        """
        nonlocal num_seats_booked, booked_seats
        choice = input(
            "Enter a seat to start with (e.g., C3, or press Enter to accept the current seating): "
        )
        if choice:
            try:
                row_char = choice[0].upper()
                col_num = int(choice[1:])
                if row_char in seat_map.index and col_num in seat_map.columns:
                    seat_map = original_seat_map.copy()
                    num_seats_booked = 0
                    booked_seats.clear()
                    found_start = False

                    for row in seat_map.index:
                        for col_name in seat_map.columns:
                            if (
                                not found_start
                                and row == row_char
                                and col_name == col_num
                            ):
                                found_start = True
                            if found_start and seat_map.loc[row, col_name] == 0:
                                seat_map.loc[row, col_name] = 1
                                booked_seats.append(str(row) + str(col_name))
                                num_seats_booked += 1
                                if num_seats_booked == seats_required:
                                    return
                else:
                    print("Invalid seat choice. Please try again.")
            except (ValueError, IndexError):
                print("Invalid seat choice format. Please use format like C3.")
        else:
            book_seats(seat_map, seats_required, num_seats_booked)

    handle_user_input(seat_map)

    print("Booking_id: " + set_booking_id(booked_seats))
    print(booked_seats)
    print(len(set(booked_seats)))
    return seat_map


def book_tickets(seats_taken, total_seat_count, seat_map):
    """Handles ticket booking functionality."""

    print("Booking tickets...")
    seats_required = input("Enter the number of seats required\n")

    if (
        not seats_required.isdigit()
        or int(seats_required) <= 0
        or int(seats_required) > total_seat_count - seats_taken
    ):
        raise ValueError("Invalid number of seats. Please try again.")

    seats_taken += int(seats_required)
    print(
        f"{seats_required} seat(s) booked. {total_seat_count - seats_taken} seats remaining."
    )

    seat_map = update_seat_map(seat_map, int(seats_required))
    return seats_taken, seat_map


def check_bookings(seat_map):
    """
    Checks the current bookings in the seat map.

    This function prints out the current bookings in the seat map, including
    the booking ID, the seats booked, and the total number of seats booked.

    Args:
        seat_map (pd.DataFrame): The seat map DataFrame.

    Returns:
        None
    """
    print("Checking bookings...")
    print(booking_id_dict.keys())

    seat_map_copy_2 = pd.DataFrame()
    choice = input("Please enter the booking id\n")

    if choice in booking_id_dict:
        seat_map_copy_2 = seat_map.copy(deep=True).astype(str)

        for item in booking_id_dict[choice]:
            # print(item[0], item[1])
            seat_map_copy_2.loc[str(item[0]), int(item[1:])] = "B"

        print(booking_id_dict[choice])
        print("Other seat bookings label: 1")
        print("Your seat bookings label: B")
        print(f"{len(booking_id_dict[choice])} seats have been booked.")
        print(seat_map_copy_2)
        cinema_screen(seat_map)

    else:
        print("Invalid booking ID. Please try again.")


def validate_input(input_str):
    """
    Validates the user input for the seat map.

    This function checks if the input string is in the correct format,
    and if the values are within the valid range.

    Args:
        input_str (str): The input string to validate.

    Returns:
        tuple: A tuple containing the validated movie title, rows, and seats per row.
        None: If the input is invalid.

    Raises:
        ValueError: If the input is invalid.
    """
    try:
        movie_title, rows_str, seats_per_row_str = input_str.split()
        rows, seats_per_row = int(rows_str), int(seats_per_row_str)
        if not movie_title:
            raise ValueError("Movie title cannot be empty")
        if rows <= 0 or seats_per_row <= 0:
            raise ValueError("Rows and SeatsPerRow must be positive integers")
        if rows > 26 or seats_per_row > 50:
            raise ValueError("Rows <= 26, SeatsPerRow <= 50")
        return movie_title, rows, seats_per_row
    except ValueError as e:
        print(f"Invalid value for format: {e}. Please try again.")
        return None


def start_menu():
    """
    Displays the start menu for the cinema booking system.

    This function prints out the main menu options for the user to choose from,
    including booking a movie, checking bookings, and exiting the system.

    Returns:
        tuple: A tuple containing the validated movie title, rows, seats per row, and seat map.
    """
    while True:
        input_str = input(
            "Please define movie title and seating map in [Title] [Row] [SeatsPerRow] format:\n"
        )
        result = validate_input(input_str)
        if result:
            movie_title, rows, seats_per_row = result
            df_init = pd.DataFrame(
                np.zeros((rows, seats_per_row), dtype=int),
                columns=range(1, seats_per_row + 1),
                index=[chr(ord("A") + i) for i in range(rows)],
            )

            print(df_init)
            return movie_title, df_init.size, df_init


def main():
    """
    Main entry point for the cinema booking system.

    This function initializes the seat map, displays the start menu, and handles
    user input to book seats or exit the system.

    Returns:
        None
    """

    result = None
    seats_taken = 0

    while result is None:
        result = start_menu()

    (movie_title_, total_seat_count_, df) = result

    main_menu(movie_title_, seats_taken, total_seat_count_, df)


if __name__ == "__main__":
    main()
