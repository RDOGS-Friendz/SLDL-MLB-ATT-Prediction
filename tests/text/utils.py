import streamlit as st


def create_description():
    """Create a description of the instructions."""
    st.markdown(
        """
        ### How to add your Twitter API credentials on your own machine
        To try this app locally, you first need to specify your Twitter API credentials:
        1.  Create a subfolder  _in this repo_, called  `.streamlit`
        2.  Create a file at  `.streamlit/secrets.toml`  file with the following body:
        """
    )

    st.markdown("")
    st.code(
        """
        [twitter]
        # Enter your secrets here. See README.md for more info.
        consumer_key = 'enter your credentials here'
        consumer_secret = 'enter your credentials here'
        """
    )

    st.markdown(
        """
        3.  Go to the  [Twitter Developer Portal](https://developer.twitter.com/en/portal), create or select an existing project + app, then go to the app's "Keys and Tokens" tab to generate your "Consumer Keys".
        4.  Copy and paste you key and secret into the file above.
        5.  Now you can run you Streamlit app as usual:

            ```
            streamlit run streamlit_app.py
            ```

        """
    )

    st.markdown(
        """
        ### How to add your Twitter API credentials on your deployed app
        To try this app in Streamlit Sharing, you need to add your Twitter API credentials in the Secrets manager:
        1.  Go to your app dashboard at `https://share.streamlit.io/`
        2.  Find your app and click on `Edit secrets`:
        """
    )

    st.markdown("")

    # st.image("01.png", width=650)
    st.image("01.png", width=650)

    st.markdown(
        """
        3.  Copy and paste you key and secret into the box below:
        """
    )

    st.markdown("")
    st.image("02.png", width=650)
    # st.image("02.png", width=650)

    st.markdown(
        """
        4.  Press `Save`
        """
    )

    st.markdown("")
    return


def create_header():
    a, b = st.columns([1, 10])

    with a:
        st.text("")
        st.image("Major_League_Baseball_logo.svg.png", width=50)
    with b:
        st.title("MLP Attendance Predictor")

    st.write("Type in a term to view the latest Twitter sentiment on that term.")
    return
