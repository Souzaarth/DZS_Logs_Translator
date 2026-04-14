import time
import re
from datetime import datetime
import os

LOG_ENTRADA = "caminho_do_log"
LOG_SAIDA = "caminho_do_log_formatado"

mapa_onus = {

   # LINHA PON 1 (1/1/1/X)

    "1/1/1/1": "Cliente-1",
    "1/1/1/2": "Cliente-2",
    "1/1/1/3": "Cliente-3",
    "1/1/1/4": "Cliente-4",

    #  LINHA PON 2
    "1/1/2/1": "Cliente-44",
    "1/1/2/2": "Cliente-45",
    "1/1/2/3": "Cliente-46",

    # Linha PON 3
    "1/1/3/1": "Cliente-69",
    "1/1/3/2": "Cliente-70",
}

def processar_linha(linha):
    if "alarm_mgr" not in linha and "gponomci" not in linha:
        return None

    # Extrair e formatar a data
    match_data = re.search(r'^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})', linha)
    if not match_data: return None

    dt_obj = datetime.strptime(match_data.group(1), "%Y-%m-%dT%H:%M:%S")
    data_formatada = dt_obj.strftime("%b %d %H:%M:%S")

    # Extrair a porta da ONU
    onu_id = "Desconhecido"

    match_line = re.search(r'Line (\d+/\d+/\d+/\d+)', linha)
    if match_line:
        onu_id = match_line.group(1)
    else:
        match_omci = re.search(r'ONU\((\d+)/(\d+)/(\d+)\)', linha)
        if match_omci:
            onu_id = f"{match_omci.group(1)}/1/{match_omci.group(2)}/{match_omci.group(3)}"

    # Buscar o nome no mapa
    nome_local = mapa_onus.get(onu_id, f"ONU-{onu_id}")

    # Traduzir o Evento
    evento = "ALERTA-DESCONHECIDO"
    linha_minuscula = linha.lower() 

    if re.search(r'dying\s*gasp', linha_minuscula) or "power" in linha_minuscula:
        evento = "Power-Failure"
    elif "alarm set" in linha_minuscula or "onu down" in linha_minuscula:
        evento = "Gpon-Link-Down"
    elif "alarms cleared" in linha_minuscula or "onu up" in linha_minuscula or "cause: active" in linha_minuscula:
        evento = "Gpon-Link-Up"
    elif "gponomci" in linha_minuscula:
        evento = "Falha-Provisionamento-OMCI"


# INÍCIO DO FILTRO INTELIGENTE

    if evento == "Falha-Provisionamento-OMCI":
        return None

    if evento == "Power-Failure" and onu_id == "Desconhecido":
        return None

    log_final = f"{data_formatada} "ip_do_chassi" syslog - [DZS-CH001] [{evento}],mac[{nome_local}],onu[{onu_id}]\n"
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
