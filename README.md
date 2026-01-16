# 📊 Análise Pluviométrica Integrada - Estações Meteorológicas Brasileiras

## 🎯 Resumo Executivo

Projeto completo de análise pluviométrica com processamento, visualização e modelagem preditiva de dados de precipitação de 4 estações meteorológicas brasileiras (1994-2024). Inclui **38 gráficos científicos** + **análise GLM** + **comparativas estatísticas**.

### Estações Analisadas:

| Estação | Estado | Período | Registros | Precipitação Média |
|---------|--------|---------|-----------|-------------------|
| **Goianésia** | GO | 1994-2024 | 11.323 dias | 122.94 mm/mês |
| **Campo Alegre de Goiás** | GO | 1994-2024 | 11.323 dias | 139.99 mm/mês |
| **Marzagão** | - | 1994-2024 | 11.323 dias | 119.81 mm/mês |
| **Três Ranchos** | - | 1994-2024 | 11.323 dias | 103.64 mm/mês |

**Série Histórica:** 31 anos (372 meses)

---

## 📁 Estrutura do Projeto

```
dados-pimenta/
├── 📄 main.py                      # Script principal: gera gráficos por estação
├── 📄 comparacao.py                # Análise comparativa entre 4 estações
├── 📄 glm_predicao.py              # Modelagem GLM com predições
├── 📄 requirements.txt             # Dependências Python
├── 📄 README.md                    # Este arquivo
│
├── data/                           # Dados brutos de entrada
│   ├── campoalegre33 (1).txt
│   ├── goianesia33 (1).txt
│   ├── marzagao33 (1).txt
│   └── tresranchos33 (1).txt
│
└── output/graficos/                # Saída: Gráficos e análises
    ├── campoalegre/                # 8 gráficos + 1 CSV
    ├── goianesia/                  # 8 gráficos + 1 CSV
    ├── marzagao/                   # 8 gráficos + 1 CSV
    ├── tresranchos/                # 8 gráficos + 1 CSV
    ├── Comparacao/                 # 6 gráficos comparativos + 2 CSV
    └── GLM_Predicoes/              # 24 gráficos GLM + 1 CSV
        ├── campoalegre/            # 6 gráficos por estação
        ├── goianesia/
        ├── marzagao/
        └── tresranchos/
```

---

## 🔍 Gráficos Gerados

### **Parte 1: Gráficos por Estação (8 por estação = 32 gráficos)**

#### Série Principal (Base ARIMA)
| # | Nome | Descrição | Análise |
|---|------|-----------|---------|
| **01** | `serie_temporal_mensal.png` | Série mensal com tendência linear e média histórica | Tendência de 31 anos, R², anomalias |

#### Análise Pentadal
| # | Nome | Descrição | Análise |
|---|------|-----------|---------|
| **02** | `analise_pentadal.png` | Precipitação em períodos de 5 dias | Distribuição intra-mensal (P1-P6) |
| **02b** | `serie_pentadal_temporal.png` | Evolução temporal das pentadas | Sazonalidade dos subperíodos |

#### Gráficos Complementares
| # | Nome | Descrição | Análise |
|---|------|-----------|---------|
| **03** | `precipitacao_anual_complementar.png` | Série anual com tendência | Variabilidade interanual |
| **04** | `climatologia_mensal.png` | Média mensal com desvio padrão | Padrão sazonal (Jan-Dez) |
| **05** | `histograma_precipitacao_diaria.png` | Distribuição de dias com chuva | Intensidade diária (n dias) |
| **06** | `histograma_anual.png` | Distribuição de totais anuais | Variabilidade entre anos |
| **07** | `boxplot_mensal.png` | Box plot por mês | Quartis, outliers, mediana |
| **08** | `boxplot_anual.png` | Box plot série completa | Resumo estatístico geral |

### **Parte 2: Gráficos Comparativos (6 gráficos)**

