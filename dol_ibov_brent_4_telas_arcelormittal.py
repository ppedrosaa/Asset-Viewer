import os, time, webbrowser
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf

INTERVALO = 30
ATIVOS = [
 {"nome":"DOLAR","ticker":"BRL=X","pre":"R$ ","pos":"","dec":4,"html":"tv_dolar.html"},
 {"nome":"IBOVESPA","ticker":"^BVSP","pre":"","pos":" pts","dec":0,"html":"tv_ibovespa.html"},
 {"nome":"PETROLEO BRENT","ticker":"BZ=F","pre":"US$ ","pos":"","dec":2,"html":"tv_brent.html"},
]
LARANJA, CINZA, FUNDO, BRANCO = "#F47D30", "#555658", "#242424", "#FFFFFF"
INDICES = [
 {"nome":"IBOVESPA", "ticker":"^BVSP"}, {"nome":"S&P 500", "ticker":"^GSPC"},
 {"nome":"NASDAQ", "ticker":"^IXIC"}, {"nome":"DOW JONES", "ticker":"^DJI"},
 {"nome":"DAX", "ticker":"^GDAXI"}, {"nome":"FTSE 100", "ticker":"^FTSE"},
 {"nome":"NIKKEI 225", "ticker":"^N225"}, {"nome":"HANG SENG", "ticker":"^HSI"},
 {"nome":"VIX", "ticker":"^VIX"},
]
ARQUIVO_INDICES = "tv_indices_globais.html"


def baixar(a):
    try:
        d = yf.download(a["ticker"], period="1d", interval="1m", progress=False, auto_adjust=False, threads=False)
        if d.empty: return None
        if isinstance(d.columns, pd.MultiIndex): d.columns = d.columns.get_level_values(0)
        if d.index.tz is None: d.index = d.index.tz_localize("UTC")
        d.index = d.index.tz_convert("America/Sao_Paulo")
        d = d[d.index.hour >= 8].dropna(subset=["Open","High","Low","Close"])
        return None if d.empty else d
    except Exception as e:
        print(f"[{a['nome']}] {e}"); return None


def numero(v, a):
    if a["dec"] == 0: n = f"{v:,.0f}".replace(",", ".")
    else: n = f"{v:,.{a['dec']}f}".replace(",","X").replace(".",",").replace("X",".")
    return a["pre"] + n + a["pos"]


def gerar(a, d):
    fig = go.Figure()
    valor, var, seta = "SEM DADOS", "AGUARDANDO", "●"
    if d is not None:
        ini, fim = float(d.Close.iloc[0]), float(d.Close.iloc[-1])
        pct = (fim / ini - 1) * 100
        valor, var = numero(fim, a), f"{pct:+.2f}%"
        seta = "▲" if pct > 0 else "▼" if pct < 0 else "●"
        fig.add_trace(go.Candlestick(x=d.index, open=d.Open, high=d.High, low=d.Low, close=d.Close,
            increasing_line_color=LARANJA, increasing_fillcolor=LARANJA,
            decreasing_line_color="#D8D8D8", decreasing_fillcolor=CINZA, whiskerwidth=.45))
    fig.update_layout(paper_bgcolor=FUNDO, plot_bgcolor=FUNDO, showlegend=False, dragmode=False,
        margin=dict(l=30,r=100,t=10,b=50), font=dict(family="Arial",color=BRANCO),
        xaxis=dict(showgrid=False,rangeslider=dict(visible=False),tickformat="%H:%M",nticks=9,fixedrange=True,tickfont=dict(size=22,color="#D8D8D8")),
        yaxis=dict(showgrid=True,gridcolor="#4B4B4B",side="right",nticks=8,fixedrange=True,tickfont=dict(size=22,color="#D8D8D8")))
    chart = fig.to_html(full_html=False, include_plotlyjs="cdn", config={"displayModeBar":False,"responsive":True})
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    template = '''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="{intervalo}"><title>{nome}</title><style>
*{{box-sizing:border-box}}html,body{{margin:0;width:100%;height:100%;overflow:hidden;background:{fundo};color:#fff;font-family:Arial}}body{{border-top:12px solid {laranja}}}.pagina{{height:calc(100vh - 12px);padding:28px 42px 18px;display:grid;grid-template-rows:245px 1fr 35px}}.topo{{display:flex;justify-content:space-between;align-items:center;border-bottom:3px solid {cinza}}}h1{{margin:0;font-size:clamp(48px,4.3vw,84px);letter-spacing:4px}}.resumo{{display:flex;align-items:baseline;gap:45px;margin-top:15px}}.valor{{font-size:clamp(72px,7.2vw,138px);font-weight:850;white-space:nowrap}}.variacao{{font-size:clamp(44px,4vw,78px);font-weight:850;color:{laranja};white-space:nowrap}}.marca{{text-align:right;color:{laranja};font-size:clamp(20px,1.5vw,30px);font-weight:700}}.grafico{{min-height:0;padding-top:14px}}.plotly-graph-div{{height:100%!important}}.rodape{{display:flex;justify-content:space-between;align-items:end;color:#D8D8D8;font-size:clamp(15px,1.05vw,21px)}}.ponto{{display:inline-block;width:13px;height:13px;border-radius:50%;background:{laranja};box-shadow:0 0 15px {laranja};margin-right:9px}}</style></head><body><div class="pagina"><header class="topo"><div><h1>{nome}</h1><div class="resumo"><span class="valor">{valor}</span><span class="variacao">{seta} {var}</span></div></div><div class="marca">ARCELORMITTAL<br>MARKET DISPLAY</div></header><main class="grafico">{chart}</main><footer class="rodape"><span>Dados intradiarios via Yahoo Finance</span><span><i class="ponto"></i>AO VIVO | {now} | {intervalo}s</span></footer></div></body></html>'''
    html = template.format(intervalo=INTERVALO,nome=a["nome"],fundo=FUNDO,laranja=LARANJA,cinza=CINZA,valor=valor,seta=seta,var=var,chart=chart,now=now)
    with open(a["html"],"w",encoding="utf-8") as f: f.write(html)


