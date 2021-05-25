#  Flight Gen!
#  Windows version.

# Requirements:     1. Python 3
#                   2. pillow in all python win installs???   (if installed on Mac, it's mandatory)


############################
#####   TO IMPLEMENT   #####
# 1.


######################
#####   TO FIX   #####
# 1.

######################
#####   BUGS TO CRUSH!!   #####
# 1.

############################################

import os
import tkinter as tk
import webbrowser
# import PyQt5
# import numpy.core
# import Tkinter
# import PIL

from tkinter import Menu
from tkinter import messagebox as msg
from tkinter import ttk
from tkinter import scrolledtext
from PIL import ImageTk
from PIL import Image
from datetime import timedelta
from random import randrange
from random import choice
from random import shuffle
from math import radians
from math import cos
from math import sin
from math import asin
from math import sqrt
from math import atan2
from math import degrees

from db_manager import DBManager_sqlite
from gui_maker import GuiMaker


program_name = "Flight Gen!"
version = "Version 1.3 for Windows"

######  Instances  ##############
gui_maker = GuiMaker()
db_manager_sqlite = DBManager_sqlite()

db_icao_codes = db_manager_sqlite.icao_codes
db_icao_codes_lat_lon = db_manager_sqlite.icao_codes_lat_lon
###################################

dep_arr_airports = []
diff_flight = []
possible_dep_airports = []  # to hold the dep airports that fulfil the requirements
possible_arr_airports = []  # to hold the arr airports that fulfil the requirements


def about():
    """To display the info about this program"""
    msg.showinfo("About", "{}                  \n{}\n\nBy Nicolás Táutiva\nnicolastautiva@hotmail.com".format(
        program_name, version))


def _open_website():
    """Small function to open my web site"""
    url = 'www.nicolastautiva.com'
    webbrowser.open(url, new=0, autoraise=True)


def _icao_codes_Guide():
    """Function to show the ICAO_code guide on a PDF file"""
    os.startfile("ICAO_codes.pdf")


def _userGuide():
    """Function to show the user guide on a PDF file"""
    os.startfile('flightGen_guide.pdf')


def clean_selection_data():
    """It deleted data in the Departure and Arrival Frame, so that
    the user can start all over again."""
    # set option for dep radio buttons to 1
    # delete checkbuttons
    dep_option_val.set("dep_random_airport")
    dep_ran_selected()
    arr_option_val.set("arr_random_airport")
    arr_ran_selected()
    # set option for arr radio buttons to 1


def clean_results_data():
    """It deletes all data in the Result Frame"""
    results_lbl = [lbl41, lbl43, lbl45, lbl47, lbl49, lbl51, lbl53,
                   lbl61, lbl63, lbl65, lbl67, lbl69, lbl71, lbl73,
                   lbl81, lbl83, lbl85]

    for i in results_lbl:
        i.config(text="")

    remarks_scrl.delete(1.0, "end")


def desition_maker():
    """Is called be the desition options.  
    It returns 'yes' or 'no'"""
    desition = randrange(2)
    if desition == 1:
        return "yes"
    else:
        return "no"


def holding():
    """To make a desition"""
    desition = desition_maker()

    messg = "Proceed to the holding?"
    if desition == "yes":
        msg.showwarning(messg, "Yes...  Proceed to the holding!")
    else:
        msg.showerror(messg, "No... you can continue your approach.")


def missed_app():
    """To make a desition"""
    desition = desition_maker()

    messg = "Make missed approach?"
    if desition == "yes":
        msg.showwarning(messg, "Yes...  make missed approach!")
    else:
        msg.showerror(messg, "No... you can continue your approach.")


def alternate():
    """To make a desition"""
    desition = desition_maker()

    messg = "Should I proceed to the alternate?"
    if desition == "yes":
        msg.showwarning(messg, "Yes...  proceed to your alternate!")
    else:
        msg.showerror(messg, "No... try to land in your destination.")


def yes_no():
    """To make a desition"""
    desition = desition_maker()

    messg = "Yes or No ?"

    if desition == "yes":
        msg.showwarning(messg, "Yes...  the answer is YES!")
    else:
        msg.showerror(messg, "No...  the answer is NO")


