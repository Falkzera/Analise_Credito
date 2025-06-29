
import streamlit as st
import pandas as pd
from utils.data_loader import load_model_data, load_confusion_matrix_data
from utils.charts import create_auc_comparison, create_confusion_matrix, create_roc_curve, COLORS
from utils.calculations import calculate_model_metrics, format_percentage


st.markdown('<h2 class="section-header">📊 Análise Detalhada de Modelos</h2>', 
            unsafe_allow_html=True)

# Carregando dados dos modelos
model_data = load_model_data()
cm_data = load_confusion_matrix_data()

# Comparação de AUC
st.markdown("### 🎯 Comparação de Performance - AUC")

col1, col2 = st.columns([2, 1])

with col1:
    fig_auc = create_auc_comparison()
    st.plotly_chart(fig_auc, use_container_width=True)

with col2:
    st.markdown("#### 📈 Interpretação")
    st.info("""
    **AUC-ROC indica a capacidade do modelo de distinguir entre classes:**
    
    - **0.5:** Aleatório
    - **0.7:** Bom (mínimo aceitável)
    - **0.8:** Muito bom
    - **0.9:** Excelente
    
    Nosso modelo alcançou **0.7163**, superando o mínimo aceitável.
    """)
    
    # Melhoria destacada
    melhoria = ((0.7163 - 0.6753) / 0.6753) * 100
    st.success(f"**Melhoria de {melhoria:.1f}%** no AUC em relação ao modelo base!")

st.markdown("---")

# Matriz de Confusão
st.markdown("### 🔍 Matriz de Confusão - Análise Detalhada")

col1, col2 = st.columns([2, 1])

with col1:
    fig_cm = create_confusion_matrix(cm_data)
    st.plotly_chart(fig_cm, use_container_width=True)

with col2:
    # Calculando métricas a partir da matriz
    tn, fp = cm_data[0]
    fn, tp = cm_data[1]
    
    metrics = calculate_model_metrics(tp, tn, fp, fn)
    
    st.markdown("#### 📊 Métricas Calculadas")
    
    # Métricas principais
    st.metric("Verdadeiros Positivos", tp, help="Inadimplentes corretamente identificados")
    st.metric("Falsos Negativos", fn, help="Inadimplentes perdidos pelo modelo")
    st.metric("Recall (Sensibilidade)", format_percentage(metrics['recall'] * 100), 
                help="% de inadimplentes corretamente identificados")
    st.metric("Especificidade", format_percentage(metrics['specificity'] * 100),
                help="% de adimplentes corretamente identificados")

# Interpretação da matriz
st.markdown("#### 💡 Interpretação de Negócio")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    **Pontos Fortes:**
    - ✅ **{tp} inadimplentes detectados** (36% recall)
    - ✅ **{tn} adimplentes aprovados** corretamente
    - ✅ **Especificidade de {metrics['specificity']:.1%}** (baixos falsos positivos para adimplentes)
    """)

with col2:
    st.markdown(f"""
    **Pontos de Atenção:**
    - ⚠️ **{fn} inadimplentes não detectados** (risco residual)
    - ⚠️ **{fp} adimplentes rejeitados** (oportunidade perdida)
    - ⚠️ **Precision de {metrics['precision']:.1%}** (muitos falsos positivos)
    """)

# Trade-off explicado
st.info("""
**📋 Trade-off do Modelo:**

O modelo foi otimizado para **maximizar a detecção de inadimplentes** (recall alto), 
mesmo ao custo de menor precision. Esta estratégia é adequada para minimizar perdas financeiras, 
pois é preferível rejeitar alguns clientes bons do que aprovar clientes ruins.

**Impacto Financeiro:** A melhoria de 64% no recall representa uma redução significativa 
nas perdas por inadimplência, justificando o trade-off.
""")

st.markdown("---")

# Curva ROC
st.markdown("### 📈 Curva ROC - Análise de Discriminação")

col1, col2 = st.columns([2, 1])

with col1:
    fig_roc = create_roc_curve()
    st.plotly_chart(fig_roc, use_container_width=True)

with col2:
    st.markdown("#### 🎯 Análise da Curva ROC")
    st.markdown("""
    **Como interpretar:**
    - **Eixo X:** Taxa de Falsos Positivos
    - **Eixo Y:** Taxa de Verdadeiros Positivos
    - **Diagonal:** Performance aleatória
    - **Área Destacada:** AUC = 0.7163
    
    **Nosso Modelo:**
    - Curva bem acima da diagonal
    - Boa capacidade de discriminação
    - Performance consistente em diferentes thresholds
    """)
    
    st.success("""
    **✅ Modelo Aprovado**
    
    AUC > 0.7 indica performance adequada para ambiente de produção.
    """)

st.markdown("---")

# Comparação detalhada entre modelos
st.markdown("### ⚖️ Comparação Detalhada Entre Modelos")

# Tabela comparativa
comparison_data = {
    'Métrica': ['AUC-ROC', 'Accuracy', 'Precision (Classe 1)', 'Recall (Classe 1)', 'Threshold'],
    'Modelo Base': ['0.6753', '92%', '12%', '22%', '0.9799'],
    'LightGBM + SMOTE': ['0.7163', '84%', '8%', '36%', '0.0922'],
    'Mudança': ['+6.1%', '-8.7%', '-33.3%', '+63.6%', '-90.6%']
}

comparison_df = pd.DataFrame(comparison_data)

# Estilizando a tabela
def highlight_improvements(val):
    if '+' in str(val) and 'Recall' in str(val) or '+' in str(val) and 'AUC' in str(val):
        return 'background-color: #10B981; color: white'
    elif '-' in str(val) and ('Precision' in str(val) or 'Accuracy' in str(val)):
        return 'background-color: #F59E0B; color: white'
    return ''

st.dataframe(comparison_df, use_container_width=True)

# Insights da comparação
st.markdown("#### 💭 Insights da Comparação")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **🟢 Melhorias Significativas:**
    - AUC +6.1% (maior discriminação)
    - Recall +63.6% (detecção superior)
    - Threshold mais realista
    """)

with col2:
    st.markdown("""
    **🟡 Trade-offs Aceitáveis:**
    - Accuracy -8.7% (esperado com SMOTE)
    - Precision -33.3% (compensado pelo recall)
    """)

with col3:
    st.markdown("""
    **🎯 Resultado Líquido:**
    - Modelo mais útil para negócio
    - Redução significativa de perdas
    - ROI positivo garantido
    """)

# Recomendações técnicas
with st.expander("🔧 Recomendações Técnicas para Melhorias Futuras"):
    st.markdown("""
    **Otimizações Recomendadas:**
    
    1. **Hyperparameter Tuning:**
        - Grid Search ou Bayesian Optimization
        - Ajuste fino dos parâmetros do LightGBM
        - Otimização do SMOTE ratio
    
    2. **Feature Engineering Avançado:**
        - Criação de ratios financeiros
        - Variáveis de tendência temporal
        - Interações entre variáveis importantes
    
    3. **Ensemble Methods:**
        - Combinação com XGBoost ou CatBoost
        - Voting classifier
        - Stacking para melhor performance
    
    4. **Validação Mais Robusta:**
        - Cross-validation estratificada
        - Validação temporal (time series split)
        - Teste em dados out-of-time
    
    5. **Monitoramento em Produção:**
        - Data drift detection
        - Performance monitoring
        - A/B testing framework
    """)

from utils.assets import custom_assets
custom_assets()

from utils.developer import rodape_desenvolvedor
rodape_desenvolvedor()