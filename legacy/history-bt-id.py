import requests

API_KEY = "sk_41ac27614ca2a6115b2c2625ed790451bf77d9be1c89c357"
BATCH_ID = "btcal_01jyqqb7axevpbrmmeq18xjhke"
response = requests.get(
    f"https://api.elevenlabs.io/v1/convai/batch-calling/workspace",
    headers={"xi-api-key": f"{API_KEY}"}
)
with open('historybtid.json', 'w') as f:
    f.write(response.text)