def inject_data_to_GUI(airports, dep_data, arr_data, dist_def, bear_def):
    """Takes info for every airport and injects into result_frame GUI
    [('SKPB', 12.221, -71.985), ('SKPA', 5.767467, -73.114944)]
    [('SKPB', 'N/A', 'PUERTO BOLIVAR', 'PUERTO BOLIVAR', 9, 0, 1591, 90, '')]
    [('SKPA', 'N/A', 'JUAN JOSE RONDON', 'PAIPA', 4, 0, 1698, 8205, '')]
    [('SKPE', 4.813, -75.739), ('SKMZ', 5.03, -75.465), "Remarks"].... from search_diff_flight()
    """

    # Variable assignement for dep
    icao_data = dep_data[0][0]
    iata_data = dep_data[0][1]
    name_data = dep_data[0][2]
    city_data = dep_data[0][3]
    rwy1_data = dep_data[0][4]
    rwy2_data = dep_data[0][5]
    if rwy2_data == 0:
        rwy2_data = ""
    else:
        rwy2_data = "- {}/{}".format(rwy2_data, rwy2_data + 18)
    rwy_len_data = dep_data[0][6]
    airport_elev_data = dep_data[0][7]
    # airport_remark_data = dep_data[0][8]  # Not implemented yet!

    # injects Dep info
    lbl41.config(text=icao_data)
    lbl43.config(text=iata_data)
    lbl45.config(text=name_data)
    lbl47.config(text=city_data)
    lbl49.config(text="{}/{} {}".format(rwy1_data, rwy1_data + 18, rwy2_data))
    lbl51.config(text="{}'".format(airport_elev_data))
    lbl53.config(text="{} mts".format(rwy_len_data))

    # Variable assignement for arr
    icao_data = arr_data[0][0]
    iata_data = arr_data[0][1]
    name_data = arr_data[0][2]
    city_data = arr_data[0][3]
    rwy1_data = arr_data[0][4]
    rwy2_data = arr_data[0][5]
    if rwy2_data == 0:
        rwy2_data = ""
    else:
        rwy2_data = "- {}/{}".format(rwy2_data, rwy2_data + 18)
    rwy_len_data = arr_data[0][6]
    airport_elev_data = arr_data[0][7]
    # airport_remark_data = arr_data[0][8]  # Not implemented yet!

    # injects Dep info
    lbl61.config(text=icao_data)
    lbl63.config(text=iata_data)
    lbl65.config(text=name_data)
    lbl67.config(text=city_data)
    lbl69.config(text="{}/{} {}".format(rwy1_data, rwy1_data + 18, rwy2_data))
    lbl71.config(text="{}'".format(airport_elev_data))
    lbl73.config(text="{} mts".format(rwy_len_data))

    # inject remarks info:
    lbl81.config(text="{} degrees".format(bear_def))
    lbl83.config(text="{} nm".format(dist_def))
    min = (dist_def / int(speed_combo.get())) * 60
    lbl85.config(text=str(timedelta(minutes=min))[:-3])
    try:
        remarks = airports[2]
        # Insert the remarks into the scrolledtext.
        remarks_scrl.insert(tk.INSERT, remarks)

        # lbl85.config(text=remarks)
    except:
        pass


def extract_airport_data(airports):
    """Takes one array (list or tuple) like these ones:
    [('SKPE', 4.813, -75.739), ('SKMZ', 5.03, -75.465), "Remarks"].... from search_diff_flight()
    or
    [('SKAR', 4.454, -75.765), ('SKBC', 9.045, -73.975)]... from random generator
    Takes list, searches on DB and takes info for the results frame:
    for dep and arrival:  ICAO, IATA, name, city, and runways
    Calculates course, distance and in case of diff_flight, injects any remarks
    """
    msg.showwarning(
        "Success!", "Check the details for your flight.\n\n                 HAVE FUN!!")

    # search for data in db for [0] and [1]
    dep_data = db_manager_sqlite.extract_airport_data(airports[0][0])
    arr_data = db_manager_sqlite.extract_airport_data(airports[1][0])

    lat_1, lon_1 = airports[0][1], airports[0][2]
    lat_2, lon_2 = airports[1][1], airports[1][2]
    dist_def, bear_def = haversine(lat_1, lon_1, lat_2, lon_2)

    # Injects info in GUI
    inject_data_to_GUI(airports, dep_data, arr_data, dist_def, bear_def)


