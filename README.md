# Personalized News Aggregator
# Introduction
The Personalized News Aggregator is designed to collect, categorize, and serve news articles from various sources like BBC and CNN. It allows users to retrieve articles based on specific filters and displays the news in a structured manner using FastAPI.  
# Project Overview  
This project scrapes news articles from multiple sources, processes and stores them, and provides an interface for users to search and interact with the news data. The application features web scraping, data preprocessing, and API integration for serving news data.  
# Key Features
Web Scraping: Collects news articles from BBC and CNN.  
Data Preprocessing: Summarizes and categorizes articles using NLP techniques.  
API Endpoints: Provides endpoints for retrieving and searching articles.  
Web Interface: Offers a simple web UI for interaction.  
Categorization: Tags articles into categories based on predefined keywords.  
# Technology Stack
Python 3.12.6  
FastAPI: For building the web API.  
Pandas: For data manipulation and storage.  
Selenium & BeautifulSoup: For web scraping.  
Gensim & SpaCy: For natural language processing.  
Uvicorn: For running the ASGI server.  
# Overview of Code Files
news_aggregator.py: Contains the FastAPI routes and handles API interactions.  
news__extractor.py: Handles web scraping from news sources (BBC, CNN).  
news__categorization.py: Processes and categorizes news articles based on keywords.  
news_articles.csv: CSV file where the scraped and processed articles are stored.  
# API Endpoints
Root (/)  
Description: Serves the homepage for the news aggregator.  
Methods: GET  
Response: HTML content with navigation links.  
Articles (/articles)  
Description: Fetches and displays all stored news articles.  
Methods: GET  
Response: HTML page displaying articles in JSON format.  
Article by ID (/article-id/{id})  
Description: Fetches and displays a specific article based on its ID.  
Methods: GET  
Parameters:  
id (int): The ID of the article.  
Response: JSON content of the requested article.  
Search (/search/{key}/{value})  
Description: Searches and displays articles based on a specific key and value.  
Methods: GET  
Parameters:  
key (str): The field to search (e.g., title, summary, category).  
value (str): The search term.  
Response: JSON content of matching articles  
# execution video :  
"https://drive.google.com/file/d/1FD6xD5A1Vi4OscsMOUsHsZc4x3TCAbOB/view?usp=drive_link"
