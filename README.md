#  CitiBike Explorer

**CitiBike Explorer** is a data-driven web app that visualizes Citi Bike rides in NYC. It offers real-time bike availability, ride histories, and interactive station maps to help users explore and understand bike-sharing patterns across the city.

---

##  Features

-  **Live Map** of Citi Bike stations with real-time bike and dock availability
-  **Historical Ride Data** with filters for date range, start/end stations, and ride duration
-  **Station Popularity** statistics and heatmaps for easy exploration
- **Interactive, responsive UI** built with JavaScript and Firebase Hosting for desktop
-  **Robust backend** with Python and PostGIS to support geospatial queries

---

##  Demo

[![Watch on YouTube](https://img.youtube.com/vi/aQjjmlc_es4/0.jpg)](https://www.youtube.com/watch?v=aQjjmlc_es4)

---

## ⚙️ Tech Stack

| Layer       | Tools & Services                                      |
|-------------|-------------------------------------------------------|
| Frontend    | React + Firebase Hosting                              |
| Backend     | Python (Flask) + PostGIS (PostgreSQL)                  |
| Data & APIs | Citi Bike GBFS API, scheduled ride data loader, BigQuery |
| Deployment  | Google Cloud Run                                       |

---

##  How It Works

1️⃣ The frontend provides a chat interface where users ask about station status or trends.  
2️⃣ User queries are sent to an **AI chatbot** powered by Generative AI.  
3️⃣ The chatbot retrieves **real-time station data** and **historical ride data**.  
4️⃣ It analyzes both current availability and historical patterns to generate insights.  
5️⃣ The AI responds with natural-language recommendations or decisions (e.g. rebalancing suggestions, expected demand).  
6️⃣ All services are deployed securely on **Google Cloud** for scalability and reliability.

---