def search_diff_flight():
    """Starts the search for a flight based on difficulty.  It then will call a func to 
    inject data to Results Frame"""
    clean_results_data()
    diff_level = flight_difficulty_combo.get()[:1]

    # create a search on DB passing the num as param
    # search will return a list of flight based on selected difficulty
    # ex: [('SKPE', 4.813, -75.739), ('SKMZ', 5.03, -75.465), "Remarks"]
    diff_flight = db_manager_sqlite.search_diff_flight(diff_level)

    # inject data to results Frame
    extract_airport_data(diff_flight)


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great distance in nm and the bearing in degrees
    between two points on the earth (specified in decimal degrees).
    Takes Lat1 Lon1, Lat2 Lon2.  Returns:  distance bearing
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 3440.065  # Radius of earth in nm.
    distance = c * r

    # bearing calc:
    bearing = atan2(sin(lon2-lon1)*cos(lat2), cos(lat1) *
                    sin(lat2)-sin(lat1)*cos(lat2)*cos(lon2-lon1))
    bearing = degrees(bearing)
    bearing = (bearing + 360) % 360

    return round(distance, 0), round(bearing, 0)


def calc_time_dist():
    """Takes info from TAS and time combo, and returns a float of
    distance to flight in nm.
    Also returns dist_min and dist_max that are the 10% of dist"""
    dist = (int(speed_combo.get()) / 60) * int(time_combo.get())
    dist = round(dist, 0)
    dist_min = dist - ((dist * 15) / 100)
    dist_max = dist + ((dist * 15) / 100)
    return dist, dist_min, dist_max


