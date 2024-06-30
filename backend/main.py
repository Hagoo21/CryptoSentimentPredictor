import re
import pandas as pd

# Input and output file names
input_file = "tweets.csv"
output_file = "tweets2.csv"

# Read the CSV file into a DataFrame
df = pd.read_csv(input_file)

# Function to clean the tweet text
def clean_text(text):
    text = re.sub('https?://\S+', '', text)
    text = re.sub('@\w+', '', text)
    return text

# Apply the cleaning function to the 'Text' column
df['text'] = df['text'].apply(clean_text)

# Save the cleaned DataFrame to a new CSV file
df.to_csv(output_file, header=True, encoding='utf-8', index=False)