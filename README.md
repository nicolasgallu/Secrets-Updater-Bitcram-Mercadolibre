
STEPS:

1-Create secrets managers for each updater. (and set the .env)
2-Only for MercadoLibre, you need to create the CODE when running the job for the first time:
https://auth.mercadolibre.com.ar/authorization?response_type=code&client_id=xxx&redirect_uri=xxx


CONSIDERATIONS:
Mercadolibre Tokens last just for 6 hours.
Bitcram Tokens last for 1 week.