def start_search():
    """Takes the user selected options and starts the flight search"""
    clean_results_data()
    # Calculates the distance in nm for the flight
    _, dist_min, dist_max = calc_time_dist()
    dep_arr_airports = []

    ###################################
    # Search for the departure airport
    ###################################
    if dep_option_val.get() == "dep_random_airport":
        # Select random airport from the DB
        dep_airport = choice(db_manager_sqlite.icao_codes_lat_lon)

        # add dep airport to list.
        dep_arr_airports.append(dep_airport)

    elif dep_option_val.get() == "dep_selected_airport":
        temp_dep_airport = dep_airport_combo.get()

        for i in db_manager_sqlite.icao_codes_lat_lon:
            if i[0] == temp_dep_airport:
                temp_index = db_manager_sqlite.icao_codes_lat_lon.index(i)

                temp_dep_airport = db_manager_sqlite.icao_codes_lat_lon[temp_index]

                # add dep airport to list.
                dep_arr_airports.append(temp_dep_airport)
    else:
        # To catch every checkbutton answer and add it to a dict
        _i = [dep_vfr_var, dep_vfr_ifr_var, dep_sid_var, dep_arc_var]

        dep_reqs = {"vfr": "False",
                    "vfr_ifr": "False",
                    "has_sid": "False",
                    "has_dep_arc": "False"}

        for i in _i:
            if i.get() != "False":
               # dep_reqs to dictionary
                dep_reqs[i.get()] = "True"

        # vfr_ifr in case other IFR options are checked
        if (dep_reqs["has_sid"] == "True") or (dep_reqs["has_dep_arc"] == "True"):
            dep_reqs["vfr_ifr"] = "True"

        if dep_reqs["has_dep_arc"] == "True":
            dep_reqs["has_sid"] = "True"

        dep_query = 'SELECT icao_code_id from airport_nav_data where("vfr"= "{}") AND("vfr_ifr"="{}") AND("has_sid"="{}") AND("has_dep_arc"="{}");'.format(
            dep_reqs["vfr"], dep_reqs["vfr_ifr"], dep_reqs["has_sid"], dep_reqs["has_dep_arc"])

        # Sends a query to DB based on options checked/unchecked.  Returns ("SKAR", lat, lon)
        temp_dep_airport = db_manager_sqlite.select_dep_airport_reqs(dep_query)

        dep_arr_airports.append(temp_dep_airport[0])

    ###################################
    # Search for the arrival airport
    ###################################
    if arr_option_val.get() == "arr_random_airport":
        # Shuffle list of airports
        shuffle(db_manager_sqlite.icao_codes_lat_lon)

        for temp_arr_airport in db_manager_sqlite.icao_codes_lat_lon:
            # take the 2 coordinates and find dist and bearing.
            dep_dist, _ = haversine(
                (dep_arr_airports[0][1]), dep_arr_airports[0][2],
                temp_arr_airport[1], temp_arr_airport[2])

            # check if dist btn dep and arr match user requirement.
            if (dep_dist >= dist_min) and (dep_dist <= dist_max):
                # add dep airport to definitive dep_arr list.
                dep_arr_airports.append(temp_arr_airport)
                break

        if len(dep_arr_airports) == 1:
            msg.showerror("Sorry, no results found.",
                          "No results for your requirements.  Change the options and try again!")
        else:
            extract_airport_data(dep_arr_airports)

    elif arr_option_val.get() == "arr_selected_airport":
        temp_arr_airport = arr_airport_combo.get()

        for i in db_manager_sqlite.icao_codes_lat_lon:
            if i[0] == temp_arr_airport:
                temp_index = db_manager_sqlite.icao_codes_lat_lon.index(i)

                temp_arr_airport = db_manager_sqlite.icao_codes_lat_lon[temp_index]

                # add dep airport to definitive dep_arr list.
                dep_arr_airports.append(temp_arr_airport)

        if dep_arr_airports[0][0] == arr_airport_combo.get():
            msg.showerror(
                "ERROR!", "Departure airport and Arrival airport should be different!")

        extract_airport_data(dep_arr_airports)

    else:
        # Read selected options:
        # To catch every checkbutton answer and add it to a dict
        _ii = [arr_vfr_var, arr_vfr_ifr_var, arr_star_var, arr_arc_var,
               arr_ils_var, arr_ndb_var, arr_vor_var, arr_vora_var]

        arr_reqs = {"vfr": "False",
                    "vfr_ifr": "False",
                    "has_star": "False",
                    "has_arr_arc": "False",
                    "ils_app": "False",
                    "ndb_app": "False",
                    "vor_app": "False",
                    "vora_app": "False"}

        for i in _ii:
            if i.get() != "False":
               # arr_reqs to dictionary
                arr_reqs[i.get()] = "True"

        # vfr_ifr in case other IFR options are checked
        if (arr_reqs["has_star"] == "True") or (arr_reqs["has_arr_arc"] == "True") or (arr_reqs["ils_app"] == "True") or (arr_reqs["ndb_app"] == "True") or (arr_reqs["vor_app"] == "True") or (arr_reqs["vora_app"] == "True"):
            arr_reqs["vfr_ifr"] = "True"

        if arr_reqs["has_arr_arc"] == "True":
            arr_reqs["has_star"] = "True"

        arr_diff = arr_difficulty_combo.get()[0]
        arr_query = 'SELECT icao_code_id from airport_nav_data where("vfr"="{}") AND("vfr_ifr"="{}") AND("has_star"="{}") AND("has_arr_arc"="{}") AND("ils_app"="{}") AND("ndb_app"="{}") AND("vor_app"="{}") AND("vora_app"="{}") AND("approach_diff"={});'.format(
            arr_reqs["vfr"], arr_reqs["vfr_ifr"], arr_reqs["has_star"], arr_reqs["has_arr_arc"],
            arr_reqs["ils_app"], arr_reqs["ndb_app"], arr_reqs["vor_app"], arr_reqs["vora_app"], int(arr_diff))

        # Sends a query to DB based on options checked/unchecked.
        temp_arr_airport = db_manager_sqlite.select_arr_airport_reqs(
            arr_query)

        if len(temp_arr_airport) == 0:
            msg.showerror("Sorry, no results found.",
                          "No results for your requirements.  Change the options and try again!")

        else:
            for i in temp_arr_airport:
                # Check if airport fulfills the user requirements of distance
                # take the 2 coordinates and find dist and bearing.
                arr_dist, _ = haversine(
                    (dep_arr_airports[0][1]), dep_arr_airports[0][2],
                    i[1], i[2])

                # check if dist btn dep and arr match user requirement.
                if (arr_dist >= dist_min) and (arr_dist <= dist_max):
                    # add dep airport to definitive dep_arr list.
                    dep_arr_airports.append(i)
                    break

            if len(dep_arr_airports) == 1:
                msg.showerror("Sorry, no results found.",
                              "No results for your requirements.  Change the options and try again!")
            else:
                extract_airport_data(dep_arr_airports)


##################################
######   GUI OF MAIN PAGE  #######
##################################
window = tk.Tk()
window.title("     " + program_name)
window.geometry("1000x760")
window.resizable(False, False)
icon_route = "images/main_ico.ico"
window.wm_iconbitmap(icon_route)

main_header = tk.PhotoImage(
    file='images/main_header.gif')
main_header_gif = tk.Label(window, image=main_header)
main_header_gif.place(x=0, y=0)


gui_maker.create_label(
    window, "lbl1", "1.  Indicate the TAS for your flight today : ", 30, 60)

speed_combo = ttk.Combobox(window, width=5, state="readonly")
speed_combo["values"] = ("100", "120", "140", "160", "180",
                         "200", "220", "240", "260", "280", "300", "340", "380", "420", "460")
