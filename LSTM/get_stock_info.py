import pandas as pd
import xlrd


#读取股票信息，历史价格等要素
def get_stock_infos():
    # df = pd.read_csv('http://quotes.money.163.com/service/chddata.html?code=0000001&start=19901220&end=&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER', encoding='GBK', na_values=["None"])
    df = pd.read_excel('C:\\Users\\crazy18\\Desktop\\000001.xls')


    df1 = df.reset_index()[['交易时间', '收盘价', '涨跌']]


    df1['涨跌'] = df1['涨跌'].astype('float')
    return df1




if __name__ == '__main__':
    get_stock_infos()