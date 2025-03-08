import streamlit as st
from pathlib import Path

from nhs_dashboard.lib import ui, data_proc


def main():
    st.set_page_config(page_title='NHS dashboard', page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

    dfs = data_proc.import_data(Path("src/nhs_dashboard/data/csv"), header=1)


    # df = data_proc.import_csv("src/nhs_dashboard/data/System_October-2024-AE-by-provider-8iWzH-1.csv", header=1)

    cols = st.columns([3,5,1,3])

    with cols[0]:
        st.header("Hello from nhs-dashboard!")
        month = st.selectbox('Select a month', dfs.keys())
        df = dfs[month]
        # select features that start with 'Percentage' as options for display
        features = data_proc.select_features(df, '^Percentage')
        display_feature = st.selectbox('Select a feature to display', features.columns)
    
    with cols[1]:
        tooltip={"text": "{%s},\n {System}" % (display_feature)}
        chart, min_val, max_val = ui.pydeck_scatter(df, display_feature, id="rates", tooltip=tooltip)
        event = st.pydeck_chart(chart, height=800, on_select="rerun", selection_mode="multi-object")

    with cols[2]:
        ui.plot_color_scale(min_val, max_val, label=display_feature)

    event.selection
    


if __name__ == "__main__":
    main()
