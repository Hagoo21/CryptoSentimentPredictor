from flask import Flask, jsonify
import apify_client

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
        "searchTerms": ["lebron"],
        "sort": "Top",
        "start": "2024-06-23",
        "startUrls": ["https://twitter.com/search?q=gpt&src=typed_query&f=live"]
    }

# Run the Actor and wait for it to finish
    run = client.actor("nfp1fpt5gUlBwPcor").call(run_input=run_input)

# Fetch and print Actor results from the run's dataset (if there are any)
    output_list = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        print(item)
        output_list.append(item.get("text", ""))
    return output_list

if __name__ == "__main__":
    app.run(debug=True)