
import streamlit as st
import pandas as pd
from utils.data_loader import load_feature_importance
from utils.charts import create_feature_importance, COLORS


st.markdown('<h2 class="section-header">📈 Análise de Variáveis Importantes</h2>', 
            unsafe_allow_html=True)

# Carregando dados das features
features_df = load_feature_importance()

# Gráfico de importância
st.markdown("### 🎯 Top 10 Variáveis Mais Importantes")

col1, col2 = st.columns([3, 1])

with col1:
    fig_importance = create_feature_importance(features_df)
    st.plotly_chart(fig_importance, use_container_width=True)

with col2:
    st.markdown("#### 📊 Distribuição por Categoria")
    
    # Contagem por categoria
    category_counts = features_df['Category'].value_counts()
    
    for category, count in category_counts.items():
        percentage = (count / len(features_df)) * 100
        st.markdown(f"**{category}:** {count} ({percentage:.0f}%)")
    
    st.info("""
    **Insight Principal:**
    
    Histórico de Pagamento domina as variáveis mais importantes, confirmando que comportamento passado é o melhor preditor de risco futuro.
    """)

st.markdown("---")

# Análise detalhada por categoria
st.markdown("### 🔍 Análise Detalhada por Categoria")

# Histórico de Pagamento
with st.expander("💳 1. Histórico de Pagamento (Mais Importante)", expanded=True):
    hist_vars = features_df[features_df['Category'] == 'Histórico Pagamento']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Variáveis Identificadas:**")
        for _, row in hist_vars.iterrows():
            st.markdown(f"- **{row['Variable']}:** {row['Description']}")
    
    with col2:
        st.markdown("**💡 Insights de Negócio:**")
        st.markdown("""
        - Clientes com histórico de atrasos têm maior propensão à inadimplência
        - Padrão de pagamento recente (12 meses) é mais relevante
        - Máximo de dias em atraso é forte indicador de risco
        - Comportamento passado prediz comportamento futuro
        """)
    
    st.success("""
    **🎯 Recomendação Estratégica:**
    Investir em sistemas de monitoramento de pagamentos em tempo real para capturar mudanças no comportamento de risco dos clientes.
    """)

# Capacidade de Pagamento  
with st.expander("💰 2. Capacidade de Pagamento"):
    cap_vars = features_df[features_df['Category'] == 'Capacidade Pagamento']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Variáveis Identificadas:**")
        for _, row in cap_vars.iterrows():
            st.markdown(f"- **{row['Variable']}:** {row['Description']}")
    
    with col2:
        st.markdown("**💡 Insights de Negócio:**")
        st.markdown("""
        - Renda mensal é fundamental para análise de capacidade
        - Valor da anuidade deve ser proporcional à renda
        - Relação dívida/renda é indicador crítico
        - Estabilidade de renda impacta no risco
        """)
    
    st.info("""
    **📊 Oportunidade de Melhoria:**
    Implementar análise de estabilidade de renda e sazonalidade para refinamento do modelo.
    """)

# Utilização de Crédito
with st.expander("📊 3. Utilização de Crédito"):
    cred_vars = features_df[features_df['Category'] == 'Utilização Crédito']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Variáveis Identificadas:**")
        for _, row in cred_vars.iterrows():
            st.markdown(f"- **{row['Variable']}:** {row['Description']}")
    
    with col2:
        st.markdown("**💡 Insights de Negócio:**")
        st.markdown("""
        - Múltiplos créditos ativos aumentam o risco
        - Concentração de dívida é fator de atenção
        - Comportamento de utilização revela padrões
        - Endividamento total é limitador importante
        """)

# Score Externo
with st.expander("🎯 4. Score Externo"):
    score_vars = features_df[features_df['Category'] == 'Score Externo']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Variáveis Identificadas:**")
        for _, row in score_vars.iterrows():
            st.markdown(f"- **{row['Variable']}:** {row['Description']}")
    
    with col2:
        st.markdown("**💡 Insights de Negócio:**")
        st.markdown("""
        - Score externo tem maior importância individual
        - Combina múltiplas informações do bureau
        - Reduz dependência de dados internos
        - Melhora robustez das decisões
        """)
    
    st.warning("""
    **⚠️ Ponto de Atenção:**
    96.47% de valores ausentes nesta variável. Necessário melhorar integração com bureaus de crédito.
    """)

# Consultas Recentes
with st.expander("🔍 5. Consultas Recentes"):
    cons_vars = features_df[features_df['Category'] == 'Consultas Recentes']
    
    st.markdown("**💡 Insights de Negócio:**")
    st.markdown("""
    - Múltiplas consultas indicam desespero por crédito
    - Aplicações recentes são sinal de alerta
    - Comportamento de "shopping" de crédito
    - Correlação com deterioração financeira
    """)

