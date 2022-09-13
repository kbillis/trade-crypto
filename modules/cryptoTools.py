# a module with collection of crypto tools. 

import os
import re
import requests


from time import sleep
import datetime


import krakenex
from pykrakenapi import KrakenAPI




def hello_test():
    print("I am cryptoTools, you find me!! :) ")

# TODO
def predict_price_movement():
    return 'Done'

# TODO
def execute_sleep(sleepFor=3):
    sleep(sleepFor)

# TODO: 
def explore_price_move():
    return 'Done'


# TODO: 
def emergency_sale(prev_price, cur_price, emergencyDifference = 0.96): 
    emergency_action = 0
    
    emergencyPriceAction = prev_price*emergencyDifference
    
    if (cur_price>emergencyPriceAction): 
        print(f'Emergency_sale check: All good!!! cp:{cur_price} pp:{prev_price} ep:{emergencyPriceAction}') 
    elif (cur_price<emergencyPriceAction ): 
        print(f'Emergency_sale check: Sale now!!! cp:{cur_price} pp:{prev_price} ep:{emergencyPriceAction} :: 2% drop in sort time!! ')        
        emergency_action = 1 
    else: 
        sys.exit("WARNING::Emergency_sale check: Issue") 
    return emergency_action


# every new action has a higher volume.  volumetowork = working_volume(volumetowork,winning_percentage)
def working_volume(volumetowork,winning_percentage):
    exchangeFee = 0.007
    winning_percentage = winning_percentage*4
    print(f'BEBUG::: VOLUME Winning percentages is {winning_percentage}')
    increasePercentage = winning_percentage - exchangeFee 
    newVolumetowork = volumetowork*increasePercentage + volumetowork
    newVolumetowork = round(newVolumetowork, 5)
    print(f'DEBUG:: previous volume to work was: {volumetowork} , while new volume is: {newVolumetowork} , increasePercentage: {increasePercentage}')
    return newVolumetowork



# TODO : trying not execute an order when price changes are very very small. like 50.11-> 50.12
# may need to rewrite this. 
def working_increased_percentage(trend, percentageCheckFromPrevious, percentageCheckFromAsking, action, tempo="null"): 
    # percDentageIncreasement = rate
    whatToDo = True
    
    print(f'DEBUG::working_increased_percentage::{trend}, {percentageCheckFromPrevious}, {percentageCheckFromAsking}, {action}')
    longPercentage = 0.1
    shortPercentage = 0.08
    
    if (tempo == "long"):
        print('TODO:: add some extra percentages.') 

    # if trend is goin down
    if (trend == "bear"): 
        print("I will wait buy. And fast sell")
        if (action == "sell"):
            print("do bear sell")
            if percentageCheckFromPrevious < shortPercentage: 
                whatToDo = False 
        elif (action == "buy"): 
            print("do bear buy")
            if percentageCheckFromPrevious < longPercentage: 
                whatToDo = False 
    # if trend is goin high
    elif (trend == "bull"):
        # increase the rate according to winning rate
        print("I will fast buy. And wait sell")
        if (action == "sell"):
            print("do bull sell high")
            if percentageCheckFromPrevious < longPercentage: 
                whatToDo = False 
        elif (action == "buy"): 
            print("do bull buy quick")
            if percentageCheckFromPrevious < shortPercentage: 
                whatToDo = False 
    else: 
        # do nothing.
        percentage_increasement = 1
        print("I will keep the same. you didn't provide anything.")
    
    if percentageCheckFromAsking > 0.9: 
        print('looks like you are going to have a good benefit')
        whatToDo = True
        
    # print(f'DEBUG:: price to previous price was: {previousPrice} and now is: {priceToCompare}')
    
    # priceToCompare=previousPrice
    return whatToDo 



# print time
def print_now_time():
    now = datetime.datetime.now()
    print("Current date and time : ")
    print(now.strftime("%Y-%m-%d %H:%M:%S"))


# check kraken order that is successful
def check_kraken_order(kraken, response):
    sleep(2)
    output= "empty"
    check_order = kraken.query_orders_info(response['txid'][0])
    checkFrequency=0
    if check_order['status'][0] == 'open' or check_order['status'][0] == 'closed':
        print('Order sent sucessfully')
        print('Status of the order is: ' + check_order['status'][0])
        while (check_order['status'][0] =='open'):
            checkFrequency += 1
            if checkFrequency < 40: 
                sleep(18)
            elif checkFrequency >= 40: 
                sleep(120) # this is for security. May cancel the order if this number is very very high! 
            print('check status again')            
            print_now_time()
            check_order = kraken.query_orders_info(response['txid'][0])
            print('checking status of the order: ' + check_order['status'][0])
            output=check_order['status'][0]
    else:
        die('Order rejected')
        
    return output


