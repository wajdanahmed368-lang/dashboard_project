# IPL Exploratory Data Analysis Dashboard

An interactive, professional-grade data visualization dashboard for analyzing the Indian Premier League (IPL) cricket datasets (`matches.csv` and `deliveries.csv`). Built with a modern **Flask Python Backend** and a responsive **HTML+JS Frontend** featuring a cyber-sports dark glassmorphism theme. 

## Features
- **10 Core Visualization Charts**:
  1. **Pie Chart**: Toss Decision Distribution (`bat` vs `field`).
  2. **Histogram**: Target Runs Frequency Distribution (with KDE curve).
  3. **Line Chart**: Trend of Matches Played over seasons.
  4. **Bar Chart**: Top 10 Teams by Wins count.
  5. **Scatter Plot**: Target Runs vs. Victory Margin (colored by win mode).
  6. **Box Plot**: Victory Margin Spread by Win Type (Runs vs Wickets).
  7. **Heatmap**: Correlation Matrix of key match attributes.
  8. **Area Chart**: Stacked Cumulative Wins trajectory for the top 4 teams.
  9. **Count Plot**: Top 10 host cities.
  10. **Violin Plot**: Target Score Density Spread across IPL seasons.
- **Dynamic Interactivity & Linked Filtering**:
  - **Date Range Picker**: Filter matches between start and end dates.
  - **Category Select**: Dropdown filter for IPL Seasons.
  - **Multi-Select Filter**: Filter matches by checking one or multiple teams.
  - **Numerical Slider**: Filter matches by a minimum winning margin.
  - **Keyword Search**: Free-text search filtering by venue, winner, or Player of the Match.
  - **Reset Button**: Instantly restores default parameters.
- **KPI Metrics Panel**: Updates dynamically to show Total Matches, Total Runs Scored, Average Target, and Toss Impact (Win %).
- **Vercel Deployable**: Configured for serverless Python deployment on Vercel.

---

## Folder Structure
```
/dashboard_project/
├── data/
│   ├── matches.csv              # Match details dataset (DO NOT RENAME)
│   └── deliveries.csv           # Ball-by-ball details dataset (DO NOT RENAME)
├── notebooks/
│   └── analysis.ipynb           # Exploratory Data Analysis (EDA) Jupyter Notebook
├── api/
│   └── index.py                 # Vercel Serverless Function entry point
├── app.py                       # Main Flask web application (Local runner)
├── charts.py                    # Matplotlib/Seaborn visualization layer
├── filters.py                   # Pandas-based filtering and KPI logic
├── requirements.txt             # Project Python dependencies
├── vercel.json                  # Vercel serverless deployment config
├── index.html                   # Dashboard web markup
├── style.css                    # Glassmorphism cyber-sports styling
├── script.js                    # AJAX query triggers and page updates
└── README.md                    # Project documentation
```

---

## Setup and Local Installation

### Prerequisites
- Python 3.8 or higher.
- `pip` package manager.

### 1. Install Dependencies
Navigate to the `/dashboard_project` directory and install the required libraries:
```bash
pip install -r requirements.txt
```

### 2. Run the Local Server
Execute the Flask server:
```bash
python app.py
```

### 3. Open in Browser
Once running, open your web browser and navigate to:
```
http://localhost:5000
```

---

## Vercel Deployment Instructions

The project is pre-configured to build on Vercel using the Vercel Python builder.

### Option A: Via Vercel CLI (Recommended)
1. Install Vercel CLI globally:
   ```bash
   npm install -g vercel
   ```
2. Navigate to the `/dashboard_project/` folder.
3. Run the deployment command:
   ```bash
   vercel
   ```
4. Follow the command-line prompts to connect your account and deploy. Use default configurations when prompted.

### Option B: Via GitHub Integration
1. Push the `/dashboard_project` folder as a repository to GitHub.
2. Import the repository in your Vercel Dashboard.
3. Vercel will automatically read the `vercel.json` and deploy your static files alongside the serverless Flask routes.

---

## Technical Stack & Libraries
- **Backend Data Layer**: Python, Pandas, NumPy
- **Visualizations**: Matplotlib, Seaborn
- **API Framework**: Flask
- **Frontend Layer**: Vanilla HTML5, CSS3 Custom Properties (CSS variables, backdrop blur), Vanilla JS (Fetch API)

---

## Course Details
- **Course Name**: Exploratory Data Analysis
- **Instructor**: Ali Hassan Sherazi
- **Submission Date**: 05-June-2026
