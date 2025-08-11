import time
import requests
import os  # <--- Importar la librería 'os' para leer variables de entorno
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- LEER SECRETOS DESDE LAS VARIABLES DE ENTORNO ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def enviar_foto_telegram(imagen_bytes, caption=""):
    """
    Envía una imagen (en bytes) a un chat de Telegram.
    """
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print(
            "Error: Las variables TELEGRAM_TOKEN y TELEGRAM_CHAT_ID no están configuradas."
        )
        return

    print("Enviando foto a Telegram...")
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    files = {"photo": ("screenshot.png", imagen_bytes, "image/png")}
    data = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption}

    response = requests.post(url, files=files, data=data)

    if response.status_code == 200 and response.json().get("ok"):
        print("¡Foto enviada a Telegram con éxito!")
    else:
        print("Error al enviar la foto a Telegram.")
        print(response.text)


def tomar_y_enviar_screenshot():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("window-size=1280,720")

    driver = webdriver.Chrome(options=chrome_options)
    url = "https://www.cobanoairport.com/camara-2/"

    print(f"Accediendo a la URL: {url}")

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 15)

        print("Cambiando al iframe de la cámara...")
        iframe_selector = (By.XPATH, "//iframe[contains(@src, 'skylinewebcams')]")
        wait.until(EC.frame_to_be_available_and_switch_to_it(iframe_selector))

        print("Haciendo clic en 'Play'...")
        play_button_selector = (By.CSS_SELECTOR, "div.player-poster.clickable")
        play_button = wait.until(EC.element_to_be_clickable(play_button_selector))
        play_button.click()

        print("Esperando a que el video cargue...")
        time.sleep(5)

        print("Tomando screenshot...")
        video_element_selector = (By.CSS_SELECTOR, "video[data-html5-video]")
        video_element = wait.until(
            EC.visibility_of_element_located(video_element_selector)
        )

        screenshot_bytes = video_element.screenshot_as_png
        print("¡Éxito! Screenshot tomado.")

        # --- ENVIAR LA IMAGEN A TELEGRAM ---
        enviar_foto_telegram(
            screenshot_bytes, caption="Cámara del Aeropuerto de Cóbano"
        )

    except Exception as e:
        print(f"Ocurrió un error general: {e}")
    finally:
        print("Cerrando el navegador.")
        driver.quit()


if __name__ == "__main__":
    tomar_y_enviar_screenshot()
