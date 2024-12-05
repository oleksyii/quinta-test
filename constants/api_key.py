API_KEY = input("Enter your Clockify API key: ")

BASE_URL = "https://api.clockify.me/api/v1"

if not API_KEY:
    raise ValueError("Invalid API key. Please enter a valid API key.")

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
}