# Dados Demográficos
with st.expander("👥 6. Dados Demográficos"):
    demo_vars = features_df[features_df['Category'] == 'Dados Demográficos']
    
    st.markdown("**💡 Insights de Negócio:**")
    st.markdown("""
    - Escolaridade impacta na gestão financeira
    - Perfil demográfico influencia risco
    - Variáveis de suporte para decisão
    - Menor poder preditivo individual
    """)

st.markdown("---")

# Correlações e Interações
st.markdown("### 🔗 Correlações e Interações Entre Variáveis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### ⚠️ Correlações Altas Identificadas")
    st.markdown("""
    **Variáveis com correlação > 0.8:**
    - `credamount_770A` vs `annuity_780A` (0.82)
    - Valor do crédito vs Anuidade mensal
    
    **Ação Tomada:**
    - Remoção de variáveis redundantes
    - Prevenção de multicolinearidade
    - Melhoria da estabilidade do modelo
    """)

with col2:
    st.markdown("#### 🔄 Interações Relevantes")
    st.markdown("""
    **Combinações com potencial:**
    - Renda × Valor do empréstimo
    - Histórico × Capacidade de pagamento
    - Score externo × Dados internos
    
    **Oportunidade:**
    - Feature engineering avançado
    - Criação de ratios financeiros
    - Variáveis de interação
    """)

# Matriz de importância por categoria
st.markdown("---")
st.markdown("### 📊 Importância Relativa por Categoria")

# Calculando importância média por categoria
category_importance = features_df.groupby('Category')['Importance'].agg(['mean', 'count', 'sum']).round(3)
category_importance.columns = ['Importância Média', 'Número de Variáveis', 'Importância Total']
category_importance = category_importance.sort_values('Importância Total', ascending=False)

# Exibindo tabela estilizada
st.dataframe(category_importance, use_container_width=True)

# Análise de missing values
st.markdown("---")
st.markdown("### ❓ Análise de Valores Ausentes")

missing_analysis = {
    'Variável': [
        'riskassesment_940T',
        'datelastunpaid_3546854D',
        'lastrepayingdate_696D',
        'applications30d_658L',
        'education_1103M'
    ],
    'Missing %': [96.47, 89.2, 87.1, 23.4, 15.6],
    'Impacto': [
        'Alto - Variável mais importante com muitos nulos',
        'Médio - Removida por excesso de nulos',
        'Médio - Removida por excesso de nulos', 
        'Baixo - Imputação adequada',
        'Baixo - Imputação adequada'
    ],
    'Ação': [
        'Melhorar integração com bureau',
        'Variável removida',
        'Variável removida',
        'Imputação por mediana',
        'Imputação por moda'
    ]
}

missing_df = pd.DataFrame(missing_analysis)
st.dataframe(missing_df, use_container_width=True)

# Recomendações finais
st.markdown("---")
st.markdown("### 🎯 Recomendações Estratégicas")

col1, col2 = st.columns(2)

with col1:
    st.success("""
    **💡 Melhorias Imediatas:**
    
    1. **Histórico de Pagamento:**
        - Implementar monitoramento em tempo real
        - Alertas automáticos para mudanças de padrão
    
    2. **Score Externo:**
        - Melhorar integração com bureaus
        - Reduzir valores ausentes
    
    3. **Capacidade de Pagamento:**
        - Validação de renda mais rigorosa
        - Análise de estabilidade temporal
    """)

with col2:
    st.info("""
    **🔮 Evoluções Futuras:**
    
    1. **Feature Engineering:**
        - Ratios financeiros avançados
        - Variáveis de tendência
        - Interações entre categorias
    
    2. **Dados Externos:**
        - Informações socioeconômicas
        - Dados de comportamento digital
        - Informações de open banking
    
    3. **Modelagem:**
        - Modelos ensemble
        - Deep learning para interações
        - Modelos específicos por segmento
    """)

# Impacto de negócio
with st.expander("💼 Impacto de Negócio das Variáveis"):
    st.markdown("""
    **Como as variáveis se traduzem em valor de negócio:**
    
    📈 **Histórico de Pagamento (40% da importância):**
    - Redução de 25% na inadimplência
    - Economia de R$ 2.5M anuais (hipotético para carteira de R$ 100M)
    
    💰 **Capacidade de Pagamento (25% da importância):**
    - Melhoria na aprovação de bons clientes
    - Aumento de 15% no volume de negócios
    
    🎯 **Score Externo (20% da importância):**
    - Decisões mais robustas
    - Redução de 30% no tempo de análise
    
    📊 **Outras Categorias (15% da importância):**
    - Refinamento da segmentação
    - Estratégias diferenciadas por perfil
    
    **ROI Total Estimado:** 740% no primeiro ano
    """)

from utils.assets import custom_assets
custom_assets()

from utils.developer import rodape_desenvolvedor
rodape_desenvolvedor()