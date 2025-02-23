from openai import OpenAI
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set API key via environment variable (recommended)
os.environ["OPENAI_API_KEY"] = ""
client = OpenAI()

def generate_booking_plan(user_request):
    prompt = f"Decompose this travel booking task into step-by-step instructions: {user_request}"
    completion = client.chat.completions.create(
        model="gpt-4o-mini",  # Change to "gpt-4" if available
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=150,
    )
    plan = completion.choices[0].message.content.strip()
    return plan

def execute_booking(plan):
    # Initialize WebDriver
    driver = webdriver.Chrome()
    driver.set_window_size(2560, 1330)  # Ensure consistent window size

    try:
        # Open the Cleartrip website
        driver.get("https://www.cleartrip.com")

        # Wait until the page loads
        wait = WebDriverWait(driver, 10)

        # Try to close any popup if it appears
        try:
            close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".pb-1 > .c-pointer")))
            close_button.click()
            print("Popup closed successfully.")
        except Exception:
            print("No popup found or already closed.")

        # Click on "Flights" section
        flight_tab = driver.find_element(By.CSS_SELECTOR, ".fs-4")
        flight_tab.click()

        # Select 'One-way' trip (optional step based on UI)
        one_way_option = driver.find_element(By.CSS_SELECTOR, ".ls-reset:nth-child(1) .sc-eqUAAy")
        one_way_option.click()

        # Select 'From' city
        from_city = driver.find_element(By.CSS_SELECTOR, ".field-1 > .fs-16")
        from_city.click()
        from_city.send_keys("Bhubaneswar")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".tt-ellipsis"))).click()

        # Select 'To' city
        to_city = driver.find_element(By.CSS_SELECTOR, ".field-2 > .fs-16")
        to_city.click()
        to_city.send_keys("Bangalore")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".tt-ellipsis"))).click()

        # Select travel date (fixed selector for the correct day)
        date_picker = driver.find_element(By.CSS_SELECTOR, ".c-inherit:nth-child(2)")
        date_picker.click()
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".DayPicker-Day[aria-disabled='false']"))).click()

        # Click on search button
        search_button = driver.find_element(By.CSS_SELECTOR, ".cIApyz")
        search_button.click()

        print("Flight search executed successfully.")

        # Allow time to view results before quitting
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".App > .flex-1")))

    except Exception as e:
        print("Error during booking execution:", str(e))

    finally:
        driver.quit()



if __name__ == "__main__":
    user_request = "Book a flight from New York to Los Angeles on March 10, 2025."
    plan = generate_booking_plan(user_request)
    print("Generated Plan:\n", plan)
    execute_booking(plan)
