import os, json, requests

TEMA = os.environ["NTFY_TEMA"]
PALABRAS = ["calendario", "adviento", "advent", "luxury"]
API = "https://www.maquillajetrendyshop.com/api/catalog_system/pub/products/search"
ARCHIVO = "vistos.json"

def avisar(titulo, msg, url):
    requests.post(f"https://ntfy.sh/{TEMA}", data=msg.encode("utf-8"),
                  headers={"Title": titulo.encode("utf-8"), "Priority": "urgent", "Click": url})

try:
    vistos = set(json.load(open(ARCHIVO)))
except Exception:
    vistos = set()

hay_nuevos = False
for palabra in PALABRAS:
    try:
        r = requests.get(API, params={"ft": palabra},
                         headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
        productos = r.json()
    except Exception as e:
        print("Error consultando", palabra, e)
        continue
    for p in productos:
        nombre = p["productName"]
        pid = p["productId"]
        if any(k in nombre.lower() for k in PALABRAS) and pid not in vistos:
            avisar("¡Salió el calendario!", nombre, p["link"])
            vistos.add(pid)
            hay_nuevos = True

if hay_nuevos:
    json.dump(sorted(vistos), open(ARCHIVO, "w"))
