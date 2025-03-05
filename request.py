import requests
def getproducts(x):
    for i in range(x):
        endpoint = f"http://localhost:8000/test/product/{i}"  # الرابط الصحيح

        get_response = requests.get(endpoint)
        print(get_response.status_code)  # كود الحالة
        #print(get_response.text)         # نص الاستجابة

        try:
            print(get_response.json())  # محاولة طباعة JSON
        except requests.exceptions.JSONDecodeError:
            print("Response is not JSON")
def post_products(title=None,content=None,price=0):
     endpoint = "http://localhost:8000/test/product/"
     data={ 
         "title": title
         ,"content": content,
         "price": price
     }
     postresponse=requests.post(endpoint,json=data)
     try:
            print(postresponse.json())  
     except requests.exceptions.JSONDecodeError:
            print("Response is not JSON")
# post_products('hello',"lofhen",1235)
getproducts(6)