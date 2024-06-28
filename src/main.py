import json
import os
import sys
from dotenv import load_dotenv
from utils.download_painting import download_painting
from utils.extract_painting_infos import extract_painting_infos
from utils.format_str import format_str

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Acessar as variáveis de ambiente
MAX_CONSECUTIVE_ERRORS = os.getenv('MAX_CONSECUTIVE_ERRORS')
DATA_DIR = os.getenv("DATA_DIR")
LINKS = os.getenv("LINKS")
ERRORS_LINKS = os.getenv("ERRORS_LINKS")
PAINTINGS_PATH = os.getenv("PAINTINGS_PATH")

# Carregar o JSON com as URLs
with open(os.path.join(DATA_DIR, LINKS), 'r', encoding='utf-8') as f:
    urlsData = json.load(f)

# Carregar o JSON com as URLs de erro
with open(os.path.join(DATA_DIR, ERRORS_LINKS), 'r', encoding='utf-8') as f:
    errorsData = json.load(f)

# Diretório onde serão salvos os arquivos JSON
output_dir = PAINTINGS_PATH
os.makedirs(output_dir, exist_ok=True)


unfinisheds_urls_to_iterate = urlsData["unfinished"][:]
errors_count = 0

# Iterar sobre as URLs no campo "unfinished"
for url in unfinisheds_urls_to_iterate:
    # Extrair informações da pintura
    painting_info = None
    try:
        painting_info = extract_painting_infos(url)
    except Exception as e:
        print(f"Erro ao acessar {url}: {e}")
        errors_count = errors_count + 1
        if (errors_count == int(MAX_CONSECUTIVE_ERRORS)):
            print(f"{MAX_CONSECUTIVE_ERRORS} erros consecutivos. Finalizando aplicação.")
            break
        pass
    
    if painting_info:
        title = "Unknown"
        year="Unknown"
        author="Unknown"
        
        # Try p/ erros de formatacao do nome do arquivo
        try:
            title = format_str(painting_info['Title'], 'title')
            year = format_str(painting_info['Year'] if "Year" in painting_info else painting_info["Date Created"] if "Date Created" in painting_info else "Unknown", 'year')
            author = format_str(painting_info['Author'] if "Author" in painting_info else painting_info["Creator"] if "Creator" in painting_info else painting_info["Painter"] if "Painter" in painting_info else painting_info["Artist"] if "Artist" in painting_info else painting_info["By"] if "By" in painting_info else "Unknown", 'author')
        except:
            urlsData['unfinished'].remove(url)
            errorsData.append(url)

            # Atualizar o JSON com as URLs movidas
            with open(os.path.join(DATA_DIR, LINKS), 'w', encoding='utf-8') as f:
                json.dump(urlsData, f, ensure_ascii=False, indent=4)
            with open(DATA_DIR + ERRORS_LINKS, 'w', encoding='utf-8') as f:
                json.dump(errorsData, f, ensure_ascii=False, indent=4)

            print("Erro ao formatar nome do arquivo: " + str(error))
            print("URL: " + url)
            errors_count = errors_count + 1
            if (errors_count == int(MAX_CONSECUTIVE_ERRORS)):
                print(f"{MAX_CONSECUTIVE_ERRORS} erros consecutivos. Finalizando aplicação.")
                break
            pass

        
        # Formatar o nome do arquivo JSON
        filename = f"({year}) {author} - {title}.json"
        
        print(filename)
        # Salvar as informações em um arquivo JSON
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as json_file:
            json.dump(painting_info, json_file, ensure_ascii=False, indent=4)

        # Try p/ pegar erro ao salvar ou baixar imagem
        try:
            download_painting(url, output_dir, f"({year}) {author} - {title}")

            # Mover a URL para a lista "finished"
            urlsData['finished'].append(url)
            urlsData['unfinished'].remove(url)
            # Atualizar o JSON com as URLs movidas
            with open(os.path.join(DATA_DIR, LINKS), 'w', encoding='utf-8') as f:
                json.dump(urlsData, f, ensure_ascii=False, indent=4)

            print("\nJSON atualizado e imagem baixada, com URL movida para 'finished'.")
            errors_count = 0
        
        except Exception as error:
            urlsData['unfinished'].remove(url)
            errorsData.append(url)

            # Atualizar o JSON com as URLs movidas
            with open(os.path.join(DATA_DIR, LINKS), 'w', encoding='utf-8') as f:
                json.dump(urlsData, f, ensure_ascii=False, indent=4)
            with open(os.path.join(DATA_DIR, ERRORS_LINKS), 'w', encoding='utf-8') as f:
                json.dump(errorsData, f, ensure_ascii=False, indent=4)

            print("Erro ao baixar e salvar arquivos e foto: " + str(error))

            errors_count = errors_count + 1
            if (errors_count == int(MAX_CONSECUTIVE_ERRORS)):
                print(f"{MAX_CONSECUTIVE_ERRORS} erros consecutivos. Finalizando aplicação.")
                break
            pass
    else:
        print(f"Falha ao acessar url p/ criar json de infos da imagem: {url}")
        errors_count = errors_count + 1
        if (errors_count == int(MAX_CONSECUTIVE_ERRORS)):
            print(f"{MAX_CONSECUTIVE_ERRORS} erros consecutivos. Finalizando aplicação.")
            break
        pass
            