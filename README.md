# Market Display Dashboard 📈

Um script em Python para monitoramento e criação de dashboards financeiros em tempo real. Este projeto consulta dados intradiários e gera páginas HTML estáticas que se atualizam automaticamente com cotações e gráficos interativos.

## 🚀 Funcionalidades

- **Gráficos em Tempo Real (Candlestick):** Monitoramento contínuo de ativos principais (Dólar, Ibovespa e Petróleo Brent) com gráficos gerados nativamente 
- **Painel de Índices Globais:** Acompanhamento das variações percentuais dos principais índices mundiais (S&P 500, NASDAQ, Dow Jones, DAX, Nikkei 225, etc.) 
- **Auto-Refresh:** As páginas geradas possuem recarregamento automático (padrão de 30 segundos), ideal para exibição em TVs ou monitores de mercado dedicados
- **Interface Otimizada:** Visual em *Dark Mode* estruturado com cores de destaque e grid responsivo 
- **Abertura Automática:** O script cria os arquivos e já os abre automaticamente no navegador padrão do sistema 

## 🛠️ Tecnologias e Dependências

O projeto utiliza as seguintes bibliotecas [cite: 1]:
- [Python 3.x](https://www.python.org/)
- `pandas` - Estruturação e manipulação de séries temporais.
- `plotly` - Geração do visual dos gráficos financeiros.
- `yfinance` - Extração de dados da API pública do Yahoo Finance.

## ⚙️ Como usar

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/ppedrosaa/Asset-Viewer.git
   cd seu-repositorio
   ```

2. **Instale as dependências:**
   ```bash
   pip install pandas plotly yfinance
   ```

3. **Execute o sistema:**
   ```bash
   python script.py
   ```
   *(Substitua `script.py` pelo nome correto do arquivo no seu repositório).*

## 📂 Saída (Arquivos Gerados)

Após a execução, os seguintes painéis HTML serão criados no diretório do projeto e atualizados em background a cada 30 segundos:
- `tv_dolar.html`
- `tv_ibovespa.html`
- `tv_brent.html`
- `tv_indices_globais.html`

## 👨‍💻 Autor

- **Pedro Henrique Vieira Pedrosa** 
