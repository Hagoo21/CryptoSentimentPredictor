import re
import pandas as pd
import requests
import json


def main():
    query = 'crypto'
    # Scrape tweets
    response = requests.get(f'http://localhost:5000/tweets?query={query}')
    tweets = response.json()

    # Analyze sentiment
    response = requests.post('http://localhost:5000/analyze_sentiment', json={'tweets': tweets})
    sentiments = response.json()

    print("Sentiment Analysis Results:", sentiments)


def clean_text(text):
    text = re.sub('https?://\S+', '', text)
    text = re.sub('@\w+', '', text)
    return text

if __name__ == '__main__':
    # Input and output file names
    input_file = "tweets.csv"
    output_file = "tweets2.csv"

# Read the CSV file into a DataFrame
    df = pd.read_csv(input_file)

# Function to clean the tweet text

# Apply the cleaning function to the 'Text' column
    df['text'] = df['text'].apply(clean_text)

# Save the cleaned DataFrame to a new CSV file
    df.to_csv(output_file, header=True, encoding='utf-8', index=False)
    main()