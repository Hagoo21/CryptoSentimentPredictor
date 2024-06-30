from flask import Flask, request, jsonify
import apify_client
import csv
import sentiment_analysis


app = Flask(__name__)

@app.route("/members")
def members():
    return {"members": ["Member1", "Member2", "Member3"]}

@app.route("/tweets",methods=['GET'])
def reddit_api():
    apify_actor_url = "https://api.apify.com/v2/acts/YOUR_ACTOR_ID/runs"
    apify_token = "apify_api_XGXscTbXXd8vgfkWxVCfMO2vOxCTjL1dHoWR"
    client = apify_client.ApifyClient("apify_api_XGXscTbXXd8vgfkWxVCfMO2vOxCTjL1dHoWR")

# Prepare the Actor input
    run_input = {
        "end": "2024-06-30",
        "maxItems": 1000,
        "searchTerms": ["$PEPE"],
        "sort": "Top",
        "start": "2024-06-23",
    }

# Run the Actor and wait for it to finish
    run = client.actor("nfp1fpt5gUlBwPcor").call(run_input=run_input)

# Fetch and print Actor results from the run's dataset (if there are any)
    output_list = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        tweet_data = {
            "text": item.get("text", ""),
            "date": item.get("createdAt", ""),
            "likes": item.get("likes", 0),
            "retweets": item.get("retweets", 0),
            "replies": item.get("replies", 0)
        }
        output_list.append(tweet_data)

    csv_file = "tweets.csv"
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["text", "date", "likes", "retweets", "replies"])
        writer.writeheader()
        writer.writerows(output_list)
    return jsonify({"message": "Data saved to CSV successfully", "csv_file": csv_file})

@app.route("/analyze_sentiment",methods=['POST'])
def analyze_sentiment():
    sentiments = sentiment_analysis.analyze_sentiment("tweets2.csv")
    return jsonify(sentiments)

COINMARKETCAP_API_KEY = "f95582r23r23r21d-d059-48c6-bb5d-7d2e10ae4fcf"

def get_ohlcv_data(symbol, convert, interval, start, end):
    url = f"https://pro-api.coinmarketcap.com/v2/cryptocurrency/ohlcv/historical"
    headers = {
        "X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY
    }
    params = {
        "symbol": symbol,
        "convert": convert,
        "time_period": interval,
        "time_start": start,
        "time_end": end
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_market_data(symbol, convert, interval, start, end):
    url = f"https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/historical"
    headers = {
        "X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY
    }
    params = {
        "symbol": symbol,
        "convert": convert,
        "interval": interval,
        "time_start": start,
        "time_end": end
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

@app.route('/api/bitcoin/data', methods=['GET'])
def get_bitcoin_data():
    symbol = "BTC"
    convert = "USD"
    interval = request.args.get('interval', 'daily')  # Default interval is daily
    start = request.args.get('start')  # Start date for the data
    end = request.args.get('end')  # End date for the data


    # Fetch OHLCV data
    ohlcv_data = get_ohlcv_data(symbol, convert, interval, start, end)
    if ohlcv_data is None:
        return jsonify({"error": "Failed to fetch OHLCV data from CoinMarketCap"}), 500

    # Fetch market cap and volume data
    market_data = get_market_data(symbol, convert, interval, start, end)
    if market_data is None:
        return jsonify({"error": "Failed to fetch market data from CoinMarketCap"}), 500

    # Combine and process the data
    combined_data = {
        "ohlcv": ohlcv_data['data']['quotes'],
        "market_data": market_data['data']['quotes']
    }

    # Calculate volatility
    df = pd.DataFrame(combined_data['ohlcv'])
    df['timestamp'] = pd.to_datetime(df['time_open'])
    df.set_index('timestamp', inplace=True)
    df['close'] = df['quote'][convert]['close']
    df['returns'] = df['close'].pct_change()
    df['volatility'] = df['returns'].rolling(window=30).std() * np.sqrt(30)

    combined_data['volatility'] = df['volatility'].tolist()

    return jsonify(combined_data)

if __name__ == "__main__":
    app.run(debug=True)