from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import keyboard
import pyperclip
import time
from sqlalchemy import create_engine, text
from datetime import datetime
import json
import re
from database import db
from unidecode import unidecode


from dotenv import load_dotenv

load_dotenv()



lista_departamentos = [
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/games/l/ga/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "games"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/ar-e-ventilacao/l/ar/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "ar_ventilacao"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/artesanato/l/am/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "artesanato"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/artigos-para-festa/l/af/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "artigos_Festa"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/audio/l/ea/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "audio"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/automotivo/l/au/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "automotivo"),
    ("https://www.magazinevoce.com.br/magazineprecompraoficial/bebe/l/bb/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "bebes"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/beleza-and-perfumaria/l/pf/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "beleza_perfumaria"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/brinquedos/l/br/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "brinquedos"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/cama-mesa-e-banho/l/cm/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "cama_mesa_banho"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/cameras-e-drones/l/cf/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "cameras_drones"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/casa-e-construcao/l/cj/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "casa_construcao"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/casa-inteligente/l/ci/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "casa_inteligente"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/celulares-e-smartphones/l/te/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "celulares_smartphones"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/colchoes/l/co/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "colchoes"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/comercio-e-industria/l/pi/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "comercio_industria"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/cursos/l/cr/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "cursos"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/decoracao/l/de/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "decoracao"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/eletrodomesticos/l/ed/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "eletrodomesticos"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/eletroportateis/l/ep/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "eletroportateis"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/esporte-e-lazer/l/es/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "esporte_lazer"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/ferramentas/l/fs/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "ferramentas"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/filmes-e-series/l/fm/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "filmes_series"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/flores-e-jardim/l/fj/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "flores_jardim"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/informatica/l/in/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "informatica"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/instrumentos-musicais/l/im/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "instrumentos_musicais"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/livros/l/li/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "livros"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/mercado/l/me/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "mercado"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/moda/l/md/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "moda"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/moveis/l/mo/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "moveis"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/musica-e-shows/l/ms/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "musica_shows"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/natal/l/na/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "natal"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/papelaria/l/pa/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "papelaria"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/pet-shop/l/pe/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "pet_shop"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/religiao-e-espiritualidade/l/rg/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "religiao_espiritualidade"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/relogios/l/re/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "relogios"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/saude-e-cuidados-pessoais/l/cp/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "saude_cuidados_pessoais"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/servicos/l/se/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "servicos"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/suplementos-alimentares/l/sa/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "suplementos_alimentares"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/tablets-ipads-e-e-reader/l/tb/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "tablets_ipads_ereaders"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/telefonia-fixa/l/tf/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "telefonia_fixa"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/tv-e-video/l/et/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "tv_video"),
    # ("https://www.magazinevoce.com.br/magazineprecompraoficial/utilidades-domesticas/l/ud/delivery_magalu---magalu_indica/?page=1&sortOrientation=desc&sortType=soldQuantity", "utilidades_domesticas")
]



def sql_build_and_insert(list_of_values):
    values_str = list_of_values
    sql_statement = f"""INSERT INTO public.product (title,
                                            description,
                                            price,
                                            associate_url,
                                            origin_url,
                                            price_historic,
                                            category,
                                            image_url,
                                            store,
                                            text_normalized
                                        ) VALUES {values_str} ;"""
    db.execute(sql_statement)
    return True


def extrair_valor(texto):
    # Extrai os dígitos e o ponto decimal do texto
    correspondencia = re.search(r"\d{1,3}(?:\.\d{3})*(?:,\d{2})?", texto)
    if correspondencia:
        valor_formatado = correspondencia.group().replace(".", "").replace(",", ".")
        return int(float(valor_formatado))


def mercado_livre():
    user_dir = 'C:/tmp/selenium'
    
    # Configuração do WebDriver
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    options.add_argument(f"user-data-dir={user_dir}")


    # Inicialização do WebDriver
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 5)

    current_date = datetime.now()


    # navega entre as categorias
    for href, departamento in lista_departamentos:

        driver.get(href)

        print(departamento)
        # navega nas paginações
        for page in range(2, 6):
            try:
                pagination = f"""//*[@id="__next"]/div/main/section[4]/div[3]/nav/ul/li[{page}]"""
                wait.until(EC.presence_of_element_located((By.XPATH, pagination))).click()
                driver.find_element(By.XPATH, pagination)
                time.sleep(2)
                pagination_url = driver.current_url

                for product_sequence in range(1, 60):
                    time.sleep(2)
                    try:
                        # preço no card
                        try:
                            price_origin = driver.find_element(By.XPATH, f"""//*[@id="__next"]/div/main/section[4]/div[2]/div/ul/li[{product_sequence}]/a/div[3]/div[2]/div/div/p""").text
                        except:
                            price_origin = driver.find_element(By.XPATH, f"""//*[@id="__next"]/div/main/section[4]/div[2]/div/ul/li[{product_sequence}]/a/div[3]/div[1]/div/div/p""").text

                        try:
                            wait.until(EC.presence_of_element_located((By.XPATH, f"""//*[@id="__next"]/div/main/section[4]/div[2]/div/ul/li[{product_sequence}]"""))).click()
                        except:
                            break

                        # # TRABALHAR NOS DADOS AQUI
                        # NAME
                        title = wait.until(EC.presence_of_element_located((By.XPATH, f"""//*[@id="__next"]/div/main/section[2]/div[2]/h1"""))).text

                        # DESCRIPTTION
                        description = driver.execute_script("""return document.querySelector('meta[name="description"]').getAttribute("content");""")

                        price = extrair_valor(price_origin)

                        # URL_ORIGIN
                        origin_url = driver.execute_script("""return document.querySelector('meta[property="og:url"]').getAttribute("content");""")

                        associate_url = driver.current_url

                        categoria_txt = departamento
    
                        text_normalized = unidecode(title+description).lower()
                        # Find the figure element using the class name
                        # Execute JavaScript para obter o valor da meta tag
                        image_url = driver.execute_script("""return document.querySelector('meta[property="og:image"]').getAttribute("content");""")

                        # Trate o price_historic separadamente
                        price_historic_case = f"""[{json.dumps({"date": f"{current_date}", "price": price})}]"""
                                                # Crie um dicionário com os valores dos bind variables
                        values = f"""('{title}', '{description}', {price}, '{associate_url}','{origin_url}', '{price_historic_case}', '{categoria_txt}', '{image_url}', 'magazine luiza', '{text_normalized}')"""
                        insert = sql_build_and_insert(values)
                       
                    except:
                        print("ERRROOOOOOOOOOOOOOU")
                        pass
                    finally:
                        driver.get(pagination_url)
                        print("VARIFICA QUANTIDADE DE PRODUCT", product_sequence)

            except:
                time.sleep(2)
                break

        
        driver.back()

    driver.quit()




mercado_livre()


