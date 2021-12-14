# -*- coding: utf-8 -*-
import webscraping_bata


def caso_estudio_bata():
    pagina_url="https://www.bata.pe/busca/?fq=H:1221"
    webscraping_bata.scraping_ofertas(pagina_url)
    
    
if __name__ == "__main__":
    # brisasDelMar()
    caso_estudio_bata()
