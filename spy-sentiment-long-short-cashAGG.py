# holding cash in AGG -> 9% CAGR with 11.1% DD
# add shorting + holding cash in AGG -> 9% CAGR with 15% DD

import numpy as np
import datetime
import pandas

def initialize(context):  
    url_optix='https://dl.dropboxusercontent.com/s/x5t2v69xb16wbws/SPY_Sentiment.csv'

    
    fetch_csv(url_optix,date_column = "date", symbol = 'SPY',date_format = "%m/%d/%Y")
    context.security = sid(8554) # SPY ETF
    context.CASH=sid(25485) #AGG ETF
    set_benchmark(sid(8554)) #SPY
    context.symbol_name='SPY'
    context.long_invested = False
    context.short_invested = False
    context.holding_CASH = False
    context.leverage = 1
    context.stop_pct = 0.97
    context.target_stop_pct = 1.1
    
##handle data is where the meat of the code is
def handle_data(context, data): 
    current_price = data[context.security].price
    
    if 'close' in data[context.symbol_name]: 
        
        # set (moving) long and short trailing stop prices.
        stop_price = data[context.security].open_price * context.stop_pct
        target_price = data[context.security].open_price * context.target_stop_pct

        #if the ratio is available put it into floating point precision
        indicator_optix = float(data[context.symbol_name]['close']) 
        threshold_long_optix = 0.75#float(data[context.symbol_name]['pess'])
        threshold_short_optix = 1.25#float(data[context.symbol_name]['opt'])
        threshold_close_optix = threshold_short_optix
        
        record(indicator_optix=indicator_optix, \
               threshold_long_optix=threshold_long_optix, \
               threshold_close_optix=threshold_close_optix)
     
        ######LONG
        if indicator_optix <= threshold_long_optix \
            and context.long_invested == False and context.short_invested == False:
            if context.holding_CASH:
                order_target_value(context.CASH, 0)
                context.holding_CASH = False
                log.info("Sold " + str(context.CASH) + " @ " + \
                          str(data[context.CASH].price))
            order_percent(context.security,  context.leverage)  
            context.long_invested = True  
            log.info("buy " + str(context.security) + " @ " + \
                     str(data[context.security].price) + \
                     " because indicator_optix is " + str(indicator_optix))
            
        elif context.long_invested == True and (indicator_optix >= threshold_close_optix):
            order_target_value(context.security, 0)
            context.long_invested = False  
            log.info("sold " + str(context.security) + " @ " + \
                     str(data[context.security].price) + \
                     " because indicator_optix is " + str(indicator_optix))
            order_percent(context.CASH, context.leverage)
            context.holding_CASH=True
            log.info("Bought " + str(context.CASH) + " @ " + str(data[context.CASH].price))

####SHORT
        if indicator_optix >= threshold_short_optix \
            and context.short_invested == False and context.long_invested == False:
            if context.holding_CASH:
                order_target_value(context.CASH, 0)
                context.holding_CASH = False
                log.info("Sold " + str(context.CASH) + " @ " + \
                          str(data[context.CASH].price))
            order_percent(context.security,  context.leverage)  
            context.short_invested = True  
            log.info("Short " + str(context.security) + " @ " + \
                     str(data[context.security].price) + \
                     " because indicator_optix is " + str(indicator_optix))
            
        elif context.short_invested == True and (indicator_optix <= threshold_long_optix):
            order_target_value(context.security, 0)
            context.short_invested = False  
            log.info("Covered " + str(context.security) + " @ " + \
                     str(data[context.security].price) + \
                     " because indicator_optix is " + str(indicator_optix))
            order_percent(context.CASH, context.leverage)
            context.holding_CASH=True
            log.info("Bought " + str(context.CASH) + " @ " + str(data[context.CASH].price))

# STOPS
        if context.long_invested and current_price <= stop_price:
             order_target_value(context.security, 0)
             context.long_invested = False  
             log.info("sold " + str(context.security) + " @ " + \
                      str(data[context.security].price) + " because stop hit ")
             order_percent(context.CASH, context.leverage)
             context.holding_CASH=True
             log.info("Bought " + str(context.CASH) + " @ " + str(data[context.CASH].price))

            
        if context.long_invested and current_price >= target_price:
             order_target_value(context.security, 0)
             context.long_invested = False  
             log.info("sold " + str(context.security) + " @ " + \
                      str(data[context.security].price) + " because target hit ")    
             order_percent(context.CASH, context.leverage)
             context.holding_CASH=True
             log.info("Bought " + str(context.CASH) + " @ " + str(data[context.CASH].price))
