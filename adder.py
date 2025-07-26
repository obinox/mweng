import json

def aggregate_cheeses_by_channel(cheeses_file="cheeses.json"):
    try:
        with open(cheeses_file, "r", encoding="utf-8") as f:
            cheeses_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {cheeses_file} not found.")
        return

    channel_cheese_sums = {}
    total = 0

    for item in cheeses_data:
        channel_url = item.get("channel")
        cheese_amount = int(item.get("cheese", 0))

        if channel_url:
            if channel_url not in channel_cheese_sums:
                channel_cheese_sums[channel_url] = 0
            channel_cheese_sums[channel_url] += cheese_amount
        total += cheese_amount

    channel_cheese_sums["total"] = total
    
    with open("channel_cheese_sums.json", "w", encoding="utf-8") as f:
        json.dump(channel_cheese_sums, f, ensure_ascii=False, indent=4)

    print("Cheese amounts aggregated by channel and saved to channel_cheese_sums.json")
    for channel, total_cheese in channel_cheese_sums.items():
        print(f"Channel: {channel}, Total Cheese: {total_cheese}")

if __name__ == "__main__":
    aggregate_cheeses_by_channel()
    