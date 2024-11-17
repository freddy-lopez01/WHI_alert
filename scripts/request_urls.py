import requests
import json


def fetch_api_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Check if the request was successful
        print(f"Response Content-Type: {response.headers['Content-Type']}")
        pretty_json = json.dumps(response.json(), indent=4)
        data = json.loads(pretty_json)
        location_data = data["pageProps"]["location"]
        filtered_data = {
            "latitude": location_data["latitude"],
            "longitude": location_data["longitude"],
            "storeCode": location_data["storeCode"],
            "businessHours": location_data["businessHours"]
            }

        
        if response.headers['Content-Type'] == 'application/json':
            res = (json.dumps(filtered_data, indent=4))
            print(res)
            with open('information.json', 'a') as info_file:
                info_file.write(res + ',\n')
            return res 

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
    

    try:
        with open('urls.json', 'r') as file:
            urls = json.load(file)  # Directly load list of URLs
            if not urls:
                print("No URLs found in the JSON file.")
                return

            # Fetch data for each URL
            for url in urls:
                print(f"Fetching data from: {url}")
                fetch_api_data(url)

    except FileNotFoundError:
        print("The urls.json file was not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON from the urls.json file.")



if __name__ == "__main__":
    main()




