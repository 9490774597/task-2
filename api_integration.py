#!/usr/bin/env python3
"""Beginner-friendly Python project for integrating public APIs without API keys."""

import os
from datetime import datetime
from urllib.parse import quote

import requests


LOG_FILE = "log.txt"


def create_log_file():
    """Create the log file if it does not exist yet."""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as file:
            file.write("API Request Log\n")
            file.write("================\n")


def log_request(service, user_input, success, message):
    """Store each request with date, time, input, and status."""
    create_log_file()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "SUCCESS" if success else "FAILURE"
    entry = f"{timestamp} | Service: {service} | Input: {user_input} | Status: {status} | Message: {message}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(entry)


def show_menu():
    """Display the main menu for the user."""
    print("\n===== API Integration Menu =====")
    print("1. Weather")
    print("2. Cryptocurrency")
    print("3. Latest News")
    print("4. Exit")


def weather_code_to_description(code):
    """Convert an Open-Meteo weather code into a readable description."""
    weather_map = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        95: "Thunderstorm",
    }
    return weather_map.get(code, "Unknown condition")


def get_weather_data(city_name):
    """Fetch weather details for a given city using Open-Meteo (no API key required)."""
    geocode_url = (
        f"https://geocoding-api.open-meteo.com/v1/search?name={quote(city_name)}"
        "&count=1&language=en&format=json"
    )
    geocode_response = requests.get(geocode_url, timeout=10)
    geocode_response.raise_for_status()
    geocode_data = geocode_response.json()

    results = geocode_data.get("results", [])
    if not results:
        raise ValueError("No matching city was found.")

    location = results[0]
    latitude = location.get("latitude")
    longitude = location.get("longitude")

    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}"
        "&current=temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m"
        "&timezone=auto"
    )
    weather_response = requests.get(weather_url, timeout=10)
    weather_response.raise_for_status()
    weather_data = weather_response.json()

    current = weather_data.get("current", {})
    description = weather_code_to_description(current.get("weather_code"))

    return {
        "name": location.get("name", city_name),
        "country": location.get("country", "Unknown"),
        "weather": [{"main": description, "description": description}],
        "main": {
            "temp": current.get("temperature_2m"),
            "feels_like": current.get("apparent_temperature"),
            "humidity": current.get("relative_humidity_2m"),
        },
        "wind": {"speed": current.get("wind_speed_10m")},
    }


def get_crypto_data(crypto_name):
    """Search for a cryptocurrency and fetch market details using CoinGecko."""
    search_url = f"https://api.coingecko.com/api/v3/search?query={quote(crypto_name)}"
    search_response = requests.get(search_url, timeout=10)
    search_response.raise_for_status()
    search_data = search_response.json()

    coins = search_data.get("coins", [])
    if not coins:
        raise ValueError("No matching cryptocurrency was found.")

    coin_id = coins[0].get("id")
    if not coin_id:
        raise ValueError("The selected cryptocurrency could not be loaded.")

    market_url = (
        f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
        f"&ids={coin_id}&order=market_cap_desc&per_page=10&page=1&sparkline=false"
    )
    market_response = requests.get(market_url, timeout=10)
    market_response.raise_for_status()
    market_data = market_response.json()

    if not market_data:
        raise ValueError("No market data is available for the selected cryptocurrency.")

    return market_data[0]


def get_news_data(keyword):
    """Fetch news related to a keyword using Hacker News Search (no API key required)."""
    url = f"https://hn.algolia.com/api/v1/search?tags=story&query={quote(keyword)}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    hits = data.get("hits", [])
    if not hits:
        raise ValueError("No news articles were found for the given keyword.")

    articles = []
    for hit in hits[:5]:
        articles.append(
            {
                "title": hit.get("title", "No title"),
                "source": {"name": "Hacker News"},
                "description": f"Points: {hit.get('points', 0)} | Author: {hit.get('author', 'Unknown')}",
                "url": hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}",
            }
        )

    return articles


def filter_lines(lines, keyword):
    """Filter output lines using a user-provided keyword."""
    if not keyword:
        return lines

    keyword = keyword.lower()
    return [line for line in lines if keyword in line.lower()]


def display_weather(data):
    """Show weather results in a clean and formatted way."""
    weather = data["weather"][0]
    main = data["main"]

    print("\n===== Weather Report =====")
    print(f"City: {data['name']}")
    print(f"Country: {data.get('country', 'Unknown')}")
    print(f"Condition: {weather['description']}")
    print(f"Temperature: {main['temp']}°C")
    print(f"Feels Like: {main['feels_like']}°C")
    print(f"Humidity: {main['humidity']}%")
    print(f"Wind Speed: {data['wind']['speed']} m/s")

    filter_keyword = input("\nEnter a keyword to filter the output (press Enter to skip): ").strip()
    summary_lines = [
        f"City: {data['name']}",
        f"Country: {data.get('country', 'Unknown')}",
        f"Condition: {weather['description']}",
        f"Temperature: {main['temp']}°C",
        f"Feels Like: {main['feels_like']}°C",
        f"Humidity: {main['humidity']}%",
        f"Wind Speed: {data['wind']['speed']} m/s",
    ]
    filtered = filter_lines(summary_lines, filter_keyword)

    print("\nFiltered Result:")
    if filtered:
        for line in filtered:
            print(line)
    else:
        print("No matching information found.")