# get price from cryptocompare
def get_crypto_price_cryptocompare(crypto='ETH', currency='EUR', service='Kraken', benchmarking_code=False):
    print('Getting price from cryptocompare')
    print_now_time()
    price_tmp = 0
    if (benchmarking_code): 
        price_tmp = mysqlTools.get_stored_data()
        print(f"I am in benchmarking_code need")
    else:     
        CRYPTOCOMPARE_KEY = os.environ['cryptocompare_key'] 
        headers = {
            'authorization': f'Apikey {CRYPTOCOMPARE_KEY}'
        }
        resp = requests.get(
            'https://min-api.cryptocompare.com/data/price', headers=headers, 
            params={'fsym': crypto, 'tsyms': currency, 'e': service}
        )
        doc = resp.json()
        # print(f"Response was: {doc} and price_tmp: {price_tmp}")
        price_tmp = doc[currency]

    return price_tmp

# get cryptocurrency price from exchange    
def get_crypto_price_exchange(crypto='ETH', currency='EUR', service='Kraken', benchmarking_code=False):
    cryptopair = crypto + currency    #'SOLEUR'   ## ETHEUR SOLEUR
    price_realtime = 0
    pair_price = 0

    if (benchmarking_code): 
        price_realtime = mysqlTools.get_stored_data()
        return price_realtime

    # create api conx
    if service == "Kraken": 
        api = krakenex.API()
        kraken = KrakenAPI(api)
        api_key_location = os.environ['api_kraken_conf'] 
        api.load_key(api_key_location)
        try:
            pair_price = kraken.get_ticker_information(cryptopair)
            # print(pair_price)
        except exception as e:
            print(f'Unable to obtain cryptocurrency data, exception is: {e}')
            
        price_realtime = float(pair_price['b'][0][0])

    print(f'### Getting price from exchange:: {crypto}, {currency}, {service}, {price_realtime}')
    return price_realtime


# nice function copied to keep log of trades
def trade_log(sym, side, price, amount):
    log(f"{side} {amount} {sym} for {price} per")
    if not os.path.isdir("trades"):
        os.mkdir("trades")

    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")


    if not os.path.isfile(f"trades/{today}.csv"):
        with open(f"trades/{today}.csv", "w") as trade_file:
            trade_file.write("sym,side,amount,price\n")

    with open(f"trades/{today}.csv", "a+") as trade_file:
        trade_file.write(f"{sym},{side},{amount},{price}\n")


