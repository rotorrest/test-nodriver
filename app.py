import json
import nodriver
import asyncio  # Agregar esta línea
from flask import Flask, jsonify
from nissei import Nissei

app = Flask(__name__)

def run_scraper():
    url = "https://nissei.com/py/belleza-salud-cosmeticos/tonico-purificante-facial-skin1004-madagascar-centella-tea-trica-210ml"

    async def main():
        browser = await nodriver.start(
            headless=True,
            chrome_args=["--no-sandbox", "--disable-dev-shm-usage"],
            lang="es-ES",
            no_sandbox=True,
            disable_gpu=True,
        )

        page = await browser.get(url)
        await asyncio.sleep(2)  # Esta función necesita asyncio
        response = await page.get_content()
        await asyncio.sleep(0.1)  # Espera para asegurarse de que el contenido se cargue correctamente
        await browser.stop()
        await asyncio.sleep(0.1)  # Espera para asegurarse de que el navegador se detenga correctamente
        
        nissei = Nissei(response)
        await nissei.scraping()

        return json.dumps(nissei.scraping_output, indent=2)

    return nodriver.loop().run_until_complete(main())

@app.route('/scrape', methods=['GET'])
def scrape():
    try:
        result = run_scraper()
        return jsonify({"data": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
