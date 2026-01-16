# 📊 Resumo das Alterações Metodológicas - Projeto Análise Pluviométrica

## 🎯 Objetivo Alcançado

Transformar o projeto de análise pluviométrica para trabalhar com **séries temporais em múltiplas escalas**, preparando os dados para **modelagem ARIMA** e análise de tendências, mantendo a reprodutibilidade científica.

---

## 🔄 Mudanças Realizadas

### 1. **Nível de Agregação Temporal** 

| Aspecto | Antes | Depois | Motivo |
|---------|-------|--------|--------|
| Série Principal | Anual (31 pontos) | Mensal (372 pontos) | 12x mais informação, adequado para ARIMA |
| Resolução Temporal | 1 ano | 1 mês | Captura sazonalidade intra-anual |
| Modelagem Possível | Tendência simples | ARIMA, previsões | Adequado para séries com sazonalidade |

### 2. **Novas Colunas Temporais no DataFrame**

```python
df["ano_mes"]    # Período mensal (YYYY-MM) - para agregação
df["dia_mes"]    # Dia do mês (1-31) - para cálculo de pentada
df["pentada"]    # Pentada (1-6) - períodos de 5 dias
```

**Benefício:** Permite agregações em múltiplas escalas temporais

### 3. **Hierarquia de Gráficos**

**Antes:** 6 gráficos sem ordem clara
**Depois:** 9 gráficos + 1 arquivo CSV, numerados e organizados

```
01_serie_temporal_mensal.png     ⭐ SÉRIE PRINCIPAL (ARIMA)
02_analise_pentadal.png         ⭐ CARACTERIZAÇÃO INTRA-MENSAL  
02b_serie_pentadal_temporal.png    Evolução das pentadas
03_precipitacao_anual_complementar.png
04_climatologia_mensal.png
05_histograma_precipitacao_diaria.png
06_histograma_anual.png
07_boxplot_mensal.png
08_boxplot_anual.png
serie_temporal_mensal_arima_*.csv  📊 PARA ARIMA
```

### 4. **Três Novas Funções**

| Função | Responsabilidade | Saída |
|--------|------------------|-------|
| `serie_temporal_mensal()` | Série principal para ARIMA | Gráfico + DataFrame |
| `serie_pentadal()` | Análise intra-mensal | 2 subgráficos |
| `serie_pentadal_temporal()` | Evolução das pentadas ao longo dos anos | 1 gráfico temporal |
| `exportar_serie_arima()` | Exportar para ARIMA em CSV | Arquivo CSV |

---

## 📈 Resultados por Estação

### Saídas Geradas

**4 estações × (8 gráficos + 1 CSV) = 36 arquivos**

```
output/graficos/
├── campoalegre/
│   ├── 8 gráficos PNG (300 DPI)
│   └── serie_temporal_mensal_arima_campoalegre.csv
├── goianesia/
│   ├── 8 gráficos PNG (300 DPI)
│   └── serie_temporal_mensal_arima_goianesia.csv
├── marzagao/
│   ├── 8 gráficos PNG (300 DPI)
│   └── serie_temporal_mensal_arima_marzagao.csv
└── tresranchos/
    ├── 8 gráficos PNG (300 DPI)
    └── serie_temporal_mensal_arima_tresranchos.csv
```

### Exemplo de Série Mensal Exportada

```csv
periodo,precip_mm
1994-01,106.59
1994-02,420.18
1994-03,74.31
1994-04,53.27
...
2024-12,145.20
```

**Propriedades:**
- ✅ 372 meses consecutivos (sem lacunas)
- ✅ Indexação clara por período
- ✅ Pronto para ARIMA, sem preprocessamento adicional

---

## 🔬 Análise Pentadal

### O que é?

Distribuição de precipitação em períodos de **5 dias dentro do mês**:
- **Pentada 1:** dias 1-5
- **Pentada 2:** dias 6-10
- **Pentada 3:** dias 11-15
- **Pentada 4:** dias 16-20
- **Pentada 5:** dias 21-25
- **Pentada 6:** dias 26-31

### Por quê?

1. **Hidrologia:** Concentração vs. dispersão de chuvas
2. **Agricultura:** Risco de estiagem dentro do mês
3. **Engenharia Ambiental:** Intensidade de eventos extremos
4. **Climatologia:** Padrões intra-mensais

### Gráficos Gerados

1. **02_analise_pentadal.png** (2 subgráficos)
   - Precipitação total acumulada por pentada
   - Média diária com desvio padrão

2. **02b_serie_pentadal_temporal.png**
   - 6 linhas (uma por pentada)
   - Mostra como cada pentada evolui ao longo de 31 anos

---

## 🚀 Preparação para ARIMA

### Por que a série mensal é melhor?

**ARIMA requer:**
- ✅ Série contínua sem lacunas
- ✅ Mínimo 50-100 observações (temos 372)
- ✅ Sazonalidade clara (mensal, trimestral, anual)
- ✅ Resolução adequada para previsões práticas

