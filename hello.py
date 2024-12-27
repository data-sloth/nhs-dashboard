import streamlit as st

from nhs_dashboard.lib import ui, data_proc


def main():
    st.set_page_config(page_title='NHS dashboard', page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

    st.header("Hello from nhs-dashboard!")

    df = data_proc.import_data("src/nhs_dashboard/data/System_October-2024-AE-by-provider-8iWzH-1.csv", header=1)

    # select columns that start with 'Percentage' as options for display
    features = data_proc.select_features(df, '^Percentage')
    display_feature = st.selectbox('Select a feature to display', features.columns)

    tooltip={"text": "{%s},\n {System}" % (display_feature)}

    chart = ui.pydeck_scatter(df, display_feature, id="rates", tooltip=tooltip)

    event = st.pydeck_chart(chart, height=1000, on_select="rerun", selection_mode="multi-object")

    event.selection
    


if __name__ == "__main__":
    main()