def formatar_indice(v):
    return "N/D" if v is None else f"{v:,.2f}".replace(",","X").replace(".",",").replace("X",".")


def baixar_indice(i):
    try:
        d = yf.download(i["ticker"], period="5d", interval="5m", progress=False, auto_adjust=False, threads=False)
        if d.empty: return None
        if isinstance(d.columns, pd.MultiIndex): d.columns = d.columns.get_level_values(0)
        d = d.dropna(subset=["Close"])
        atual = float(d.Close.iloc[-1])
        datas = pd.Series(d.index.date, index=d.index)
        dias = list(dict.fromkeys(datas.tolist()))
        anterior = float(d.loc[datas == dias[-2], "Close"].iloc[-1]) if len(dias) >= 2 else float(d.Open.iloc[0])
        return atual, (atual / anterior - 1) * 100
    except Exception as e:
        print(f"[{i['nome']}] {e}"); return None


def gerar_indices():
    cards = []
    for i in INDICES:
        d = baixar_indice(i)
        if d is None: valor, var, seta, classe = "N/D", "AGUARDANDO", "●", "neutro"
        else:
            valor, pct = formatar_indice(d[0]), d[1]
            var, seta = f"{pct:+.2f}%", "▲" if pct > 0 else "▼" if pct < 0 else "●"
            classe = "alta" if pct >= 0 else "baixa"
        cards.append(f'<section class="card"><div class="nome-indice">{i["nome"]}</div><div class="valor-indice">{valor}</div><div class="variacao-indice {classe}">{seta} {var}</div></section>')
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    template = '''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="{intervalo}"><title>Indices Globais</title><style>
*{{box-sizing:border-box}}html,body{{margin:0;width:100%;height:100%;overflow:hidden;background:{fundo};color:#fff;font-family:Arial}}body{{border-top:12px solid {laranja}}}.pagina{{height:calc(100vh - 12px);padding:22px 38px 16px;display:grid;grid-template-rows:105px 1fr 34px;gap:16px}}.topo{{display:flex;justify-content:space-between;align-items:center;border-bottom:3px solid {cinza}}}h1{{margin:0;font-size:clamp(42px,3.5vw,68px);letter-spacing:3px}}.marca{{text-align:right;color:{laranja};font-size:clamp(18px,1.25vw,26px);font-weight:800}}.grade{{display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(3,1fr);gap:16px}}.card{{background:#2D2D2D;border-left:8px solid {laranja};border-radius:8px;padding:16px 22px;display:flex;flex-direction:column;justify-content:center;box-shadow:0 8px 20px #0005}}.nome-indice{{color:#D8D8D8;font-size:clamp(18px,1.45vw,28px);font-weight:800;letter-spacing:1.5px}}.valor-indice{{font-size:clamp(34px,3vw,58px);font-weight:850;margin-top:8px;white-space:nowrap}}.variacao-indice{{font-size:clamp(25px,2vw,39px);font-weight:850;margin-top:6px}}.alta{{color:{laranja}}}.baixa{{color:#D8D8D8}}.neutro{{color:#A7A7A7}}.rodape{{display:flex;justify-content:space-between;align-items:end;color:#D8D8D8;font-size:clamp(14px,1vw,19px)}}.ponto{{display:inline-block;width:12px;height:12px;border-radius:50%;background:{laranja};box-shadow:0 0 14px {laranja};margin-right:9px}}</style></head><body><div class="pagina"><header class="topo"><h1>INDICES GLOBAIS</h1><div class="marca">ARCELORMITTAL<br>MARKET DISPLAY</div></header><main class="grade">{cards}</main><footer class="rodape"><span>Dados via Yahoo Finance | Variacao sobre fechamento anterior</span><span><i class="ponto"></i>AO VIVO | {now} | {intervalo}s</span></footer></div></body></html>'''
    html = template.format(intervalo=INTERVALO, fundo=FUNDO, laranja=LARANJA, cinza=CINZA, cards="".join(cards), now=now)
    with open(ARQUIVO_INDICES,"w",encoding="utf-8") as f: f.write(html)
    print(f"Atualizado: {ARQUIVO_INDICES}")

def atualizar():
    for a in ATIVOS:
        gerar(a, baixar(a)); print(f"Atualizado: {a['html']}")
    gerar_indices()

if __name__ == "__main__":
    atualizar()
    for a in ATIVOS:
        webbrowser.open("file://" + os.path.realpath(a["html"]), new=1); time.sleep(1)
    webbrowser.open("file://" + os.path.realpath(ARQUIVO_INDICES), new=1)
    try:
        while True: time.sleep(INTERVALO); atualizar()
    except KeyboardInterrupt: print("\nEncerrado.")
