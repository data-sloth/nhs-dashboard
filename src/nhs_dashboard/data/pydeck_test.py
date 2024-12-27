import streamlit as st
import pydeck
import pandas as pd


st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

data = pd.read_csv(
    "src/nhs_dashboard/data/System_October-2024-AE-by-provider-8iWzH-1.csv",
    header=1,
)

data.columns = data.columns.str.replace(' ', '')
data.columns = data.columns.str.replace('<', 'lessthan')
data.columns = data.columns.str.replace('>', 'morethan')
data.columns = data.columns.str.replace('(', 'of')
data.columns = data.columns.str.replace(')', '')

data.replace('-', pd.NA, inplace=True)

# Convert relevant columns to numeric
data['Percentagein4hoursorlessoftype2'] = pd.to_numeric(data['Percentagein4hoursorlessoftype2'], errors='coerce')

st.write(data['Percentagein4hoursorlessoftype2'])

features = (data.filter(regex='^Percentage'))

display_feature = st.selectbox('Select a feature to display', features.columns)


def set_color_scale(df, feature, na_value=0, higher_is_better=True):
    min_val = df[feature].min(skipna=True)
    max_val = df[feature].max(skipna=True)
    
    st.write(f'Min: {min_val}, Max: {max_val}')

    def calculate_color(value, na_value=na_value):
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


set_color_scale(data, display_feature, na_value=100, higher_is_better=True)

point_layer = pydeck.Layer(
    "ScatterplotLayer",
    data=data,
    id="rates",
    get_position=["Longitude", "Latitude"],
    get_color=["R", "G", "B"],
    pickable=True,
    auto_highlight=True,
    get_radius=4000,
)

view_state = pydeck.ViewState(
    latitude=53, longitude=-2, controller=True, zoom=5, pitch=0
)

chart = pydeck.Deck(
    point_layer,
    initial_view_state=view_state,
    tooltip={"text": "{%s},\n {System}" % (display_feature)},
)

event = st.pydeck_chart(chart, height=1000, on_select="rerun", selection_mode="multi-object")

event.selection