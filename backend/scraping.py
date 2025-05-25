from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from bs4 import BeautifulSoup
from bs4.element import Tag
import requests
import bleach
from bleach import clean
import multiprocessing
import time
import warnings
import os
from bleach.css_sanitizer import CSSSanitizer
import tinycss2

# Configure Flask app
from flask import Blueprint, render_template

main = Blueprint('main', __name__)


main.secret_key = "Alexander Oluwaseun Kwesi"
CORS(main)

# Suppress multiprocessing resource tracker warnings
warnings.filterwarnings("ignore", category=UserWarning, message="resource_tracker:.*")

last_scraped_data = {}


# Background worker function using semaphore
def worker(sem):
    print("Worker: Trying to acquire semaphore...")
    sem.acquire()
    print("Worker: Semaphore acquired.")
    time.sleep(2)  # Simulated work
    print("Worker: Releasing semaphore.")
    sem.release()
    print("Worker: Done.")

# Scraping endpoint
@main.route('/scrapes', methods=['POST'])
def scrapes():
    if request.method == 'POST':

        #if not request.is_json:
            #return jsonify({
                #"error": "Unsupported Media Type: Expected application/json"
            #}), 415

        # Optional: Enforce Accept header for JSON
        #if 'application/json' not in request.headers.get('Accept', ''):
            #return jsonify({
                #"error": "Not Acceptable: Client must accept application/json"
            #}), 406

        data = request.get_json()
        url = data.get('url_')

        if not url:
            return jsonify({
                "error": "Missing required field: 'url_'"
            }), 400

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            divs = soup.find_all('div', class_="container")

            #allowed_tags = list(bleach.sanitizer.ALLOWED_TAGS) + [
               # "p", "div", "span", "h1", "h2", "h3", "ul", "li", "strong", "em", 
               # "table", "thead", "tbody", "tr", "th", "td"
            #]
            #allowed_attrs = {
            #    "*": ["class", "style"],
            #    "a": ["href", "title"],
            #    "img": ["src", "alt", "title"]
            #}

            #css_sanitizer = CSSSanitizer(
            #    allowed_css_properties=[
            #        'color', 'background-color', 'font-size', 'font-weight',
            #        'text-align', 'margin', 'padding', 'border'
            #    ]
            #)

            #cleaned_data = [
            #    clean(str(tag), tags=allowed_tags, attributes=allowed_attrs, #css_sanitizer=css_sanitizer)
            #    for tag in divs if isinstance(tag, Tag)
            #]
            
            responses = [
                str(tag).replace("\n",'') if isinstance(tag, Tag) else str(tag).replace('\n','')
                for tag in divs
            ]
               
            #for responses in divs:
            
            print(responses)
            return jsonify({"responses": responses}), 200
                #return Response(responses, content_type='text/html')

        except requests.exceptions.RequestException as e:
            return jsonify({
                "error": f"Request failed: {str(e)}"
            }), 500



