import pandas as pd



#读取股票信息，历史价格等要素
def get_stock_infos():
    df = pd.read_csv('http://quotes.money.163.com/service/chddata.html?code=0000001&start=19901219&end=&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER', encoding='GBK')
    df1 = df.reset_index()[['日期', '收盘价']]
    df1 = df1.sort_index(ascending=False)
    return df1




if __name__ == '__main__':
    get_stock_infos()