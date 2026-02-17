from mercadolibre_secrets import updating_meli_secrets
from bitcram_secrets import updating_bitcram_secrets
from settings import RUN_BITCRAM

updating_meli_secrets()
if RUN_BITCRAM == 1:
    updating_bitcram_secrets()