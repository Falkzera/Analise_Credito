
# 🚀  - Análise de Risco de Crédito  
[🔗 Acesse a aplicação online](https://case-credito.streamlit.app/)  
  
## 📊 Aplicação Streamlit Interativa  

Esta aplicação apresenta de forma interativa e dinâmica os resultados do modelo de análise de risco de crédito, utilizando LightGBM com SMOTE.

### 🎯 Principais Funcionalidades

#### 🏠 Dashboard Principal
- KPIs de performance em tempo real
- Distribuição de risco da carteira
- Comparação visual entre modelos
- Métricas de impacto de negócio

#### 📊 Análise de Modelos
- Comparação detalhada de AUC-ROC
- Matriz de confusão interativa
- Curva ROC com interpretação
- Métricas calculadas automaticamente

#### 📈 Análise de Variáveis
- Top 10 variáveis mais importantes
- Categorização por tipo de informação
- Insights de negócio por categoria
- Análise de correlações e missing values

#### 💰 Calculadora de ROI
- Cenários pré-definidos (Conservador, Moderado, Agressivo)
- Calculadora personalizada
- Timeline de retorno sobre investimento
- Análise de sensibilidade

#### 🔍 Simulador de Risco
- Análise individual de perfis de crédito
- Medidor visual de risco
- Recomendações personalizadas
- Comparação com outros perfis

### 🎨 Design e Identidade Visual


- **Interface Responsiva** com sidebar de navegação
- **Gráficos interativos** com Plotly
- **Layout profissional** e moderno

### 📈 Dados e Métricas

**Performance do Modelo:**
- AUC-ROC: 0.7163
- Melhoria de 64% na detecção de inadimplentes
- ROI projetado: 740% no primeiro ano
- Redução de inadimplência: 25%

**Especificações Técnicas:**
- Algoritmo: LightGBM com SMOTE
- Dataset: 20.000 registros, 54 features
- Threshold otimizado: 0.0922
- Validação: 80/20 (treino/teste)

### 🚀 Como Executar

1. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Executar aplicação:**
   ```bash
   streamlit run app.py
   ```

3. **Acessar no navegador:**
   ```
   http://localhost:8501
   ```

### 📁 Estrutura do Projeto

```
streamlit_credito_app/
├── app.py                 # Aplicação principal
├── assets/                # Imagens e recursos
│   └── logo.png          # Logo da Power of Data
├── pages/                 # Módulos das páginas
│   ├── dashboard.py      # Dashboard principal
│   ├── model_analysis.py # Análise de modelos
│   ├── variable_analysis.py # Análise de variáveis
│   ├── roi_calculator.py # Calculadora de ROI
│   └── risk_simulator.py # Simulador de risco
├── utils/                 # Utilitários
│   ├── data_loader.py    # Carregamento de dados
│   ├── charts.py         # Gráficos e visualizações
│   └── calculations.py   # Cálculos e métricas
├── data/                  # Dados e datasets
├── requirements.txt       # Dependências
└── README.md             # Documentação
```

### 🎯 Principais Insights

1. **Histórico de Pagamento** é o fator mais importante (85% de relevância)
2. **Capacidade de Pagamento** representa 25% da importância total
3. **Score Externo** tem 96.47% de valores ausentes - oportunidade de melhoria
4. **SMOTE** melhora significativamente a detecção de inadimplentes
5. **ROI positivo** em todos os cenários analisados