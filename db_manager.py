# Class to handle all DB CRUD managment.

import sqlite3
from random import choice
from random import shuffle


class DBManager_sqlite:
    def __init__(self):
        """Attributes"""
        self.GUIDB = 'Flight_Gen_airports.db'
        self.icao_codes = []
        self.icao_codes_lat_lon = []
        self.connect_db()
        self.create_db()
        self.show_icao_codes()
        self.show_icao_codes_lat_lon()

    # Module working ok! :)
    def connect_db(self):
        """Connecting to SQLite"""
        con_db = sqlite3.connect(self.GUIDB)
        cursor = con_db.cursor()
        # we return the connection and the cursor.
        return con_db, cursor

    # Module working ok! :)
    def close(self, cursor, con_db):
        """To close the SQLite connection and cursor"""
        cursor.close()
        con_db.close()

    # Module working ok! :)
    def create_db(self):
        """Connecting and creating the SQLite db"""
        # connect and create Data Base!!!
        con_db = sqlite3.connect(self.GUIDB)

        # creating the cursor to send commands to SQLite
        cursor = con_db.cursor()

        # Creating the tables

        cursor.execute("CREATE TABLE IF NOT EXISTS airport_info  \
            (icao_code_id INTEGER PRIMARY KEY AUTOINCREMENT,     \
            icao_code TEXT,                                      \
            iata_code TEXT,                                      \
            airport_name TEXT,                                   \
            city TEXT,                                           \
            lat_decimal INTEGER,                                 \
            lon_decimal INTEGER,                                 \
            rwy_avail1 INTEGER,                                  \
            rwy_avail2 INTEGER,                                  \
            rwy_len INTEGER,                                     \
            airport_elev INTEGER,                                \
            airport_remarks TEXT)")

        cursor.execute("CREATE TABLE IF NOT EXISTS airport_nav_data   \
            (airport_nav_data_id INTEGER PRIMARY KEY AUTOINCREMENT,   \
            icao_code_id INTEGER,                                        \
            vfr TEXT,                                                 \
            vfr_ifr TEXT,                                             \
            has_sid TEXT,                                             \
            has_star TEXT,                                            \
            has_arr_arc TEXT,                                         \
            has_dep_arc TEXT,                                         \
            ils_app TEXT,                                             \
            ndb_app TEXT,                                             \
            vor_app TEXT,                                             \
            vora_app TEXT,                                            \
            approach_diff INTEGER,                                    \
            airport_nav_data_remarks TEXT)")

        cursor.execute("CREATE TABLE IF NOT EXISTS diff_flights  \
            (diff_flights_id INTEGER PRIMARY KEY AUTOINCREMENT,  \
            icao_code_id_dep TEXT,                               \
            icao_code_id_arr TEXT,                               \
            flight_diff_level INTEGER,                           \
            flight_diff_remarks TEXT)")

    # Module working ok! :)
    def insert_airport_info(self, icao_code, iata_code, airport_name, city,
                            lat_decimal, lon_decimal, rwy_avail1, rwy_avail2,
                            rwy_len, airport_elev, airport_remarks):
        """To insert airport_info data in the airport_info
        It takes 11 params:  """

        con_db, cursor = self.connect_db()

        # insert data
        cursor.execute("INSERT INTO airport_info (icao_code, iata_code, airport_name, city, lat_decimal, lon_decimal, rwy_avail1, rwy_avail2, rwy_len, airport_elev, airport_remarks) \
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (icao_code, iata_code, airport_name, city, lat_decimal, lon_decimal, rwy_avail1, rwy_avail2, rwy_len, airport_elev, airport_remarks))

        # commit transaction
        con_db.commit()

        # close cursor and connection
        self.close(cursor, con_db)

    # Module working ok! :)
    def insert_airport_nav_data(self, icao_code, vfr,
                                vfr_ifr, has_sid, has_star, has_arr_arc, has_dep_arc, ils_app,
                                ndb_app, vor_app, vora_app, approach_diff, airport_nav_data_remarks):

        con_db, cursor = self.connect_db()

        # Get icao_code_id on airport_info table:
        cursor.execute(
            "SELECT icao_code_id FROM airport_info WHERE icao_code = (?);", [icao_code])
        result_icao_code_id = cursor.fetchall()[0][0]

        # Insert data for icao_code_id in another table called airport_nav_data
        # insert data
        cursor.execute("INSERT INTO airport_nav_data (icao_code_id,  vfr, vfr_ifr, has_sid, has_star, has_arr_arc, has_dep_arc, ils_app, ndb_app, vor_app, vora_app, approach_diff, airport_nav_data_remarks) \
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (result_icao_code_id, vfr, vfr_ifr, has_sid, has_star, has_arr_arc, has_dep_arc, ils_app, ndb_app, vor_app, vora_app, approach_diff, airport_nav_data_remarks))

        # commit transaction
        con_db.commit()

        # close cursor and connection
        self.close(cursor, con_db)

    # Module working ok! :)
    def insert_diff_flight(self,
                           icao_code_id_dep, icao_code_id_arr, flight_diff_level, flight_diff_remarks):
        """To insert data in the diff_flight table
        It takes 4 params:
        ("SKAR", "SKMZ", 3, "Comentarios AXM-MZL"),
        icao_code_id_dep, icao_code_id_arr, flight_diff_level, and flight_diff_remarks"""

        con_db, cursor = self.connect_db()

        # Get dep icao_code_id on airport_info table:
        cursor.execute("SELECT icao_code_id FROM airport_info WHERE icao_code = (?);", [
                       icao_code_id_dep])
        result_dep_icao_code_id = cursor.fetchall()[0][0]

        # Get arr icao_code_id on airport_info table:
        cursor.execute("SELECT icao_code_id FROM airport_info WHERE icao_code = (?);", [
                       icao_code_id_arr])
        result_arr_icao_code_id = cursor.fetchall()[0][0]

        # insert data
        cursor.execute("INSERT INTO diff_flights (icao_code_id_dep, icao_code_id_arr, flight_diff_level, flight_diff_remarks) \
                VALUES (?, ?, ?, ?)", (result_dep_icao_code_id, result_arr_icao_code_id, flight_diff_level, flight_diff_remarks))

        # commit transaction
        con_db.commit()

        # close cursor and connection
        self.close(cursor, con_db)

    # Module working ok! :)
    def show_icao_codes(self):
        """To take all the icao_codes from the DB.
        The information is added to a list."""
        con_db, cursor = self.connect_db()

        self.icao_codes = []

        # execute command
        cursor.execute("SELECT icao_code FROM airport_info")

        # create a var to name each item in the fetchall()
        icao_code_titles = cursor.fetchall()

        # add each word to a list:
        for row in icao_code_titles:
            self.icao_codes.append(row[0])

        # close cursor and connection
        self.close(cursor, con_db)

    # Module working ok! :)
    def show_icao_codes_lat_lon(self):
        """To take every icao_codes, lat_decimal and lon_decimal from the DB.
        The information is added to a list."""
        con_db, cursor = self.connect_db()

        self.icao_codes_lat_lon = []

        # execute command
        cursor.execute(
            "SELECT icao_code, lat_decimal, lon_decimal FROM airport_info")

        # create a var to name each item in the fetchall()
        self.icao_codes_lat_lon = cursor.fetchall()

        # close cursor and connection
        self.close(cursor, con_db)

    # Module working ok! :)
    def search_diff_flight(self, diff_level):
        """Searches on DB passing the diff_level as param
        search will return a list of 1 flight based on selected difficulty.
        ex: [('SKPE', 4.813, -75.739), ('SKMZ', 5.03, -75.465), "Remarks"]"""

        con_db, cursor = self.connect_db()

        list_diff_flights = []  # To store values from DB.

        cursor.execute("SELECT                                       \
            icao_code_id_dep, icao_code_id_arr, flight_diff_remarks  \
            FROM diff_flights                                        \
            WHERE flight_diff_level = (?);", [diff_level])

        list_diff_flights = cursor.fetchall()

        # select random flight. returns ('1', '12', '')
        temp_diff_flight = choice(list_diff_flights)

        diff_flight = []

        i1, i2, i3 = int(temp_diff_flight[0]), int(
            temp_diff_flight[1]), temp_diff_flight[2]

        cursor.execute("SELECT                               \
            i.icao_code, i.lat_decimal, i.lon_decimal        \
            FROM airport_info i, diff_flights d              \
            WHERE d.icao_code_id_dep = (?) AND d.icao_code_id_dep = i.icao_code_id;", [i1])

        i1_list = cursor.fetchone()
        diff_flight.append(i1_list)

        cursor.execute("SELECT                               \
            i.icao_code, i.lat_decimal, i.lon_decimal        \
            FROM airport_info i, diff_flights d              \
            WHERE d.icao_code_id_arr = (?) AND d.icao_code_id_arr = i.icao_code_id;", [i2])
        i2_list = cursor.fetchone()

        diff_flight.append(i2_list)
        diff_flight.append(i3)

        self.close(cursor, con_db)

        return diff_flight

    # Module working ok! :)
    def extract_airport_data(self, icao_code):
        """Will take an ICAO code as argument and will return a list with:
        ICAO, IATA, name, city, runways, rwy_elev, airport_elev, and remarks.
        """
        con_db, cursor = self.connect_db()

        airport_data = []  # To store values from DB.

        cursor.execute("SELECT                                  \
            icao_code, iata_code, airport_name, city, rwy_avail1, rwy_avail2,  \
            rwy_len, airport_elev,  airport_remarks\
            FROM airport_info                                   \
            WHERE icao_code = (?);", [icao_code])

        airport_data = cursor.fetchall()

        self.close(cursor, con_db)

        return airport_data

    # Module working ok! :)
    def select_dep_airport_reqs(self, dep_query):
        """Makes a query to DB based on departure options checked/unchecked.  Returns [("SKAR", lat, lon)]"""

        con_db, cursor = self.connect_db()
        temp_dep_airport_reqs = []  # To store values from DB.

        cursor.execute(dep_query)
        temp_dep_airport_reqs = cursor.fetchall()

        dep_airport_reqs = []

        # add each icao_code_id to a new list:
        for row in temp_dep_airport_reqs:
            dep_airport_reqs.append(row[0])

        # select one airport from list
        temp_dep_airport = choice(dep_airport_reqs)

        cursor.execute(
            "SELECT icao_code, lat_decimal, lon_decimal FROM airport_info WHERE icao_code_id = (?)", [temp_dep_airport])

        temp_dep_airport = cursor.fetchall()

        self.close(cursor, con_db)

        return temp_dep_airport

    # Module working ok! :)
    def select_arr_airport_reqs(self, arr_query):
        """Makes a query to DB based on arrival options checked/unchecked.  
        Returns a list with all airports: [("SKAR", lat, lon), ("SKAR", lat, lon), ]... or an empty list"""

        con_db, cursor = self.connect_db()

        temp_arr_airport_reqs = []  # To store values from DB.

        cursor.execute(arr_query)
        temp_arr_airport_reqs = cursor.fetchall()

        arr_airport_reqs = []

        # add each icao_code_id to a new list:
        for row in temp_arr_airport_reqs:
            arr_airport_reqs.append(row[0])
        shuffle(arr_airport_reqs)
        shuffle(arr_airport_reqs)

        # final list to return (either empty or with items)
        temp_arr_airport = []

        if len(arr_airport_reqs) >= 1:

            for i in arr_airport_reqs:
                cursor.execute(
                    "SELECT icao_code, lat_decimal, lon_decimal FROM airport_info WHERE icao_code_id = (?)", [i])

                temp_arr_airport_i = cursor.fetchall()
                temp_arr_airport.append(temp_arr_airport_i[0])

        self.close(cursor, con_db)

        return temp_arr_airport