speed_combo.current([7])
speed_combo.place(x=260, y=60)

gui_maker.create_label(
    window, "lbl1", " ... and the time available for your flight today :                         minutes. ", 330, 60)

time_combo = ttk.Combobox(window, width=5, state="readonly")
time_combo["values"] = ("30", "45", "60", "75", "90",
                        "105", "120", "150", "180", "210", "240")
time_combo.current([4])
time_combo.place(x=590, y=60)

gui_maker.create_label(
    window, "lbl2", "2.  Select the way you want to create your flight : ", 30, 90)

########################
# Notebook
main_notebook = ttk.Notebook(window)
rel_data = 0.81
window_tab1 = ttk.Frame(main_notebook)
main_notebook.add(window_tab1, text=" Selection based on details ")
main_notebook.place(x=50, y=120, relwidth=0.5, relheight=rel_data)

# Departure Frame
departure_frame = ttk.LabelFrame(
    window_tab1, text="  Select one option for your departure airport : ")
departure_frame.place(x=25, y=15, relheight=0.31, relwidth=0.9)


def disable_dep_checkbuttons():
    dep_vfr_ifr_option.config(state=tk.DISABLED)
    dep_sid_option.config(state=tk.DISABLED)
    dep_arc_option.config(state=tk.DISABLED)


def set_dep_options_unchecked():
    dep_vfr_ifr_var.set("False")
    dep_sid_var.set("False")
    dep_arc_var.set("False")


def dep_ran_selected():
    dep_airport_combo.config(state=tk.DISABLED)
    disable_dep_checkbuttons()
    set_dep_options_unchecked()


def dep_sel_selected():
    dep_airport_combo.config(state=tk.NORMAL)
    dep_airport_combo.config(state="readonly")
    disable_dep_checkbuttons()
    set_dep_options_unchecked()


def dep_opt_selected():
    dep_airport_combo.config(state=tk.DISABLED)
    dep_vfr_ifr_option.config(state=tk.NORMAL)
    dep_sid_option.config(state=tk.NORMAL)
    dep_arc_option.config(state=tk.NORMAL)


dep_option_val = tk.StringVar()
dep_random_airport = ttk.Radiobutton(
    departure_frame, text="Select random airport.", variable=dep_option_val,
    value="dep_random_airport", command=dep_ran_selected)
dep_random_airport.place(x=30, y=10)

dep_selected_airport = ttk.Radiobutton(
    departure_frame, text="Depart from this airport:", variable=dep_option_val,
    value="dep_selected_airport", command=dep_sel_selected)
dep_selected_airport.place(x=30, y=40)

# Update this tuple from the DB
dep_airport_combo = ttk.Combobox(departure_frame, width=10, state="readonly")
dep_airport_combo["values"] = db_icao_codes
dep_airport_combo.current([0])
dep_airport_combo.place(x=210, y=40)


dep_detailed_airport = ttk.Radiobutton(
    departure_frame, text="Departure airport must have: ", variable=dep_option_val,
    value="dep_options_airport", command=dep_opt_selected)
dep_detailed_airport.place(x=30, y=70)

dep_vfr_var = tk.StringVar()
dep_vfr_option = ttk.Checkbutton(departure_frame, text="Only VFR operations.",
                                 state=tk.DISABLED, variable=dep_vfr_var,
                                 onvalue="vfr", offvalue="False")
dep_vfr_option.place(x=210, y=72)
dep_vfr_var.set("vfr")

dep_vfr_ifr_var = tk.StringVar()
dep_vfr_ifr_option = ttk.Checkbutton(
    departure_frame, text="VFR and IFR operations.", variable=dep_vfr_ifr_var,
    onvalue="vfr_ifr", offvalue="False")
dep_vfr_ifr_option.place(x=210, y=92)

dep_sid_var = tk.StringVar()
dep_sid_option = ttk.Checkbutton(
    departure_frame, text="SID.", variable=dep_sid_var,
    onvalue="has_sid", offvalue="False")
dep_sid_option.place(x=210, y=112)

dep_arc_var = tk.StringVar()
dep_arc_option = ttk.Checkbutton(
    departure_frame, text="SID with an arc on the departure.", variable=dep_arc_var,
    onvalue="has_dep_arc", offvalue="False")
dep_arc_option.place(x=210, y=132)

dep_option_val.set("dep_random_airport")
dep_ran_selected()


# Arrival Frame

