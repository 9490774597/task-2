# API Integration Project

## Project Description
This project is a beginner-friendly Python application that demonstrates how to connect to public APIs, parse JSON responses, and display results in a clean and organized way. The app includes a simple menu for weather, cryptocurrency, and news data.

## Features
- User-friendly menu system
- Weather information for any city
- Cryptocurrency market details
- Latest news search by keyword or category
- Search and filter tools for displayed results
- Clean output formatting
- Exception handling for invalid input and network issues
- Request logging to a file for beginner-friendly debugging

## APIs Used
- Weather: Open-Meteo
  - Free public API
  - No API key required
- Cryptocurrency: CoinGecko
  - Free public API
  - No API key required
- News: Hacker News Search API
  - Free public API
  - No API key required

## Installation Steps
1. Install Python 3.9 or newer.
2. Open the project folder.
3. Install the required package:
   ```bash
   pip install -r requirements.txt
   ```
4. No API keys are needed for this project.

## How to Run
Run the program using:
```bash
python api_integration.py
```

## Folder Structure
```text
API-Integration/
├── api_integration.py
├── README.md
├── requirements.txt
└── log.txt
```

## Sample Input / Output
Example:
```text
1. Weather
Enter a city name: London
```

Sample output:
```text
===== Weather Report =====
City: London
Condition: Clear sky
Temperature: 18°C
Humidity: 65%
```

## Technologies Used
- Python
- Requests library
- JSON handling
- File handling for logging

## Future Improvements
- Add a graphical user interface (GUI)
- Add more categories for news
- Save favorite searches
- Use a database for logging
- Add charts for crypto prices

## Notes
This project is designed for beginners and can be used as an internship assignment or a GitHub portfolio project.
