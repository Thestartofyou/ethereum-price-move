import requests
import time
import smtplib

# Enter your Coinbase API key and secret
api_key = 'YOUR_API_KEY'
api_secret = 'YOUR_API_SECRET'

# Enter your email address and password for sending alerts
sender_email = 'YOUR_EMAIL_ADDRESS'
sender_password = 'YOUR_EMAIL_PASSWORD'
recipient_email = 'RECIPIENT_EMAIL_ADDRESS'

# Set the initial price to compare against
initial_price = 0

# Continuously monitor the price of Ethereum
while True:
    # Make a request to the Coinbase API to get the current price of Ethereum
    response = requests.get('https://api.coinbase.com/v2/prices/ETH-USD/spot', auth=(api_key, api_secret))
    data = response.json()
    price = float(data['data']['amount'])

    # If this is the first time through the loop, set the initial price to the current price
    if initial_price == 0:
        initial_price = price

    # Calculate the percentage change in price
    percentage_change = abs((price - initial_price) / initial_price) * 100

    # If the percentage change is greater than or equal to 5%, send an email alert
    if percentage_change >= 5:
        # Construct the email message
        subject = 'Ethereum Alert'
        body = f'The price of Ethereum has moved by {percentage_change:.2f}%!'
        message = f'Subject: {subject}\n\n{body}'

        # Send the email using SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(sender_email, sender_password)
            smtp.sendmail(sender_email, recipient_email, message)

        # Reset the initial price to the current price
        initial_price = price

    # Wait for 5 minutes before checking the price again
    time.sleep(300)