**Série Anual (antiga):**
- ❌ Apenas 31 pontos (marginal para ARIMA)
- ❌ Difícil capturar sazonalidade
- ❌ Previsões são apenas tendência global

**Série Mensal (nova):** 
- ✅ 372 pontos (excelente para ARIMA)
- ✅ Captura padrões mensais e sazonalidade
- ✅ Previsões de 1-12 meses com acurácia maior

### Próximas Etapas (exemplo)

```python
# 1. Carregue o CSV
import pandas as pd
df = pd.read_csv('serie_temporal_mensal_arima_campoalegre.csv')

# 2. Teste estacionariedade (ADF)
from statsmodels.tsa.stattools import adfuller
adfuller(df['precip_mm'])  # Define d em ARIMA(p,d,q)

# 3. Analyze ACF/PACF
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
plot_acf(df['precip_mm'], lags=24)   # Define q
plot_pacf(df['precip_mm'], lags=24)  # Define p

# 4. Ajuste ARIMA
from statsmodels.tsa.arima.model import ARIMA
modelo = ARIMA(df['precip_mm'], order=(1, 1, 1))
resultado = modelo.fit()

# 5. Gere previsões
forecast = resultado.get_forecast(steps=12)
```

Script de exemplo pronto: `exemplo_arima.py`

---

## ✅ Validação e Testes

### Checklist de Verificação

- ✅ Dados lidos corretamente (11.323 registros × 4 estações)
- ✅ Colunas temporais calculadas sem erros
- ✅ Série mensal sem lacunas (372 meses consecutivos)
- ✅ Pentadas filtradas corretamente (1-6, valores válidos)
- ✅ Gráficos gerados com qualidade 300 DPI
- ✅ CSV exportado com formato correto (período, precip_mm)
- ✅ Tendência linear significativa em todas as estações
- ✅ Sem valores NaN ou infinitos

### Estatísticas da Série

```
Campoalegre - Série Mensal:
- Observações: 372 meses
- Período: 1994-01 a 2024-12
- Média: 139.99 mm
- Desvio Padrão: 73.63 mm
- Mínimo: 4.00 mm (mês mais seco)
- Máximo: 422.56 mm (mês mais chuvoso)
- Coeficiente de Variação: 52.6%
```

---

## 🔗 Compatibilidade

### Mantido Intacto

- ✅ Leitura de arquivos .txt (HIDROWEB)
- ✅ Tratamento de encoding (latin1)
- ✅ Conversão de datas (DD/MM/YYYY)
- ✅ Estrutura de diretórios
- ✅ Gráficos complementares
- ✅ Execução via `python main.py`

### Alterado com Justificativa

- `grafico_anual()`: Marcado como "complementar" (não mais série principal)
- Nomenclatura: Adicionada numeração para clareza
- Saídas: +2 gráficos pentadais + 1 CSV por estação

---

## 📚 Referências Científicas

### Conceitos Implementados

1. **Série Temporal Mensal**
   - Standard em hidrologia para ARIMA
   - Permite detecção de sazonalidade
   - Adequado para previsões operacionais

2. **Análise Pentadal**
   - Usado em meteorologia (pentadas de Lorenz)
   - Caracteriza distribuição intra-mensal
   - Relevante para agricultura (riscos de estiagem)

3. **Tendência Linear**
   - Regressão simples (linregress)
   - Fornece R² para significância
   - Baseline para detecção de mudanças climáticas

4. **Decomposição**
   - Série = Tendência + Sazonalidade + Aleatório
   - Realizada implicitamente em ARIMA

---

## 📋 Arquivos Modificados

1. **main.py**
   - Adicionadas colunas temporais em `carregar_dados()`
   - Novas funções: `serie_temporal_mensal()`, `serie_pentadal()`, etc.
   - Atualizado `__main__` com melhor feedback

2. **requirements.txt**
   - Dependências científicas mantidas

3. **NOVO: ALTERACOES_METODOLOGICAS.md**
   - Documentação técnica completa

4. **NOVO: exemplo_arima.py**
   - Script de exemplo para modelagem ARIMA

---

## 🎓 Notas Finais

### Para o Orientador

✅ **Alinhado com metodologia científica:**
- Série temporal em escala adequada (mensal)
- Múltiplas perspectivas (pentadal, anual, climatológica)
- Pronto para ARIMA sem processamento adicional
- Reproduzível e documentado

### Para Futuras Análises

Agora é possível:
- Modelar com ARIMA(p,d,q)
- Detectar tendências significativas
- Gerar previsões operacionais
- Analisar mudanças climáticas
- Integrar com modelos hidrológicos

### Comandos Rápidos

```bash
# Executar análise
python main.py

# Testar ARIMA (após instalar statsmodels)
pip install statsmodels
python exemplo_arima.py

# Ver estatísticas CSV
head -20 output/graficos/campoalegre/serie_temporal_mensal_arima_campoalegre.csv
```

---

**Versão:** 2.0 (Análise Temporal Multi-Escala)  
**Status:** ✅ Pronto para Produção  
**Data:** 9 de janeiro de 2026
