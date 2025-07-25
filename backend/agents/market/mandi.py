# import requests

# # API endpoint
# url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

# # Specify the state you want to filter by.
# # You can change "Uttar Pradesh" to any other state.
# target_state = "Uttar Pradesh"
# api_key = "579b464db66ec23bdd000001de5b9efe20fe44f273570082d48519b7"
# limit = 100
# offset = 0
# all_records = []

# while True:
#     params = {
#         "api-key": api_key,
#         "format": "json",
#         "limit": limit,
#         "offset": offset,
#         "filters[state]": target_state
#     }

#     # Send GET request
#     response = requests.get(url, params=params)

#     if response.status_code == 200:
#         data = response.json()
#         records = data.get("records", [])
        
#         if not records:
#             # No more records to fetch
#             break
            
#         all_records.extend(records)
        
#         if len(records) < limit:
#             # Last page of results
#             break
            
#         offset += limit
#     else:
#         print("Error:", response.status_code, response.text)
#         break

# # Print all fetched data
# print(f"Total records fetched for {target_state}:", len(all_records))
# if not all_records:
#     print("No records found for the specified state. Please check the state name or try another one.")
# for record in all_records:
#     print(
#         f"State: {record['state']}, District: {record['district']}, Market: {record['market']}, "
#         f"Commodity: {record['commodity']}, Variety: {record['variety']}, Grade: {record['grade']}, "
#         f"Arrival Date: {record['arrival_date']}, Min Price: {record['min_price']}, "
#         f"Max Price: {record['max_price']}, Modal Price: {record['modal_price']}"
#     )


import requests

# ---------------- CONFIG ----------------
url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
api_key = "579b464db66ec23bdd000001de5b9efe20fe44f273570082d48519b7"

# ✅ List of states (main + nearby)
target_states = ["Uttar Pradesh", "Bihar", "Madhya Pradesh", "Rajasthan", "Haryana"]

limit = 100
# ----------------------------------------

def fetch_mandi_data(state):
    offset = 0
    all_records = []

    while True:
        params = {
            "api-key": api_key,
            "format": "json",
            "limit": limit,
            "offset": offset,
            "filters[state]": state
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            records = data.get("records", [])

            if not records:
                break

            all_records.extend(records)

            if len(records) < limit:
                break

            offset += limit
        else:
            print(f"Error fetching data for {state}: {response.status_code}")
            break

    return all_records

# ---------------- MAIN ----------------
for state in target_states:
    records = fetch_mandi_data(state)
    if records:
        print(f"\n✅ Prices in {state} ({len(records)} records):")
        for r in records:
            print(f"{r['commodity']} ({r['variety']}): ₹{r['min_price']} - ₹{r['max_price']} (Modal: ₹{r['modal_price']}) | Market: {r['market']}, District: {r['district']}")
