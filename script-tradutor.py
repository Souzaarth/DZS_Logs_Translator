 GNU nano 7.2                                                                               tradutor_dzs.py
import time
import re
from datetime import datetime
import os

LOG_ENTRADA = "/var/log/dzs_olt.log"
LOG_SAIDA = "/var/log/dzs_olt_formatado.log"

mapa_onus = {

   # === LINHA PON 1 (1/1/1/X)
    "1/1/1/1": "PAT",
    "1/1/1/2": "Escola-Joao-Marciano",
    "1/1/1/3": "EMEB-Antonio-Sicchierolli",
    "1/1/1/4": "Tiro-de-Guerra",
    "1/1/1/5": "Almoxarifado-Transito",
    "1/1/1/6": "EE-Prof-Benedito-Eufrasio",
    "1/1/1/7": "EE-CAPITAO-JOSE-PINHEIRO-DE-LACERDA",
    "1/1/1/8": "EE-Carmem-Munhoz-Coelho",
    "1/1/1/9": "CRAS-Leste",
    "1/1/1/10": "EE-Angelo-Gosuen",
    "1/1/1/11": "EE-Carmem-Nogueira",
    "1/1/1/12": "UBS-Paulista",
    "1/1/1/13": "UBS-Brasilandia",
    "1/1/1/14": "EE-Suely-Machado",
    "1/1/1/15": "EMEB-Luzinete-Baliero",
    "1/1/1/16": "EMEB-Cesar-Augusto",
    "1/1/1/17": "EMEB-Milton-Gama",
    "1/1/1/18": "UBS-Paulistano",
    "1/1/1/19": "EE-Michel-Haber",
    "1/1/1/20": "EMEB-Marilourdes",
    "1/1/1/21": "EE-Jose-Donadelli",
    "1/1/1/22": "PSF-Palma",
    "1/1/1/23": "UBS-Planalto",
    "1/1/1/24": "EMEB-Frei-Lauro",
    "1/1/1/25": "Alimentação-Escolar",
    "1/1/1/26": "SVO",
    "1/1/1/27": "Cemiterio-Santo-Agostinho",
    "1/1/1/28": "EE-Adelina-Pasquino",
    "1/1/1/29": "Rack-Infra",
    "1/1/1/30": "Bombeiros",
    "1/1/1/31": "Sassom",
    "1/1/1/32": "EMEB-Emilia-Tarantelli",
    "1/1/1/33": "Cadastro-Unico",
    "1/1/1/34": "EE-Torquato-Caleiro",
    "1/1/1/35": "CREAS-I",
    "1/1/1/36": "Fussol",
    "1/1/1/37": "Laboratorio-Teste",
    "1/1/1/38": "Junta-Militar",
    "1/1/1/39": "Central-de-Monitoramento",
    "1/1/1/40": "CEI",
    "1/1/1/41": "EE-Caetano-Petraglia",
    "1/1/1/42": "SIAS",
    "1/1/1/43": "CEFAP",

    #  LINHA PON 2 (1/1/2/X)
    "1/1/2/1": "UBS-Estacao",
    "1/1/2/2": "EMEB-Dorotea-Paulino",
    "1/1/2/3": "UBS-Estacao-2",
    "1/1/2/4": "UBS-Sao-Sebastiao",
    "1/1/2/5": "EMEB-Augusto-Marques",
    "1/1/2/6": "EE-Jeronimo-Sandoval",
    "1/1/2/7": "EE-Ana-Junqueira",
    "1/1/2/8": "EE -Prof-Helio-Palermo",
    "1/1/2/9": "CREAS-II",
    "1/1/2/10": "EE-David-Ewbank",
    "1/1/2/11": "EMEB-Nair-Martins-Rocha",
    "1/1/2/12": "EE-Barao-da-Franca",
    "1/1/2/13": "EMEB-Domenico-Pugliesi",
    "1/1/2/14": "EMEB-Guiomar-Ferreira",
    "1/1/2/15": "EMEB-Rita-De-Cassia",
    "1/1/2/16": "UBS-Santa-Clara",
    "1/1/2/17": "EMEB-Nelson-Damasceno",
    "1/1/2/18": "UPA-Anita",
    "1/1/2/19": "EMEB-Etelgina-de-Fatima",
    "1/1/2/20": "EE-Luiz-Paride-Sinelli",
    "1/1/2/21": "EE-Prof-Stella-Mata-Ambrosio",
    "1/1/2/22": "EE-Prof-Israel-Niceus-Moreira",
    "1/1/2/23": "EMEB-Nadeide-Scarabucci",
    "1/1/2/24": "EMEB-Sonia-Menezes-Pizzo",
    "1/1/2/25": "Biblioteca-Estacao",

    # Linha PON 3
    "1/1/3/1": "UBS-Estacao(1-1-3-1)",
    "1/1/3/2": "EMEB-Nair-Martins-Rocha",
    "1/1/3/3": "UBS-Estacao-2(1-1-3-3)",
    "1/1/3/4": "UBS-Sao-Sebastiao",
    "1/1/3/5": "EMEB-Augusto-Marques",
    "1/1/3/6": "EMEB-Dorotea-Paulino",
    "1/1/3/7": "Champagnat",
    "1/1/3/8": "Biblioteca-Central",
    "1/1/3/9": "SEC-Acao-Social",
    "1/1/3/10": "Casa-do-Diabetico",
    "1/1/3/11": "EMEB-Domenico-Pugliesi",
    "1/1/3/12": "EMEB-Rita-de-Cassia",
    "1/1/3/13": "EMEB-Etelgina-de-Fatima",
    "1/1/3/16": "EMEB-Nelson-Damasceno",
    "1/1/3/17": "UPA-Anita(1-1-3-17)",
}

