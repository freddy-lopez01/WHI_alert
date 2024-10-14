import requests


def fetch_api_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Check if the request was successful
        # Print the content type and response text for debugging
        print(f"Response Content-Type: {response.headers['Content-Type']}")
        print(f"Response Text: {response.text}")
        
        # Try to parse the response as JSON
        if response.headers['Content-Type'] == 'application/json':
            return response.json()
        else:
            print("The response is not in JSON format.")
            return None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.JSONDecodeError as json_err:
        print(f"JSON decode error: {json_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None


def main():
    api_url = "https://locations.wafflehouse.com/api/587d236eeb89fb17504336db/location-details"
    data = fetch_api_data(api_url)


if __name__ == "__main__":
    main()




