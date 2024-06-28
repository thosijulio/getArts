import requests
from bs4 import BeautifulSoup
from utils.format_str import format_str

# Função para extrair informações de uma pintura através de uma URL, usando BeautifulSoup.
def extract_painting_infos(url: str):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        painting_info = {}

        # Extrair ano
        heading_span = soup.find('h2', class_='SThaNc')
        year_span = heading_span.find('span', class_="QtzOu") if heading_span != None else None


        details_section = soup.find('section', class_='WDSAyb QwmCXd')
        details_paragraph = details_section.find('p') if details_section != None else None

        author_section = soup.find("span", "QIJnJ")
        author_paragraph = author_section.find('a') if author_section != None else None

        painting_info["Details"] = details_paragraph.get_text() if details_paragraph != None else ""
        painting_info["Author"] = author_paragraph.get_text() if author_paragraph != None else author_section.get_text() if author_section != None else ""
        
        if year_span:
            painting_info["Year"] = format_str(year_span.text.strip(), 'year')
        
        li_elements = soup.find_all('li', class_='XD0Pkb')
        
        for li in li_elements:
            key = li.find('span', class_='PUhAff').text.replace(':', '').strip()
            value = li.text.replace(f"{key}:", '').strip()
            painting_info[key] = value
        
        return painting_info