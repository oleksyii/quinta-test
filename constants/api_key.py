API_KEY = input("Enter your Clockify API key: ")
# API_KEY = 'OThjMTU0NWMtOGM2OC00NjA0LWFiNDktNGRkN2M2YThmYjQ4'

BASE_URL = "https://api.clockify.me/api/v1"

if not API_KEY:
    raise ValueError("Invalid API key. Please enter a valid API key.")

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
}