def disable_arr_checkbuttons():
    arr_ifr_option.config(state=tk.DISABLED)
    arr_star_option.config(state=tk.DISABLED)
    arr_arc_option.config(state=tk.DISABLED)
    arr_ils_option.config(state=tk.DISABLED)
    arr_ndb_option.config(state=tk.DISABLED)
    arr_vor_option.config(state=tk.DISABLED)
    arr_vora_option.config(state=tk.DISABLED)
    lbl5.config(state=tk.DISABLED)
    arr_difficulty_combo.config(state=tk.DISABLED)


def set_arr_options_unchecked():
    arr_vfr_ifr_var.set("False")
    arr_star_var.set("False")
    arr_arc_var.set("False")
    arr_ils_var.set("False")
    arr_ndb_var.set("False")
    arr_vor_var.set("False")
    arr_vora_var.set("False")


def arr_ran_selected():
    arr_airport_combo.config(state=tk.DISABLED)
    disable_arr_checkbuttons()
    set_arr_options_unchecked()


def arr_sel_selected():
    arr_airport_combo.config(state=tk.NORMAL)
    arr_airport_combo.config(state="readonly")
    disable_arr_checkbuttons()
    set_arr_options_unchecked()


def arr_opt_selected():
    arr_airport_combo.config(state=tk.DISABLED)
    arr_ifr_option.config(state=tk.NORMAL)
    arr_star_option.config(state=tk.NORMAL)
    arr_arc_option.config(state=tk.NORMAL)
    arr_ils_option.config(state=tk.NORMAL)
    arr_ndb_option.config(state=tk.NORMAL)
    arr_vor_option.config(state=tk.NORMAL)
    arr_vora_option.config(state=tk.NORMAL)
    lbl5.config(state=tk.NORMAL)
    arr_difficulty_combo.config(state=tk.NORMAL)
    arr_difficulty_combo.config(state="readonly")


arrival_frame = ttk.LabelFrame(
    window_tab1, text="  Now select one option for your arrival airport : ")
arrival_frame.place(x=25, y=205, relheight=0.49, relwidth=0.9)


arr_option_val = tk.StringVar()
arr_random_airport = ttk.Radiobutton(
    arrival_frame, text="Select random airport     (Considering your time available).",
    variable=arr_option_val, value="arr_random_airport", command=arr_ran_selected)
arr_random_airport.place(x=30, y=10)

arr_selected_airport = ttk.Radiobutton(
    arrival_frame, text="Select this airport for arrival:", variable=arr_option_val,
    value="arr_selected_airport", command=arr_sel_selected)
arr_selected_airport.place(x=30, y=40)

# Update this tuple from the DB
arr_airport_combo = ttk.Combobox(arrival_frame, width=10, state="readonly")
arr_airport_combo["values"] = db_icao_codes
arr_airport_combo.current([0])
arr_airport_combo.place(x=210, y=40)


arr_detailed_airport = ttk.Radiobutton(
    arrival_frame, text="Arrival airport must have: ", variable=arr_option_val,
    value="arr_options_airport", command=arr_opt_selected)
arr_detailed_airport.place(x=30, y=70)

arr_vfr_var = tk.StringVar()
arr_vfr_option = ttk.Checkbutton(arrival_frame, text="Only VFR operations.",
                                 state=tk.DISABLED, variable=arr_vfr_var,
                                 onvalue="vfr", offvalue="False")
arr_vfr_option.place(x=210, y=72)
arr_vfr_var.set("vfr")

arr_vfr_ifr_var = tk.StringVar()
arr_ifr_option = ttk.Checkbutton(
    arrival_frame, text="VFR and IFR operations.", variable=arr_vfr_ifr_var,
    onvalue="vfr_ifr", offvalue="False")
arr_ifr_option.place(x=210, y=92)

arr_star_var = tk.StringVar()
arr_star_option = ttk.Checkbutton(
    arrival_frame, text="STAR.", variable=arr_star_var, onvalue="has_star", offvalue="False")
arr_star_option.place(x=210, y=112)

arr_arc_var = tk.StringVar()
arr_arc_option = ttk.Checkbutton(
    arrival_frame, text="STAR with an arc on the arrival.", variable=arr_arc_var,
    onvalue="has_arr_arc", offvalue="False")
arr_arc_option.place(x=210, y=132)

arr_ils_var = tk.StringVar()
arr_ils_option = ttk.Checkbutton(
    arrival_frame, text="ILS approach.", variable=arr_ils_var,
    onvalue="ils_app", offvalue="False")
arr_ils_option.place(x=210, y=152)

