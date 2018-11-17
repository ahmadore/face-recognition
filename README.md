#FACE RECOGNITION SOFTWARE

##SETUP
clone the repo with

```git clone https://github.com/ahmadore/face-recognition.git```

#install dependencies with 
    ```pip install -r requirements.txt```

    create an empty folder called 'ds'
###initialize the project with
    ```python encode_faces.py -i ds -e encodings.pickle```
 
###run: 
    ```cd web/```
    ```python manage.py makemigrations```
    ```python manage.py migrate```
    ```python manage.py runserver```

###goto: 
    127.0.0.1:8000/

## Report Endpoint

    ```/api/report/```


    ```method = POST ```


    ```resonse = {'status': 'success/failed'}```

## Search Endpoint
    ```/api/find/```


    ```method = POST```


    ```body= formdata, field = image```


    ```found response = {found: true, data: data_object}```


    ```not found response = {found:false}```


    ```failure response = error message```