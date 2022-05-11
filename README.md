# Wish List

My wish list web app

## Adding wishes API

Assuming you start the server with `uvicorn app.main:app --reload --port 8080`...

```python
url = "http://localhost:8080"
d = {"person": "rodney", "item": "bat", "purchased": False, "link": "http://rodney.me"}
p = requests.post(f"{url}/api/wishes", json=d)
```