| # | Nome | Descrição | Análise |
|---|------|-----------|---------|
| **01** | `series_temporais_comparacao.png` | Sobreposição das 4 séries mensais | Padrões sincronizados/defasados |
| **02** | `media_precipitacao_comparacao.png` | Barras comparativas de médias | Ranking: Campo Alegre > Goianésia > Marzagão > Três Ranchos |
| **03** | `boxplot_comparacao.png` | Box plots lado a lado | Distribuições relativas |
| **04** | `climatologia_mensal_comparacao.png` | Linhas sobrepostas (Jan-Dez) | Sincronismo sazonal |
| **05** | `tendencia_linear_comparacao.png` | Linhas de tendência (1994-2024) | Taxas de variação (R²) |
| **06** | `coeficiente_variacao_comparacao.png` | Variabilidade relativa (CV%) | Estabilidade pluviométrica |

### **Parte 3: Gráficos GLM - Predição (24 gráficos)**

Por estação (6 gráficos) × 4 estações = 24 gráficos

#### Distribuição Gamma (adequada para precipitação)
| Gráfico | Descrição |
|---------|-----------|
| `01_predicao_vs_observado_gamma.png` | Scatter plot: Observado vs Predito (treino/teste) |
| `02_serie_temporal_predicao_gamma.png` | Série com overlay de predição |
| `03_diagnostico_residuos_gamma.png` | 4 gráficos: resíduos, histograma, Q-Q, ACF |

#### Distribuição Gaussiana (comparação)
| Gráfico | Descrição |
|---------|-----------|
| `01_predicao_vs_observado_gaussian.png` | Scatter plot: Observado vs Predito |
| `02_serie_temporal_predicao_gaussian.png` | Série com overlay de predição |
| `03_diagnostico_residuos_gaussian.png` | 4 gráficos: diagnósticos |

---

## 📊 Variáveis Analisadas

### Dados de Entrada
- **Precipitação diária (mm)** - Variável primária
- **Data de observação** - DD/MM/YYYY
- **Período: 1994-2024** - 31 anos

### Agregações e Transformações
```python
# Temporal
ano, mês, dia_mês, ano_mes, pentada (P1-P6)

# Estatísticas
precip_total, precip_media, precip_std, media_diaria, std_diaria

# Defasagens (para GLM)
precip_lag1 (precipitação mês anterior)

# Índices
t (tempo linear: 0-371), trimestre (1-4)
```

### Métricas Calculadas

**Descritivas:**
- Média mensal (mm)
- Mediana, Desvio Padrão
- Mínimo, Máximo
- Quartis (Q1, Q3)
- Coeficiente de Variação (CV%)

**Tendência:**
- Slope (inclinação linear)
- R² (coeficiente de determinação)
- Intercepto

**GLM:**
- MAE (Erro Médio Absoluto)
- RMSE (Raiz do Erro Quadrático Médio)
- R² (Coeficiente de correlação)

---

## 🚀 Como Executar

### Pré-requisitos
```bash
Python 3.8+
macOS/Linux/Windows
```

### Instalação

#### 1. Criar e ativar ambiente virtual
```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# ou
.venv\Scripts\activate  # Windows
```

#### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

#### 3. Executar análises

**Gráficos por estação:**
```bash
python main.py
```

**Gráficos comparativos:**
```bash
python comparacao.py
```

**Modelagem GLM (predição):**
```bash
python glm_predicao.py
```

**Executar tudo de uma vez:**
```bash
python main.py && python comparacao.py && python glm_predicao.py
```

---

## 📦 Dependências

| Pacote | Versão | Função |
|--------|--------|--------|
| pandas | ≥2.0.0 | Manipulação de DataFrames |
| numpy | ≥1.23.0 | Operações numéricas |
| matplotlib | ≥3.6.0 | Visualização gráfica |
| scipy | ≥1.9.0 | Estatística (linregress) |
| scikit-learn | ≥1.0.0 | Machine Learning (train_test_split, métricas) |
| statsmodels | ≥0.13.0 | GLM, diagnóstico de resíduos, ACF/PACF |

**Instalação rápida:**
```bash
pip install pandas numpy matplotlib scipy scikit-learn statsmodels
```

---

## 🔬 Metodologia

