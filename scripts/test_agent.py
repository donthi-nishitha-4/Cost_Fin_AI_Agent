import requests

BASE_URL = "http://127.0.0.1:8000/agent"

test_cases = [
    "what is cost of subsystem 1",
    "cost breakdown of subsystem 1",
    "what is cost of subsystem 2",
    "hello",
    "show subsystem 1 cost"
]

for query in test_cases:
    try:
        response = requests.get(BASE_URL, params={"query": query})
        print("\n==============================")
        print("QUERY:", query)
        print("STATUS:", response.status_code)
        print("RESPONSE:", response.json())

    except Exception as e:
        print("ERROR for query:", query)
        print(str(e))