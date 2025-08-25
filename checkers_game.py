from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def play_checkers():
    driver = webdriver.Chrome()   # or webdriver.Firefox()
    driver.maximize_window()
    driver.get("https://www.gamesforthebrain.com/game/checkers/")

    wait = WebDriverWait(driver, 10)

    # Step 2: Confirm site is up by checking title
    assert "Checkers" in driver.title, "Site did not load properly!"

    # Perform 5 legal moves
    moves = [
        ("space62", "space73"),   # Move 1: orange piece forward
        ("space22", "space13"),   # Move 2
        ("space13", "space35"),   # Move 3
        ("space42", "space53"),   # Move 4
        ("space71", "space53"),   # Move 5

    ]
    # wait for the page to load to start the game?
    text = "Select an orange piece to move."
    wait.until(EC.text_to_be_present_in_element((By.ID, "message"),text))

    print("Game is ready. Start making moves!")

    for piece, target in moves:
        # Click piece
        driver.find_element(By.NAME, piece).click()
        time.sleep(2)
        # Click target square
        driver.find_element(By.NAME, target).click()
        time.sleep(2)

        exp_text = "Make a move."
        actual_text = wait.until(EC.presence_of_element_located((By.ID, "message")))
        act_text = actual_text.text.strip()
        if exp_text == act_text:
            print("Make a move - text appears")
        else:
            print("Make a move - text does not appear")
    # driver.find_element(By.NAME, "space62").click()
    # driver.find_element(By.NAME, "space53").click()
    time.sleep(2)


    # Step 3: Restart game
    restart_link = driver.find_element(By.LINK_TEXT, "Restart...")
    restart_link.click()
    print("clicked Resart... button")
    time.sleep(4)

    # Step 4: Confirm restart successful
    exp_text = "Select an orange piece to move."
    actual_text = wait.until(EC.presence_of_element_located((By.ID, "message")))
    act_text = actual_text.text.strip()
    if exp_text == act_text:
        print("Restart successful!")
    else:
        print(f"Restart failed! Current message: '{act_text}'")
    driver.quit()


if __name__ == "__main__":
    play_checkers()

