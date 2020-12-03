# Used to make call to the Discord API
import requests

# Used to read the config file
import json

# Used to display the last update
from datetime import datetime

# Read the config file
with open("config.json", "r") as f:
    config = json.load(f)


def update_custom_status(text):
    """
    Update the Discord Custom Status of the user

    Args:
        text (str): The new custom status content

    Returns:
        data (any): The Discord response
    """

    custom_status = {'custom_status':{'text': text}}

    url = "https://discordapp.com/api/v6/users/@me/settings"
    headers = {
        "Authorization": config["discord_token"],
        "Content-Type": "application/json",
    }
    response = requests.patch(url, json.dumps(custom_status), headers=headers)
    data = response.json()
    return data


def get_weather_of(city):
    """
    Get the weather of a specific city

    Args:
        city (str): The name of the city whose weather we want

    Returns:
        weather (str): The weather of the city
    """
    # Open Weather Map API Base url
    base_url = (
        "http://api.openweathermap.org/data/2.5/weather?appid="
        + config["weather"]
        + "&q="
        + city
        + "&units="
        + config["units"]
    )
    response = requests.get(base_url)
    data = response.json()
    # Returns weather info
    return data


def generate_custom_status_content(weather):
    """
    Generate the custom status content

    Args:
        weather (str): The weather of the city

    Returns:
        custom_status_content (str): The final custom status content
    """
    # The current time (hours and minutes)
    now = datetime.now().strftime("%I:%M %p")

    # Some useful variables
    desc = weather["weather"][0]["description"]
    temp = round(weather["main"]["temp"])
    temp_symbol = (
        "°C"
        if config["units"] == "metric"
        else "°F"
        if config["units"] == "imperial"
        else "K"
    )
    feels_like = round(weather["main"]["feels_like"])
    city = config["city"]

    # Returns the final string wich contain the city, the current temp, the felt temp, the weather, the last update and the credits
    return (
        "Current weather in "
        + city
        + ": "
        + str(temp)
        + str(temp_symbol)
        + ". "
        + "Feels like "
        + str(feels_like)
        + str(temp_symbol)
        + ". "
        + str(desc.upper())
        + " | Last update: "
        + now
        + " | Made using Python"
    )


def main():
    """
    Main code which call the other functions
    """
    # Get the weather of the city
    weather = get_weather_of(config["city"])
    # Get the custom status content
    custom_status_content = generate_custom_status_content(weather)
    # Update the Custom Status
    status = update_custom_status(custom_status_content)
    # Log
    log_prefix = "[" + datetime.now().strftime("%I:%M %p") + "]"

    if "locale" in status:
        print(log_prefix + " Successfully updated custom status.")
    else:
        # If Github returned a message
        if "message" in status:
            # If the error is caused by the personal access token
            if status["message"] == "Unauthorized":
                print(
                    log_prefix
                    + " Seems like your Discord personal access token is invalid..."
                )
            else:
                print(
                    log_prefix
                    + " Something happened. Message is the following: "
                    + status["message"]
                )
        # If Github didn't return anything
        else:
            print(
                log_prefix
                + " Something happened. Here is the Discord API response: "
                + status["message"]
            )


if __name__ == "__main__":
    main()