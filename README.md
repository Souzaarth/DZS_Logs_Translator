# Tradutor de Logs DZS (Dasan Fiber Chassis)

## Contexto e Motivação

Este projeto foi criado para suprir uma necessidade na infraestrutura de rede da prefeitura municipal, que utiliza o chassi de fibra óptica Dasan (DZS). Após a configuração de um serviço de syslog (ativado pela CLI do equipamento) e seu redirecionamento para uma máquina virtual Linux atuando como Syslog Center, notou-se um problema crítico: as logs fornecidas pelo equipamento chegavam da maneira mais crua possível.
O maior impacto desse formato nativo era a ineficiência em capturar o evento de *"dying gasp"*, uma mensagem fundamental que indica falta de energia no local (queda elétrica) da respectiva ONU. 
Para resolver essa limitação, este script foi desenvolvido para atuar como um "tradutor" e filtro. Ele processa a saída bruta das logs, identifica o evento crítico de falta de energia e padroniza a formatação para uma visualização clara e objetiva para as secretarias e setores.

## Funcionalidades da Solução

- **Reconhecimento do "Dying Gasp":** Captura e traduz eventos de queda elétrica das ONUs de forma clara sob a classificação `Power-Failure`.
- **Filtro Inteligente de Eventos:** Tratamento automático de eventos de conexão óptica (como `Gpon-Link-Down` e `Gpon-Link-Up`), ignorando eventos irrelevantes que poluem o log (como testes repetitivos de provisionamento `Falha-Provisionamento-OMCI`).
- **Formatação de Saída Estruturada:** Lê e formata a data, hora, IP da rede, chassi, evento, MAC/Nome e porta da ONU, gerando entradas limpas:
  `[Data/Hora] [IP_DO_CHASSI] syslog - [DZS-CH001] [EVENTO],mac[Nome_Local],onu[PORTA]`
- **Monitoramento em Tempo Real:** O script lê o arquivo original de forma contínua, gravando as informações traduzidas instantaneamente em um novo arquivo (modo *tail*).

## Configuração e Instalação

Siga os passos abaixo para preparar o arquivo no respectivo Syslog Center:

### 1. Definição do Log de Origem e Destino

Edite as variáveis principais informando o arquivo onde o rsyslog do Linux grava as saídas da porta 514, e decida onde as logs ficarão traduzidas:
```python
LOG_ENTRADA = "/var/log/syslog_bruto.log" 
LOG_SAIDA = "/var/log/syslog_filtrado.log" 
```
### 2. Mapeamento Manual das ONUs

A correlação das portas PON com suas secretarias e locais de atendimento tem de ser feita manualmente em código. Abaixo da variável `mapa_onus = {`, mapeie o equipamento conforme a arquitetura da prefeitura e identificação do ramal óptico:
```python
mapa_onus = {
    # LINHA PON 1 (1/1/1/X)
    "1/1/1/1": "Secretaria-de-Educacao",
    "1/1/1/2": "Escola-Municipal",
    "1/1/1/3": "Posto-de-Saude-Bairro",
    
    # LINHA PON 2
    "1/1/2/1": "Prefeitura-Gabinete",
}
```
### 3. Execução do Tradutor

Após garantir que os serviços de redirecionamento (rsyslog) estão injetando as logs passivas na porta/arquivo correto (`LOG_ENTRADA`), ative o script preferencialmente em background no ambiente Linux (utilizando serviço no Systemd ou `nohup`).
```bash
python3 script_tradutor_DZS.py

```
## Requisitos Globais (Bibliotecas Utilizadas)
Sendo prático, o script baseia-se unicamente nas bibliotecas nativas da linguagem Python padrão.
* `time`: Intervalo do tail para leitura do processo da máquina virtual.
* `re` (Regex): Localização das strings de dying gasp e portas PON no texto cru.
* `datetime` e `os`: Verificação da estampa de horário e presença do log no diretório raiz do disco.


Prints Demonstrativos: 

Log que o CHASSI DZS manda:

<img width="1007" height="75" alt="image" src="https://github.com/user-attachments/assets/6745639c-2745-40ba-8649-411d5b64e518" />


Log depois de formatado pelo script em tempo real:

<img width="992" height="48" alt="image" src="https://github.com/user-attachments/assets/91a9fe74-a4ab-4078-8a58-7cc165a2136d" />

