"""
Script de Predição GLM (Generalized Linear Model)

Modela a precipitação mensal usando GLM com diferentes distribuições:
- Gamma (mais adequado para precipitação)
- Gaussian (comparação)

Gera predições e visualizações para as 4 estações.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings

warnings.filterwarnings('ignore')

try:
    import statsmodels.api as sm
    from statsmodels.formula.api import glm
    from statsmodels.genmod.cov_struct import Exchangeable
    from statsmodels.genmod.generalized_estimating_equations import GEE
except ImportError:
    print("⚠️  Instalando statsmodels...")
    import subprocess
    subprocess.check_call(["/Users/joaovictorrochavilelagodoi/dados-pimenta/.venv/bin/python", "-m", "pip", "install", "statsmodels", "-q"])
    import statsmodels.api as sm
    from statsmodels.formula.api import glm

# ===============================
# CONFIGURAÇÕES
# ===============================
OUTPUT_DIR = Path("output/graficos")
GLM_DIR = OUTPUT_DIR / "GLM_Predicoes"
GLM_DIR.mkdir(parents=True, exist_ok=True)

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
    'font.family': 'Times New Roman',
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'lines.linewidth': 1.5,
})

# ===============================
# CARREGAMENTO E PREPARAÇÃO
# ===============================

def carregar_dados_estacao(pasta_estacao):
    """Carrega a série mensal de uma estação."""
    arquivo_csv = OUTPUT_DIR / pasta_estacao / f"serie_temporal_mensal_arima_{pasta_estacao}.csv"
    
    if arquivo_csv.exists():
        df = pd.read_csv(arquivo_csv)
        df['periodo'] = pd.to_datetime(df['periodo'] + '-01')
        df = df.sort_values('periodo').reset_index(drop=True)
        
        # Adicionar variáveis temporais
        df['ano'] = df['periodo'].dt.year
        df['mes'] = df['periodo'].dt.month
        df['trimestre'] = df['periodo'].dt.quarter
        df['t'] = np.arange(len(df))  # Índice de tempo
        df['precip_lag1'] = df['precip_mm'].shift(1)
        
        return df
    else:
        return None

def preparar_dados_glm(df):
    """Prepara dados removendo NaN da defasagem."""
    df_prep = df.dropna().reset_index(drop=True)
    return df_prep

# ===============================
# MODELOS GLM
# ===============================

def ajustar_modelo_glm(df, familia='gamma'):
    """Ajusta modelo GLM com distribuição especificada."""
    
    # Preparar dados
    df_prep = preparar_dados_glm(df)
    
    # Evitar valores zero/negativos para Gamma
    if familia == 'gamma':
        df_prep = df_prep[df_prep['precip_mm'] > 0].reset_index(drop=True)
    
    if len(df_prep) < 20:
        return None, None, None
    
    # Dividir em treino e teste (80/20)
    X = df_prep[['t', 'mes', 'precip_lag1']]
    y = df_prep['precip_mm']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Ajustar modelo GLM
    try:
        # Adicionar constante
        X_train_sm = sm.add_constant(X_train)
        X_test_sm = sm.add_constant(X_test)
        
        if familia == 'gamma':
            modelo = sm.GLM(y_train, X_train_sm, family=sm.families.Gamma()).fit()
        else:  # gaussian
            modelo = sm.GLM(y_train, X_train_sm, family=sm.families.Gaussian()).fit()
        
        # Fazer predições
        y_pred_train = modelo.predict(X_train_sm)
        y_pred_test = modelo.predict(X_test_sm)
        
        # Calcular métricas
        mae_train = mean_absolute_error(y_train, y_pred_train)
        mae_test = mean_absolute_error(y_test, y_pred_test)
        rmse_train = np.sqrt(mean_squared_error(y_train, y_pred_train))
        rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))
        r2_train = r2_score(y_train, y_pred_train)
        r2_test = r2_score(y_test, y_pred_test)
        
        metricas = {
            'mae_train': mae_train,
            'mae_test': mae_test,
            'rmse_train': rmse_train,
            'rmse_test': rmse_test,
            'r2_train': r2_train,
            'r2_test': r2_test
        }
        
        # Armazenar X_test_sm para uso posterior
        return modelo, (X_train_sm, X_test_sm, y_train, y_test), metricas
        
    except Exception as e:
        print(f"   ⚠️  Erro ao ajustar modelo: {str(e)}")
        return None, None, None

# ===============================
# VISUALIZAÇÕES
# ===============================

def plotar_predicao_vs_observado(modelo, dados, nome_estacao, cor, familia):
    """Plota predição vs observado."""
    X_train, X_test, y_train, y_test = dados
    
    y_pred_train = modelo.predict(X_train)
    y_pred_test = modelo.predict(X_test)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Gráfico 1: Treino
    ax1.scatter(y_train, y_pred_train, alpha=0.6, s=50, color=cor, edgecolors='black', linewidth=0.5)
    min_val = min(y_train.min(), y_pred_train.min())
    max_val = max(y_train.max(), y_pred_train.max())
    ax1.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfeito')
    ax1.set_xlabel('Precipitação Observada (mm)')
    ax1.set_ylabel('Precipitação Predita (mm)')
    ax1.set_title(f'Treino - {nome_estacao}\n(GLM {familia})', fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Gráfico 2: Teste
    ax2.scatter(y_test, y_pred_test, alpha=0.6, s=50, color=cor, edgecolors='black', linewidth=0.5)
    min_val = min(y_test.min(), y_pred_test.min())
    max_val = max(y_test.max(), y_pred_test.max())
    ax2.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfeito')
    ax2.set_xlabel('Precipitação Observada (mm)')
    ax2.set_ylabel('Precipitação Predita (mm)')
    ax2.set_title(f'Teste - {nome_estacao}\n(GLM {familia})', fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def plotar_series_com_predicao(df, modelo, nome_estacao, cor, familia):
    """Plota série temporal com predição sobreposta."""
    df_prep = preparar_dados_glm(df)
    
    if familia == 'gamma':
        df_prep = df_prep[df_prep['precip_mm'] > 0].reset_index(drop=True)
    
    X = df_prep[['t', 'mes', 'precip_lag1']]
    X_sm = sm.add_constant(X)
    y_pred = modelo.predict(X_sm)
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    ax.plot(df_prep.index, df_prep['precip_mm'], 'o-', label='Observado', 
            color=cor, alpha=0.6, linewidth=1.5, markersize=3)
    ax.plot(df_prep.index, y_pred, 's-', label='Predito (GLM)', 
            color='red', alpha=0.7, linewidth=2, markersize=2)
    
    ax.fill_between(df_prep.index, df_prep['precip_mm'], y_pred, alpha=0.2, color='gray')
    
    ax.set_xlabel('Mês')
    ax.set_ylabel('Precipitação (mm)')
    ax.set_title(f'Série Temporal com Predição GLM - {nome_estacao}\n(Distribuição: {familia})', 
                 fontweight='bold', fontsize=13)
    ax.legend(loc='best', framealpha=0.95)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def plotar_residuos(modelo, dados, nome_estacao, cor, familia):
    """Plota gráficos de diagnóstico dos resíduos."""
    X_train, X_test, y_train, y_test = dados
    
    y_pred = modelo.predict(X_test)
    residuos = y_test - y_pred
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Gráfico 1: Resíduos vs Predito
    axes[0, 0].scatter(y_pred, residuos, alpha=0.6, s=50, color=cor, edgecolors='black', linewidth=0.5)
    axes[0, 0].axhline(y=0, color='r', linestyle='--', lw=2)
    axes[0, 0].set_xlabel('Valores Preditos')
    axes[0, 0].set_ylabel('Resíduos')
    axes[0, 0].set_title('Resíduos vs Preditos')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Gráfico 2: Histograma de resíduos
    axes[0, 1].hist(residuos, bins=15, color=cor, edgecolor='black', alpha=0.7)
    axes[0, 1].set_xlabel('Resíduos')
    axes[0, 1].set_ylabel('Frequência')
    axes[0, 1].set_title('Distribuição dos Resíduos')
    axes[0, 1].grid(True, alpha=0.3, axis='y')
    
    # Gráfico 3: Q-Q plot
    from scipy import stats
    stats.probplot(residuos, dist="norm", plot=axes[1, 0])
    axes[1, 0].set_title('Q-Q Plot')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Gráfico 4: ACF dos resíduos
    from statsmodels.graphics.tsaplots import plot_acf
    plot_acf(residuos, lags=20, ax=axes[1, 1])
    axes[1, 1].set_title('Autocorrelação dos Resíduos')
    
    fig.suptitle(f'Diagnóstico de Resíduos - {nome_estacao} (GLM {familia})', 
                 fontweight='bold', fontsize=13, y=1.00)
    plt.tight_layout()
    return fig

# ===============================
# COMPARAÇÃO ENTRE MODELOS
# ===============================

def gerar_relatorio_metricas():
    """Gera relatório comparativo de métricas."""
    resultados = []
    
    for nome_estacao, pasta_estacao in ESTACOES.items():
        df = carregar_dados_estacao(pasta_estacao)
        if df is None:
            continue
        
        # Ajustar modelos
        for familia in ['gamma', 'gaussian']:
            modelo, dados, metricas = ajustar_modelo_glm(df, familia)
            if modelo is None or metricas is None:
                continue
            
            resultados.append({
                'Estação': nome_estacao,
                'Distribuição': familia.capitalize(),
                'MAE Treino': metricas['mae_train'],
                'MAE Teste': metricas['mae_test'],
                'RMSE Treino': metricas['rmse_train'],
                'RMSE Teste': metricas['rmse_test'],
                'R² Treino': metricas['r2_train'],
                'R² Teste': metricas['r2_test']
            })
    
    df_resultados = pd.DataFrame(resultados)
    df_resultados.to_csv(GLM_DIR / "metricas_glm.csv", index=False)
    return df_resultados

# ===============================
# EXECUÇÃO PRINCIPAL
# ===============================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🔬 MODELAGEM GLM - PREDIÇÃO DE PRECIPITAÇÃO")
    print("="*70)
    
    print("\n📊 Carregando dados e ajustando modelos...\n")
    
    for nome_estacao, pasta_estacao in ESTACOES.items():
        print(f"📈 {nome_estacao}")
        
        # Carregar dados
        df = carregar_dados_estacao(pasta_estacao)
        if df is None:
            print(f"   ✗ Dados não encontrados\n")
            continue
        
        cor = CORES[nome_estacao]
        pasta_estacao_glm = GLM_DIR / pasta_estacao
        pasta_estacao_glm.mkdir(parents=True, exist_ok=True)
        
        # Ajustar modelos (Gamma)
        print(f"   ► Ajustando GLM (Distribuição Gamma)...")
        modelo_gamma, dados_gamma, metricas_gamma = ajustar_modelo_glm(df, 'gamma')
        
        if modelo_gamma is not None:
            print(f"      R² Teste: {metricas_gamma['r2_test']:.3f} | RMSE: {metricas_gamma['rmse_test']:.2f}")
            
            # Gráficos
            fig1 = plotar_predicao_vs_observado(modelo_gamma, dados_gamma, nome_estacao, cor, 'Gamma')
            fig1.savefig(pasta_estacao_glm / "01_predicao_vs_observado_gamma.png", dpi=300, bbox_inches='tight')
            plt.close(fig1)
            
            fig2 = plotar_series_com_predicao(df, modelo_gamma, nome_estacao, cor, 'gamma')
            fig2.savefig(pasta_estacao_glm / "02_serie_temporal_predicao_gamma.png", dpi=300, bbox_inches='tight')
            plt.close(fig2)
            
            fig3 = plotar_residuos(modelo_gamma, dados_gamma, nome_estacao, cor, 'Gamma')
            fig3.savefig(pasta_estacao_glm / "03_diagnostico_residuos_gamma.png", dpi=300, bbox_inches='tight')
            plt.close(fig3)
            
            print(f"      ✓ 3 gráficos GLM Gamma salvos")
        else:
            print(f"      ✗ Erro ao ajustar modelo")
        
        # Ajustar modelos (Gaussian)
        print(f"   ► Ajustando GLM (Distribuição Gaussiana)...")
        modelo_gaussian, dados_gaussian, metricas_gaussian = ajustar_modelo_glm(df, 'gaussian')
        
        if modelo_gaussian is not None:
            print(f"      R² Teste: {metricas_gaussian['r2_test']:.3f} | RMSE: {metricas_gaussian['rmse_test']:.2f}")
            
            # Gráficos
            fig1 = plotar_predicao_vs_observado(modelo_gaussian, dados_gaussian, nome_estacao, cor, 'Gaussian')
            fig1.savefig(pasta_estacao_glm / "01_predicao_vs_observado_gaussian.png", dpi=300, bbox_inches='tight')
            plt.close(fig1)
            
            fig2 = plotar_series_com_predicao(df, modelo_gaussian, nome_estacao, cor, 'gaussian')
            fig2.savefig(pasta_estacao_glm / "02_serie_temporal_predicao_gaussian.png", dpi=300, bbox_inches='tight')
            plt.close(fig2)
            
            fig3 = plotar_residuos(modelo_gaussian, dados_gaussian, nome_estacao, cor, 'Gaussian')
            fig3.savefig(pasta_estacao_glm / "03_diagnostico_residuos_gaussian.png", dpi=300, bbox_inches='tight')
            plt.close(fig3)
            
            print(f"      ✓ 3 gráficos GLM Gaussian salvos")
        else:
            print(f"      ✗ Erro ao ajustar modelo")
        
        print()
    
    # Gerar relatório de métricas
    print("📋 Gerando relatório de métricas...")
    df_metricas = gerar_relatorio_metricas()
    print("✓ Relatório salvo: metricas_glm.csv\n")
    print(df_metricas.to_string(index=False))
    
    print("\n" + "="*70)
    print("✅ MODELAGEM GLM CONCLUÍDA!")
    print("="*70)
    print("\n📁 Arquivo: output/graficos/GLM_Predicoes/")
    print("\n📊 Arquivos gerados por estação:")
    print("   - 01_predicao_vs_observado_gamma.png")
    print("   - 02_serie_temporal_predicao_gamma.png")
    print("   - 03_diagnostico_residuos_gamma.png")
    print("   - 01_predicao_vs_observado_gaussian.png")
    print("   - 02_serie_temporal_predicao_gaussian.png")
    print("   - 03_diagnostico_residuos_gaussian.png")
    print("\n📋 Relatório: metricas_glm.csv")
    print("="*70 + "\n")
