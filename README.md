# News Summarization and Sentiment Analysis Application

## Project Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/news-summarizer-tts.git
    cd news-summarizer-tts
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python -m venv venv
    venv\Scripts\activate  # On Windows
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Create a `.env` file and add your API key:**
    ```env
    NEWS_API_KEY=your_news_api_key_here
    ```

### Running the Application

1. **Start the Flask API server:**
    ```sh
    python api.py
    ```

2. **Run the Streamlit application:**
    ```sh
    streamlit run app.py
    ```

3. **Open your web browser and go to:**
    ```
    http://localhost:8501
    ```

## Model Details

### Summarization Model

- **Model:** `facebook/bart-large-cnn`
- **Library:** Hugging Face Transformers
- **Description:** This model is used to generate concise summaries of the news articles.

### Sentiment Analysis Model

- **Model:** `distilbert-base-uncased-finetuned-sst-2-english`
- **Library:** Hugging Face Transformers
- **Description:** This model is used to perform sentiment analysis on the news articles, categorizing them as Positive, Negative, or Neutral.

### Text-to-Speech (TTS) Model

- **Library:** `gTTS`
- **Description:** This library is used to convert the summarized sentiment report into Hindi speech.

## API Development

### Endpoints

- **GET /get_news**
    - **Description:** Fetch news articles related to a given company, perform summarization, sentiment analysis, and generate a comparative analysis.
    - **Parameters:** `company` (string) - The name of the company to fetch news for.
    - **Response:** JSON object containing the articles, comparative analysis, and a link to the audio file.

### Using the API with Postman

1. **Start the Flask API server:**
    ```sh
    python [api.py](http://_vscodecontentref_/0)
    ```

2. **Open Postman and create a new GET request:**
    ```
    http://127.0.0.1:5000/get_news?company=Tesla
    ```

3. **Send the request and view the response.**

## API Usage

### Third-Party APIs

- **News API**
    - **Purpose:** Fetch news articles related to the given company.
    - **Integration:** The API key is stored in the `.env` file and accessed using the `os.getenv` method.

## Assumptions & Limitations

### Assumptions

- The application assumes that the News API will return articles with the necessary fields (`title`, `content`).
- The application assumes that the text-to-speech conversion will work correctly for the translated Hindi text.

### Limitations

- The application currently supports only English news articles.
- The TTS output is in Hindi, which may not be perfect due to translation limitations.
- The summarization and sentiment analysis models are pre-trained and may not be perfectly accurate for all types of news articles.

## Conclusion

This application provides a comprehensive solution for summarizing news articles, performing sentiment analysis, and generating a comparative analysis report with a text-to-speech output in Hindi. The user-friendly interface and API endpoints make it easy to use and integrate into other applications.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.