def processar_linha(linha):
    # Focar apenas nas linhas que indicam alarmes (Up/Down/Power/OMCI)
    if "alarm_mgr" not in linha and "gponomci" not in linha:
        return None

    # 1. Extrair e formatar a data
    match_data = re.search(r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})', linha)
    if not match_data: return None

    dt_obj = datetime.strptime(match_data.group(1), "%Y-%m-%dT%H:%M:%S")
    data_formatada = dt_obj.strftime("%b %d %H:%M:%S")

    # 2. Extrair a porta da ONU
    onu_id = "Desconhecido"

    # Formato dos alarmes gerais (Ex: Line 1/1/1/7)
    match_line = re.search(r'Line (\d+/\d+/\d+/\d+)', linha)
    if match_line:
        onu_id = match_line.group(1)
    else:
        # Formato dos erros OMCI (Ex: ONU(1/1/7))
        # O DZS omite o segundo '1' no OMCI, então adicionamos para padronizar a busca no mapa
        match_omci = re.search(r'ONU\((\d+)/(\d+)/(\d+)\)', linha)
        if match_omci:
            onu_id = f"{match_omci.group(1)}/1/{match_omci.group(2)}/{match_omci.group(3)}"

    # Buscar o nome no nosso mapa
    nome_local = mapa_onus.get(onu_id, f"ONU-{onu_id}")

    # 3. Traduzir o Evento
    evento = "ALERTA-DESCONHECIDO"
    linha_minuscula = linha.lower() # Converte tudo para minúsculo para facilitar a busca

# Primeiro caçamos o Power Failure, pois ele é o mais específico
    if re.search(r'dying\s*gasp', linha_minuscula) or "power" in linha_minuscula:
        evento = "Power-Failure"
    # Adicionamos "onu down" junto com o "alarm set" antigo
    elif "alarm set" in linha_minuscula or "onu down" in linha_minuscula:
        evento = "Gpon-Link-Down"
    # Adicionamos "onu up" e "cause: active" junto com o "alarms cleared" antigo
    elif "alarms cleared" in linha_minuscula or "onu up" in linha_minuscula or "cause: active" in linha_minuscula:
        evento = "Gpon-Link-Up"
    elif "gponomci" in linha_minuscula:
        evento = "Falha-Provisionamento-OMCI"

# --- INÍCIO DO FILTRO INTELIGENTE ---
    # Ignora OMCI completamente (pois o Zabbix só precisa saber do Link Down/Up)
    if evento == "Falha-Provisionamento-OMCI":
        return None

    # Ignora falso Power Failure APENAS quando não informa a porta
    if evento == "Power-Failure" and onu_id == "Desconhecido":
        return None

    # 4. Montar a string idêntica ao Furukawa
    log_final = f"{data_formatada} 172.21.30.248 syslog - [DZS-CH001] [{evento}],mac[{nome_local}],onu[{onu_id}]\n"
    return log_final

if not os.path.exists(LOG_ENTRADA):
    print(f"Erro: Arquivo {LOG_ENTRADA} não encontrado. Certifique-se que o rsyslog está rodando.")
    exit(1)

print("Iniciando o tradutor de logs DZS...")
with open(LOG_ENTRADA, "r") as f_in, open(LOG_SAIDA, "a") as f_out:
    f_in.seek(0, 2)

    while True:
        linha = f_in.readline()
        if not linha:
            time.sleep(0.5)
            continue

        nova_linha = processar_linha(linha)
        if nova_linha:
            f_out.write(nova_linha)
            f_out.flush()




