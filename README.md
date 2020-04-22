## First use
1. Create a virtual env

```shell
virtualenv -p python env
```
NB: **virtualenv** *should be installed before*

2. Activate your virtual env
```shell
.\env\Scripts\activate
```
3. Install the dependencies
```shell
pip install -r requirements.txt
```

## How to lunch ?
```shell
python main.py
```

## Versions
* Python: 3.7.0 64bits

## Download spaCy models
* en
```shell
python -m spacy download en_core_web_sm  
```
* fr
```shell
python -m spacy download fr_core_news_sm 
```