arr_ndb_var = tk.StringVar()
arr_ndb_option = ttk.Checkbutton(
    arrival_frame, text="NDB approach.", variable=arr_ndb_var,
    onvalue="ndb_app", offvalue="False")
arr_ndb_option.place(x=210, y=172)

arr_vor_var = tk.StringVar()
arr_vor_option = ttk.Checkbutton(
    arrival_frame, text="VOR approach.", variable=arr_vor_var,
    onvalue="vor_app", offvalue="False")
arr_vor_option.place(x=210, y=192)

arr_vora_var = tk.StringVar()
arr_vora_option = ttk.Checkbutton(
    arrival_frame, text="VOR-A approach.", variable=arr_vora_var,
    onvalue="vora_app", offvalue="False")
arr_vora_option.place(x=210, y=212)

lbl5 = ttk.Label(arrival_frame, text="Difficulty level")
lbl5.place(x=228, y=232)

arr_difficulty_combo = ttk.Combobox(
    arrival_frame, width=12, state="readonly")
arr_difficulty_combo["values"] = ("1. Easy", "2. Medium", "3. Hard")
arr_difficulty_combo.current([0])
arr_difficulty_combo.place(x=318, y=232)

arr_option_val.set("arr_random_airport")
arr_ran_selected()


# Buttons:
gui_maker.create_red_button(
    window_tab1, "start_search_btn1", "Start Search", 12, start_search, 100, 500)
gui_maker.create_button(window_tab1, "clean_data_btn1",
                        "Clean Data", 15, clean_selection_data, 310, 510)

# Create another Notebook
window_tab2 = ttk.Frame(main_notebook)
main_notebook.add(window_tab2, text="  Selection based on difficulty  ")
main_notebook.place(x=50, y=120, relwidth=0.5, relheight=rel_data)


gui_maker.create_label(
    window_tab2, "lbl2", "You are about to select a flight based on the difficulty.\n\nThese flights don't take into account your time available, so select one when you\n have enough time to complete the flight.\n\n These flights range between 35 minutes to 1.5 hours at a speed of 240 knots, which\n is the regular speed for the King 350.\n\nThe main objective of these flights is to test your ability to find the route and\n navigate using the charts.\n\nWhen you are ready select the difficulty level and click the red button to search\n for a flight.  Pay special attention to the remarks for the selected flight.  ", 30, 30)

lbl10 = ttk.Label(window_tab2, text="I would like a flight ...", font=20)
lbl10.place(x=40, y=300)

flight_difficulty_combo = ttk.Combobox(
    window_tab2, width=43, state="readonly", font=20)
flight_difficulty_combo["values"] = ("1.  Easy:         This may be too easy for me!",
                                     "2.  Medium:   yeah... I can do that! ",
                                     "3.  Hard:         WTF!... How am I supposed to do this!?")
flight_difficulty_combo.place(x=60, y=340)
flight_difficulty_combo.current([0])

# buttons
gui_maker.create_red_button(
    window_tab2, "create_diff_btn2", "Select a flight for me", 20, search_diff_flight, 150, 450)


########################
# Results Frame
results_frame = ttk.LabelFrame(
    window, text=" 3.  These are the details for your flight.  HAVE FUN!  ")
results_frame.place(x=580, y=135, relheight=0.55, relwidth=0.38)

result_frame_departure = ttk.LabelFrame(
    results_frame, text="  Departure airport : ")
result_frame_departure.place(x=25, y=5, relheight=0.29, relwidth=0.9)

gui_maker.create_label(result_frame_departure, "lbl40", "ICAO:", 20, 10)
lbl41 = ttk.Label(result_frame_departure, text="icao_data")
lbl41.place(x=60, y=10)
gui_maker.create_label(result_frame_departure, "lbl42", "IATA:", 120, 10)
lbl43 = ttk.Label(result_frame_departure, text="iata_data")
lbl43.place(x=160, y=10)
gui_maker.create_label(result_frame_departure, "lbl50",
                       "AD Elev:", 210, 10)
lbl51 = ttk.Label(result_frame_departure, text="elev_data")
lbl51.place(x=270, y=10)
gui_maker.create_label(result_frame_departure, "lbl44",
                       "Airport name:", 20, 30)
lbl45 = ttk.Label(result_frame_departure, text="airport_name_data")
lbl45.place(x=120, y=30)
gui_maker.create_label(result_frame_departure, "lbl46", "City:", 20, 50)
lbl47 = ttk.Label(result_frame_departure, text="city_data")
lbl47.place(x=120, y=50)
gui_maker.create_label(result_frame_departure, "lbl48",
                       "RWY available:", 20, 70)
