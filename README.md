# trade-crypto
trade-crypto is about simple trading of crypto currencies via kraken.  

# disclaimer 
I am not a trader and this is not a financial tool or advice. This is purely for fun.

# Need: 
- install with pip very few python libraries. 
- create an account in cryptocompare and make this cryptocompare_key available to the script. Script will get this variable from your (bash) env. 
- create an account in kraken and make the file with keys available to the script. Script will get this file name from your (bash) env.

how to run the script: 
python3 crypto_get_price_do_transactions.py -v -p 34.9  -c SOL  -y EUR  -a buy  -l 2.5   -w 0.01 -t normal -tr bear -r

