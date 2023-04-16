import csv
import subprocess
import requests

# Configurações de autenticação da API do cPanel
host = 'seu_servidor'
user = 'seu_usuario_cpanel'
password = 'sua_senha_cpanel'

# Endpoint da API do cPanel
api_endpoint = f'https://{host}:2083/json-api/'

# Cabeçalho da requisição
headers = {'Authorization': f'cpanel {user}:{password}'}

# Obtém a lista de contas cPanel
response = requests.get(api_endpoint + 'listaccts', headers=headers)
accounts = response.json()['acct']

# Cria uma lista vazia para armazenar os resultados da pesquisa
results = []

# Percorre cada conta cPanel
for account in accounts:
    # Obtém a lista de domínios da conta cPanel
    response = requests.get(api_endpoint + f'listsubdomains?domain={account["domain"]}', headers=headers)
    domains = response.json()['cpanelresult']['data']

    # Percorre cada domínio da conta cPanel
    for domain in domains:
        # Executa o comando nslookup para pesquisar pelo DNS autoritativo do domínio
        cmd = f'nslookup -type=ns {domain["domain"]}'
        output = subprocess.check_output(cmd, shell=True, text=True)

        # Verifica se o DNS autoritativo está apontando para o servidor correto
        if 'dns1.idc.redeunifique.com.br' in output:
            # Adiciona o domínio e o DNS autoritativo na lista de resultados
            results.append({'domain': domain['domain'], 'nameserver': 'dns1.idc.redeunifique.com.br'})

# Exporta os resultados para um arquivo CSV
with open('results.csv', 'w', newline='') as csvfile:
    fieldnames = ['domain', 'nameserver']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for result in results:
        writer.writerow(result)
