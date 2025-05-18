import requests

def valsx(val, basval):
    API='30390c093d1ae7bf786feeb0'
    res = requests.get(f'https://v6.exchangerate-api.com/v6/{API}/latest/{basval}')
    vallist = res.json()
    return vallist['conversion_rates'][val]
    
