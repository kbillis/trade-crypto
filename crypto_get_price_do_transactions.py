#!/usr/bin/python

# TODO: getting data and running in test mode. 



# libraries

import os
import requests
from time import sleep
import argparse
import sys

# particulary: 
import datetime
import numpy as np


# import modules from other dir
sys.path.append('./modules/')
import cryptoTools
# import mysqlTools

# cryptoTools.hello_test()


###################
#### FUNCTIONS ####
###################


# print time
def print_now_time():
    now = datetime.datetime.now()
    print("Current date and time : ")
    print(now.strftime("%Y-%m-%d %H:%M:%S"))




##############
#### MAIN ####
##############

def main():
    """
    main function
    """
    # get arguments from command line:
    parser = argparse.ArgumentParser(description="Parses command.")
    parser.add_argument("-v", "--verbose",dest='verbose',action='store_true', help="Verbose mode.")
    parser.add_argument("-p", "--priceToUse",type=float, help="Price to start.")
    parser.add_argument("-c", "--cryptocurrency", help="What crypto dude?")
    parser.add_argument("-y", "--currency", help="What currency dude?")
    parser.add_argument("-a", "--action", help="What I have to do?")
    parser.add_argument("-t", "--tempo", help="What is your tempo do?")
    parser.add_argument("-l", "--volume",type=float, help="Volume? ")
    parser.add_argument("-r", "--checkRate", dest='checkRate',action='store_true', help="how often to check? ")
    parser.add_argument("-w", "--winningPercentage",type=float, help="how much to win? ")
    parser.add_argument("-b", "--benchmarking_code",dest='benchmarking_code',action='store_true', help="benchmarking_code mode.")    
    parser.add_argument("-s", "--service", help="What service to use (Kraken?)?")
    parser.add_argument("-k", "--checker", action="store_true", help="checker real? ")
    parser.add_argument("-j", "--checkPriceAdj", action="store_true", help="checker price dif to previous? ")
    parser.add_argument("-tr", "--trend", help="What is the trend (bear/bull/NA)?")
    parser.add_argument("-tl", "--transactionsLimit",type=float, help="What is your transactionsLimit? ")
    parser.add_argument("-st", "--strategy", help="What is your tempo do?")
    options = parser.parse_args()    
    
    verbose = options.verbose
    benchmarking_code = options.benchmarking_code # False
    service = options.service
    checker = options.checker 
    checkPriceAdj = options.checkPriceAdj
    transactionsLimit = options.transactionsLimit
    check_rate = options.checkRate

    if verbose:
        print("Verbose mode on")
    else:
        print("Verbose mode off")
     
    if benchmarking_code: 
        print("Benchmarking code")
    else: 
        print("Normal run")
    
    if service: 
        print(f'I will be using {service}')
    else: 
        service = 'Kraken'

    if checker: 
        print(f'I will be using {service} and real price')
        checker = 'real'
    else: 
        checker = 'cryptoPrice'

    if checkPriceAdj : 
        checkPriceAdj = 1 
    else: 
        checkPriceAdj = 0

    if transactionsLimit: 
        transactionsLimit = transactionsLimit  
    else: 
        transactions_limit=80
    

    # variables to provide:    
    priceToUse = options.priceToUse 
    cryptocurrency =  options.cryptocurrency # SOL ETH DOT SOL
    currency = options.currency
    action = options.action
    volumetowork = options.volume
    winning_percentage = options.winningPercentage
    tempo = options.tempo
    trend = options.trend
    
    pairwork = cryptocurrency + currency    #'SOLEUR'   ## ETHEUR SOLEUR
    diffFromGoal = 10000000000000
    
    # variables to edit:
    updateWorkingVolume = True # I Will update the volume in every transaction. 
    work_extremes = False # TODO
    price_of_last_action = '000'
    extreme_low = priceToUse - priceToUse*0.05
    extreme_high = priceToUse + priceToUse*0.05
    how_many_times_to_buy_sell_extremes = 0
    limit_extremes = 1
    count_wait_period = 0
    list_of_prices = []
    list_of_buys_TODO = np.empty((0, 4))   # price volume date empty
    list_of_sells_TODO = np.empty((0, 4))  # price volume date empty
    price_kraken = 0
    final_sleep = 2 
    greenFlag=0 # IF set to 1, it will not double check.
    
    ## correction need to be here. 
    number_of_transactions=0
    transactions_limit=80
    
    while number_of_transactions < transactions_limit :
        print('\n')
        print('### START NEW transaction ###')
        print_now_time() 
        
        if (checker == 'real' and benchmarking_code == False) : 
            price = cryptoTools.get_crypto_price_exchange(cryptocurrency,currency, service, benchmarking_code)
        else:     
            price = cryptoTools.get_crypto_price_cryptocompare(cryptocurrency,currency,service,benchmarking_code)

        diffFromGoal_previous = diffFromGoal
        diffFromGoal = abs(price-priceToUse)
        diffFromGoalPercent = (diffFromGoal /priceToUse)*100

        print(f'transaction count: {number_of_transactions} ' )
        print(f'volume of {cryptocurrency} crypto to work is: {volumetowork} ' )
        print(f'price of last action: {price_of_last_action}')
        print(f'price in cryptocompare is: {price} , while priceToUse is {priceToUse} and action is {action}' )
        print(f'price low extreme is: {extreme_low} and high extreme is: {extreme_high} ')
        print(f'min difference in price is {diffFromGoal} and as a percentage is: {diffFromGoalPercent}, while it was: {diffFromGoal_previous}')
    
        
        # if many prices collected, I will do some checks if prices goes up or down. 
        list_of_prices.append(price) 
        if len(list_of_prices) > 4 and len(list_of_prices) < 21: 
            av_price=np.average(list_of_prices)
            print(f'min aver in price is: {av_price} ')
        elif len(list_of_prices) > 20: 
            print(f'I can do some magic, there are few values.')
            
            
            
        # list_of_buys_TODO
        # list_of_sells_TODO
        if (list_of_buys_TODO.size == 0): 
            print("list_of_buys_TODO is empty")
        else: 
            print("list_of_buys_TODO:")
            list_of_buys_TODO[list_of_buys_TODO[:, 1].argsort()]
            for values in list_of_buys_TODO: 
                print(values)

        if (list_of_sells_TODO.size == 0): 
            print("list_of_sells_TODO is empty")
        else: 
            print("list_of_sells_TODO:")
            list_of_sells_TODO[list_of_sells_TODO[:, 1].argsort()]            
            for values in list_of_sells_TODO: 
                print(values)
            
        
        # 
        if (benchmarking_code): 
            print('I am in benchmarking code')
            final_sleep = 0
        else: 
            final_sleep = cryptoTools.working_rate(diffFromGoal,diffFromGoal_previous,tempo,check_rate,benchmarking_code=False)
            print('DEBUGG::diffFromGoal_previous::' , diffFromGoal_previous)
        
        print(f'I will sleep for {final_sleep} sec') 
        # breakpoint()

 
        if (price <= priceToUse and action == 'buy'): 
            # second check of buy. Is the price going down or up? if down, wait and check again
            sleep(1)
            times_the_same=0
            while greenFlag == 0: 
                print('check price again. if is dropping, wait...')
                sleep(final_sleep)
                price_prev = price                
                if (checker == 'real' and benchmarking_code == False) : 
                    price = cryptoTools.get_crypto_price_exchange(cryptocurrency,currency, service, benchmarking_code)
                else:     
                    price = cryptoTools.get_crypto_price_cryptocompare(cryptocurrency,currency,service,benchmarking_code)
                    
                priceDiffPrevious = (abs(price_prev-price)/price_prev)*100
                priceDiffAsking   = (abs(priceToUse-price)/price_prev)*100
                priceDiffCheck = cryptoTools.working_increased_percentage(trend, priceDiffPrevious, priceDiffAsking, action)
                print(f'compare prices:: pp: {price_prev}  cp: {price}  priceToUse: {priceToUse} '
                  f'priceDiffPrevious: {priceDiffPrevious}  priceDiffAsking: {priceDiffAsking}  % \n'
                  f'Is difference ok: {priceDiffCheck}'  )

                if price < price_prev: 
                    greenFlag = 0
                    sleep(final_sleep)
                    print('dropping... wait... ')                    
                elif price > price_prev: 
                    print('last check and go')
                    if (checkPriceAdj ): 
                        # TODO another check... 
                        if (priceDiffCheck):  
                            greenFlag = 1
                            print('Did pass adj price - so there is a significant higher level. ')
                        else : 
                            print('Did not pass adj price - so there is NOT a significant higher level.') 
                            greenFlag = 0
                    else: 
                        greenFlag = 1

                elif price == price_prev:
                    print('price the same.. wait... ')
                    times_the_same=times_the_same+1
                    sleep(final_sleep) 
                    if times_the_same>3:
                        print('price stayed the same for long... ')
                        greenFlag = 1 

            print('# will try to execute the order...if price is still ok')
            print(f'last compare prices:: pp: {price_prev}  cp: {price}  priceToUse: {priceToUse}' )          
            if (price <= priceToUse) : 
                status,price_kraken = cryptoTools.execute_kraken_order(price_prev, action, pairwork, volumetowork, benchmarking_code, priceToUse)
            else: 
                status = 'NONE'
                
            
            print(f'current_status: {status} ' )
            if status == 'NONE' or status == 'canceled'  : 
                # do nothing
                print('do nothing the order did not make it.')
            else: 
                price = priceToUse # because previous price is the one from kraken
                price_of_last_action = price_kraken # because previous price is the one from kraken
                action = 'sell'
                priceToUse = price_of_last_action + price_of_last_action*winning_percentage
                diffFromGoal = 10000000000000
                count_wait_period = 0 
                number_of_transactions = number_of_transactions + 1
                now = datetime.datetime.now()
                list_of_sells_TODO = np.append(list_of_sells_TODO , np.array([[priceToUse, volumetowork, now, price_of_last_action]]), axis=0)                

        elif (price >= priceToUse and action == 'sell'):
            # second check of buy. Is the price going down or up? If up, wait and check again. 
            sleep(1)
            times_the_same=0
            while greenFlag == 0: 
                print('check price again. if is going high, wait...')
                sleep(final_sleep)
                price_prev = price                
                
                if (checker == 'real' and benchmarking_code == False) : 
                    price = cryptoTools.get_crypto_price_exchange(cryptocurrency,currency, service, benchmarking_code)
                else:
                    price = cryptoTools.get_crypto_price_cryptocompare(cryptocurrency,currency,service,benchmarking_code)

                priceDiffPrevious = (abs(price_prev-price)/price_prev)*100
                priceDiffAsking   = (abs(priceToUse-price)/price_prev)*100
                priceDiffCheck = cryptoTools.working_increased_percentage(trend, priceDiffPrevious, priceDiffAsking, action)
                print(f'compare prices:: pp: {price_prev}  cp: {price}  priceToUse: {priceToUse} '
                  f'priceDiffPrevious: {priceDiffPrevious}  priceDiffAsking: {priceDiffAsking}  % \n' 
                  f'Is difference ok: {priceDiffCheck}'  )

                if price > price_prev: 
                    # wait
                    sleep(final_sleep)
                    greenFlag = 0
                    print('going up... wait... ')                    
                elif price < price_prev:
                    print('go')
                    if (checkPriceAdj ): 
                        # TODO another check... 
                        if (priceDiffCheck ):  
                            greenFlag = 1
                            print('Did pass adj price - so there is a significant higher level. ')
                        else : 
                            print('Did not pass adj price - so there is NOT a significant higher level.') 
                            greenFlag = 0 
                    else: 
                        greenFlag = 1
                elif price == price_prev:
                    print('price the same.. wait... ')
                    times_the_same=times_the_same+1
                    sleep(final_sleep) 
                    if times_the_same>3:
                        print('price stayed the same for long... ')
                        greenFlag = 1 
            
            print('will try to execute the order...')
            print(f'last compare prices:: pp: {price_prev}  cp: {price}  priceToUse: {priceToUse}' )
            if (price >= priceToUse) : 
                status,price_kraken = cryptoTools.execute_kraken_order(price_prev, action, pairwork, volumetowork, benchmarking_code, priceToUse)
            else: 
                status = 'NONE'
            print(f'current_status: {status} ' )

            if status == 'NONE' or status == 'canceled'  : 
                # do nothing
                print('do nothing the order did not make it.')
            else: 
                price = priceToUse # because previous price is the one from kraken
                price_of_last_action = price_kraken # because previous price is the one from kraken
                action = 'buy'
                if updateWorkingVolume: 
                    volumetowork = cryptoTools.working_volume(volumetowork,winning_percentage)                
                priceToUse = price_of_last_action - price_of_last_action*winning_percentage
                diffFromGoal = 10000000000000
                count_wait_period = 0 
                number_of_transactions = number_of_transactions + 1
                now = datetime.datetime.now()
                list_of_buys_TODO = np.append(list_of_buys_TODO , np.array([[priceToUse, volumetowork, now, price_of_last_action]]), axis=0)


        elif price <= extreme_low and limit_extremes < how_many_times_to_buy_sell_extremes and work_extremes:
            volumetowork = 4
            print(f'buy the dip - extreme low {extreme_low}')
            how_many_times_to_buy_sell_extremes= how_many_times_to_buy_sell_extremes+1
            status,price = cryptoTools.execute_kraken_order(price, 'buy', pairwork, volumetowork, benchmarking_code)
            priceToUse = price + price*winning_percentage
            if status == 'NONE' : 
                # do nothing
                print('do nothing the order did make it.')                
            else: 
                action = 'sell'
                diffFromGoal = 10000000000000
                count_wait_period = 0 
            
        elif price >= extreme_high and limit_extremes < how_many_times_to_buy_sell_extremes and work_extremes:
            print(f'sell the rise - extreme high {extreme_high}')
            how_many_times_to_buy_sell_extremes= how_many_times_to_buy_sell_extremes+1
            status,price = cryptoTools.execute_kraken_order(price, 'sell', pairwork, volumetowork, benchmarking_code)
            priceToUse = price - price*winning_percentage 
            if status == 'NONE' : 
                # do nothing
                print('do nothing the order did not make it.')
            else: 
                action = 'buy' 
                diffFromGoal = 10000000000000 
                count_wait_period = 0 

        # waiting for too much, we may need :
        # there is a problem here, if we buy high and sell lower than the threeshold... 
        changeLimits = 0 # 0 or 1
        count_wait_period = count_wait_period + 1
        if count_wait_period > 55 and changeLimits == 1: 
            if (action == 'sell'): 
                priceToUse = priceToUse - diffFromGoal/2 
            elif (action == 'buy'): 
                priceToUse = priceToUse + diffFromGoal/2 
            
            count_wait_period = 0 
        
        
        print('loop finish, I will sleep.')
        sleep(final_sleep) 





if __name__ == "__main__":
    main()





