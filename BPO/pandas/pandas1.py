import pandas as pd
# df = pd.read_excel(r"C:\Users\Administrator\Desktop\新建 Microsoft Excel 工作表.xlsx",sheet_name='Sheet2',index_col=None)
# print(df.dtypes)
# df.head()
Salaries = pd.read_csv('Salaries.csv')
x = pd.DataFrame(Salaries)
print(x.describe())
