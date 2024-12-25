import plotly.graph_objects as go
import plotly.io as pio

# Credit goes to Nelson Tang for the straightforward way of creating Plotly templates.
# https://www.nelsontang.com/blog/2021-08-01-build-your-first-plotly-template

pio.templates["Wildcats"] = go.layout.Template(
    # LAYOUT
    layout = {
        # Fonts!
        'title':
            {'font': {'family': 'Campton, Bold, Sans-serif',
                      'size': 32,
                      'color': '#4E2A84',
                      },
            },

        'font': {'family': 'Campton Extra Thin, Sans-serif',
                 'size': 8,
                 'color': '#342F2E'
                },

        # Colorways, which are the default colors of the points, lines, or other 
        #   visualizations on the dataplot...
        #   Northwestern color hue.
        'colorway': ['#4E2A84'], # first color is NU purple

        'hovermode': 'x unified',
        'plot_bgcolor': 'white',
        'paper_bgcolor': 'white',

        'xaxis': {'showgrid': False,
                  'showticklabels': False, # hide the years of label
                  'scaleratio': 2,
                  'type': 'category',
                  'categoryorder': 'category ascending',
                 },

        'yaxis': {'showgrid': False, 
                  'zeroline': True, 
                  'zerolinecolor': '#342F2E', 
                  'zerolinewidth': 3, 
                  'type': 'linear',
                  'showticklabels': False,
                  'visible' : True, # Need this to be true to show the timeline "line", though by default this is already True.
                  #'automargin': 'height', 
                },

        # This makes sure that super small text is not displayed on the graph
        'uniformtext_minsize': 8, 
        'uniformtext_mode': 'hide',
        # 'autosize' : False,
        # 'height' : 24 * 8,
        # 'width' : 56 * 5
    },


    # Formatting specfic to the type of plot used.
    data = {
        # Each graph object must be in a tuple or list for each trace
        'scatter': [go.Scatter(
                               # texttemplate = '%{value:$.2s}',
                               # textposition='bottom center',
                               textfont={'family': 'Campton Extra Thin, Sans-serif',
                                       'size': 16,
                                       'color': '#842a2a'
                                       },
                               marker = {'symbol': 'octagon',
                                         'size': 8,
                                        }
                               ),
                    ],
    }
)