from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.action_chains import ActionChains
import threading
import time
import random
import os

# Flask App
app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Aviator Predictor Bot</title>
        <style>
            body {
                background-color: black;
                color: white;
                font-family: Arial, sans-serif;
                text-align: center;
            }
            h1 {
                color: red;
                font-size: 48px;
            }
            form {
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                display: inline-block;
                margin-top: 20px;
            }
            label {
                font-weight: bold;
                color: black;
            }
            input, select, button {
                display: block;
                margin: 10px auto;
                padding: 10px;
                width: 80%;
                font-size: 16px;
            }
            button {
                background-color: red;
                color: white;
                border: none;
                cursor: pointer;
            }
            button:hover {
                background-color: darkred;
            }
            .logo {
                width: 200px;
                margin: 20px auto;
            }
        </style>
    </head>
    <body>
        <img class="logo" src="https://via.placeholder.com/200x100.png?text=Aviator+Logo" alt="Aviator Logo">
        <h1>Aviator Predictor Bot</h1>
        <form action="/start" method="post">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required><br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required><br>
            <label for="platform">Platform:</label>
            <select id="platform" name="platform">
                <option value="hollywoodbets">Hollywoodbets</option>
                <option value="lottostar">LottoStar</option>
            </select><br>
            <button type="submit">Start Bot</button>
        </form>
    </body>
    </html>
    '''

@app.route('/start', methods=['POST'])
def start():
    username = request.form['username']
    password = request.form['password']
    platform = request.form['platform']

    # Start bot in a separate thread
    threading.Thread(target=start_bot, args=(username, password, platform)).start()
    
    return "Bot started! Check the console for updates."

def start_bot(username, password, platform):
    print("Starting bot...")

    # Set up WebDriver
    driver_path = r"C:\Users\Student\Downloads\edgedriver_win64\msedgedriver.exe"  # Adjust this to your WebDriver path
    service = EdgeService(driver_path)
    driver = webdriver.Edge(service=service)
    
    # Navigate to the selected platform
    if platform == 'hollywoodbets':
        url = "https://www.hollywoodbets.net"
    elif platform == 'lottostar':
        url = "https://www.lottostar.co.za"

    driver.get(url)
    time.sleep(5)
    
    # Login automation
    try:
        driver.find_element(By.ID, 'username').send_keys(username)
        driver.find_element(By.ID, 'password').send_keys(password)
        driver.find_element(By.ID, 'login-button').click()
        print("Logged in successfully!")
    except Exception as e:
        print("Login error:", e)
    
    # Handle popups
    try:
        popup = driver.find_element(By.CLASS_NAME, 'close-popup')
        popup.click()
        print("Popup closed.")
    except:
        print("No popups detected.")
    
    # Simulate prediction and betting
    while True:
        print("Predicting next round...")
        prediction = random.uniform(1.5, 4.0)  # Placeholder prediction logic
        print(f"Prediction: {prediction:.2f}x")

        try:
            # Simulate placing bet
            bet_button = driver.find_element(By.CLASS_NAME, 'bet-button')
            bet_button.click()
            print("Bet placed!")

            # Simulate early cash-out
            time.sleep(random.randint(2, 4))
            cashout_button = driver.find_element(By.CLASS_NAME, 'cashout-button')
            cashout_button.click()
            print("Cashed out early!")
        except Exception as e:
            print("Betting error:", e)

        # Wait for the next round
        time.sleep(10)
    
    driver.quit()
    print("Bot session ended.")

if __name__ == '__main__':
    app.run(debug=True)
