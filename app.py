from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', result=None)

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']
    tag = request.form['tag']
    attributes = request.form['attributes']
    
    download_images = 'download_images' in request.form
    handle_pagination = 'handle_pagination' in request.form
    scrape_js_content = 'scrape_js_content' in request.form

    result = []

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Handle attributes if provided
        if attributes:
            attr_dict = {}
            for attr in attributes.split(','):
                key_value = attr.split('=')
                if len(key_value) == 2:
                    attr_dict[key_value[0].strip()] = key_value[1].strip()
            elements = soup.find_all(tag, attrs=attr_dict)
        else:
            elements = soup.find_all(tag)

        for element in elements:
            result.append(element.text.strip())
        
        # Handle download_images option if checked
        if download_images:
            images = soup.find_all('img')
            for img in images:
                img_url = img.get('src')
                if img_url:
                    result.append(f"Image URL: {img_url}")

    except Exception as e:
        result.append(f"Error occurred: {str(e)}")

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run()
