from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import json
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Acessar as variáveis de ambiente
CATEGORY_URL = os.getenv('CATEGORY_URL')
MAX_CONSECUTIVE_ERRORS = os.getenv('MAX_CONSECUTIVE_ERRORS')
DATA_DIR = os.getenv("DATA_DIR")
NEW_LINKS = os.getenv("NEW_LINKS")

# Configuração do driver do Chrome
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL da página que queremos acessar
driver.get(CATEGORY_URL)

# Aguardando a página carregar
time.sleep(5)

# Set p/ guardar os links, para depois transformar em uma lista (garartir valores únicos)
paintingsSet = set([])

try:
    clicked = 0
    consecutiveErrors = 0

    for i in range(2000):
        painting_links = []
        element = driver.find_elements(By.CSS_SELECTOR, 'svg.LKARhb')[1]
        
        try:
            ActionChains(driver).move_to_element(element).click(element).perform()

            if i % 50 == 0:
                print(f"Já clicado {clicked} vezes.")
                new_elements = driver.find_elements(By.CSS_SELECTOR, 'div.vyQv6 > a.e0WtYb')
                paintings = []

                for new_element in new_elements:
                    paintingsSet.add(new_element)
                
                paintings = list(paintingsSet)

                for painting in paintings:
                        href = painting.get_attribute("href")
                        if href:
                            painting_links.append(href)

                

                print(f"{len(painting_links)} pinturas encontradas.")
                # Opcional: Salvar as URLs em um arquivo ou realizar outras operações
                
                with open(os.path.join(DATA_DIR, NEW_LINKS), 'w', encoding='utf-8') as json_file:
                    json.dump({ "finished": [], "unfinished": painting_links}, json_file, ensure_ascii=True, indent=4)
                consecutiveErrors = 0
        except:
            consecutiveErrors = consecutiveErrors + 1
            print("Erro nº: " + consecutiveErrors)
            new_elements = driver.find_elements(By.CSS_SELECTOR, 'div.vyQv6 > a.e0WtYb')
            paintings = []

            for new_element in new_elements:
                paintingsSet.add(new_element)
            
            paintings = list(paintingsSet)

            for painting in paintings:
                    href = painting.get_attribute("href")
                    if href:
                        painting_links.append(href)

            

            print(f"{len(painting_links)} pinturas encontradas.")
            # Opcional: Salvar as URLs em um arquivo ou realizar outras operações
            
            with open(os.path.join(DATA_DIR, NEW_LINKS), 'w', encoding='utf-8') as json_file:
                json.dump({ "finished": [], "unfinished": painting_links}, json_file, ensure_ascii=True, indent=4)

        if (consecutiveErrors == int(MAX_CONSECUTIVE_ERRORS)):
            print(f"{MAX_CONSECUTIVE_ERRORS} erros consecutivos. Encerrando aplicação.")
            break
        
        clicked = clicked + 1
        time.sleep(0.7)  # Pequena pausa entre os cliques para evitar problemas de sincronização 

except Exception as error:
    print(error)

finally:
    # Fechando o navegador
    driver.quit()
