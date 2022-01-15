# World Romance Translation API

API dari website komik [World Romance Translation](https://wrt.my.id/) dengan menggunakan Flask dan metode Scraping

## Example 

Base URL = https://wrt-api.herokuapp.com/

## Instalasi

* Clone this Repo
* Buat environment
```bash
python -m venv venv
```
* Aktifkan environment
```bash
venv\Scripts\activate.bat
```
* Install Flask
```bash
pip install Flask
```
* Install semua library yang diperlukan
```bash
pip install -r requirements.txt
```


## Cara Penggunaan

* (For Windows) set flask_app
```bash
set FLASK_APP=app.py
```
* Start server:
```bash
flask run
```

Url [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Endpoint

| Url        | Params           | Type | Description |
| ------------- |:-------------:| :-----:| :----------:|
| /      | - | - | Cek Status koneksi ke server |
| /home  | - | - | Get komik list homepage |
| /genre  | - | - | Get list genre |
| /project/all  | - | - | Get all list project |
| /project  | page | Number | Get list project in page |
| /mangalist  | - | - | Get all manga list |
| /manga  | link | String | Get detail page manga |
| /search  | keyword, page | String, Number | Get search result |
| /read  | link | String | Get reading page image data url |





## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
