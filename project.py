# # Importing the required libraries for the task:
# pandas for data manipulation, dash for building the interactive dashboard,
# and plotly.express for creating visualizations.
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Reading the dataset from the local directory (previously downloaded from Kaggle)
# and loading it into a pandas DataFrame.
df = pd.read_csv("E:\Dashboard\KaggleV2-May-2016.csv")
print(df)
print("*"*20)
# Exploratory Data Analysis (EDA) /Data Overview
print(df.head()) # => Display the first 5 rows
print("*"*20)
print(df.info()) # => Column information and data types
print("*"*20)
print(df.isnull().sum()) # => Missing values
print("*"*20)
print(df.describe()) # => Statistical description of numeric columns

# Important notes from the EDA:
# No missing values → Good for cleaning.
# Irrelevant ages (negative values) should be removed. 
# Booking dates and appointments are present but must be converted to datetime.
# The absence rate (No-show) must be analyzed.
# We need to add additional columns for analysis:
# The difference in days between booking and appointment (DaysDiff).
# The day of the week for the appointment (AppointmentWeekday).


# Data Cleaning
df = df[df['Age'] >= 0] # => Remove any row with an Age less than 0 because it doesn't make sense.

df['ScheduledDay'] = pd.to_datetime(df['ScheduledDay'])  # => Convert the ScheduledDay column from a string to a datetime format so we can perform calculations on it.

df['AppointmentDay'] = pd.to_datetime(df['AppointmentDay']) # => Convert the AppointmentDay column to datetime format so we can perform calculations on it.

df['DaysDiff'] = (df['AppointmentDay'] - df['ScheduledDay']).dt.days # => Calculate the difference between the appointment date and the booking date (in days) and add it as a new column, DaysDiff. This is important to understand the waiting time and its impact on absences.

df = df[df['DaysDiff'] >= 0] # => Remove any row where the difference between the reservation and the appointment is negative, as this is a data error.


# Remove any extra spaces from the text values in the three columns (Gender, Neighborhood, No-show) to ensure clean data when analyzed.
df['Gender'] = df['Gender'].str.strip()
df['Neighbourhood'] = df['Neighbourhood'].str.strip()
df['No-show'] = df['No-show'].str.strip()

df['No_show_flag'] = df['No-show'].map({'No': 0, 'Yes': 1}) # => Convert the No-show column from text to a number (0, attended) or (1, not attended) for easier analysis.

df['AppointmentWeekday'] = df['AppointmentDay'].dt.day_name() # => Add a new column named AppointmentWeekday containing the name of the day of the week to specify the distribution of appointments by day.


# Save the cleaned and optimized data in a new CSV file named cleaned_data.csv in the specified path.
# Index=False means that row numbers (Index) are not saved in the file.
# Display the first 10 rows to confirm.
df.to_csv("E:/Dashboard/cleaned_data.csv", index=False)
print(df.head(10))


# Initialize the Dash application and set the dashboard title
app = dash.Dash(__name__)
app.title = "📊 Medical Appointments Dashboard"

# Define the layout of the dashboard using Dash HTML components
app.layout = html.Div([
    html.H1("📊 Medical Appointments Dashboard", style={   # => Main Title of the Dashboard with custom styling
        'textAlign': 'center',  # => Center align the text
        'color': "#921097",   # => Title color (purple)
        'fontSize': '36px',       # =>  Large font size
        'fontWeight': 'bold',  # =>  Bold font
        'fontFamily': 'Poppins, Arial, sans-serif'  # => Font style
    }),

   # Filters Section (Inside a styled Box
    html.Div([
        # Dropdown for selecting Neighborhood
        html.Div([
            html.Label("Select Neighborhood:", style={'font-weight': 'bold', 'color': '#083663'}), # => Dynamic options from data.
            dcc.Dropdown(
                id='neighborhood-dropdown',
                options=[{'label': nb, 'value': nb} for nb in sorted(df['Neighbourhood'].unique())],
                value=None, # => Default value (None = All neighborhoods)
                placeholder="All Neighborhoods"
            ),
        ], style={'width': '30%', 'display': 'inline-block', 'margin-right': '20px'}),

        # Range Slider for selecting Age range
        html.Div([
            html.Label("Select Age Range:", style={'font-weight': 'bold', 'color': '#083663'}),
            dcc.RangeSlider(
                id='age-slider',
                min=0,
                max=100,
                step=1,
                value=[0, 100],
                marks={i: str(i) for i in range(0, 101, 10)} # => Show labels every 10 year
            ),
        ], style={'width': '65%', 'display': 'inline-block'}),
    ], style={
        'backgroundColor': "#F8F9FA",
        'padding': '15px',
        'borderRadius': '10px',
        'boxShadow': '2px 2px 10px lightgrey',
        'marginBottom': '20px'
    }),

    # Visualization - Graphs inside Styled Boxes
    # Each chart is placed inside a separate HTML Div with custom styling:
    # Light background
    # Padding for inner spacing
    # Rounded corners for modern design
    # Box shadow for a card-like effect
    # Margin bottom for spacing between charts

    # Pie Chart: Shows vs No-shows
    html.Div([
        dcc.Graph(id='pie-show-noshows', style={'height': '450px'})
    ], style={'backgroundColor': '#F8F9FA', 'padding': '10px', 'borderRadius': '10px', 'boxShadow': '2px 2px 10px lightgrey', 'marginBottom': '20px'}),
    
    # Histogram: Age and Gender Impact on Attendance
    html.Div([
        dcc.Graph(id='age-gender-impact', style={'height': '450px'})
    ], style={'backgroundColor': '#F8F9FA', 'padding': '10px', 'borderRadius': '10px', 'boxShadow': '2px 2px 10px lightgrey', 'marginBottom': '20px'}),

    # Histogram: Appointment Distribution by Weekday
    html.Div([
        dcc.Graph(id='weekday-distribution', style={'height': '450px'})
    ], style={'backgroundColor': '#F8F9FA', 'padding': '10px', 'borderRadius': '10px', 'boxShadow': '2px 2px 10px lightgrey', 'marginBottom': '20px'}),
 
    # Histogram: Attendance Patterns by Top Neighborhoods
    html.Div([
        dcc.Graph(id='neighborhood-patterns', style={'height': '600px'})
    ], style={'backgroundColor': '#F8F9FA', 'padding': '10px', 'borderRadius': '10px', 'boxShadow': '2px 2px 10px lightgrey', 'marginBottom': '20px'}),

    # Histogram: Impact of Chronic Conditions on Attendance
    html.Div([
        dcc.Graph(id='chronic-conditions-impact', style={'height': '450px'})
    ], style={'backgroundColor': '#F8F9FA', 'padding': '10px', 'borderRadius': '10px', 'boxShadow': '2px 2px 10px lightgrey', 'marginBottom': '20px'}),

    # Box Plot: Delay between Scheduling and Appointment vs Attendance
    html.Div([
        dcc.Graph(id='delay-impact', style={'height': '450px'})
    ], style={'backgroundColor': '#F8F9FA', 'padding': '10px', 'borderRadius': '10px', 'boxShadow': '2px 2px 10px lightgrey', 'marginBottom': '20px'}),

    html.Hr(),
    html.Div("Dashboard created with Dash & Plotly | Dataset: Medical Appointment No-Show",
             style={'textAlign': 'center', 'color': '#7F8C8D', 'fontSize': '14px'})

    # Set the overall page background and padding
], style={'backgroundColor': "#6EDBC39B", 'padding': '20px'})



