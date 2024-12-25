import customtkinter as ctk
from tkinter import font
import data_vis


input_filepath = ""
output_filename = ""
timeline_title = ""
is_scaled = False

# Default, testing button
def button_function():
    print("button pressed")

def set_input_filepath():
    global input_filepath
    input_filepath = ctk.filedialog.askopenfilename()
    print(input_filepath)

def set_output_filename():
    global output_filename
    output_filename = output_text.get()
    print(output_filename)

def set_timeline_title():
    global timeline_title 
    timeline_title = timeline_title_text.get()
    print(timeline_title)

def set_scaled():
    global is_scaled
    is_scaled = scaled_switch.get()
    print(is_scaled)

# Calls data_vis to create data visualization timeline
def create_image():

    data_vis.csv_to_img(input_filepath= input_filepath, 
                        output_filename = output_filename, 
                        output_filepath = "images/",
                        chart_type = 'timeline',
                        is_scaled = is_scaled, 
                        plot_title =  timeline_title)
    print("Done!")

# --------------------------------------
# MAIN LOOP BELOW
# --------------------------------------
# This will be the front end that interacts with data_vis.py
# TODO: create custom theme based on Northwestern University.
# Like, include the Northwestern logo
ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
ctk.set_default_color_theme("./gui_nu_theme.json")  # Themes: blue (default), dark-blue, green

# Creating the window
app = ctk.CTk()  # create CTk window like you do with the Tk window
app.title("Nice Data Visualization")
app.grid_columnconfigure((1, 2, 3), weight = 1)

# --------------------------------------
# IMPLEMENTING INTERACTIONS WITH DATA_VIS BELOW
# --------------------------------------
# 0. Setup side bar
# 1. input file directory, which should also include the filename! (of csv or JSON)
# 2. output folder directory (where we save the folder) TODO: will be implemented in future versions
# 3. output filename (what we want to save image as!)
# 4. timeline title
# 5. scaled vs unscaled, true or false

# 0. sidebar
sidebar_frame = ctk.CTkFrame(master = app, width = 150, corner_radius = 3)
sidebar_frame.grid(row = 0, column = 0, rowspan = 5, sticky="NSEW")
sidebar_frame.grid_rowconfigure(4, weight = 2)

program_title = ctk.CTkLabel(master = sidebar_frame, text="Nice Data Visualizer")
program_title.grid(row=0, column=0, padx=20, pady=(20, 10))

# 1. Ask for file directory
input_file = ctk.CTkButton(master= sidebar_frame, text='Open Input File', command = set_input_filepath)
input_file.grid(row = 1, column = 0, padx=0, pady=(20, 10))


# 2. Output folder directory
# WILL BE IMPLEMENTED IN THE FUTURE


# 3. Output filename (NOTE: make sure to also include image file format as well!)
output_text = ctk.CTkEntry(app, placeholder_text="Enter Image Name")
output_text.grid(row = 1, column = 1, columnspan = 3, padx=(20, 0), pady=(20, 20), sticky="W")
output_text_button = ctk.CTkButton(master = app, text="Enter", border_width= 3, command = set_output_filename)
output_text_button.grid(row = 1, column = 2, padx=(0, 20), pady=(20, 20), sticky="W")


# 4. Have user enter timeline title
timeline_title_text = ctk.CTkEntry(master = app, placeholder_text="Enter Timeline Name")
timeline_title_text.grid(row = 2, column = 1, columnspan = 3, padx=(20, 0), pady=(20, 20), sticky="W")
timeline_title_text_button = ctk.CTkButton(master = app, text="Enter", border_width=2, command = set_timeline_title)
timeline_title_text_button.grid(row = 2, column=2, padx=(0, 20), pady=(20, 20), sticky="W")


# 5. Have slider for scaled vs unscaled
scaled_switch = ctk.CTkSwitch(master = app, text='Scaled Timeline', command= set_scaled)
scaled_switch.grid(row= 3, column=1, padx=(20, 20), pady=(20, 20))


# 6. Have button to create the file!
image_button = ctk.CTkButton(master = app, text = "Create image!", border_width = 2, command = create_image)
image_button.grid(row = 4, column = 1, columnspan = 3, padx = (20, 20), pady = (20, 20), sticky='NSEW')


app.mainloop()