def display_crypto(data):
    """Display cryptocurrency data clearly."""
    print("\n===== Cryptocurrency Report =====")
    print(f"Name: {data.get('name', 'Unknown')}")
    print(f"Symbol: {data.get('symbol', 'N/A').upper()}")
    print(f"Current Price: ${data.get('current_price', 0):,.2f}")
    print(f"Market Cap: ${data.get('market_cap', 0):,.0f}")
    print(f"24h High: ${data.get('high_24h', 0):,.2f}")
    print(f"24h Low: ${data.get('low_24h', 0):,.2f}")
    print(f"24h Change: {data.get('price_change_percentage_24h', 0):.2f}%")

    filter_keyword = input("\nEnter a keyword to filter the output (press Enter to skip): ").strip()
    summary_lines = [
        f"Name: {data.get('name', 'Unknown')}",
        f"Symbol: {data.get('symbol', 'N/A').upper()}",
        f"Current Price: ${data.get('current_price', 0):,.2f}",
        f"Market Cap: ${data.get('market_cap', 0):,.0f}",
        f"24h High: ${data.get('high_24h', 0):,.2f}",
        f"24h Low: ${data.get('low_24h', 0):,.2f}",
        f"24h Change: {data.get('price_change_percentage_24h', 0):.2f}%",
    ]
    filtered = filter_lines(summary_lines, filter_keyword)

    print("\nFiltered Result:")
    if filtered:
        for line in filtered:
            print(line)
    else:
        print("No matching information found.")


def display_news(articles):
    """Show the latest news in a structured format."""
    print("\n===== Latest News =====")
    for index, article in enumerate(articles, start=1):
        print(f"\n{index}. {article.get('title', 'No title')}")
        print(f"Source: {article.get('source', {}).get('name', 'Unknown')}")
        print(f"Description: {article.get('description', 'No description')}")
        print(f"Link: {article.get('url', 'No link')}")

    filter_keyword = input("\nEnter a keyword to filter the articles (press Enter to skip): ").strip()
    if not filter_keyword:
        return

    filtered_articles = [
        article
        for article in articles
        if filter_keyword.lower() in (article.get("title", "").lower() + " " + article.get("description", "").lower())
    ]

    print("\nFiltered News:")
    if filtered_articles:
        for index, article in enumerate(filtered_articles, start=1):
            print(f"\n{index}. {article.get('title', 'No title')}")
            print(f"Source: {article.get('source', {}).get('name', 'Unknown')}")
            print(f"Description: {article.get('description', 'No description')}")
            print(f"Link: {article.get('url', 'No link')}")
    else:
        print("No articles matched your filter.")


def main():
    """Run the program loop."""
    print("Welcome to the API Integration Project")
    print("This app shows how to connect Python to public APIs without any API keys.")

    while True:
        show_menu()
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "4":
            print("Goodbye!")
            break

        try:
            if choice == "1":
                city_name = input("Enter a city name: ").strip()
                if not city_name:
                    raise ValueError("City name cannot be empty.")
                data = get_weather_data(city_name)
                display_weather(data)
                log_request("Weather", city_name, True, "Weather data retrieved successfully")

            elif choice == "2":
                crypto_name = input("Enter a cryptocurrency name (for example Bitcoin): ").strip()
                if not crypto_name:
                    raise ValueError("Cryptocurrency name cannot be empty.")
                data = get_crypto_data(crypto_name)
                display_crypto(data)
                log_request("Cryptocurrency", crypto_name, True, "Crypto data retrieved successfully")

            elif choice == "3":
                keyword = input("Enter a news keyword or category: ").strip()
                if not keyword:
                    raise ValueError("News keyword cannot be empty.")
                articles = get_news_data(keyword)
                display_news(articles)
                log_request("News", keyword, True, "News data retrieved successfully")

            else:
                print("Invalid choice. Please select 1, 2, 3, or 4.")
                log_request("Menu", choice, False, "Invalid menu selection")

        except ValueError as error:
            print(f"\nInput Error: {error}")
            log_request("General", choice, False, str(error))
        except requests.exceptions.RequestException as error:
            print(f"\nNetwork Error: {error}")
            log_request("General", choice, False, f"Network error: {error}")
        except Exception as error:
            print(f"\nUnexpected Error: {error}")
            log_request("General", choice, False, str(error))


if __name__ == "__main__":
    main()