### 1. Processamento de Dados
- **Leitura:** Encoding Latin1 (HIDROWEB)
- **Parsing:** Automático de data DD/MM/YYYY
- **Validação:** Filtro de valores válidos (> 0)
- **Agregação:** Mensal (372 meses = 31 anos)

### 2. Análise Exploratória
- **Tendência:** Regressão linear OLS
- **Sazonalidade:** Médias por mês/pentada
- **Distribuição:** Histogramas e box plots
- **Variabilidade:** Desvio padrão, CV%

### 3. Modelagem Preditiva (GLM)
- **Distribuições:** Gamma (primária), Gaussian (comparação)
- **Variáveis:** Tempo (t), Mês, Lag-1 de precipitação
- **Divisão:** 80% treino, 20% teste
- **Métricas:** MAE, RMSE, R²
- **Diagnóstico:** Resíduos, ACF, Q-Q plot

### 4. Comparação Entre Estações
- **Sincronismo:** Correlação temporal
- **Magnitude:** Ranking de precipitação
- **Variabilidade:** Coeficiente de variação
- **Tendência:** Taxa de mudança (R²)

---

## 📈 Resultados Principais

### Estatísticas Descritivas (Média Mensal em mm)

```
Goianésia:                 122.94 mm  (Intermediária)
Campo Alegre de Goiás:     139.99 mm  ⭐ MAIOR
Marzagão:                  119.81 mm
Três Ranchos:              103.64 mm  ⭐ MENOR
```

### Coeficiente de Variação (Variabilidade Relativa)

Maior CV = Maior inconsistência pluviométrica

```
Exemplo: Se CV% = 50%, a precipitação varia bastante mês a mês
```

### Performance GLM - R² Teste

**Modelo Gaussian (melhor desempenho geral):**
```
Goianésia:            R² = 0.495  ✓ Bom
Marzagão:             R² = 0.336  ✓ Moderado
Três Ranchos:         R² = 0.337  ✓ Moderado
Campo Alegre de Goiás: R² = -0.003 ✗ Fraco
```

**Interpretação:** Modelo explica 49.5% da variância em Goianésia, mas apenas ~0% em Campo Alegre (precipitação muito aleatória)

---

## 🔍 Interpretação dos Gráficos

### Série Temporal Mensal
```
📌 Linha azul: Precipitação observada (mensal)
📌 Linha vermelha tracejada: Tendência linear
📌 Linha verde pontilhada: Média histórica (baseline)
```
**Leia:** Aumenta ou diminui precipitação? Há anomalias? Qual a variabilidade?

### Climatologia Mensal
```
📌 Pico em: Determina estação chuvosa
📌 Vale em: Determina estação seca
📌 Barras de erro: Variabilidade interanual por mês
```
**Leia:** Qual mês é mais chuvoso? Quanto varia?

### Box Plot
```
📌 Linha no meio: Mediana (50º percentil)
📌 Caixa: Intervalo interquartil (IQR = 25º-75º)
📌 Losango vermelho: Média
📌 Pontos: Outliers (extremos)
```
**Leia:** Qual é a distribuição? Há meses extremos?

### Tendência Linear
```
📌 R² próximo de 1.0: Forte tendência de longo prazo
📌 R² próximo de 0.0: Sem tendência clara
📌 Slope positivo: Aumento (chuvas maiores nos últimos anos)
📌 Slope negativo: Diminuição (secas mais frequentes)
```

### GLM Predição
```
📌 Pontos vermelhos próximos à linha diagonal: Boas predições
📌 Espalhamento: Incerteza do modelo
📌 Residuos normalizados: Validação das premissas
```

---

## 📋 Arquivos de Saída

### CSVs Gerados

1. **serie_temporal_mensal_arima_*.csv**
   - Colunas: periodo, precip_mm
   - Pronto para ARIMA, Prophet, etc.

2. **estatisticas_descritivas.csv**
   - Média, Mediana, StdDev, Min, Max, Q1, Q3
   - Comparativo entre 4 estações

3. **coeficiente_variacao.csv**
   - CV% por estação
   - Indicador de estabilidade pluviométrica

