from playwright.async_api import async_playwright
import asyncio
import time
import os
from datetime import datetime

# Función asincrónica principal
async def main():
    async with async_playwright() as p:
        # Configuración de la extensión y directorio de usuario
        user_data_dir = os.path.join(os.getcwd(), 'pw-temp')

        # Lanzar el contexto del navegador con la extensión
        browser = await p.chromium.launch_persistent_context(user_data_dir, 
                                                            headless=False
                                                            )

        # Define las cookies
        print('-> Agregando cookies...')
        cookies = [
            {
                'name': 'cookieName',
                'value': 'cookieValue',
                'domain': 'cookieDomain',
                'path': '/',
                'expires': datetime(2099, 1, 1).timestamp(), #example
                'http_only': True,
                'secure': True,
                'same_site': 'Lax'
            },
            # Agregar más cookies si es necesario
        ]

        # Agregar cookies al contexto
        await browser.add_cookies(cookies)

        # Crear una nueva página
        page = await browser.new_page()

        # Establecer el tamaño del viewport
        await page.set_viewport_size({"width": 1920, "height": 1080})

        # Espera para evitar problemas de sincronización
        await asyncio.sleep(1)

        # Navegar a la URL
        print('-> Navegando a la URL...')
        await page.goto('urlToNavigate')

        # Espera para evitar problemas de sincronización
        await asyncio.sleep(2)

        # Interactúa con la página
        await page.click('body')

        # Espera para evitar problemas de sincronización
        await asyncio.sleep(2)

        print('!!! Capturando !!!')

        # Selector del elemento a capturar
        selector = 'selectorCssElementoAcapturar'

        # Obtener dimensiones del elemento
        dimensions = await page.evaluate('''(selector) => {
            const element = document.querySelector(selector);
            return {
                width: element.scrollWidth,
                height: element.scrollHeight
            };
        }''', selector)

        # Ajustar tamaño del viewport
        await page.set_viewport_size({'width': dimensions['width'], 'height': dimensions['height']})

        # Capturar elemento específico
        element = await page.query_selector(selector)

        await asyncio.sleep(5)

        await element.screenshot(path='element-screenshot.png')

        # Cerrar el contexto del navegador
        print('Cerrando el navegador...')
        await browser.close()
        print('Screenshot tomada y guardada como element-screenshot.png')

# Ejecutar la función principal
asyncio.run(main())
