import requests
from datetime import datetime
import smtplib
import os
from dotenv import load_dotenv

load_dotenv("keys.env")

MY_LAT = float(os.environ.get("MY_LAT"))  # Your latitude
MY_LONG = float(os.environ.get("MY_LONG"))  # Your longitude

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data_iss = response.json()

iss_latitude = float(data_iss["iss_position"]["latitude"])
iss_longitude = float(data_iss["iss_position"]["longitude"])

def is_near_and_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    time_response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    time_response.raise_for_status()
    data_time = time_response.json()
    sunrise = int(data_time["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data_time["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if iss_latitude >= MY_LAT - 5 and iss_latitude >= MY_LAT + 5 and sunset <= time_now <= sunrise:
        return True
    else:
        return False


if is_near_and_dark():
    MY_EMAIL = os.environ.get("MY_EMAIL")
    PASSWORD = os.environ.get("PASSWORD")
    RECIPIENT = os.environ.get("RECIPIENT")

    subject = "The ISS is near."
    body = "Look up!"
    msg = f"Subject: {subject}\n\n{body}"  # The \n\n is to write the body of the msg, it recognizes it as such.

    with smtplib.SMTP("smtp-mail.outlook.com", port=587) as connection:
        connection.starttls()  # It makes the connection secure
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=RECIPIENT, msg=msg)
        connection.close()