4. **metricas_glm.csv**
   - MAE, RMSE, R² para cada combinação
   - Distribuição Gamma vs Gaussian

---

## 🛠️ Troubleshooting

| Erro | Causa | Solução |
|------|-------|--------|
| `ModuleNotFoundError: pandas` | Dependências não instaladas | `pip install -r requirements.txt` |
| `FileNotFoundError: data/*.txt` | Arquivos de dados faltando | Verificar pasta `data/` |
| Gráficos vazios | Encoding incorreto no arquivo .txt | Converter para Latin1 |
| `ValueError: Invalid dtype` | Formato decimal incorreto | Usar vírgula (formato brasileiro) |
| GLM não converge | Dados incompletos/zero | Filtro de valores > 0 aplicado |

---

## 📚 Referências Técnicas

### Fórmulas Utilizadas

**Regressão Linear:**
$$y = \beta_0 + \beta_1 x + \epsilon$$
onde R² = 1 - (SS_{res} / SS_{tot})

**Coeficiente de Variação:**
$$CV = \frac{\sigma}{\mu} \times 100\%$$

**GLM (Generalized Linear Model):**
$$E(y) = g^{-1}(\beta_0 + \beta_1 x_1 + ... + \beta_p x_p)$$
com family = Gamma ou Gaussian

---

## ✅ Checklist de Execução

```
☑️ Dados carregados (4 estações × 11.323 registros)
☑️ Gráficos por estação (32 PNG @ 300 DPI)
☑️ Gráficos comparativos (6 PNG)
☑️ Modelos GLM (24 PNG + métricas)
☑️ CSVs exportados (5 arquivos)
☑️ Estatísticas calculadas (8 métricas × 4 estações)
☑️ Nomes de cidades corrigidos (português)
☑️ Documentação completa (este README)
```

**Total gerado:** 38 gráficos + 5 CSVs + Documentação

---

## 📝 Histórico de Alterações

| Data | Alteração |
|------|-----------|
| 15 Jan 2026 | ✅ Adicionado análise GLM (24 gráficos) |
| 15 Jan 2026 | ✅ Gráficos comparativos (6 gráficos) |
| 14 Jan 2026 | ✅ Nomes de cidades corrigidos |
| 14 Jan 2026 | ✅ Gráficos por estação (32 gráficos) |
| 14 Jan 2026 | ✅ Estrutura inicial do projeto |

---

## 👨‍💻 Detalhes Técnicos Avançados

### Configuração Matplotlib
```python
plt.style.use('seaborn-v0_8-darkgrid')
DPI: 300 (publicação científica)
Font: Sans-serif, 10pt
Cores: Paleta RdYlBu_r (colorblind-friendly)
```

### Validação de Dados
```python
# Remove zeros para Gamma
df_gamma = df[df['precip'] > 0]

# Remove NaN da defasagem
df_prep = df.dropna()

# Train/Test split: 80/20
X_train, X_test = train_test_split(..., test_size=0.2)
```

### Agregação Pentadal
```
P1: dias 1-5     (5 dias)
P2: dias 6-10    (5 dias)
P3: dias 11-15   (5 dias)
P4: dias 16-20   (5 dias)
P5: dias 21-25   (5 dias)
P6: dias 26-31   (6 dias - inclui 31º)
```

---

## 🎓 Uso em Pesquisa

Este projeto é adequado para:
- ✅ Artigos científicos em hidrologia
- ✅ Dissertações/Teses sobre clima regional
- ✅ Relatórios de órgãos ambientais
- ✅ Análise de mudanças climáticas
- ✅ Planejamento de recursos hídricos

**Cite como:**
> Análise Pluviométrica Integrada (2026). Estações meteorológicas brasileiras 1994-2024.

---

## 📞 Suporte

Para dúvidas sobre os gráficos, consulte:
- 📄 Documentação inline nos scripts (.py)
- 🔍 Comentários no código explicando cada função
- 📊 CSVs com valores numéricos brutos

---

**Status:** ✅ Pronto para Produção  
**Última Atualização:** 15 de janeiro de 2026  
**Versão:** 2.0 (com GLM e Comparação)
