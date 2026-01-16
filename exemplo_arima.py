"""
EXEMPLO: Preparação de dados para ARIMA

Este script demonstra como usar os arquivos CSV exportados
para modelagem ARIMA. Execute após `python main.py`.

Requisitos adicionais:
    pip install statsmodels scikit-learn
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ==============================================================================
# 1. CARREGAR SÉRIE MENSAL
# ==============================================================================

pasta_dados = Path("output/graficos/campoalegre")
arquivo_csv = pasta_dados / "serie_temporal_mensal_arima_campoalegre.csv"

if not arquivo_csv.exists():
    print(f"❌ Arquivo não encontrado: {arquivo_csv}")
    print("   Execute primeiro: python main.py")
    exit(1)

print("📊 Carregando série temporal mensal...")
df = pd.read_csv(arquivo_csv)
df['periodo'] = pd.to_datetime(df['periodo'] + '-01')
df = df.sort_values('periodo')

print(f"   ✓ {len(df)} meses carregados ({df['periodo'].min().year}-{df['periodo'].max().year})")

# ==============================================================================
# 2. VISUALIZAR SÉRIE
# ==============================================================================

print("\n📈 Estatísticas da série:")
print(f"   Precipitação média: {df['precip_mm'].mean():.2f} mm")
print(f"   Desvio padrão: {df['precip_mm'].std():.2f} mm")
print(f"   Mínimo: {df['precip_mm'].min():.2f} mm")
print(f"   Máximo: {df['precip_mm'].max():.2f} mm")

# ==============================================================================
# 3. TESTE DE ESTACIONARIEDADE (ADF)
# ==============================================================================

try:
    from statsmodels.tsa.stattools import adfuller
    
    print("\n🔍 Teste de Estacionariedade (Augmented Dickey-Fuller)...")
    resultado_adf = adfuller(df['precip_mm'])
    
    print(f"   Estatística ADF: {resultado_adf[0]:.6f}")
    print(f"   p-value: {resultado_adf[1]:.6f}")
    
    if resultado_adf[1] < 0.05:
        print("   ✓ Série é ESTACIONÁRIA (p < 0.05)")
        d = 0
    else:
        print("   ✗ Série NÃO é estacionária")
        print("   → Usar d=1 ou d=2 em ARIMA(p,d,q)")
        d = 1
        
except ImportError:
    print("\n⚠️  Biblioteca statsmodels não instalada")
    print("   Execute: pip install statsmodels")
    d = 1

# ==============================================================================
# 4. ANÁLISE DE AUTOCORRELAÇÃO (ACF/PACF)
# ==============================================================================

try:
    from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
    
    print("\n📊 Analisando correlações...")
    
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    
    plot_acf(df['precip_mm'], lags=24, ax=axes[0])
    axes[0].set_title('Autocorrelação (ACF) - Série Mensal', fontweight='bold')
    axes[0].set_ylabel('ACF')
    
    plot_pacf(df['precip_mm'], lags=24, ax=axes[1], method='ywm')
    axes[1].set_title('Autocorrelação Parcial (PACF) - Série Mensal', fontweight='bold')
    axes[1].set_ylabel('PACF')
    
    plt.tight_layout()
    plt.savefig(pasta_dados / "acf_pacf.png", dpi=300, bbox_inches='tight')
    print("   ✓ Gráfico ACF/PACF salvo: acf_pacf.png")
    plt.close()
    
    print("\n   Interpretação:")
    print("   - ACF: Mostra relação entre observações distantes")
    print("   - PACF: Mostra relação direta entre observações")
    print("   - Use para escolher p (PACF) e q (ACF)")
    
except ImportError:
    print("\n⚠️  Biblioteca statsmodels não instalada")

# ==============================================================================
# 5. SUGESTÃO DE PARÂMETROS ARIMA
# ==============================================================================

print("\n💡 RECOMENDAÇÃO DE PARÂMETROS ARIMA:")
print(f"   Ordem sugerida: ARIMA(1,{d},1)")
print(f"   - p: Usar ACF para decidir (geralmente 1-2)")
print(f"   - d: {d} (diferenciação necessária para estacionariedade)")
print(f"   - q: Usar PACF para decidir (geralmente 1-2)")

# ==============================================================================
# 6. EXEMPLO DE AJUSTE ARIMA
# ==============================================================================

try:
    from statsmodels.tsa.arima.model import ARIMA
    
    print("\n⚙️  Ajustando ARIMA(1,1,1)...")
    
    modelo = ARIMA(df['precip_mm'], order=(1, d, 1))
    resultado = modelo.fit()
    
    print(resultado.summary())
    
    print("\n📊 Diagnostics:")
    print(f"   AIC: {resultado.aic:.2f}")
    print(f"   BIC: {resultado.bic:.2f}")
    
except ImportError:
    print("\n⚠️  Biblioteca statsmodels não instalada")
    print("   Para usar ARIMA: pip install statsmodels")

# ==============================================================================
# 7. VERIFICAÇÃO FINAL
# ==============================================================================

print("\n✅ SÉRIE PRONTA PARA MODELAGEM!")
print("\nProximas ações:")
print("   1. Instalar: pip install statsmodels")
print("   2. Explorar ACF/PACF para definir p,q")
print("   3. Ajustar ARIMA com diferentes ordens")
print("   4. Validar previsões com teste fora-da-amostra")
print("   5. Gerar previsões para 6-12 meses à frente")

print(f"\n📝 Arquivo CSV: {arquivo_csv.name}")
print(f"📦 Série: {df['periodo'].min().strftime('%Y-%m')} a {df['periodo'].max().strftime('%Y-%m')}")
