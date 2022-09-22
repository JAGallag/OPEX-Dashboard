import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

st.set_page_config(page_title="Operating Expenses and Budget", page_icon=":bar_chart:", layout='wide')

df = pd.read_excel(
    io='CostData.xlsx',
    engine='openpyxl',
    sheet_name='CostData',
    skiprows=0,
    usecols='A:H',
    nrows=81611,
)

# st.dataframe(df)

st.sidebar.header("Please Filter Here:")
function = st.sidebar.multiselect(
    "Select the Function:",
    options=df["Function"].unique(),
    default=df["Function"].unique()
)

region = st.sidebar.multiselect(
    "Select the Region:",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

cost_type = st.sidebar.multiselect(
    "Select the Cost Type Category:",
    options=df["Cost_element_group"].unique(),
    default=df["Cost_element_group"].unique()
)

df_selection = df.query(
    "Function == @function & Region == @region & Cost_element_group == @cost_type"
)

# st.dataframe(df_selection)

st.title(":bar_chart: Operating Expenses and Budget:")
st.markdown("##")

total_budget = int(df_selection["Budget Current Year"].sum())
total_actual_cy = int(df_selection["Actual Current Year"].sum())
total_actual_py = int(df_selection["Actual Prior Year"].sum())
under_over = int(total_budget - total_actual_cy)
if (under_over > 0):
    variance_header = ("Surplus")
else:
    variance_header = ("Deficit")

left_column, middle_column, right_column, empty_column = st.columns((2, 2, 2, 4))
with left_column:
    st.subheader("Budget Total:")
    st.subheader(f"US $ {total_budget:,}")
with middle_column:
    st.subheader("Actual Total:")
    st.subheader(f"US $ {total_actual_cy:,}")
with right_column:
    st.subheader(variance_header + ":")
    st.subheader(f"US $ {under_over:,}")

st.markdown("---")

##  this will make sure to sort by months
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
df_selection['Month'] = pd.Categorical(df_selection['Month'], categories=months, ordered=True)



costs_by_month = (
    df_selection.groupby(by=["Month"]).sum()[["Actual Current Year", "Actual Prior Year",
                                              "Budget Current Year"]].sort_values(by="Month")

)

fig=go.Figure()

# create the  line chart
c1, c2 = st.columns(2)

with c1:
    st.markdown("### Operating Expenses by Month:")
    fig.add_trace(
    go.Scatter(
    
        x=costs_by_month.index,
        y=costs_by_month["Budget Current Year"],
        line=dict(color='red'),
        name="Budget current Year",
        orientation="v")
    )
# create the bar chart
    fig.add_trace(
        go.Bar(
            x=costs_by_month.index,
            y=costs_by_month['Actual Prior Year'],
            name="Actual Prior Year",
                marker_line_color='rgb(8,48,107)',
                        marker_line_width=2)
    )
    fig.add_trace(
        go.Bar(
            x=costs_by_month.index,
            y=costs_by_month['Actual Current Year'],
            name="Actual Current Year",
            marker_line_color='rgb(8,48,107)',
            marker_line_width=2)
    )

    st.plotly_chart(fig)

with c2:
    st.markdown(""+'### Actual Current Year Expenses:')
    fig_pie = px.pie(df_selection, values='Actual Current Year', names='Function')

    st.plotly_chart(fig_pie)

# Local URL: x`
# Network URL: http://192.168.86.47:8501