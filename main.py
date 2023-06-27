import requests

import json

import csv

import os.path

from funcs import flatten_dict, write_to_file


OFFSET = 0  # символ, с которого надо начать
LIMIT = 500  # увеличение пагинации

tickers = []  # массив с тикерами

for exchange in exchanges:
    worked = 0  # счетчик для обработанных тикеров
    while True:
        exchange_r = requests.get(url=exchange_url+exchange+url_param+API_TOKEN+"&fmt=json", params={"offset": OFFSET,
                                                                                                   "limit": LIMIT})
        if exchange_r.status_code == 200:
            exchange_data = json.loads(exchange_r.text)
            if not exchange_data:  # если данные закончились
                break

            for index in exchange_data.keys():

                # крафт тикера
                ticker = f'{exchange_data[index]["General"]["Code"]}.{exchange_data[index]["General"]["CountryISO"]}'

                if exchange_data[index]["General"]["CountryISO"] == "RU":
                    ticker = f'{exchange_data[index]["General"]["Code"]}.{exchange_data[index]["General"]["Exchange"]}'

                tickers.append(ticker)
                worked += 1

            OFFSET += LIMIT  # пагинация, следующая страница
        else:
            print("Error:", exchange_r.status_code)
    OFFSET = 0  # сбросить пагинацию для новой биржи
    print(f"{exchange}: {worked}")

errors = 0  # счетчик для непредвиденных ошибок

for ticker in tickers:
    try:
        company_r = requests.get(url=company_url + ticker + url_param + API_TOKEN + "&fmt=json")
        company_data = json.loads(company_r.text)

        # нужные для выборки ключи
        needed_keys = [
            "Code", "Name", "Exchange", "CurrencyCode", "CountryName", "Sector", "Industry",
            "WebURL", "LogoURL", "FullTimeEmployees", "MarketCapitalization",
            "EBITDA", "PERatio", "PEGRatio", "WallStreetTargetPrice", "BookValue", "DividendYield",
            "EarningsShare", "EPSEstimateCurrentYear", "EPSEstimateNextYear", "EPSEstimateNextQuarter",
            "EPSEstimateCurrentQuarter", "ProfitMargin", "OperatingMarginTTM", "ReturnOnAssetsTTM",
            "ReturnOnEquityTTM", "RevenueTTM", "QuarterlyRevenueGrowthYOY", "GrossProfitTTM",
            "DilutedEpsTTM", "QuarterlyEarningsGrowthYOY", "date", "period", "growth",
            "earningsEstimateAvg", "earningsEstimateGrowth", "revenueEstimateAvg",
            "revenueEstimateGrowth", "epsTrendCurrent", "TrailingPE", "ForwardPE",
            "PriceSalesTTM", "PriceBookMRQ", "EnterpriseValue", "EnterpriseValueRevenue",
            "EnterpriseValueEbitda", "SharesOutstanding", "SharesFloat", "PercentInsiders",
            "PercentInstitutions", "Beta", "52WeekHigh", "52WeekLow", "50DayMA", "200DayMA",
            "ForwardAnnualDividendRate", "ForwardAnnualDividendYield", "PayoutRatio",
            "Rating", "TargetPrice", "StrongBuy", "Buy", "Hold", "Sell", "StrongSell",
            "totalAssets", "totalLiab", "totalStockholderEquity", "commonStock",
            "netDebt", "longTermDebt", "freeCashFlow", "ebit"
        ]

        values = [0] * len(needed_keys)  # значения

        data = {}
        try:
            data = flatten_dict(company_data)  # раскрыть словарь
        except:
            print(f"Ошибка в {company_url + ticker + url_param + API_TOKEN + '&fmt=json'}")
            continue

        for i in range(len(needed_keys)):  # найти значение каждого ключа
            try:
                value = data[needed_keys[i]]
                if value == '' or value is None:
                    value = 'null'
                values[i] = value
            except:  # ключа нет -> ошибка -> подставка null
                values[i] = "null"

        values[1] = data['Name']  # чтобы не перезаписалось другое значение

        if os.path.isfile('fin.csv'):  # если файл уже существует
            with open('fin.csv', 'a', newline='', encoding="utf-8") as file:
                writer = csv.writer(file)

                if write_to_file("fin.csv", values):
                    writer.writerow(values)

        else:
            with open('fin.csv', 'w', newline='', encoding="utf-8") as file:
                writer = csv.writer(file)

                writer.writerow(needed_keys)
                writer.writerow(values)

    except Exception as e:
        errors += 1
        print(f"В тикере {ticker} ошибка {str(e)}")

print(f"Ошибок: {errors}")
