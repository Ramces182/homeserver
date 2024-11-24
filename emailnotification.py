import os
from email.message import EmailMessage
import ssl
import smtplib
import requests

def send_email(subject: str, body: str, email_receiver: str = "estif78@live.com.mx"):
    """Send an email with the given subject and body.

    Args:
        subject (str): The subject of the email.
        body (str): The body content of the email.
        email_receiver (str): The recipient's email address. Defaults to 'estif78@live.com.mx'.
    """
    email_sender = os.environ.get("email")
    email_password = os.environ.get("emailpassword")

    if not email_sender or not email_password:
        raise ValueError("Environment variables 'email' or 'emailpassword' are not set.")

    # Create the email message
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    # Secure connection and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

def get_costco_product():
    url = "https://www.costco.com.mx/rest/v2/mexico/products/search?fields=FULL&query=A25WU&pageSize=24&lang=es_MX&curr=MXN"
    
    try:
        # Perform the GET request
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP issues

        # Parse the JSON response
        data = response.json()

        # Check if products exist in the response
        products = data.get("products", [])
        for product in products:
            name = product.get("name", "")
            price_info = product.get("price", {})
            price_value = price_info.get("value", float("inf"))
            
            # Check for the desired product and price condition
            if name.startswith("Apple Watch Ultra 2") and price_value < 15999.0:
                # Save the price in a variable
                price = price_info.get("formattedValue", f"${price_value:.2f}")
                
                # Prepare email details
                subject = "Apple Watch Ultra 2 Price Drop"
                body = f"El Apple Watch Ultra 2 esta a: {price}. checaleeee"
                
                # Call the send_email function
                send_email(subject, body)
                break  # Stop checking once the desired product is found

    except requests.RequestException as e:
        print(f"An error occurred while making the request: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    print ("done")

if __name__ == "__main__":
    get_costco_product()
