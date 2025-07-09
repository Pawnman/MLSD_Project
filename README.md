# MLSD_Project

<h1>Smartphone Price Prediction using Machine Learning</h1>
<p>Created by Maksim Peshkov</p>

<p>Tech Stack:
  <li>Python, Aiogram, CatBoost, Docker, Pandas, Joblib</li></p>
<p>Key Skills:
  <li>Telegram Bot Development, Machine Learning, Data Analysis & Processing, Docker, Model Deployment</li></p>

<h2>Project Overview:</h2>
<p>This project, part of the ML System Design course, is focused on developing a Telegram bot that helps users estimate the average rental price of an apartment based on the data they provide, including district, number of rooms, and total square meters. The tool offers users a quick and easy way to get an estimated rent price based on their specified parameters. The key features of the project include prediction accuracy and ease of use, making it useful for potential tenants and property owners. </p>

<h2>Business Goal:</h2>
<p>The goal of this project is to provide a convenient and accurate tool for estimating rental prices, which can attract users and increase the appeal of our platform or real estate services. By offering accurate predictions, the bot can become a valuable asset for both renters and property owners looking for insights into the rental market. </p>


<h2>Machine Learning Goal:</h2>
<p>The machine learning objective is to develop a model capable of predicting the average rental price of an apartment based on parameters such as the neighborhood, number of rooms, and area. We aim to create an accurate and reliable algorithm that ensures high precision in forecasting real estate prices, making the service both useful and competitive in the real estate market.</p>

<h2>Machine Learning Model:</h2>
<p>The CatBoost Regressor is used in this project as the machine learning model, which is based on gradient boosting over decision trees. It is a robust regression model for predicting numerical values like rental prices.</p>

<h2>Project Architecture:</h2>
  <li>Telegram Bot: The bot collects user inputs and provides apartment rent price predictions.</li>
  <li>Machine Learning Model: A trained model that predicts the price based on user inputs.</li>
  <li>Data Parser: A web scraper (CianParser) extracts real estate data from the Cian website for the training and prediction process.</li>
    <li>Docker Container: The project is containerized using Docker for easier deployment.</li>

<h2>Bot Link</h2>
<p>https://t.me/apartment_rent_price_bot</p>


<h2>Commands to Build and Run the Project:</h2>
To build the project:
docker build -t mlsd_project .

To run the project:
docker run mlsd_project

