import pandas as pd

customers = {
    'CustomerId': [1,2,3,4],
    'FirstName': ["Ahmet","Ali","Hasan","Canan"],
    'LastName': ["Yılmaz","Korkmaz","Çelik","Toprak"]
    }
orders = {
    'OrderId': [10,11,12,13],
    'CustomerId': [1,2,5,7],
    'OrderDate': ['2010-07-04','2010-07-05','2010-17-04','2010-27-05']
}
df_customers = pd.DataFrame(customers,columns=['CustomerId','FirstName','LastName'])

df_orders = pd.DataFrame(orders,columns=['OrderId','CustomerId','OrderDate'])
print(df_customers)
print(df_orders)
result = pd.merge(df_customers,df_orders, how='outer')
result = result.dropna(how='any')
print(result)