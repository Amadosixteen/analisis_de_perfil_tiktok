import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import yt_dlp

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

try:
    driver = webdriver.Chrome(options=chrome_options)
    
    # 1. BUSCAR LA PESTAÑA DE TIKTOK AUTOMÁTICAMENTE
    tiktok_handle = None
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if "tiktok.com" in driver.current_url.lower():
            tiktok_handle = handle
            break
    
    if not tiktok_handle:
        print("❌ Error: No encontré ninguna pestaña de TikTok abierta en Brave.")
        exit()

    print(f"cuenta: {driver.title}")
    
    print("\n--- INSTRUCCION ---")
    print("1. Ve a la sección 'Compartidos' en TikTok.")
    input("2. presiona ENTER aquí.")

    # 2. SELECTOR FLEXIBLE
    selectores = [
        'div[data-e2e="user-repost-item-list"]',
        'div[class*="DivShareLayoutMain"] div[class*="DivVideoFeedV2"]',
        'main div[class*="DivThreeColumnContainer"]'
    ]
    
    contenedor = None
    for sel in selectores:
        try:
            contenedor = driver.find_element(By.CSS_SELECTOR, sel)
            if contenedor:
                print(f"----------------------")
                break
        except:
            continue

    if not contenedor:
        print("❌ No se pudo localizar la lista de videos.")
        exit()

    # --- LÓGICA DE ORDENAMIENTO VISUAL ---
    elementos_a = contenedor.find_elements(By.TAG_NAME, 'a')
    lista_con_posicion = []
    seen = set()

    for el in elementos_a:
        href = el.get_attribute("href")
        if href and "/video/" in href:
            clean_url = href.split('?')[0]
            if clean_url not in seen:
                # Capturamos la posición Y (vertical) y X (horizontal)
                pos = el.location
                lista_con_posicion.append({
                    'y': pos['y'], 
                    'x': pos['x'], 
                    'url': clean_url
                })
                seen.add(clean_url)

    # Ordenamos primero por Y (fila) y luego por X (columna)
    # Esto garantiza que el orden sea exacto a como se lee (de izquierda a derecha, arriba a abajo)
    lista_con_posicion.sort(key=lambda pos: (pos['y'], pos['x']))
    
    # Extraemos solo las URLs ya ordenadas
    video_urls = [item['url'] for item in lista_con_posicion]

    print(f"\nSe encontro {len(video_urls)} videos en orden visual correcto.")
    
    # 3. EXTRACCIÓN CON YT-DLP
    biblioteca_datos = []
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
        'cookiefile': 'cookies.txt',
        'ignoreerrors': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for index, url in enumerate(video_urls, start=1):
            try:
                print(f"[{index}/{len(video_urls)}] Extrayendo metadatos: {url}")
                info = ydl.extract_info(url, download=False)
                if info:
                    biblioteca_datos.append({
                        "orden_visual": index,
                        "descripcion": info.get('description') or info.get('title'),
                        "hashtags": info.get('tags'),
                        "autor": info.get('uploader'),
                        "url": url
                    })
                time.sleep(0.3)
            except: 
                continue

    # Guardar el JSON ORDENADO y LIMPIO
    with open("datos_brutos.json", "w", encoding="utf-8") as f:
        json.dump(biblioteca_datos, f, indent=4, ensure_ascii=False)
    
    print("\n" + "="*40)
    print("terminado.")
    print(f"Se obtuvieron {len(biblioteca_datos)} videos COMPARTIDOS Y SU INFORMACION.")
    print("="*40)

except Exception as e:
    print(f"❌ Error crítico: {e}")