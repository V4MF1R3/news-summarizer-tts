import streamlit as st
import requests
import json

st.title("News Summarization and Sentiment Analysis")
company = st.text_input("Enter Company Name")

if st.button("Generate Report"):
    response = requests.get(f"http://127.0.0.1:5000/get_news?company={company}").json()

    st.write(f"### Sentiment Analysis for {company}")

    # Display articles
    for article in response["Articles"]:
        st.subheader(article["title"])
        st.write(f"**Summary:** {article['Summary']}")
        st.write(f"**Sentiment:** {article['Sentiment']}")
        st.write(f"**Topics:** {', '.join(article['Topics'])}")
        st.write("---")

    # Display comparative analysis
    st.write("### Comparative Analysis")
    st.write("#### Sentiment Distribution")
    st.json(response["Comparative Analysis"]["Sentiment Distribution"])

    st.write("#### Coverage Differences")
    for difference in response["Comparative Analysis"]["Coverage Differences"]:
        st.write(f"**{difference['Comparison']}**")
        st.write(difference["Impact"])
        st.write("---")

    st.write("#### Topic Overlap")
    st.write(
        f"**Common Topics:** {', '.join(response['Comparative Analysis']['Topic Overlap']['Common Topics'])}"
    )
    st.write(
        f"**Unique Topics in Article 1:** {', '.join(response['Comparative Analysis']['Topic Overlap']['Unique Topics in Article 1'])}"
    )
    st.write(
        f"**Unique Topics in Article 2:** {', '.join(response['Comparative Analysis']['Topic Overlap']['Unique Topics in Article 2'])}"
    )

    # Play audio
    st.audio(response["Audio"])

    # Add a download button for the report
    report_json = json.dumps(response, indent=4)
    st.download_button(
        label="Download Report",
        data=report_json,
        file_name=f"{company}_sentiment_report.json",
        mime="application/json",
    )
