import os
import time
import base64
import PyPDF2
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv

def setup_selenium_driver(download_dir: str):
    """Set up the Selenium WebDriver with specified download directory."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    prefs = {
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True,
        "download.open_pdf_in_system_reader": False,
        "profile.default_content_settings.popups": 0,
        "download.default_directory": download_dir,
        "download.directory_upgrade": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def wait_for_downloads(download_dir: str) -> None:
    """Wait for the downloads to complete by checking for .crdownload files."""
    print("Waiting for downloads", end="")
    while any(filename.endswith(".crdownload") for filename in os.listdir(download_dir)):
        time.sleep(2)
        # print(".", end="")
    # print(" done!")

def download_pdf(url: str) -> str:
    """Download the PDF from the specified URL and return the file path."""
    download_dir = os.getenv('FILE_STORAGE_LOC')
    driver = setup_selenium_driver(download_dir)
    driver.get(url)
    time.sleep(2)  # Wait for the download to start
    wait_for_downloads(download_dir)
    driver.quit()  # Use quit instead of close to ensure proper cleanup

    return os.path.join(download_dir, url.split('/')[-1])

def get_base64_string(filepath: str) -> str:
    """Convert PDF file to a base64 encoded string."""
    with open(filepath, "rb") as file:
        binary_data = file.read()
    base64_string =base64.standard_b64encode(binary_data).decode("utf-8")
    return {
            'agent_type': 'anthropic',
            'content': [base64_string]
        }

def get_file_stream(filepath: str):
    """Return a file stream for the given PDF file."""
    file_stream =  [open(filepath, 'rb')]
    return {
            'agent_type': 'openai',
            'content': file_stream
        }

def pdf_preprocessing(filepath: str) -> dict:
    """Process the PDF file and return the agent mode."""
    with open(filepath, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)

    if num_pages < 100:
        return get_base64_string(filepath=filepath)
    else:
        return get_file_stream(filepath)

if __name__ == "__main__":
    load_dotenv()
    download_directory = os.getenv('FILE_STORAGE_LOC')
    pdf_url = "https://example.com/sample.pdf"  # Replace with actual PDF URL
    filepath = download_pdf(pdf_url, download_directory)
    # print(pdf_preprocessing(filepath)['agent_type'])
