import requests
import time
import sys

API_KEY = ""
COLUMN_TO_CHECK = "pulse_updated_mkqpfssf"
COLUMN_TO_CLEAR = "color_mkt86f8b"
TARGET_DATE = sys.argv[1] if len(sys.argv) > 1 else None
if not TARGET_DATE:
    print("❌ No date provided. Usage: python app.py YYYY-MM-DD")
    sys.exit(1)

URL = "https://api.monday.com/v2"
HEADERS = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}


def fetch_all_items():
    cursor = None
    all_items = []

    while True:
        query = """
        query ($boardId: [ID!], $cursor: String) {
          boards(ids: $boardId) {
            items_page(limit: 500, cursor: $cursor) {
              items {
                id
                name
                column_values(ids: ["pulse_updated_mkqpfssf"]) {
                  id
                  text
                }
              }
              cursor
            }
          }
        }
        """
        variables = {
            "boardId": [BOARD_ID],
            "cursor": cursor
        }

        response = requests.post(URL, json={"query": query, "variables": variables}, headers=HEADERS)
        data = response.json()
        items = data["data"]["boards"][0]["items_page"]["items"]
        all_items.extend(items)
        cursor = data["data"]["boards"][0]["items_page"]["cursor"]

        if not cursor:
            break

    return all_items


def clear_column_value(item_id):
    mutation = """
    mutation ($boardId: ID!, $itemId: ID!, $columnId: String!, $value: String!) {
      change_simple_column_value(
        board_id: $boardId,
        item_id: $itemId,
        column_id: $columnId,
        value: $value
      ) {
        id
      }
    }
    """
    variables = {
        "boardId": BOARD_ID,
        "itemId": item_id,
        "columnId": COLUMN_TO_CLEAR,
        "value": ""
    }

    response = requests.post(URL, json={"query": mutation, "variables": variables}, headers=HEADERS)
    json_response = response.json()
    if "errors" in json_response:
        print(f"❌ Failed for item {item_id}: {json_response['errors'][0]['message']}")
    else:
        print(f"✅ Cleared column for item {item_id}")


# Run everything
items = fetch_all_items()
print(f"🔍 Total items fetched: {len(items)}")

for item in items:
    date_col = next((col["text"] for col in item["column_values"] if col["id"] == COLUMN_TO_CHECK), None)
    if date_col:
        date_only = date_col.split(" ")[0]
        if date_only == TARGET_DATE:
            clear_column_value(item["id"])
            time.sleep(0.5)  # Respect rate limit
