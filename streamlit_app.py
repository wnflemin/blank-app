import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px

# --- Page Configuration ---
# Must be the first Streamlit command in your script
st.set_page_config(
    page_title="Streamlit Showcase App",
    page_icon="🎉",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- App Title and Description ---
st.title("🎉 Streamlit Showcase App")
st.write(
    """
    Welcome to this comprehensive showcase of Streamlit's features! This app demonstrates various widgets, 
    data display elements, charting capabilities, and layout options. Explore the sidebar and the tabs below to see what's possible.
    """
)
st.markdown("---")


# --- Sidebar ---
# The sidebar is a great place for controls and options
st.sidebar.header("App Controls")
st.sidebar.write("Use these widgets to control the main app content.")

# Sidebar selectbox
app_mode = st.sidebar.selectbox(
    "Choose a section to explore",
    ["Interactive Widgets", "Data & Charts", "Layout & Media", "Status & State"],
)

# Sidebar slider
alpha = st.sidebar.slider("Chart Opacity", 0.0, 1.0, 0.7)

# Sidebar button
if st.sidebar.button("Show Balloons!"):
    st.balloons()
    st.toast("Here are some balloons!", icon="🎈")


# --- Main Content based on Sidebar Selection ---

# --- Section 1: Interactive Widgets ---
if app_mode == "Interactive Widgets":
    st.header("Interactive Widgets Showcase")
    st.write(
        "Streamlit offers a variety of widgets to get user input. Here are a few examples:"
    )

    # Columns for side-by-side widgets
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Basic Inputs")
        # Text input
        text_input = st.text_input("Enter some text", "Hello, Streamlit!")
        st.write("You entered:", text_input)

        # Number input
        num_input = st.number_input("Enter a number", min_value=0, max_value=100, value=42)
        st.write(f"The number is: {num_input}")

        # Date input
        date_input = st.date_input("Pick a date")
        st.write(f"You selected: {date_input}")

    with col2:
        st.subheader("Selection Widgets")
        # Selectbox
        select_box = st.selectbox(
            "What's your favorite color?", ("Blue", "Green", "Red", "Yellow")
        )
        st.write(f"Your favorite color is **{select_box}**.")

        # Multiselect
        multi_select = st.multiselect(
            "What pets do you own?", ["Dog", "Cat", "Fish", "Parrot", "Hamster"]
        )
        st.write(f"You own: {', '.join(multi_select) if multi_select else 'No pets selected'}")

    # Checkbox and Radio buttons
    st.markdown("---")
    st.subheader("Boolean Widgets")
    col3, col4 = st.columns(2)
    with col3:
        # Checkbox
        if st.checkbox("Show additional details"):
            st.info("Here are some more details you asked for!")

    with col4:
        # Radio buttons
        delivery_option = st.radio(
            "Choose a delivery option:", ("Standard", "Express", "Pickup")
        )
        st.write(f"You chose: **{delivery_option}**")

    # Form to group inputs
    st.markdown("---")
    st.subheader("Using `st.form` for Batched Input")
    with st.form("my_form"):
        st.write("This form groups inputs. The app only reruns when you click 'Submit'.")
        name = st.text_input("Name")
        email = st.text_input("Email")
        feedback = st.text_area("Your Feedback")
        
        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.success(f"Thanks, {name}! We received your feedback.")
            st.write(f"**Email:** {email}")
            st.write(f"**Feedback:** {feedback}")


# --- Section 2: Data & Charts ---
elif app_mode == "Data & Charts":
    st.header("Displaying Data and Charts")

    # Function to generate sample data (with caching)
    @st.cache_data
    def get_sample_data(rows=20):
        data = {
            "Category A": np.random.randn(rows) + 5,
            "Category B": np.random.randn(rows) * 2,
            "Category C": np.random.choice(["X", "Y", "Z"], rows),
            "Date": pd.to_datetime(pd.date_range("2023-01-01", periods=rows))
        }
        return pd.DataFrame(data)

    df = get_sample_data()

    st.subheader("Displaying a DataFrame")
    st.write("You can display a pandas DataFrame directly:")
    st.dataframe(df)

    st.subheader("Metric Display")
    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", "70 °F", "1.2 °F")
    col2.metric("Wind", "9 mph", "-8%")
    col3.metric("Humidity", "86%", "4%")

    st.markdown("---")
    st.subheader("Built-in Charts")

    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.write("`st.line_chart`")
        st.line_chart(df, x='Date', y=['Category A', 'Category B'])
    
    with col_chart2:
        st.write("`st.bar_chart`")
        # Aggregate data for bar chart
        bar_data = df.groupby('Category C').mean(numeric_only=True)[['Category A', 'Category B']]
        st.bar_chart(bar_data)
        
    st.markdown("---")
    st.subheader("Advanced Charting with Plotly")
    st.write("Use libraries like Plotly for more control over your charts.")

    # Create a Plotly scatter plot
    fig = px.scatter(
        df,
        x="Category A",
        y="Category B",
        color="Category C",
        hover_data=['Date'],
        title="Interactive Scatter Plot (Plotly)",
        opacity=alpha # Use the opacity from the sidebar slider
    )
    st.plotly_chart(fig, use_container_width=True)


# --- Section 3: Layout & Media ---
elif app_mode == "Layout & Media":
    st.header("Layout Options and Media Elements")

    st.subheader("Tabs")
    st.write("Use `st.tabs` to organize content into separate sections.")
    tab1, tab2, tab3 = st.tabs(["🖼️ Image", "📄 Expander", "🖥️ Code"])

    with tab1:
        st.write("Display images easily with `st.image`.")
        # Example image from a URL
        st.image(
            "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
            caption="A screenshot of the Streamlit documentation homepage.",
            width=600,
        )

    with tab2:
        st.write("Use `st.expander` for collapsible content sections.")
        with st.expander("Click to see the explanation"):
            st.write(
                """
                An expander is a great way to hide content that is not immediately necessary, 
                keeping your app interface clean and tidy. Users can click on it to reveal 
                more information.
                """
            )
            st.code("with st.expander('Title'):\n    st.write('Content goes here.')", language="python")

    with tab3:
        st.write("Display code blocks with `st.code`.")
        st.code(
            """
@st.cache_data
def get_data():
    # This function is cached. 
    # Streamlit will only rerun it if the code changes.
    df = pd.read_csv("my_data.csv")
    return df
            """,
            language="python",
        )


# --- Section 4: Status & State ---
elif app_mode == "Status & State":
    st.header("Status Elements and Session State")

    st.subheader("Status Updates")
    st.write("Provide feedback to your users about what's happening.")

    # Progress bar
    if st.button("Run a long process"):
        progress_text = "Operation in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)
        
        for percent_complete in range(100):
            time.sleep(0.02)
            my_bar.progress(percent_complete + 1, text=f"{progress_text} ({percent_complete+1}%)")
        
        my_bar.empty() # Clear the progress bar
        st.success("Process completed successfully!")
    
    # Spinner
    with st.spinner("Wait for it... performing a complex calculation..."):
        time.sleep(2) # Simulate a delay
    st.info("Calculation finished!")

    st.markdown("---")
    st.subheader("Managing State with `st.session_state`")
    st.write("`st.session_state` allows you to preserve information across app reruns.")

    # Initialize state
    if "counter" not in st.session_state:
        st.session_state.counter = 0

    # Create two columns for the counter
    col_state1, col_state2 = st.columns([1, 4])
    
    with col_state1:
        # Buttons to increment and decrement
        if st.button("➕ Increment"):
            st.session_state.counter += 1
        if st.button("➖ Decrement"):
            st.session_state.counter -= 1

    with col_state2:
        st.write(f"### Current Counter Value: `{st.session_state.counter}`")
        st.write("This value persists even when you interact with other widgets.")
