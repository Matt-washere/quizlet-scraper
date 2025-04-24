from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

def get_quizlet_cards(url):
    try:
        # Set up undetected-chromedriver
        options = uc.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        
        # Add random user agent
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        ]
        options.add_argument(f'user-agent={random.choice(user_agents)}')
        
        # Initialize the driver with undetected-chromedriver
        driver = uc.Chrome(options=options)
        
        try:
            # Load the page
            driver.get(url)
            
            # Add random delays to mimic human behavior
            time.sleep(random.uniform(2, 4))
            
            # Scroll down slowly to mimic human behavior
            for i in range(3):
                driver.execute_script(f"window.scrollTo(0, {i * 300});")
                time.sleep(random.uniform(0.5, 1.5))
            
            # Wait for terms to be present with increased timeout
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.SetPageTerm-content"))
            )
            
            # Additional wait to ensure all content is loaded
            time.sleep(2)
            
            # Get all term elements
            term_elements = driver.find_elements(By.CSS_SELECTOR, "div.SetPageTerm-content")
            
            terms = []
            for element in term_elements:
                try:
                    # Add small random delay between processing each term
                    time.sleep(random.uniform(0.1, 0.3))
                    
                    term = element.find_element(By.CSS_SELECTOR, ".SetPageTerm-wordText").text
                    definition = element.find_element(By.CSS_SELECTOR, ".SetPageTerm-definitionText").text
                    
                    if term and definition:  # Only add if both term and definition are not empty
                        terms.append((term, definition))
                except Exception as e:
                    print(f"Error extracting term: {e}")
                    continue
            
            return terms
        
        except Exception as e:
            print(f"An error occurred while scraping: {e}")
            return []
        
        finally:
            driver.quit()
            
    except Exception as e:
        print(f"An error occurred while setting up the driver: {e}")
        return []

if __name__ == "__main__":
    url = input("Enter a quizlet set URL: ")
    cards = get_quizlet_cards(url)
    
    if cards:
        print("\n Flashcards Found:")
        for i, (term, definition) in enumerate(cards, 1):
            print(f"{i}. {term} - {definition}")
    else:
        print("\nNo flashcards were found. The page might be protected or the URL might be invalid.")
