from flask import Flask, jsonify
import apify_client
import csv


app = Flask(__name__)

@app.route("/members")
def members():
    return {"members": ["Member1", "Member2", "Member3"]}

@app.route("/reddit")
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

if __name__ == "__main__":
    app.run(debug=True)