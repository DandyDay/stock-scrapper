from django.shortcuts import render

import yfinance as yf

stock_list = ['AAPL', 'AMZN', 'FB', 'NFLX', 'NVDA', 'GOOG', '005930.KS']
stock_list_display = ['Apple Inc.', 'Amazon', 'Facebook', 'Netflix',
                      'NVIDIA', 'ALPHABET', 'Samsung Electronics Co., Ltd.']
stock_YTD = []
stock_WER = []        # WeeklyEarningRate
stock_DFH = []        # DeclineFromHighest


def YTD(data):
    today = data[-1]
    firstday = data['2021-01-01']
    diff = round(today-firstday, 2)
    percent = diff/firstday*100
    return (diff, percent)


def WeeklyEarningRate(data):
    today = data[-1]
    firstday = data[-8]
    diff = round(today-firstday, 2)
    percent = diff/firstday*100
    return (diff, percent)


def DeclineFromHighest(data):
    today = data[-1]
    price_max = 0
    for i in data:
        if price_max < i:
            price_max = i
    diff = round(today-price_max, 2)
    percent = diff/price_max*100
    return (diff, percent)


for quote in stock_list:
    tmp = yf.download(quote, start='2020-01-01')
    data = tmp['Close']
    data_High = tmp['High']
    stock_YTD.append(YTD(data))
    stock_DFH.append(DeclineFromHighest(data_High))
    stock_WER.append(WeeklyEarningRate(data))


def index(request):
    context = {'stock_list': stock_list,
               'stock_list_display': stock_list_display,
               'stock_YTD': stock_YTD,
               'stock_DFH': stock_DFH,
               'stock_WER': stock_WER}
    return render(request, 'finance/index.html', context)