# Callbacks - Dynamic Update of Charts based on Filters
# Define callback to update all 6 graphs when user changes:
# - Neighborhood selection (Dropdown)
# - Age range selection (RangeSlider)

@app.callback(
    Output('pie-show-noshows', 'figure'),
    Output('age-gender-impact', 'figure'),
    Output('weekday-distribution', 'figure'),
    Output('neighborhood-patterns', 'figure'),
    Output('chronic-conditions-impact', 'figure'),
    Output('delay-impact', 'figure'),
    Input('neighborhood-dropdown', 'value'),
    Input('age-slider', 'value')
)
# Make a copy of the main dataframe
def update_charts(selected_neighborhood, age_range):
    dff = df.copy()

    # Apply Filters
    # Filter by neighborhood if user selected a specific one
    if selected_neighborhood:
        dff = dff[dff['Neighbourhood'] == selected_neighborhood]

    # Filter by selected age range from RangeSlider
    dff = dff[(dff['Age'] >= age_range[0]) & (dff['Age'] <= age_range[1])]

    # Pie Chart: Show vs No-show
    pie_fig = px.pie(
        dff, names='No-show', title='Show vs No-show Rate', color='No-show',
        color_discrete_map={'No': '#2ECC71', 'Yes': '#E74C3C'}
    )

    # Age & Gender Impact
    age_gender_fig = px.histogram(
        dff, x='Age', color='Gender', barmode='overlay', nbins=40,
        title='Age and Gender Impact on Attendance',
        color_discrete_sequence=["#AD749F", "#271588"]
    )

    # Appointments by Day of the Week
    weekday_fig = px.histogram(
        dff, x='AppointmentWeekday', color='No-show', barmode='group',
        category_orders={'AppointmentWeekday': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']},
        title='Appointments by Weekday',
        color_discrete_map={'No': "#CFC141", 'Yes': "#642901"}
    )

    # Neighborhood Patterns (Top 20)
    top_nb = dff['Neighbourhood'].value_counts().head(20).index
    nb_fig = px.histogram(
        dff[dff['Neighbourhood'].isin(top_nb)], x='Neighbourhood', color='No-show', barmode='group',
        title='Attendance Patterns (Top 20 Neighborhoods)',
        color_discrete_map={'No': "#CC602E", 'Yes': "#C04343"}
    )
    nb_fig.update_xaxes(tickangle=45)

    # Chronic Conditions Impact
    dff['HasChronic'] = dff[['Hipertension', 'Diabetes', 'Alcoholism']].sum(axis=1)
    dff['ChronicCondition'] = dff['HasChronic'].apply(lambda x: 'Yes' if x > 0 else 'No')
    chronic_fig = px.histogram(
        dff, x='ChronicCondition', color='No-show', barmode='group',
        title='Impact of Chronic Conditions',
        color_discrete_map={'No': "#2B4B0D", 'Yes': "#0F3147"}
    )

    # Delay Between Scheduling and Appointment
    delay_fig = px.box(
        dff, x='No-show', y='DaysDiff',
        title='Delay Between Scheduling and Appointment vs Attendance',
        color='No-show',
        color_discrete_map={'No': "#0C524C", 'Yes': '#660925'}
    )

    # Return all figures to be displayed in dashboard
    return pie_fig, age_gender_fig, weekday_fig, nb_fig, chronic_fig, delay_fig

# Run the Dash app only if this script is executed directly 
if __name__ == '__main__':
    app.run(debug=True)