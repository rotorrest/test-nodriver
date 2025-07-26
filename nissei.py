import re
import json


class Nissei:
    def __init__(self, response: str):
        self.response = response

    async def scraping(self):
        if not hasattr(self, "response") or self.response is None:
            raise Exception(
                "No hay respuesta disponible para el scraping."
            )
        original_price_value = 0

        price_match = re.search(
            r"<span id=[\"']old-price-(\d+)[\"'](.*?)data-price-type=[\"']oldPrice[\"'](.*?)><span class=[\"']price[\"']>(.*?)</span></span>",
            self.response,
        )
        if price_match:
            match = re.search(r"(\d[\d\.]*)", price_match.group(4))
            original_price_value = float(match.group().replace(".", "") or 0)

        match = re.search(
            r'<script type="application/ld\+json">(.*?)</script>',
            self.response,
            re.DOTALL,
        )

        if match:
            json_text = match.group(1)
            try:
                data = json.loads(json_text)
            except json.JSONDecodeError as e:
                raise Exception(f"Error al parsear JSON: {e}")

            try:
                sku_value = data.get("sku", "")
                title = data.get("name", "")
                price_value = round(float(data.get("offers", {}).get("price", 0) or 0))
                url_image = data.get("image", "")
                url_product = re.sub(
                    r"^(https|http)\:\/\/", "", data.get("offers", {}).get("url", "")
                )
            except AttributeError as e:
                raise Exception(f"Error al obtener la data desde el JSON: {e}")

            if original_price_value < price_value:
                original_price_value = price_value
                price_value = 0

            self.scraping_output = {
                "sku": sku_value,
                "nombre_producto": title,
                "precio_venta_final": price_value,
                "precio_original": original_price_value,
                "url_producto": url_product,
                "imagen_producto": url_image,
            }
        else:
            self.scraping_output = {
                "sku": "no-chrome",
                "nombre_producto": "Chrome not found",
                "precio_venta_final": 0,
                "precio_original": 0,
                "url_producto": "https://placeholder.com/",
                "imagen_producto": "https://placeholder.com/error.png",
            }
            raise Exception("Error al encontrar la data dentro de la respuesta.")
