import datetime
query_date = "2023-4-8"
todate = datetime.datetime.today()
q_date = datetime.datetime.strptime(query_date, '%Y-%m-%d')

dif = (q_date-todate).days
print(dif)
if dif<0 or dif>7:
    content = "請輸入一週內日期"
else:
    query_date = q_date.strftime('%Y-%m-%d')
    print(query_date, type(query_date))