import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def tomar_screenshot_camara():
    """
    Navega a la página de la cámara del Aeropuerto de Cóbano,
    hace clic en play y toma un screenshot del video.
    """
    # --- Configuración de Selenium para correr en un servidor (Headless) ---
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Esencial para servidores, no abre UI.
    chrome_options.add_argument(
        "--no-sandbox"
    )  # Requerido para entornos como Docker/Railway.
    chrome_options.add_argument(
        "--disable-dev-shm-usage"
    )  # Evita problemas de memoria en contenedores.
    chrome_options.add_argument("window-size=1280,720")  # Define un tamaño de ventana.

    # Inicializa el driver
    driver = webdriver.Chrome(options=chrome_options)

    # URL de la cámara
    url = "https://www.cobanoairport.com/camara-2/"

    print(f"Accediendo a la URL: {url}")

    try:
        driver.get(url)

        # Espera de 15 segundos máximo para que los elementos carguen
        wait = WebDriverWait(driver, 15)

        # --- El reproductor de video está dentro de un <iframe> ---
        # Primero, esperamos a que el iframe esté disponible y cambiamos el contexto a él.
        print("Esperando y cambiando al iframe de la cámara...")
        iframe_selector = (By.XPATH, "//iframe[contains(@src, 'skylinewebcams')]")
        wait.until(EC.frame_to_be_available_and_switch_to_it(iframe_selector))
        print("Contexto cambiado al iframe.")

        # --- Hacer clic en el botón de "Play" ---
        # El botón es un div con la clase 'player-poster' y 'clickable'
        print("Buscando el botón de 'Play'...")
        play_button_selector = (By.CSS_SELECTOR, "div.player-poster.clickable")
        play_button = wait.until(EC.element_to_be_clickable(play_button_selector))

        print("Haciendo clic en 'Play'...")
        play_button.click()

        # --- Esperar a que el video comience a reproducirse ---
        # Damos un tiempo prudencial (ej. 5 segundos) para que el stream cargue.
        print("Esperando a que el video cargue...")
        time.sleep(5)

        # --- Tomar el screenshot del elemento <video> ---
        print("Buscando el elemento de video para la captura...")
        video_element_selector = (By.CSS_SELECTOR, "video[data-html5-video]")
        video_element = wait.until(
            EC.visibility_of_element_located(video_element_selector)
        )

        screenshot_path = "camara_cobano_screenshot.png"
        if video_element.screenshot(screenshot_path):
            print(f"¡Éxito! Screenshot guardado en: {screenshot_path}")
        else:
            print("Error al guardar el screenshot.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        # --- Cerrar el navegador para liberar recursos ---
        print("Cerrando el navegador.")
        driver.quit()


# Ejecutar la función
if __name__ == "__main__":
    tomar_screenshot_camara()
