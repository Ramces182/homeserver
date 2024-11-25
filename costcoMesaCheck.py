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

def get_costco_product(url, priceThreshold, productName):
    
    try:
        # Perform the GET request
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP issues

        # Parse the JSON response
        data = response.json()

        # Extract the product's base price information
        base_price = data.get("price", {})
        price_value = base_price.get("value", float("inf"))
        formatted_price = base_price.get("formattedValue", f"${price_value:.2f}")

        # Check the price condition
        if price_value < priceThreshold:
            # Prepare email details
            subject = productName
            body = f"{productName} está a: {formatted_price}. ¡Checa el precio ahora!"
            
            # Call the send_email function
            send_email(subject, body)

    except requests.RequestException as e:
        print(f"An error occurred while making the request: {e}")
        send_email("Costco Checker Failed", f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        send_email("Costco Checker Failed", f"Error: {e}")

if __name__ == "__main__":
    nombreMesaGrande = "Gabite, Monza, Mesa de Comedor"
    urlMesaGrande = "https://www.costco.com.mx/rest/v2/mexico/products/5948704/?fields=FULL&lang=es_MX&curr=MXN"
    precioMesaGrande = 11999.0
    nombreMesaChica = "Gabite, Lomas Diamante, Mesa de Comedor"
    urlMesaChica = "https://www.costco.com.mx/rest/v2/mexico/products/5948700/?fields=FULL&lang=es_MX&curr=MXN"
    precioMesaChica = 11999.0
    get_costco_product(urlMesaGrande, precioMesaGrande, nombreMesaGrande)
    get_costco_product(urlMesaChica, precioMesaChica, nombreMesaChica)
