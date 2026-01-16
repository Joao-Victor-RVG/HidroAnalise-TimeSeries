import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# ===============================
# CONFIGURAÇÕES
# ===============================
DATA_DIR = Path("data")
OUTPUT_DIR = Path("output/graficos")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MESES = [
    "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
    "Jul", "Ago", "Set", "Out", "Nov", "Dez"
]

# Dicionário de correção de nomes de cidades (português correto como nome próprio)
NOMES_CORRECAO = {
    "Goianesia": "Goianésia",
    "Campoalegre": "Campo Alegre de Goiás",
    "Marzagao": "Marzagão",
    "Tresranchos": "Três Ranchos",
}

# Configurar estilo de gráficos para padrão científico
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams.update({
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'font.size': 10,
    'font.family': 'Times New Roman',
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'lines.linewidth': 1.5,
    'axes.grid': True,
})

# ===============================
# FUNÇÃO DE LEITURA DOS TXT
# ===============================
def carregar_dados(caminho_arquivo):
    """
    Lê arquivo de estação pluviométrica em formato .txt (padrão HIDROWEB).
    Identifica início da tabela pela linha "Data", extrai data e precipitação.
    Trata encoding latin1 e valores decimais em formato brasileiro (vírgula).
    """
    linhas = open(caminho_arquivo, encoding="latin1").readlines()

    # Encontrar onde começa a tabela (linha com "Data" no início)
    inicio = None
    for i, linha in enumerate(linhas):
        if linha.strip().startswith("Data"):
            inicio = i + 1
            break
    
    if inicio is None:
        raise ValueError(f"Não foi encontrada linha 'Data' em {caminho_arquivo}")

    # Processar linhas de dados
    dados = []
    for linha in linhas[inicio:]:
        linha_limpa = linha.strip()
        
        # Pular linhas vazias
        if not linha_limpa:
            continue
        
        # Separar por espaços múltiplos
        partes = linha_limpa.split()
        
        # Precisa de pelo menos data (partes[0]) e precipitação (partes[1])
        if len(partes) < 2:
            continue
        
        try:
            data = partes[0]
            prec_str = partes[1].replace(",", ".")
            prec = float(prec_str)
            dados.append([data, prec])
        except (ValueError, IndexError):
            # Pular linhas com formato inválido
            continue

    if not dados:
        raise ValueError(f"Nenhum dado foi extraído de {caminho_arquivo}")

    df = pd.DataFrame(dados, columns=["data", "precip"])
    df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
    df = df.sort_values("data").reset_index(drop=True)
    
    # Colunas temporais
    df["ano"] = df["data"].dt.year
    df["mes"] = df["data"].dt.month
    df["dia_mes"] = df["data"].dt.day
    df["ano_mes"] = df["data"].dt.to_period("M")  # Período mensal (YYYY-MM)
    
    # Calcular pentada (1 a 6 - períodos de 5 dias)
    # Pentada 1: dias 1-5, Pentada 2: dias 6-10, ..., Pentada 6: dias 26-31
    df["pentada"] = np.ceil(df["dia_mes"] / 5).astype(int)

    return df

# ===============================
# GRÁFICOS
# ===============================

