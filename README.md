# MarketPulse.Monitor

[![Python Version](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A real-time financial asset monitoring dashboard built with Python. It fetches and plots intraday data for multiple tickers using an object-oriented structure and a custom Matplotlib UI.

## Demo

![MarketPulse.Monitor Demo](demo.gif)

## Key Features

- Automatic data refresh and plot updates via `matplotlib.animation`.
- Custom dark-themed UI with a scrolling ticker tape for live data.
- Dynamic on-plot labels and legends displaying the latest asset value.
- Stable layout engine with fixed axes for a smooth, non-jiggling animation.
- Object-Oriented design for clean, scalable, and maintainable code.

## Technologies Used

- Python 3
- yfinance
- Pandas
- Matplotlib & Seaborn

## Setup and Installation

To run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/SEU-USUARIO/MarketPulse-Monitor.git](https://github.com/SEU-USUARIO/MarketPulse-Monitor.git)
    cd MarketPulse-Monitor
    ```

2.  **Create and activate a virtual environment:**
    * On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    * On Windows:
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    * On macOS/Linux:
        ```bash
        python3 src/monitor.py
        ```
    * On Windows:
        ```bash
        python src/monitor.py
        ```

<br>

<details>
<summary><h3>Project Evolution / Evolução do Projeto</h3></summary>

---
#### **v4.0**
- Refactored the initial static script into a real-time, object-oriented application.
- Implemented a multi-panel dashboard with a custom dark theme and color palette.
- Added dynamic UI elements, including a scrolling ticker tape and on-plot value labels.
- Developed a stable layout engine using Matplotlib's Gridspec and manual subplot adjustments to prevent visual artifacts during the animation loop.
- Optimized the animation engine for cross-platform stability.

---
#### **v1.0**
- Initial version of the project.
- Fetched financial data and generated a single, static chart.
---
</details>

<br>

## Author

- **[Alexis Barragam]** - [LinkedIn Profile](https://www.linkedin.com/in/alexisbarragam/)