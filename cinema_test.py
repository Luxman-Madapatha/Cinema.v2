import unittest
import pandas as pd
import numpy as np
from unittest.mock import patch
import io
import sys

from cinema_app import (
    cinema_screen,
    set_booking_id,
    main_menu,
    update_seat_map,
    book_tickets,
    check_bookings,
    validate_input,
    start_menu,
    main,
    booking_id_dict,
)


class TestCinemaBooking(unittest.TestCase):

    def setUp(self):
        self.seat_map_small = pd.DataFrame(
            np.zeros((3, 5), dtype=int),
            columns=range(1, 6),
            index=["A", "B", "C"],
        )
        self.seat_map_large = pd.DataFrame(
            np.zeros((10, 20), dtype=int),
            columns=range(1, 21),
            index=[chr(ord("A") + i) for i in range(10)],
        )
        booking_id_dict.clear()

    def test_cinema_screen_small(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        cinema_screen(self.seat_map_small)
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().strip(), "-----SCREEN-----")

    def test_cinema_screen_large(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        cinema_screen(self.seat_map_large)
        sys.stdout = sys.__stdout__
        self.assertEqual(
            captured_output.getvalue().strip(),
            "-----------------------------SCREEN-----------------------------",
        )

    def test_set_booking_id(self):
        seats = ["A1", "B2"]
        booking_id = set_booking_id(seats)
        self.assertTrue(booking_id.startswith("GIC"))
        self.assertIn(booking_id, booking_id_dict)
        self.assertEqual(booking_id_dict[booking_id], seats)

    # @patch("builtins.input", return_value="A1")
    # def test_update_seat_map_booking(self, mock_input):
    #     seat_map_copy = self.seat_map_small.copy()
    #     updated_map = update_seat_map(seat_map_copy, 2)
    #     booked_seats = []
    #     for row in updated_map.index:
    #         for col in updated_map.columns:
    #             if updated_map.loc[row, col] == 1:
    #                 booked_seats.append(str(row) + str(col))
    #     self.assertEqual(len(booked_seats), 2)

    @patch("builtins.input", side_effect=["2", ""])
    def test_book_tickets_valid(self, mock_input):
        seat_map_copy = self.seat_map_small.copy()
        seats_taken, updated_map = book_tickets(0, 15, seat_map_copy)
        self.assertEqual(seats_taken, 2)

    @patch("builtins.input", side_effect=["-1"])
    def test_book_tickets_invalid(self, mock_input):
        seat_map_copy = self.seat_map_small.copy()
        with self.assertRaises(ValueError):
            book_tickets(0, 15, seat_map_copy)

    def test_check_bookings_valid(self):
        seat_map_copy = self.seat_map_small.copy()
        booking_id = set_booking_id(["A1", "B2"])
        captured_output = io.StringIO()
        sys.stdout = captured_output
        with patch("builtins.input", return_value=booking_id):
            check_bookings(seat_map_copy)
        sys.stdout = sys.__stdout__
        self.assertIn("B", captured_output.getvalue())

    @patch("builtins.input", side_effect=["invalid_id"])
    def test_check_bookings_invalid(self, mock_input):
        seat_map_copy = self.seat_map_small.copy()
        captured_output = io.StringIO()
        sys.stdout = captured_output
        check_bookings(seat_map_copy)
        sys.stdout = sys.__stdout__
        self.assertIn("Invalid booking ID", captured_output.getvalue())

    def test_validate_input_valid(self):
        result = validate_input("Movie 5 10")
        self.assertEqual(result, ("Movie", 5, 10))

    def test_validate_input_invalid_format(self):
        result = validate_input("Movie 5")
        self.assertIsNone(result)

    def test_validate_input_invalid_values(self):
        result = validate_input("Movie -1 0")
        self.assertIsNone(result)

    @patch("builtins.input", side_effect=["Movie 5 10"])
    def test_start_menu(self, mock_input):
        movie_title, total_seats, seat_map = start_menu()
        self.assertEqual(movie_title, "Movie")
        self.assertEqual(total_seats, 50)
        self.assertEqual(seat_map.shape, (5, 10))

    @patch("builtins.input", side_effect=["1", "2", "3"])
    def test_main_menu_choice_1(self, mock_input):
        seat_map_copy = self.seat_map_small.copy()
        with patch("cinema_app.book_tickets", return_value=(2, seat_map_copy)):
            with patch("cinema_app.check_bookings"):
                main_menu("Movie", 0, 15, seat_map_copy)

    @patch("builtins.input", side_effect=["2", "3"])
    def test_main_menu_choice_2(self, mock_input):
        seat_map_copy = self.seat_map_small.copy()
        with patch("cinema_app.book_tickets"):
            with patch("cinema_app.check_bookings"):
                main_menu("Movie", 0, 15, seat_map_copy)
