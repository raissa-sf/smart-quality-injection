import requests
from io import BytesIO
from PIL import Image

def carregar_imagem_drive(url):
    """
    Converte links compartilháveis do Google Drive em links diretos 
    e retorna um objeto de imagem do PIL.
    """
    try:
        if not url:
            return None
            
        if "drive.google.com" in url:
            if "id=" in url:
                file_id = url.split("id=")[1].split("&")[0]
            elif "/d/" in url:
                file_id = url.split("/d/")[1].split("/")[0]
            else:
                return None
            
            url = f"https://drive.google.com/uc?export=download&id={file_id}"
            
        response = requests.get(url, timeout=10)
        response.raise_for_status() 
        return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"Erro ao carregar imagem: {e}")

        return None
