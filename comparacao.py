"""
Script de Comparação: Análise Comparativa das 4 Estações Pluviométricas

Compara os dados de precipitação de:
- Goianésia (GO)
- Campo Alegre (SC)
- Marzagão
- Três Ranchos

Gera gráficos comparativos e estatísticas.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.stats import linregress

# ===============================
# CONFIGURAÇÕES
# ===============================
OUTPUT_DIR = Path("output/graficos")
COMPARACAO_DIR = OUTPUT_DIR / "Comparacao"
COMPARACAO_DIR.mkdir(parents=True, exist_ok=True)

ESTACOES = {
    "Goianésia": "goianesia",
    "Campo Alegre de Goiás": "campoalegre",
    "Marzagão": "marzagao",
    "Três Ranchos": "tresranchos"
}

CORES = {
    "Goianésia": "#1f77b4",
    "Campo Alegre de Goiás": "#ff7f0e",
    "Marzagão": "#2ca02c",
    "Três Ranchos": "#d62728"
}

# Configurar estilo
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams.update({
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'font.size': 10,
    'font.family': 'sans-serif',
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'lines.linewidth': 1.5,
    'axes.grid': True,
})

# ===============================
# CARREGAMENTO DE DADOS
# ===============================
def carregar_series_mensais():
    """Carrega as séries mensais de todas as estações."""
    dados = {}
    
    for nome_estacao, pasta_estacao in ESTACOES.items():
        arquivo_csv = OUTPUT_DIR / pasta_estacao / f"serie_temporal_mensal_arima_{pasta_estacao}.csv"
        
        if arquivo_csv.exists():
            df = pd.read_csv(arquivo_csv)
            df['periodo'] = pd.to_datetime(df['periodo'] + '-01')
            df = df.sort_values('periodo')
            dados[nome_estacao] = df
            print(f"✓ {nome_estacao}: {len(df)} meses | {df['precip_mm'].mean():.2f} mm média")
        else:
            print(f"✗ {nome_estacao}: arquivo não encontrado")
    
    return dados

# ===============================
# GRÁFICOS COMPARATIVOS
# ===============================

def comparacao_series_temporais(dados):
    """Compara as séries temporais mensais de todas as estações."""
    fig, ax = plt.subplots(figsize=(14, 7))
    
    for nome_estacao, df in dados.items():
        ax.plot(df['periodo'], df['precip_mm'], 
                label=nome_estacao, color=CORES[nome_estacao], 
                linewidth=2, alpha=0.8, marker='o', markersize=2)
    
    ax.set_title('Comparação de Séries Temporais Mensais de Precipitação\n(1994-2024)', 
                 fontweight='bold', fontsize=13)
    ax.set_xlabel('Data')
    ax.set_ylabel('Precipitação (mm)')
    ax.legend(loc='best', framealpha=0.95)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(COMPARACAO_DIR / "01_series_temporais_comparacao.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfico: 01_series_temporais_comparacao.png")

def comparacao_estatisticas(dados):
    """Compara estatísticas descritivas das 4 estações."""
    estatisticas = []
    
    for nome_estacao, df in dados.items():
        precip = df['precip_mm']
        estatisticas.append({
            'Estação': nome_estacao,
            'Média': precip.mean(),
            'Mediana': precip.median(),
            'Desvio Padrão': precip.std(),
            'Mínimo': precip.min(),
            'Máximo': precip.max(),
            'Q1': precip.quantile(0.25),
            'Q3': precip.quantile(0.75)
        })
    
    df_stats = pd.DataFrame(estatisticas)
    
    # Gráfico de barras: Média de precipitação
    fig, ax = plt.subplots(figsize=(10, 6))
    nomes = df_stats['Estação'].values
    medias = df_stats['Média'].values
    cores_lista = [CORES[nome] for nome in nomes]
    
    bars = ax.bar(nomes, medias, color=cores_lista, edgecolor='black', linewidth=1.5, alpha=0.8)
    
    for bar, val in zip(bars, medias):
        ax.text(bar.get_x() + bar.get_width()/2, val + 10, f'{val:.1f}', 
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax.set_title('Precipitação Mensal Média - Comparação entre Estações', 
                 fontweight='bold', fontsize=13)
    ax.set_ylabel('Precipitação Média Mensal (mm)')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(COMPARACAO_DIR / "02_media_precipitacao_comparacao.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfico: 02_media_precipitacao_comparacao.png")
    
    # Salvar tabela de estatísticas
    df_stats.to_csv(COMPARACAO_DIR / "estatisticas_descritivas.csv", index=False)
    print("✓ Arquivo: estatisticas_descritivas.csv")
    
    return df_stats

def comparacao_boxplot(dados):
    """Boxplot comparativo das 4 estações."""
    dados_lista = [dados[nome]['precip_mm'].values for nome in ESTACOES.keys()]
    nomes = list(ESTACOES.keys())
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bp = ax.boxplot(dados_lista, labels=nomes, patch_artist=True, 
                     notch=True, showmeans=True,
                     meanprops=dict(marker='D', markerfacecolor='red', markersize=7))
    
    # Colorir as caixas
    for patch, nome in zip(bp['boxes'], nomes):
        patch.set_facecolor(CORES[nome])
        patch.set_alpha(0.8)
    
    ax.set_title('Distribuição de Precipitação Mensal - Boxplot Comparativo', 
                 fontweight='bold', fontsize=13)
    ax.set_ylabel('Precipitação (mm)')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(COMPARACAO_DIR / "03_boxplot_comparacao.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfico: 03_boxplot_comparacao.png")

def comparacao_climatologia_mensal(dados):
    """Compara a climatologia mensal (média de todos os anos por mês)."""
    MESES = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
             "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
    
    fig, ax = plt.subplots(figsize=(13, 6))
    
    for nome_estacao in ESTACOES.keys():
        # Recalcular climatologia a partir dos dados mensais
        df_mensal = dados[nome_estacao]
        df_mensal['mes'] = df_mensal['periodo'].dt.month
        climatologia = df_mensal.groupby('mes')['precip_mm'].mean()
        
        ax.plot(range(1, 13), climatologia.values, 
                marker='o', markersize=7, linewidth=2,
                label=nome_estacao, color=CORES[nome_estacao], alpha=0.8)
    
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(MESES)
    ax.set_title('Climatologia Mensal - Padrão Sazonal Comparativo', 
                 fontweight='bold', fontsize=13)
    ax.set_xlabel('Mês do Ano')
    ax.set_ylabel('Precipitação Média Mensal (mm)')
    ax.legend(loc='best', framealpha=0.95)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(COMPARACAO_DIR / "04_climatologia_mensal_comparacao.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfico: 04_climatologia_mensal_comparacao.png")

def comparacao_tendencia_linear(dados):
    """Compara as tendências lineares das 4 estações."""
    fig, ax = plt.subplots(figsize=(14, 7))
    
    for nome_estacao, df in dados.items():
        # Preparar dados
        x = np.arange(len(df))
        y = df['precip_mm'].values
        
        # Calcular tendência
        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        tendencia = intercept + slope * x
        
        # Plotar
        ax.plot(df['periodo'], y, color=CORES[nome_estacao], alpha=0.3, linewidth=1)
        ax.plot(df['periodo'], tendencia, color=CORES[nome_estacao], 
                linewidth=2.5, label=f"{nome_estacao} (R²={r_value**2:.3f})", linestyle='--')
    
    ax.set_title('Análise de Tendência Linear - Comparação entre Estações', 
                 fontweight='bold', fontsize=13)
    ax.set_xlabel('Data')
    ax.set_ylabel('Precipitação (mm)')
    ax.legend(loc='best', framealpha=0.95)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(COMPARACAO_DIR / "05_tendencia_linear_comparacao.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfico: 05_tendencia_linear_comparacao.png")

def comparacao_coeficiente_variacao(dados):
    """Compara o coeficiente de variação (variabilidade relativa)."""
    cv_data = []
    
    for nome_estacao, df in dados.items():
        precip = df['precip_mm']
        media = precip.mean()
        desvio = precip.std()
        cv = (desvio / media) * 100  # CV em percentual
        cv_data.append({'Estação': nome_estacao, 'CV (%)': cv})
    
    df_cv = pd.DataFrame(cv_data)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    nomes = df_cv['Estação'].values
    cvs = df_cv['CV (%)'].values
    cores_lista = [CORES[nome] for nome in nomes]
    
    bars = ax.bar(nomes, cvs, color=cores_lista, edgecolor='black', linewidth=1.5, alpha=0.8)
    
    for bar, val in zip(bars, cvs):
        ax.text(bar.get_x() + bar.get_width()/2, val + 1, f'{val:.1f}%', 
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax.set_title('Coeficiente de Variação (Variabilidade Relativa)\nMaior CV = Maior variabilidade', 
                 fontweight='bold', fontsize=13)
    ax.set_ylabel('Coeficiente de Variação (%)')
    ax.set_ylim(0, max(cvs) + 10)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(COMPARACAO_DIR / "06_coeficiente_variacao_comparacao.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfico: 06_coeficiente_variacao_comparacao.png")
    
    df_cv.to_csv(COMPARACAO_DIR / "coeficiente_variacao.csv", index=False)

# ===============================
# EXECUÇÃO
# ===============================
if __name__ == "__main__":
    print("\n" + "="*70)
    print("📊 ANÁLISE COMPARATIVA - 4 ESTAÇÕES PLUVIOMÉTRICAS")
    print("="*70)
    
    print("\n📈 Carregando dados das séries mensais...")
    dados = carregar_series_mensais()
    
    if len(dados) < 4:
        print("⚠️  Apenas {} estações foram carregadas.".format(len(dados)))
        exit(1)
    
    print("\n📉 Gerando gráficos comparativos...")
    comparacao_series_temporais(dados)
    df_stats = comparacao_estatisticas(dados)
    comparacao_boxplot(dados)
    comparacao_climatologia_mensal(dados)
    comparacao_tendencia_linear(dados)
    comparacao_coeficiente_variacao(dados)
    
    print("\n" + "="*70)
    print("✅ COMPARAÇÃO CONCLUÍDA!")
    print("="*70)
    print("\n📁 Arquivo: output/graficos/Comparacao/")
    print("\n📊 Gráficos gerados:")
    print("   1. Series temporais comparativas")
    print("   2. Média de precipitação mensal")
    print("   3. Boxplot comparativo")
    print("   4. Climatologia mensal sazonal")
    print("   5. Tendência linear")
    print("   6. Coeficiente de variação")
    print("\n📋 Tabelas CSV:")
    print("   - estatisticas_descritivas.csv")
    print("   - coeficiente_variacao.csv")
    print("\n" + "="*70)
