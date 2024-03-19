import requests
from bs4 import BeautifulSoup
import re
from database import db
import json
from datetime import datetime
import asyncio
import time

def extrair_valor(texto):
    # Extrai os dígitos e o ponto decimal do texto
    correspondencia = re.search(r"\d{1,3}(?:\.\d{3})*(?:,\d{2})?", texto)
    if correspondencia:
        valor_formatado = correspondencia.group().replace(".", "").replace(",", ".")
        return int(float(valor_formatado))

def enviar_mensagem_webhook(url, mensagem):
    # Cria o payload da mensagem
    payload = {
        "content": mensagem
    }

    # Converte o payload para JSON
    payload_json = json.dumps(payload)

    # Envia a mensagem para o webhook
    response = requests.post(url, data=payload_json, headers={"Content-Type": "application/json"})

    # Verifica se a mensagem foi enviada com sucesso
    if response.status_code == 200:
        print("Mensagem enviada com sucesso!")
    else:
        print(f"Erro ao enviar mensagem: {response.status_code} - {response.text}")

current_date = datetime.now()
webhook_url = "https://discord.com/api/webhooks/1215532903015129149/nDyv8xTp-HnI9nuL8YqEMvOKKqMQsB3XFYXH_XCoDppYQIOos2ftH6_InaJD8j_WYzGN"

async def magalu():
    anuncios = db.execute("SELECT id, origin_url FROM public.product WHERE store = 'magazine luiza'")
    
    verificados = 0
    alterados = 0
    inicio_loop = time.time()
    for data_product in anuncios:

        id = (data_product['id'])
        url = (data_product['origin_url'])
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Use um seletor CSS para encontrar o elemento desejado
                price_element = soup.select_one('[data-testid="price-value"]')
                # Verifica se o elemento foi encontrado antes de tentar acessar seu conteúdo
                if price_element:
                    # Obtém o texto do elemento
                    price_text = price_element.get_text(strip=True)
                    price = extrair_valor(price_text)
                    print("Preço:", price)

                    insert_new_price = f"""[{json.dumps({"date": f"{current_date}", "price": price})}]"""
                    
                    update_price = "{-1,price}"

                    #  --UPDATE 1 COMPRA RO VALOR E O ULTIMO REGISTRO E INCLUI OUTRO NOVO 
                    #  --UPDATE 1 ATUALIZA O VALOR DA ULTIMA DATA
                    query = (f"""UPDATE product
                                SET price = {price}, is_active='true', updated_at = '{current_date}', price_historic = price_historic || '{insert_new_price}'
                                WHERE id = {id} AND ((SELECT price FROM(
                                                     SELECT (jsonb_array_elements(price_historic)->>'price')::NUMERIC AS price,
                                                        (jsonb_array_elements(price_historic)->>'date')::TIMESTAMP AS reference_time
                                                        FROM product WHERE id = {id}  ORDER BY reference_time DESC LIMIT 1)) != {price})
										AND ((SELECT reference_date FROM(
                                                     		SELECT (jsonb_array_elements(price_historic)->>'date')::DATE AS reference_date,
                                                        (jsonb_array_elements(price_historic)->>'date')::TIMESTAMP AS reference_time
                                                        FROM product WHERE id = {id}  ORDER BY reference_time DESC LIMIT 1)) != '{current_date}'::DATE);

                                UPDATE product
                                SET price = {price}, is_active='true', updated_at = '{current_date}', price_historic = jsonb_set(price_historic::jsonb, '{update_price}', '{price}'::jsonb)
                                WHERE id = {id} AND ((SELECT reference_date FROM(
                                                                    SELECT (jsonb_array_elements(price_historic)->>'price')::NUMERIC AS price,
                                                                    (jsonb_array_elements(price_historic)->>'date')::DATE AS reference_date
                                                                    FROM product WHERE id = {id} ORDER BY reference_date DESC LIMIT 1))::DATE  = '{current_date}'::DATE) ;
                                                        """)
                    insert = db.execute(query)

                    if insert == "No rows were affected by the operation.":
                        verificados += 1
                    else:
                        verificados += 1
                        alterados += 1
                
                else:
                    query_desativa = f"""UPDATE public.product SET is_active='false' WHERE  id={id}; """
                    db.execute(query_desativa)
                    print("Elemento não encontrado.")
            else:
                print(f"Erro na solicitação: {response.status_code}")
        except Exception as e:
            print(f"Erro: {e}")
    fim_loop = time.time()
    tempo_decorrido = fim_loop - inicio_loop
    mensagem =f"Atualização de preços Magazine Luiza {verificados} produtos verificados e {alterados} atualizados!"
    enviar_mensagem_webhook(webhook_url, mensagem)

# Substitua a URL abaixo pela URL que você deseja acessar

async def main():
    print('Iniciando o loop assíncrono')
    await magalu()
    print('Loop assíncrono finalizado')

# Executa o loop assíncrono
asyncio.run(main())