def serie_temporal_mensal(df, nome, pasta):
    """
    Série temporal mensal com tendência linear e média histórica.
    
    Esta é a SÉRIE PRINCIPAL para modelagem ARIMA.
    Agregação: precipitação total acumulada por mês.
    
    Retorna também o dataframe mensal indexado por período.
    """
    # Agregar por período mensal
    mensal_agg = df.groupby("ano_mes")["precip"].agg(
        ["sum", "count", "mean", "std"]
    ).reset_index()
    
    mensal_agg.columns = ["ano_mes", "precip_total", "n_dias", "media_diaria", "std_diaria"]
    
    # Converter para série temporal com índice de data
    mensal_agg["data"] = pd.to_datetime(mensal_agg["ano_mes"].astype(str) + "-01")
    mensal = mensal_agg.sort_values("data").reset_index(drop=True)
    
    x = np.arange(len(mensal))
    y = mensal["precip_total"].values
    
    # Calcular tendência linear
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    tendencia = intercept + slope * x

    fig, ax = plt.subplots(figsize=(13, 6))
    ax.plot(mensal["data"], y, marker='o', linewidth=1.5, markersize=4, 
            label='Precipitação Mensal', color='steelblue')
    ax.plot(mensal["data"], tendencia, linestyle='--', linewidth=2, 
            label=f'Tendência Linear (R²={r_value**2:.3f})', color='red')
    ax.axhline(y.mean(), linestyle=':', linewidth=1.5, label='Média Histórica', 
               color='green', alpha=0.7)
    
    ax.fill_between(mensal["data"], y, alpha=0.2, color='steelblue')
    ax.set_title(f'Série Temporal Mensal de Precipitação - {nome}\n(Base para modelagem ARIMA)', 
                 fontweight='bold', fontsize=13)
    ax.set_xlabel('Data')
    ax.set_ylabel('Precipitação Total (mm)')
    ax.legend(loc='best', framealpha=0.95)
    ax.grid(True, alpha=0.3)
    
    # Formatar eixo x para mostrar datas melhor
    import matplotlib.dates as mdates
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig(pasta / "01_serie_temporal_mensal.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    return mensal

def serie_pentadal(df, nome, pasta):
    """
    Análise pentadal: acúmulo de precipitação em períodos de 5 dias.
    
    Mostra a distribuição intra-mensal de precipitação.
    Útil para identificar padrões de concentração de chuvas.
    
    Pentadas:
    - P1: dias 1-5
    - P2: dias 6-10
    - P3: dias 11-15
    - P4: dias 16-20
    - P5: dias 21-25
    - P6: dias 26-30 (note: pode incluir dia 31 em alguns meses)
    """
    # Agregar por pentada (média dos 31 anos)
    # Limitar a pentadas 1-6
    df_pentadas = df[df["pentada"] <= 6].copy()
    
    pentadal_agg = df_pentadas.groupby("pentada")["precip"].agg(
        ["sum", "mean", "std", "count"]
    ).reset_index()
    
    pentadal_agg.columns = ["pentada", "precip_total", "media_diaria", "std_diaria", "n_dias"]
    pentadal_media = pentadal_agg.copy()
    
    # Nomes descritivos das pentadas
    pentadas_nomes = [
        "Pentada 1\n(dias 1-5)",
        "Pentada 2\n(dias 6-10)",
        "Pentada 3\n(dias 11-15)",
        "Pentada 4\n(dias 16-20)",
        "Pentada 5\n(dias 21-25)",
        "Pentada 6\n(dias 26-31)"
    ]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Gráfico 1: Precipitação total por pentada
    cores = plt.cm.viridis(np.linspace(0, 1, 6))
    bars1 = ax1.bar(pentadas_nomes, pentadal_media["precip_total"], 
                    color=cores, edgecolor='black', linewidth=1, alpha=0.8)
    
    for bar, val in zip(bars1, pentadal_media["precip_total"]):
        ax1.text(bar.get_x() + bar.get_width()/2, val + 2, f'{val:.0f}', 
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    ax1.set_title(f'Precipitação Total por Pentada\n(Acúmulo histórico)', 
                  fontweight='bold', fontsize=12)
    ax1.set_ylabel('Precipitação (mm)')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Gráfico 2: Média diária por pentada
    bars2 = ax2.bar(pentadas_nomes, pentadal_media["media_diaria"], 
                    yerr=pentadal_media["std_diaria"],
                    color=cores, edgecolor='black', linewidth=1, alpha=0.8, capsize=5)
    
    for bar, val in zip(bars2, pentadal_media["media_diaria"]):
        ax2.text(bar.get_x() + bar.get_width()/2, val + 0.2, f'{val:.2f}', 
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    ax2.set_title(f'Precipitação Média Diária por Pentada\n(com desvio padrão)', 
                  fontweight='bold', fontsize=12)
    ax2.set_ylabel('Precipitação Média Diária (mm)')
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(pasta / "02_analise_pentadal.png", dpi=300, bbox_inches='tight')
    plt.close()

def serie_pentadal_temporal(df, nome, pasta):
    """
    Série temporal pentadal: precip acumulada em períodos de 5 dias ao longo do tempo.
    
    Mostra como a distribuição pentadal varia ao longo dos anos.
    """
    # Agregar por ano e pentada
    pentadal_anual = df.groupby(["ano", "pentada"])["precip"].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(13, 6))
    
    # Criar um gráfico de linha para cada pentada
    pentadas_nomes = ["P1", "P2", "P3", "P4", "P5", "P6"]
    cores = plt.cm.viridis(np.linspace(0, 1, 6))
    
    for pentada, cor, nome_pentada in zip(range(1, 7), cores, pentadas_nomes):
        dados_pentada = pentadal_anual[pentadal_anual["pentada"] == pentada]
        ax.plot(dados_pentada["ano"], dados_pentada["precip"], 
                marker='o', markersize=3, linewidth=1.5, 
                label=nome_pentada, color=cor, alpha=0.8)
    
    ax.set_title(f'Evolução Temporal da Precipitação por Pentada - {nome}', 
                 fontweight='bold', fontsize=13)
    ax.set_xlabel('Ano')
    ax.set_ylabel('Precipitação Pentadal (mm)')
    ax.legend(loc='best', ncol=2, framealpha=0.95)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(pasta / "02b_serie_pentadal_temporal.png", dpi=300, bbox_inches='tight')
    plt.close()

def grafico_anual(df, nome, pasta):
    """Série temporal de precipitação anual com tendência linear e média histórica.
    
    NOTA: Mantido como análise complementar. A série PRINCIPAL é a mensal.
    """
    anual = df.groupby("ano")["precip"].sum()

    x = anual.index.values.astype(float)
    y = anual.values

    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    tendencia = intercept + slope * x

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(x, y, marker='o', linewidth=1.5, markersize=5, label='Precipitação Anual', color='steelblue')
    ax.plot(x, tendencia, linestyle='--', linewidth=2, label=f'Tendência (R²={r_value**2:.3f})', color='red')
    ax.axhline(y.mean(), linestyle=':', linewidth=1.5, label='Média Histórica', color='green', alpha=0.7)
    
    ax.fill_between(x, y, alpha=0.2, color='steelblue')
    ax.set_title(f'Precipitação Total Anual - {nome}\n(Análise complementar)', fontweight='bold', fontsize=13)
    ax.set_xlabel('Ano')
    ax.set_ylabel('Precipitação (mm)')
    ax.legend(loc='best', framealpha=0.95)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(pasta / "03_precipitacao_anual_complementar.png", dpi=300, bbox_inches='tight')
    plt.close()

def grafico_mensal(df, nome, pasta):
    """Precipitação média mensal com barra de desvio padrão.
    
    Análise climatológica (média de todos os anos) por mês do ano.
    """
    mensal = df.groupby("mes")["precip"].agg(["mean", "std"])

    fig, ax = plt.subplots(figsize=(11, 6))
    cores = plt.cm.RdYlBu_r(np.linspace(0.2, 0.8, 12))
    bars = ax.bar(MESES, mensal["mean"], yerr=mensal["std"], capsize=6, 
                   color=cores, edgecolor='black', linewidth=0.5, alpha=0.8)
    
    # Adicionar valores nas barras
    for i, (bar, val) in enumerate(zip(bars, mensal["mean"])):
        ax.text(bar.get_x() + bar.get_width()/2, val + mensal["std"].iloc[i] + 5, 
                f'{val:.1f}', ha='center', va='bottom', fontsize=8)

    ax.set_title(f'Climatologia Mensal de Precipitação - {nome}\n(Média de todos os anos)', fontweight='bold', fontsize=13)
    ax.set_xlabel('Mês do Ano')
    ax.set_ylabel('Precipitação Média (mm)')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(pasta / "04_climatologia_mensal.png", dpi=300, bbox_inches='tight')
    plt.close()

def histograma_mensal(df, nome, pasta):
    """Histograma de distribuição de precipitação diária."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Remover zeros para melhor visualização
    precip_nao_zero = df[df["precip"] > 0]["precip"]
    
    ax.hist(precip_nao_zero, bins=35, color='steelblue', edgecolor='black', 
            alpha=0.7, label=f'Dias com chuva (n={len(precip_nao_zero)})')
    
    ax.axvline(precip_nao_zero.mean(), color='red', linestyle='--', linewidth=2, label=f'Média={precip_nao_zero.mean():.1f} mm')
    ax.axvline(precip_nao_zero.median(), color='green', linestyle='--', linewidth=2, label=f'Mediana={precip_nao_zero.median():.1f} mm')
    
    ax.set_title(f'Distribuição de Precipitação Diária - {nome}', fontweight='bold', fontsize=13)
    ax.set_xlabel('Precipitação (mm)')
    ax.set_ylabel('Frequência')
    ax.legend(loc='best', framealpha=0.95)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(pasta / "05_histograma_precipitacao_diaria.png", dpi=300, bbox_inches='tight')
    plt.close()

def histograma_anual(df, nome, pasta):
    """Histograma de distribuição de precipitação anual (complementar)."""
    anual = df.groupby("ano")["precip"].sum()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(anual, bins=15, color='coral', edgecolor='black', alpha=0.7)
    
    ax.axvline(anual.mean(), color='red', linestyle='--', linewidth=2, label=f'Média={anual.mean():.1f} mm')
    ax.axvline(anual.median(), color='green', linestyle='--', linewidth=2, label=f'Mediana={anual.median():.1f} mm')
    
    ax.set_title(f'Distribuição de Precipitação Anual - {nome}\n(Análise complementar)', fontweight='bold', fontsize=13)
    ax.set_xlabel('Precipitação Total Anual (mm)')
    ax.set_ylabel('Frequência')
    ax.legend(loc='best', framealpha=0.95)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(pasta / "06_histograma_anual.png", dpi=300, bbox_inches='tight')
    plt.close()

def boxplot_mensal(df, nome, pasta):
    """Boxplot de precipitação por mês do ano."""
    dados = [df[df["mes"] == m]["precip"] for m in range(1, 13)]

    fig, ax = plt.subplots(figsize=(11, 6))
    bp = ax.boxplot(dados, labels=MESES, patch_artist=True, 
                     notch=True, showmeans=True,
                     meanprops=dict(marker='D', markerfacecolor='red', markersize=6))
    
    # Colorir as caixas
    cores = plt.cm.RdYlBu_r(np.linspace(0.2, 0.8, 12))
    for patch, color in zip(bp['boxes'], cores):
        patch.set_facecolor(color)
        patch.set_alpha(0.8)

    ax.set_title(f'Variabilidade Mensal de Precipitação - {nome}\n(Distribuição diária por mês)', fontweight='bold', fontsize=13)
    ax.set_xlabel('Mês do Ano')
    ax.set_ylabel('Precipitação (mm)')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(pasta / "07_boxplot_mensal.png", dpi=300, bbox_inches='tight')
    plt.close()

def boxplot_anual(df, nome, pasta):
    """Boxplot de precipitação anual (complementar)."""
    anual = df.groupby("ano")["precip"].sum()

    fig, ax = plt.subplots(figsize=(8, 6))
    bp = ax.boxplot(anual, patch_artist=True, notch=True, showmeans=True,
                    meanprops=dict(marker='D', markerfacecolor='red', markersize=8))
    
    bp['boxes'][0].set_facecolor('lightblue')
    bp['boxes'][0].set_alpha(0.8)

    ax.set_title(f'Variabilidade Anual de Precipitação - {nome}\n(Análise complementar)', fontweight='bold', fontsize=13)
    ax.set_ylabel('Precipitação Total Anual (mm)')
    ax.set_xticklabels(['Série Completa'])
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(pasta / "08_boxplot_anual.png", dpi=300, bbox_inches='tight')
    plt.close()

# ===============================
# FUNÇÕES AUXILIARES
# ===============================

def exportar_serie_arima(mensal_df, nome_estacao, pasta):
    """
    Exporta a série temporal mensal em formato CSV para futuro uso com ARIMA.
    
    A série é:
    - Indexada por período (YYYY-MM)
    - Sem lacunas temporais (todos os meses estão presentes)
    - Com valores de precipitação total mensal em mm
    
    Estrutura do CSV:
    periodo,precip_total,n_dias,media_diaria,std_diaria
    """
    mensal_df_arima = mensal_df[["ano_mes", "precip_total"]].copy()
    mensal_df_arima.columns = ["periodo", "precip_mm"]
    
    arquivo_csv = pasta / f"serie_temporal_mensal_arima_{nome_estacao.lower().replace(' ', '_')}.csv"
    mensal_df_arima.to_csv(arquivo_csv, index=False, sep=",")
    
    return arquivo_csv

# ===============================
# EXECUÇÃO PRINCIPAL
# ===============================
if __name__ == "__main__":
    arquivos = list(DATA_DIR.glob("*.txt"))
    
    if not arquivos:
        print(f"⚠️  Nenhum arquivo .txt encontrado em {DATA_DIR}")
    else:
        print(f"📊 Processando {len(arquivos)} estação(ões)...\n")
        print("=" * 70)
        
        for arquivo in arquivos:
            try:
                # Extrair nome da estação
                nome_arquivo = arquivo.stem
                nome_estacao = nome_arquivo.split("33")[0].strip()
                nome_estacao = nome_estacao.replace("_", " ").title()
                
                # Aplicar correção de acentuação e português correto
                nome_estacao_corrigido = NOMES_CORRECAO.get(nome_estacao, nome_estacao)
                
                pasta_saida = OUTPUT_DIR / nome_estacao.lower().replace(" ", "_")
                pasta_saida.mkdir(parents=True, exist_ok=True)

                print(f"\n📈 Estação: {nome_estacao_corrigido}")
                print(f"   Arquivo: {arquivo.name}")
                
                # Carregar dados
                df = carregar_dados(arquivo)
                print(f"   ✓ Dados carregados: {len(df)} registros | Anos: {df['ano'].min():.0f}-{df['ano'].max():.0f}")
                
                # Gerar série mensal (SÉRIE PRINCIPAL)
                print(f"   ► Gerando série temporal mensal (base ARIMA)...")
                mensal_df = serie_temporal_mensal(df, nome_estacao_corrigido, pasta_saida)
                print(f"      ✓ {len(mensal_df)} meses agregados")
                
                # Análise pentadal
                print(f"   ► Gerando análise pentadal...")
                serie_pentadal(df, nome_estacao_corrigido, pasta_saida)
                serie_pentadal_temporal(df, nome_estacao_corrigido, pasta_saida)
                print(f"      ✓ 2 gráficos pentadais criados")
                
                # Gráficos complementares
                print(f"   ► Gerando gráficos complementares...")
                grafico_anual(df, nome_estacao_corrigido, pasta_saida)
                grafico_mensal(df, nome_estacao_corrigido, pasta_saida)
                histograma_mensal(df, nome_estacao_corrigido, pasta_saida)
                histograma_anual(df, nome_estacao_corrigido, pasta_saida)
                boxplot_mensal(df, nome_estacao_corrigido, pasta_saida)
                boxplot_anual(df, nome_estacao_corrigido, pasta_saida)
                print(f"      ✓ 6 gráficos complementares criados")
                
                # Exportar série para ARIMA
                print(f"   ► Exportando série mensal para ARIMA...")
                arquivo_csv = exportar_serie_arima(mensal_df, nome_estacao, pasta_saida)
                print(f"      ✓ Arquivo CSV: {arquivo_csv.name}")
                
                print(f"   ✅ Total: 8 gráficos + 1 arquivo CSV | Pasta: {pasta_saida}")
                
            except Exception as e:
                print(f"   ❌ Erro: {str(e)}")
                continue
        
        print("\n" + "=" * 70)
        print("✅ Processamento concluído!")
        print("\n📌 NOTA IMPORTANTE:")
        print("   - Série PRINCIPAL: Série temporal mensal (01_serie_temporal_mensal.png)")
        print("   - Use para: Análise de tendência, ARIMA, previsões")
        print("   - Arquivos CSV (serie_temporal_mensal_arima_*.csv) estão prontos para modelagem")
