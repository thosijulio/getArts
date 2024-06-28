import subprocess
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Acessar as variáveis de ambiente
DEZOOMIFY_PATH = os.getenv('DEZOOMIFY_PATH')

# Função para baixar uma pintura usando o Dezoomify-rs
def download_painting(url: str, output_dir: str, filename: str):
    print(DEZOOMIFY_PATH, output_dir)
    # Comando para executar o Dezoomify-rs
    command = [DEZOOMIFY_PATH, url, "-l", f"{output_dir}/{filename}.png"]
    subprocess.run(command, check=True)
