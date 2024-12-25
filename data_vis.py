# Python 3.10.5
# This program takes in .csv or .json files and turns the data in 
# them into pretty visualizations.

# For the GUI, use Tkinter
# For the data visualization, use Plotly
# Also, used Kaleido for image writing via Plotly (saving plotly plots as images).
import pandas as pd
import plotly.express as px
import nu_template # pylance says this template is not accessed, but it really is (for the template itself...)
import os # For finding the folder we want to get our input files from 
import numpy as np # Just to create an array of 0s
import textwrap # Used for the timeline events text boxes


# --------------------------------------
# HELPER FUNCTIONS
# --------------------------------------
# Helper function for creating the event text boxes.
# width is number of characters that are on a single line before breakline occurs
def __customwrap(string):
    formatted_string =  "<br>".join(textwrap.wrap(string, width = 24))
    return formatted_string
    

# This is a helper function that scales the x-axis if the user chooses to do so.
# Basically, this fills in the dates that are empty.
def __scale_x_timeline(df : pd.DataFrame):
    # Going through all of the years...
    for index, d in enumerate(df['Year'].diff()):
        # Though, if we find a different with the CURRENT row, the we want to adjust the PREVIOUS row,
        # Note that the row at index = 0 will always have .diff() of NaN.
        if d > 1:
            # Then, going through the years that have no events (between 2 specific years)
            for i in range(1,  int(d)):
                # print(df.iloc[index, 0])
                new_row = pd.DataFrame({'Year': [df.iloc[index, 0] - i], 'Event': ['IGNORE']})
                # print(new_row)
                df = pd.concat([df,new_row])
            # print(d)
    
    # Then, after appending to the dataframe, make sure to sort the years so that the newly appended years are in chronological order.
    # This also updates the indices of the rows
    df = df.sort_values(by=['Year'], ignore_index=True, ascending=True)
    # print(df)

    return df


# --------------------------------------
# TIMELINE-CREATOR FUNCTION
# --------------------------------------
# __timeline_chart() is actually a scatterplot underneath...
# Accepts is_scaled to provide a timeline that is scaled, shows dates apart.
def __timeline_chart(df : pd.DataFrame, is_scaled = False, plot_title = "Default Title") :
    # Scaling the x-axis to have non-constant spacing between each year.
    if is_scaled:
        df = __scale_x_timeline(df)
        
    # NOTE: width and height parameters are in here because without them, the 'event' text box annotations would be squished
    # NOTE: may want to adjust width and height depending on the number of rows and columns
    num_rows, num_columns = df.shape

    # NOTE: currently relying on Plotly's auto-sizing for the height of the plot.
    #   This leaves quite a bit of empty space when is_scaled = False and all of the event textboxes are below the timeline.
    fig = px.scatter(df, 
                     x = 'Year', 
                     y = np.zeros(len(df.loc[:, 'Event'])), # Filling y-axis data with all 0's so that the events are on the x-axis line
                     title = plot_title,  
                     template = 'Wildcats', 
                     width = 150 * num_rows, # We need this custom width calculation or else the timeline will squish the events together, causing overlapping event boxes
                     )
    
    # Updating the label names so that they do not appear on the timeline
    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="")

    # Going through each row of data
    for row in df.itertuples():
        index, year, event = row

        # This is to determine whether event text box is below or above the timeline line
        box_posn = 1

        # This 'if' is to alterate event text box position to be above the x-axis line if year is even.
        #   aka, 1 on top, 1 on bottom, 1 on top, etc...
        #   This is so that we can avoid overlapping text boxes.
        if (year % 2 == 0) and is_scaled:
            box_posn = -1
        
        # This is so that we do not add year + event textbox for the filler dates in our 
        #   scaled timeline plot.
        if (event != 'IGNORE'):
            # Adding the event textbox
            fig.add_annotation(
                x = index,
                y = 0,
                text = __customwrap(event),
                yanchor ='bottom',
                showarrow = True,
                arrowhead = 0,
                arrowsize = 1,
                arrowwidth = 2,
                arrowcolor = '#4E2A84',
                ax = 0,
                ay = 108 * box_posn,
                align = "center",
                bordercolor = '#4E2A84',
                borderwidth = 2,
                font = {'family' : 'Campton',
                        'size' : 8},
                bgcolor = "white",
            )

            # Adding the year
            fig.add_annotation(
                x = index,
                y = 0,
                showarrow = True,
                arrowhead = 0,
                arrowsize = 1,
                arrowwidth = 2,
                text = year,
                ax = -16,
                ay = -16 * box_posn,
                align = "center",
                arrowcolor = '#4E2A84',
                font = {'family' : 'Campton', 'size' : 12}
            )

    return fig


# --------------------------------------
# MAIN FUNCTION
# --------------------------------------
# Parameters: csv_name, chart_type (timeline, pie, bar, etc...), img_name, img_filetype
# OVERRIDE PARAMETERS: header = 0
# (like, if this is wrong, the user has the option of changing them)
def csv_to_img(input_filepath : str,
               output_filepath : str,
               output_filename : str, # NOTE: as of right now, we are using /images/ folder as a place to store our output images. 
                                        # In the future, giving the user an option as to where to store images would be preferred.
               chart_type : str,
               is_scaled : str,
               plot_title: str):
    """
    Converts user-inputted .csv file and turns it to a plot image.

    Parameters
    ----------
    input_filepath
        str
        filetype must be either a .csv or .json file
    output_filepath
        str
    output_filename
        str
    plot_title
        str
        what we want the title of the timeline to appear at the top of the timeline
    is_scaled
        bool
        if we want our timeline to be scaled or not

    Returns
    -------
    none (though, it does create a file in the specified filepath)
    """

    # https://plotly.com/python/static-image-export/
    # This just creates a folder to save our images.
    if not os.path.exists('images'):
        os.mkdir('images')


    # Detecting the filetype, must be either .csv or .json
    # Load the file as a Pandas Dataframe
    # Though, with large files, we would want to break down the input file into chunks 
    #   to not load the whole dataset into memory.
    # NOTE: This is very case sensitive. Future versions should make this check case insensitive
    if input_filepath.endswith('.csv'):
        df = pd.read_csv(input_filepath)
    elif input_filepath.endswith('.json'):
        df = pd.read_json(input_filepath)
    else:
        print("Unknown Filetype")
        print(input_filepath)
        exit() # TODO: this might bring up some problems...
        

    # Other types of charts would be added here.
    match chart_type:
        case 'timeline':
            fig = __timeline_chart(df, is_scaled, plot_title)


    # Convert the Plotly plot to a PNG image
    # NOTE: needed kaleido 0.1.0post1 to save the image or else terminal hangs!
    #   pip install kaleido==0.1.0post1
    fig.write_image(output_filepath + output_filename, scale = 6)

# TODO: should this work with absolute directories to work alongside the GUI???
# csv_to_img(input_filepath="./test-files/King_County_History_Timeline.csv", 
#            output_filename="timeline2_category_CSV.png", 
#            output_filepath="images/",
#            chart_type='timeline',
#            is_scaled= True, 
#            plot_title = "King County History Timeline")
# 
# csv_to_img(input_filepath="./test-files/King_County_History_Timeline.json", 
#            output_filename="timeline2_category_JSON.png", 
#            output_filepath="images/",
#            chart_type='timeline',
#            is_scaled= True, 
#            plot_title = "King County History Timeline")
# csv_to_img("King_County_History_Timeline_SHORT.csv", "./test-files/", "timeline", "timeline3_category.png", "images/",  is_scaled= True, plot_title = "King County History Timeline")