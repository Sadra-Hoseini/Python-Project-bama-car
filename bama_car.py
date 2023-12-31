import requests
import mysql.connector
from bs4 import BeautifulSoup
import re
from sklearn import tree

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="mydatabase"
)




headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537. 36'}




''' this code written by regex but I found that website uses api so I tried to connect to api
r = requests.get('https://bama.ir/car/hyundai-sonata-4cylautomatic/?pageIndex=1', headers=headers)
# print(r.text.encode('utf-8'))


soup = BeautifulSoup(r.text, 'html.parser')
all_cars = soup.find_all('a', attrs={'class': 'bama-ad'})

for car in all_cars:
    #print( re.sub(r'\s+',' ', car.text.strip()))
    str = re.sub(r'\s+',' ', car.text.strip())
    print(re.sub(r'^.*(هیوندای).*(سوناتا).*(\d{4})\s*(\d+.\d+|کارکرد\s*صفر).*\s(\d+.\d+.\d+.\d+|توافقی).*$','\g<1> \g<2> , \g<3> , \g<4> , \g<5>' , str))
'''
'''
val = all_cars[0]
car = re.split(r'\s+', val.text.strip())
print(car[0])
''' ''' In the following im triying to use api for collecting data'''
i = 0
all_cars = []
all_database_cars = []
url = []
x = []
y = []
test_data = []

for i in range(0,3):
    url.append('https://bama.ir/cad/api/search?vehicle=hyundai%2Csonata%2C4cylautomatic&pageIndex='+str(i))
    r = requests.get(url[i] , headers = headers)
    for car_number_in_page in range(0,len(r.json()['data']['ads'])):
        mycursor = mydb.cursor()
        if(r.json()['data']['ads'][car_number_in_page]['type'] == 'ad'):

            title = r.json()['data']['ads'][car_number_in_page]['detail']['title']
            year = r.json()['data']['ads'][car_number_in_page]['detail']['year']
            mileage = r.json()['data']['ads'][car_number_in_page]['detail']['mileage']
            price = r.json()['data']['ads'][car_number_in_page]['price']['price']

            test_data.append([year,re.sub(r'\s*(\d+).(\d+)\s*.*','\g<1>\g<2>',mileage)])
            if(price == '0' or price == '-1'):
                price = 'توافقی'

            if(price != 'توافقی'):
                x.append([year,re.sub(r'\s*(\d+).(\d+)\s*.*','\g<1>\g<2>',mileage)])
                y.append(price)

            all_cars.append(['%s , %s , %s , %s' % (title,year,mileage,price)])

            sql = "INSERT INTO cars (title,year,mileage,price) VALUES (%s, %s , %s , %s)"
            val = (title,year,mileage,price)
            mycursor.execute("SELECT * FROM cars")
            all_database_cars = mycursor.fetchall()
            result = val in all_database_cars
            if (result == False) :
                mycursor.execute(sql, val)
                mydb.commit()

        else:
            pass


clf = tree.DecisionTreeClassifier()
clf = clf.fit(x,y)
data = [['2028','20000']]
answer = clf.predict(data)
print(answer)

for car in all_cars:
    print(car)