lbl49 = ttk.Label(result_frame_departure, text="rwys_data")
lbl49.place(x=120, y=70)
gui_maker.create_label(result_frame_departure, "lbl53",
                       "RWY length:", 210, 70)
lbl53 = ttk.Label(result_frame_departure, text="rwy_len_data")
lbl53.place(x=280, y=70)


result_frame_arrival = ttk.LabelFrame(
    results_frame, text="  Arrival airport : ")
result_frame_arrival.place(x=25, y=125, relheight=0.29, relwidth=0.9)

gui_maker.create_label(result_frame_arrival, "lbl60", "ICAO:", 20, 10)

lbl61 = ttk.Label(result_frame_arrival, text="icao_data")
lbl61.place(x=60, y=10)

gui_maker.create_label(result_frame_arrival, "lbl62", "IATA:", 120, 10)
lbl63 = ttk.Label(result_frame_arrival, text="iata_data")
lbl63.place(x=160, y=10)

gui_maker.create_label(result_frame_arrival, "lbl70",
                       "AD Elev:", 210, 10)
lbl71 = ttk.Label(result_frame_arrival, text="elev_data")
lbl71.place(x=270, y=10)

gui_maker.create_label(result_frame_arrival, "lbl64",
                       "Airport name:", 20, 30)
lbl65 = ttk.Label(result_frame_arrival, text="airport_name_data")
lbl65.place(x=120, y=30)

gui_maker.create_label(result_frame_arrival, "lbl66", "City:", 20, 50)
lbl67 = ttk.Label(result_frame_arrival, text="city_data")
lbl67.place(x=120, y=50)

gui_maker.create_label(result_frame_arrival, "lbl68",
                       "RWY available:", 20, 70)
lbl69 = ttk.Label(result_frame_arrival, text="rwys_data")
lbl69.place(x=120, y=70)
gui_maker.create_label(result_frame_arrival, "lbl73",
                       "RWY length:", 210, 70)
lbl73 = ttk.Label(result_frame_arrival, text="rwy_len_data")
lbl73.place(x=280, y=70)


result_frame_remarks = ttk.LabelFrame(
    results_frame, text="  Remarks : ")
result_frame_remarks.place(x=25, y=240, relheight=0.35, relwidth=0.9)

gui_maker.create_label(result_frame_remarks, "lbl80",
                       "Course    (aprox):", 20, 5)
lbl81 = ttk.Label(result_frame_remarks, text="course... 2 b modified")
lbl81.place(x=130, y=5)
gui_maker.create_label(result_frame_remarks, "lbl82",
                       "Distance (aprox):", 20, 25)
lbl83 = ttk.Label(result_frame_remarks, text="distance 2... 2 b modified")
lbl83.place(x=130, y=25)
gui_maker.create_label(result_frame_remarks, "lbl84",
                       "EET:", 210, 25)
lbl85 = ttk.Label(result_frame_remarks, text="Time in minutes")
lbl85.place(x=240, y=25)

remarks_scrl = scrolledtext.ScrolledText(
    result_frame_remarks, width=35, height=3, wrap=tk.WORD)
remarks_scrl.place(x=15, y=50)

########################
# Make Desitions Frame
desition_frame = ttk.LabelFrame(
    window, text="  Use these options to make desitions : ")
desition_frame.place(x=580, y=560, relheight=0.215, relwidth=0.38)

gui_maker.create_button(desition_frame, "holding_btn",
                        "Proceed to the holding?", 25, holding, 15, 20)

gui_maker.create_button(desition_frame, "missed_btn",
                        "Make missed approach?", 25, missed_app, 200, 20)

gui_maker.create_button(desition_frame, "missed_btn",
                        "Proceed to the alternate?", 25, alternate, 15, 70)

gui_maker.create_button(desition_frame, "yes_no_btn",
                        "Yes or No", 25, yes_no, 200, 70)

#############################################
# Creating the menu bar
#############################################
menu_bar = Menu(window)
window.config(menu=menu_bar)

# Creating the menu and adding items
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Exit", command=quit)

help_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(
    label="Go to www.nicolastautiva.com", command=_open_website)
help_menu.add_command(label="ICAO airport list", command=_icao_codes_Guide)
help_menu.add_command(label="User guide", command=_userGuide)
help_menu.add_command(label="About", command=about)

clean_results_data()
window.mainloop()
