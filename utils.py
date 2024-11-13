from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os 
import time 
from dotenv import load_dotenv
import PyPDF2
import base64

def setup_selenium_driver(download_dir: str):
    # Set up Chrome options to configure the download directory
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service()
    # Set Chrome preferences to automatically download files without prompting
    print(download_dir)
    prefs= {"download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True,
    "download.open_pdf_in_system_reader": False,
    "profile.default_content_settings.popups": 0,
    # add location preference...
    "download.default_directory": download_dir,
    "download.directory_upgrade": True}
    chrome_options.add_experimental_option("prefs", prefs)

    # Use WebDriver Manager to get the correct ChromeDriver version automatically
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def wait_for_downloads()-> None:
    load_dotenv(override=True)
    print("Waiting for downloads", end="")
    while any([filename.endswith(".crdownload") for filename in os.listdir(os.getenv('FILE_STORAGE_LOC'))]):
        time.sleep(2)
        print(".", end="")
    print("done!")

def download_pdf(url)-> str:
    # Send a GET request to the URL
    driver = setup_selenium_driver(download_dir=os.getenv('FILE_STORAGE_LOC'))
    driver.get(url)
    time.sleep(2)
    wait_for_downloads()
    driver.close()

    return url.split('/')[-1]

def pdf_preprocessing(filepath):
    with open(filepath,"rb") as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)

        binary_data = file.read()
        base64_encoded_data = base64.standard_b64encode(binary_data)
        base64_string = base64_encoded_data.decode("utf-8")
        file_streams = [open(path,'rb') for path in [filepath]]

    if num_pages<100:
        return {
            'agent_type':'anthropic',
            'content':[base64_string]
        }
    else:
        return{
            'agent_type':'openai',
            'content':file_streams
        }
    
if __name__=="__main__":
    filepath = "./dataset/Swiggy Limited - RHP.pdf"
    print(pdf_preprocessing(filepath)['agent_type'])