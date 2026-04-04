import os
import binascii

# Chave gerada para forçar o deslogue global de todas as sessões anteriores
SECRET_KEY = f"LEALDADE_NEW_SECURE_{binascii.hexlify(os.urandom(12)).decode('utf-8')}"
PORT = 5000
