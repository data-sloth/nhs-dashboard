# import streamlit as st
import pandas as pd
import pydeck
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colorbar import ColorbarBase
import streamlit as st


# default view state for pydeck map (centred on UK)
VIEW_STATE = pydeck.ViewState(
    latitude=53, longitude=-2, controller=True, zoom=5.5, pitch=0
)

# grayscale display intensity for NA values (max = 255)
NA_VALUE = 100

def set_color_scale(df, feature, na_value=NA_VALUE, higher_is_better=True):
        '''
        Set color scale for a feature in a DataFrame.
        RGB values are calculated based on the feature values, and stored in df.
        Color scales from red to green (or vice versa), green is better.
        '''
        min_val = df[feature].min(skipna=True)
        max_val = df[feature].max(skipna=True)

        def calculate_color(value, na_value=na_value):
            
            # color NA values as grayscale with intensity given by na_value (max 255)
            if pd.isnull(value):
                return na_value, na_value, na_value
            
            scaled_val = (value - min_val) / (max_val - min_val)

            # by default, higher values are good (and colored green)
            if not higher_is_better:
                scaled_val = 1 - scaled_val

            g = int(255 * scaled_val)
            r = int(255 * (1 - scaled_val))
            b = 0
            return r, g, b
        
        df[['R', 'G', 'B']] = pd.DataFrame(df[feature].map(calculate_color,).tolist(), index=df.index)

        return min_val, max_val

def plot_color_scale(min_val, max_val, label='Value'):
    '''
    Create a red-green colorbar for a color scale from min_val to max_val using matplotlib
    '''

    fig, ax = plt.subplots(figsize=(0.5, 6))
    plt.rcParams.update({'font.size': 5})

    # Define a custom colormap from red to green
    cdict = {
        'red':   [(0.0, 1.0, 1.0),
                  (1.0, 0.0, 0.0)],

        'green': [(0.0, 0.0, 0.0),
                  (1.0, 1.0, 1.0)],

        'blue':  [(0.0, 0.0, 0.0),
                  (1.0, 0.0, 0.0)]
    }

    custom_cmap = LinearSegmentedColormap('RedGreen', cdict)
    norm = plt.Normalize(vmin=min_val, vmax=max_val)

    cb1 = ColorbarBase(ax, cmap=custom_cmap, norm=norm, orientation='vertical')
    cb1.set_label(label)

    st.pyplot(fig)

def pydeck_scatter(df, display_feature, id, tooltip=None, view_state=VIEW_STATE):
    '''
    Create a pydeck scatterplot from a DataFrame
    '''

    # set color scale for display feature
    min_val, max_val = set_color_scale(df, display_feature, na_value=NA_VALUE, higher_is_better=True)

    point_layer = pydeck.Layer(
        "ScatterplotLayer",
        data=df,
        id=id,
        get_position=["Longitude", "Latitude"],
        get_color=["R", "G", "B"],
        pickable=True,
        auto_highlight=True,
        get_radius=4000,
    )

    # default tooltip is value of selected feature
    if tooltip is None:        
        tooltip={"text": "{%s}" % (display_feature)}

    chart = pydeck.Deck(
        point_layer,
        initial_view_state=view_state,
        tooltip=tooltip,
    )

    return chart, min_val, max_val