# execute kraken order
def execute_kraken_order(priceToUse, action, cryptopair, volume_to_action, benchmarking_code=False, absolute_min=0, order_type='limit'):
    # if benchmarking, you will not fix check anything related to kraken order execution system. All will consider fine!
    store_orders = 0
    superCheck= 1  # this is a hardcode value in order not to execute orders. 
    print('You are executing kraken order! ')
    if (benchmarking_code == True or superCheck == 0):
        # store_order_info()
        print(f'####execute_kraken_order in benchmarking_code#### {priceToUse} {action}')
        print(priceToUse, action, cryptopair, volume_to_action, absolute_min)
        return 'DONE',priceToUse
    
    status = 'NONE'
    check_price_on_kraken = 1
    techicaladd = 0
    if re.search("ETH", cryptopair) : 
        techicaladd = 1 
    elif re.search("BTC", cryptopair) : 
        techicaladd = 10 
    elif re.search("SOL", cryptopair) : 
        volume_to_action = round(volume_to_action, 5)

    # create api conx
    api = krakenex.API()
    kraken = KrakenAPI(api)
    KrakenKeyConf = os.environ['api_kraken_conf'] 
    
    api.load_key(KrakenKeyConf)
    
    try:
        pair_price = kraken.get_ticker_information(cryptopair)
        # print(pair_price)
    except exception as e:
        print(f'Unable to obtain cryptocurrency data, exception is: {e}')
    
    price_realtime = float(pair_price['b'][0][0])
    print(f'Current price: {price_realtime}')
    print(f'price to do: {priceToUse}') 
    print(f'action is: {action} ')
    print(f'volume is: {volume_to_action} ') 
    print(f'technical fix: {techicaladd}')
    print(f'absolute_min: {absolute_min}')
       
    # sell it
    if (price_realtime >= priceToUse and action == 'sell'): # 
        print("#execure_order::sell::kraken_price higher than asked.")
        try:
            ETH = float((kraken.get_ticker_information(cryptopair))['a'][0][0]) + techicaladd
            print('I will sell')
            print(ETH)
            response = kraken.add_standard_order(pair=cryptopair, type='sell', ordertype=order_type, 
                                                 volume=volume_to_action, price=ETH, validate=False)
            print(response)
        except exception as e:
            print(f'Error placing order: {e}')
        sleep(1)
        status = check_kraken_order(kraken, response)
    elif (check_price_on_kraken == 1 and action == 'sell'):
        if (price_realtime>=absolute_min): 
            print("execure_order::sell::kraken_price doesn't matter - It is above absolute min! I will sell.")
        else: 
            return status,price_realtime

        # sent order (if requirement on kraken didn't match) and wait... 
        try:
            response = kraken.add_standard_order(pair=cryptopair, type='sell', ordertype=order_type, 
                                                 volume=volume_to_action, price=price_realtime, validate=False)
            print(response)
        except exception as e:
            print(f'Error placing order: {e}')
        sleep(2)
        status = check_kraken_order(kraken, response)
    else:
        print('Requirement to sell not happen')

    # buy it
    if (price_realtime <= priceToUse and action == 'buy'): # 
        print("#execure_order::buy::kraken_price less than what I asked.")        
        try:
            print('You sold and now I will let you buy')
            ETH = float((kraken.get_ticker_information(cryptopair))['a'][0][0]) - techicaladd
            print(ETH)
            response = kraken.add_standard_order(pair=cryptopair, type='buy', ordertype='limit', 
                                                 volume=volume_to_action, price=ETH, validate=False)
            print(response)
        except exception as e:
            print(f'Error placing order: {e}')
        sleep(1)
        status = check_kraken_order(kraken, response)
    elif (check_price_on_kraken == 1 and action == 'buy'):
        if (price_realtime<=absolute_min): 
            print("execure_order::buy::kraken_price doesn't matter - It is above absolute min! I will sell.")
        else: 
            return status,price_realtime        
        # sent order (if requirement on kraken didn't match) and wait... 
        try:
            response = kraken.add_standard_order(pair=cryptopair, type='buy', ordertype='limit', 
                                                 volume=volume_to_action, price=price_realtime, validate=False)
            print(response)
        except exception as e:
            print(f'Error placing order: {e}')
        sleep(1)
        status = check_kraken_order(kraken, response)
    else:
        print('Requirement to buy not happen')

    if (store_orders == 1): 
        print("Store all info...")
        # store_order_info() 
        # trade_log()
    
    return status,price_realtime



# under construction....
def working_rate(diffFromGoal,diffFromGoalPrevious,tempo,check_rate=False,benchmarking_code=False):
    
    if (benchmarking_code): 
        print("working_rate:in benchmarking code, so no sleep time")
        return 0

    if (tempo == 'normal'): 
        print(f'you are in a normal tempo mode')
        internal_sleep_rate = 25
    elif (tempo == 'long'): 
        print(f'you are in a long tempo mode')
        internal_sleep_rate = 150
    elif (tempo == 'fast'): 
        print(f'you are in a fast tempo mode')
        internal_sleep_rate = 8
    elif (tempo == 'instant'): 
        print(f'you are in an instant tempo mode')
        internal_sleep_rate = 3
    else: 
        print(f'you are in an no tempo mode')
        
    internal_sleep_rate_before = internal_sleep_rate 
    internal_sleep_rate_after  = internal_sleep_rate

    if check_rate: 
        if diffFromGoal < diffFromGoalPrevious:
            print('getting closer to goal')
            internal_sleep_rate_after = internal_sleep_rate_before/1.1
        elif diffFromGoal > diffFromGoalPrevious : 
            print('getting away from goal')
            internal_sleep_rate_after = internal_sleep_rate_before/0.9
        else: 
            print('stay the same from the goal')
    
    if internal_sleep_rate_after< 4:
        print("I can't update your rate. It is already too low. ")
        internal_sleep_rate_after =4

    if internal_sleep_rate_after> 150:
        print("I can't update your rate. It is already too high. ")
        internal_sleep_rate_after = 130
    
    print(f'# sleep before: {internal_sleep_rate_before} and after: {internal_sleep_rate_after}')    
    return internal_sleep_rate_after

