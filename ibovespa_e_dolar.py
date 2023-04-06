import pandas as pd
import datetime
import os
from dotenv import load_dotenv
import yfinance as yf
from matplotlib import pyplot as plt
import mplcyberpunk
import smtplib
from email.message import EmailMessage

columns ={
    '^BVSP': 'ibovespa',
    'BRL=X': 'dolar'
}


ativos = ['^BVSP','BRL=X']

def dados_ativos ():
    hoje = datetime.datetime.now()
    ano = hoje - datetime.timedelta(days=365)
    dados_mercados = yf.download(ativos,ano,hoje)
    dados_fechamento = dados_mercados['Adj Close'].rename(columns=columns)
    dados_fechamento = dados_fechamento.dropna(subset=['ibovespa'])
    dados_fechamento_mensal = dados_fechamento.resample('M').last()
    dados_fechamento_anual = dados_fechamento.resample('Y').last()
    retorno_ano = dados_fechamento_anual.pct_change().dropna()
    retorno_mes = dados_fechamento_mensal.pct_change().dropna()
    retorno_dia = dados_fechamento.pct_change().dropna()
    retorno_dia_dolar = retorno_dia.iloc[-1, 0]
    retorno_dia_ibovespa = retorno_dia.iloc[-1, 1]

    retorno_mes_dolar = retorno_mes.iloc[-1, 0]
    retorno_mes_ibovespa = retorno_mes.iloc[-1, 1]

    retorno_ano_dolar = retorno_ano.iloc[-1, 0]
    retorno_ano_ibovespa = retorno_ano.iloc[-1, 1]

    retorno_dia_dolar = round(retorno_dia_dolar * 100, 2)
    retorno_dia_ibovespa = round(retorno_dia_ibovespa * 100, 2)

    retorno_mes_dolar = round(retorno_mes_dolar * 100, 2)
    retorno_mes_ibovespa = round(retorno_mes_ibovespa * 100, 2)

    retorno_ano_dolar = round(retorno_ano_dolar * 100, 2)
    retorno_ano_ibovespa = round(retorno_ano_ibovespa * 100, 2)
    plt.style.use("cyberpunk")

    dados_fechamento.plot(y='ibovespa', use_index=True, legend=False)

    plt.title("Ibovespa")

    plt.savefig('ibovespa.png', dpi=300)

    plt.style.use("cyberpunk")

    dados_fechamento.plot(y='dolar', use_index=True, legend=False)

    plt.title("Dolar")

    plt.savefig('dolar.png', dpi=300)

    load_dotenv()

    senha = os.environ.get('senha')
    email = os.environ.get('email')
    msg = EmailMessage()

    msg['Subject']= "Enviando e-mail com o Python"
    msg['From'] = email

    msg.set_content(f'''Prezado diretor, segue o relatório diário:

    Bolsa:

    No ano o Ibovespa está tendo uma rentabilidade de {retorno_ano_ibovespa}%, 
    enquanto no mês a rentabilidade é de {retorno_mes_ibovespa}%.

    No último dia útil, o fechamento do Ibovespa foi de {retorno_dia_ibovespa}%.

    Dólar:

    No ano o Dólar está tendo uma rentabilidade de {retorno_ano_dolar}%, 
    enquanto no mês a rentabilidade é de {retorno_mes_dolar}%.

    No último dia útil, o fechamento do Dólar foi de {retorno_dia_dolar}%.


    ''')

    with open('dolar.png','rb') as content_file:
        content = content_file.read()
        msg.add_attachment(content,maintype='application', subtype='png',filename='dolar.png')

    with open('ibovespa.png', 'rb') as content_file:
        content = content_file.read()
        msg.add_attachment(content, maintype='application', subtype='png', filename='ibovespa.png')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email, senha)
        smtp.send_message(msg)

if __name__ == '__main__':
    print(dados_ativos())



