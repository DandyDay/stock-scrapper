from django.shortcuts import render

import yfinance as yf

from .models import StockCategory

YTD_dict = {}


def YTD(data):
    today = data[-1]
    firstday = data['2021-01-04']
    diff = round(today-firstday, 2)
    percent = round(diff/firstday*100, 1)
    return (diff, percent)


def WeeklyEarningRate(data):
    today = data[-1]
    firstday = data[-8]
    diff = round(today-firstday, 2)
    percent = round(diff/firstday*100, 1)
    return (diff, percent)


def DeclineFromHighest(data):
    today = data[-1]
    price_max = 0
    for i in data:
        if price_max < i:
            price_max = i
    diff = round(today-price_max, 2)
    percent = round(diff/price_max*100, 1)
    return (diff, percent)


for category in StockCategory.objects.all():
    for stock in category.stock_set.all():
        data = yf.download(stock.stock_quote, start='2020-01-01')
        YTD_dict[stock.stock_quote] = YTD(data['Close'])[1]
        stock.WER = WeeklyEarningRate(data['Close'])
        stock.DFH = DeclineFromHighest(data['High'])


def index(request):
    stock_category_list = StockCategory.objects.all()
    context = {'stock_category_list': stock_category_list,
               'YTD_dict': YTD_dict}
    return render(request, 'finance/index.html', context)
