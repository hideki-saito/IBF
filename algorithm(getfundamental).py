import pandas as pd  
import numpy as np  
import talib

def initialize(context):  
    # Dictionary of stocks and their respective weights
    context.exchange_months = [1, 4, 7,10]
    context.num_stocks = 20 
    context.stock_weights = {}  
    context.PER = 15
    context.ROA = 0.15
    context.DER = 1
    
    # Rebalance monthly on the first day of the month at market open  
    schedule_function(rebalance,  
                      date_rule=date_rules.month_start(),  
                      time_rule=time_rules.market_open())  
def rebalance(context, data):
    current_time = get_datetime()
    #print context.portfolio.cash
    if current_time.date().month in context.exchange_months:
        for stock in context.stocks:
            if stock in data:
                if stock in context.three_score_stocks:
                    log.info("Price Plus Score of Stock: %s, %d + %d" % (stock, data[stock].price, 3))
                elif stock in context.two_score_stocks:
                    log.info("Price Plus Score of Stock: %s, %d + %d" % (stock, data[stock].price, 2))
                else:
                    log.info("Price Plus Score of Stock: %s, %d + %d" % (stock, data[stock].price, 1))
            
        dropped_stocks = []        
        for stock in context.portfolio.positions:  
            if stock not in context.stocks:
                dropped_stocks.append(stock)
                order_target_percent(stock, 0)
        log.info("Dropped Stocks %s" % (dropped_stocks))
       
     #  Create weights for each stock  
        weight = create_weights(context, context.stocks)

    # Rebalance all stocks to target weights  
        for stock in context.stocks:
            if stock in data:
                order_target_percent(stock, weight)
    else:
        pass

    # # track how many positions we're holding  
    #ecord(num_positions = len(context.fundamental_df))

def before_trading_start(context): 
    
    fundamental_df_three_score = get_fundamentals(  
        query(  
            
        )  
        .filter(fundamentals.valuation_ratios.pe_ratio < context.PER)
        .filter(fundamentals.operation_ratios.roa > context.ROA)        
        .filter(fundamentals.operation_ratios.total_debt_equity_ratio < context.DER)  
        .order_by()  
        .limit(context.num_stocks)  
    )
    context.three_score_stocks = []
    for stock in fundamental_df_three_score:
        context.three_score_stocks.append(stock)
        
    context.two_score_stocks = []
    fundamental_df_two_score = get_fundamentals(  
        query(  
            
        )  
        .filter(fundamentals.valuation_ratios.pe_ratio < context.PER)
        .filter(fundamentals.operation_ratios.roa > context.ROA)        
 #       .filter(fundamentals.operation_ratios.total_debt_equity_ratio < context.DER)  
        .order_by()  
        .limit(context.num_stocks)  
    )
    for stock in fundamental_df_two_score:
        context.two_score_stocks.append(stock)
    
    fundamental_df_two_score = get_fundamentals(  
        query(  
            
        )  
        .filter(fundamentals.valuation_ratios.pe_ratio < context.PER)
  #      .filter(fundamentals.operation_ratios.roa > context.ROA)        
        .filter(fundamentals.operation_ratios.total_debt_equity_ratio < context.DER)  
        .order_by()  
        .limit(context.num_stocks)  
    )
    for stock in fundamental_df_two_score:
        context.two_score_stocks.append(stock)
    
    fundamental_df_two_score = get_fundamentals(  
        query(  
            
        )  
   #     .filter(fundamentals.valuation_ratios.pe_ratio < context.PER)
        .filter(fundamentals.operation_ratios.roa > context.ROA)        
        .filter(fundamentals.operation_ratios.total_debt_equity_ratio < context.DER)  
        .order_by()  
        .limit(context.num_stocks)  
    )
    for stock in fundamental_df_two_score:
        context.two_score_stocks.append(stock)
        
    context.two_score_stocks = list(set(context.two_score_stocks))
    context.two_score_stocks = filter(lambda x: x not in context.three_score_stocks, context.two_score_stocks)
    
    if len(context.three_score_stocks) + len(context.two_score_stocks) >= 20:
        context.stocks = (context.three_score_stocks + context.two_score_stocks)[0:context.num_stocks]
    else:
        context.stocks = context.three_score_stocks + context.two_score_stocks
        fundamental_df_one_score = get_fundamentals(  
        query(  
            
        )  
        .filter(fundamentals.valuation_ratios.pe_ratio < context.PER)
        # .filter(fundamentals.operation_ratios.roa > context.ROA)        
        # .filter(fundamentals.operation_ratios.total_debt_equity_ratio < context.DER)  
        .order_by()  
        .limit(context.num_stocks)  
    )
        for stock in fundamental_df_one_score:
            if stock not in context.stocks: 
                context.stocks.append(stock)
                if len(context.stocks) == 20:
                    break
            else:
                continue
        
        fundamental_df_one_score = get_fundamentals(  
        query(  
            
        )  
        # .filter(fundamentals.valuation_ratios.pe_ratio < context.PER)
        .filter(fundamentals.operation_ratios.roa > context.ROA)        
        # .filter(fundamentals.operation_ratios.total_debt_equity_ratio < context.DER)  
        .order_by()  
        .limit(context.num_stocks)  
    )
        for stock in fundamental_df_one_score:
            if stock not in context.stocks: 
                context.stocks.append(stock)
                if len(context.stocks) == 20:
                    break
            else:
                continue
        
        fundamental_df_one_score = get_fundamentals(  
        query(  
            
        )  
        # .filter(fundamentals.valuation_ratios.pe_ratio < context.PER)
        # .filter(fundamentals.operation_ratios.roa > context.ROA)        
        .filter(fundamentals.operation_ratios.total_debt_equity_ratio < context.DER)  
        .order_by()  
        .limit(context.num_stocks)  
    )
        for stock in fundamental_df_one_score:
            if stock not in context.stocks: 
                context.stocks.append(stock)
                if len(context.stocks) == 20:
                    break
            else:
                continue
                
    #print len(context.stocks)

    update_universe(context.stocks)  

def create_weights(context, stocks):  
    """  
        Takes in a list of securities and weights them all equally  
    """  
    if len(stocks) == 0:  
        return 0  
    else:  
        weight = 1.0/len(stocks)  
        return weight  
def handle_data(context, data):  
    """  
      Code logic to run during the trading day.  
      handle_data() gets called every bar.  
    """  
    pass