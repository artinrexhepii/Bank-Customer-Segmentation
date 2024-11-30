# Raiffeisen Bank Customer Analytics Dashboard

## Overview
A sophisticated customer analytics dashboard built for Raiffeisen Bank that leverages machine learning to segment customers and provide personalized product recommendations. The application uses K-means clustering to categorize customers into three distinct segments, enabling targeted marketing strategies and improved customer retention.

## Hackathon Achievement 
This project was developed during the 24-hour Data Hackathon organized by Raiffeisen Bank in 2024. Our team won first place, competing against 5 other teams. The project is intended for hackathon demonstration purposes only.

### Contributors
- [Artin Rexhepi](https://github.com/artinrexhepii)
- [Daris Dragusha](https://github.com/darisdragusha)

## Live Demo 
Try out the live demo of our application here:
[Raiffeisen Bank Analytics Dashboard](https://data-hackathon-raiffeisen-bank.streamlit.app/)

## Features

### 1. Customer Segmentation
- Real-time customer segmentation using machine learning
- Three distinct customer segments:
  - Engaged Mid-Tier Customers
  - Low-Balance Loyalists
  - High-Balance At-Risk Customers
- Detailed segment analysis and characteristics

### 2. Interactive Dashboard
- Overview section with key metrics and visualizations
- Customer profiling with instant segment prediction
- Product recommendations tailored to each segment
- Comprehensive data visualization using Plotly

### 3. Email Marketing Integration
- Automated product recommendation emails
- Personalized HTML email templates
- Direct customer communication capabilities

## Technology Stack
- Python 3.11+
- Streamlit for web interface
- Scikit-learn for machine learning
- Pandas for data manipulation
- Plotly for interactive visualizations
- SMTP for email functionality

## Project Structure
- `ui.py`: Main application interface and logic
- `modelPrediction.ipynb`: Jupyter notebook containing model development
- `clustered_data.csv`: Processed customer data with cluster assignments
- `scaler_and_model.pkl`: Saved ML model and scaler
- `requirements.txt`: Project dependencies

## Customer Segments

### Engaged Mid-Tier Customers 🎯
- Middle-aged customers
- Low tenure, average balance
- Moderate activity with 1-2 products
- Slight exit risk

### Low-Balance Loyalists 💎
- Middle-aged customers
- Moderate tenure, low balances
- Multiple products
- High salary, strong loyalty

### High-Balance At-Risk Customers ⚡
- Middle-aged customers
- Moderate tenure
- Highest average balance
- Fewer products, highest exit risk






