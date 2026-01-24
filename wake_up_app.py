import asyncio
from playwright.async_api import async_playwright

# Lista de tus aplicaciones
APPS = [
    "https://forecast-demand-retail.streamlit.app/",
    "https://smartretail-crm-intelligence.streamlit.app/",
    "https://price-optimization-model.streamlit.app/",
    "https://socioeconomic-status-classification-model.streamlit.app/",
    "https://firebird-erp-analytics-dashboard.streamlit.app/",
    "https://apporization-rate-estimation.streamlit.app/",
    "https://quantitative-analysis.streamlit.app/",
    "https://mathematical-modeling-of-covid.streamlit.app/",
    "https://circumbinary-planet-stability.streamlit.app/"
]

async def wake_app(browser, url):
    # Creamos un contexto con un User-Agent real para evitar bloqueos
    context = await browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    page = await context.new_page()
    
    try:
        print(f"Visitando: {url}")
        # Tiempo de espera de 60 segundos para permitir carga lenta de Streamlit
        await page.goto(url, wait_until="networkidle", timeout=60000)
        
        # El selector busca el texto exacto del boton de hibernacion
        wake_button = page.get_by_text("Yes, get this app back up!")
        
        if await wake_button.is_visible():
            print(f"App dormida detectada. Despertando: {url}")
            await wake_button.click()
            # Esperamos 15 segundos para asegurar que la señal llegue al servidor
            await page.wait_for_timeout(15000) 
            print(f"Senal de reactivacion enviada con exito a: {url}")
        else:
            print(f"La app {url} ya esta despierta.")
            
    except Exception as e:
        print(f"Error procesando {url}: {str(e)}")
    finally:
        await page.close()
        await context.close()

async def main():
    async with async_playwright() as p:
        # Iniciamos el navegador en modo headless (sin ventana)
        browser = await p.chromium.launch(headless=True)
        # Ejecutamos todas las visitas en paralelo para ahorrar tiempo
        tasks = [wake_app(browser, url) for url in APPS]
        await asyncio.gather(*tasks)
        await browser.close()
        print("Proceso de mantenimiento finalizado.")

if __name__ == "__main__":
    asyncio.run(main())
