import json
import nodriver
import asyncio
import logging
from flask import Flask, jsonify
from nissei import Nissei
import logfire


# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)

logfire.configure(token='pylf_v1_us_vgCM05Ppc7t55MQKpWWhqp8CQh8mPTr6D7qmY6tNTvnd')
logfire.configure()


app = Flask(__name__)

def run_scraper():
    url = "https://nissei.com/py/belleza-salud-cosmeticos/tonico-purificante-facial-skin1004-madagascar-centella-tea-trica-210ml"
    logging.info(f"Iniciando scraper para la URL: {url}")

    async def main():
        try:
            logging.info("Iniciando navegador Nodriver...")
            browser = await nodriver.start(
                path="/usr/bin/google-chrome",
                headless=True,
                chrome_args=["--no-sandbox", "--disable-dev-shm-usage"],
                lang="es-ES",
                no_sandbox=True,
                disable_gpu=True,
            )
            logging.info("Navegador iniciado correctamente.")

            logging.info(f"Accediendo a la página: {url}")
            page = await browser.get(url)
            await asyncio.sleep(2)

            logging.info("Obteniendo contenido HTML de la página...")
            response = await page.get_content()
            await asyncio.sleep(0.1)

            logging.info("Deteniendo navegador...")
            browser.stop()
            await asyncio.sleep(0.1)

            logging.info("Iniciando scraping con clase Nissei...")
            nissei = Nissei(response)
            await nissei.scraping()
            logging.info("Scraping finalizado correctamente.")

            return json.dumps(nissei.scraping_output, indent=2)

        except Exception as e:
            logging.exception("Error durante la ejecución de main()")
            raise e

    try:
        return nodriver.loop().run_until_complete(main())
    except Exception as e:
        logging.error(f"Error al ejecutar run_scraper: {str(e)}")
        raise e

@app.route('/scrape', methods=['GET'])
def scrape():
    logging.info("Petición recibida en /scrape")
    try:
        result = run_scraper()
        logging.info("Scraper ejecutado correctamente, enviando respuesta.")
        return jsonify({"data": result})
    except Exception as e:
        logging.error(f"Error en el endpoint /scrape: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    logging.info("Iniciando servidor Flask...")
    app.run(debug=True, host='0.0.0.0', port=80)
