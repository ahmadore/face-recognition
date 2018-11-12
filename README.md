#FACE RECOGNITION SOFTWARE

##SETUP
clone the repo with

```git clone https://github.com/ahmadore/face-recognition.git```

#install dependencies with 
    ```pip install -r requirements.txt```

    create an empty folder called 'ds'
###initialize the project with
    ```python encode_caes.py -i ds -e encodings.pickle```
 
###run: 
    ```python web/manage.py makemigrations```
    ```python web/manage.py migrate```
    ```python web/manage.py runserver```

###goto: 
    127.0.0.1:8000/