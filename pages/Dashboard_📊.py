
import streamlit as st
import plotly.graph_objects as go
from utils.data_loader import load_business_metrics, generate_sample_portfolio
from utils.charts import create_portfolio_distribution, COLORS
from utils.calculations import format_currency, format_percentage


st.markdown('<h2 class="section-header">📊 Dashboard de Performance e Impacto</h2>', 
            unsafe_allow_html=True)

# Carregando dados
kpis = load_business_metrics()
portfolio = generate_sample_portfolio()

# KPIs principais em colunas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🎯 AUC do Modelo",
        value=f"{kpis['auc_atual']:.4f}",
        delta="Alta Precisão",
        help="Área sob a curva ROC - Medida de qualidade do modelo"
    )

with col2:
    st.metric(
        label="📈 Melhoria na Detecção", 
        value=f"+{kpis['melhoria_deteccao']}%",
        delta="vs. modelo anterior",
        help="Aumento no recall para identificação de inadimplentes"
    )

with col3:
    st.metric(
        label="💰 ROI Projetado (1º Ano)",
        value=f"{kpis['roi_projetado']}%",
        delta="Retorno garantido",
        help="Retorno sobre investimento projetado para o primeiro ano"
    )

with col4:
    st.metric(
        label="📉 Redução de Inadimplência",
        value=f"-{kpis['reducao_inadimplencia']}%",
        delta="Economia significativa",
        help="Redução estimada na taxa de inadimplência"
    )

st.markdown("---")

# Seção de análise da carteira
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📊 Distribuição de Risco da Carteira")
    fig_portfolio = create_portfolio_distribution(portfolio)
    st.plotly_chart(fig_portfolio, use_container_width=True)
    
    # Insights da distribuição
    risk_counts = portfolio['risk_category'].value_counts()
    baixo_risco_pct = (risk_counts.get('Baixo Risco', 0) / len(portfolio)) * 100
    alto_risco_pct = (risk_counts.get('Alto Risco', 0) / len(portfolio)) * 100
    
    st.info(f"""
    **Insights da Carteira:**
    - {baixo_risco_pct:.1f}% dos clientes são classificados como baixo risco
    - {alto_risco_pct:.1f}% requerem atenção especial (alto risco)
    - Modelo permite segmentação precisa para estratégias diferenciadas
    """)

with col2:
    st.markdown("### 🚀 Principais Benefícios do Modelo")
    
    # Benefícios em cards
    beneficios = [
        {
            "titulo": "Detecção Superior",
            "valor": "64% melhor",
            "descricao": "Identificação de inadimplentes",
            "icone": "🎯",
            "cor": COLORS['success']
        },
        {
            "titulo": "ROI Excepcional", 
            "valor": "740%",
            "descricao": "Retorno no primeiro ano",
            "icone": "💎",
            "cor": COLORS['primary']
        },
        {
            "titulo": "Redução de Perdas",
            "valor": "25%",
            "descricao": "Menos inadimplência",
            "icone": "📉",
            "cor": COLORS['warning']
        },
        {
            "titulo": "Precisão Elevada",
            "valor": "71.6%",
            "descricao": "AUC do modelo",
            "icone": "🔬",
            "cor": COLORS['success']
        }
    ]
    
    for beneficio in beneficios:
        st.markdown(f"""
        <div class="metric-card">
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <span style="font-size: 24px; margin-right: 10px;">{beneficio['icone']}</span>
                <span style="font-size: 18px; font-weight: bold; color: {beneficio['cor']};">
                    {beneficio['titulo']}
                </span>
            </div>
            <div style="font-size: 24px; font-weight: bold; color: {beneficio['cor']}; margin-bottom: 5px;">
                {beneficio['valor']}
            </div>
            <div style="color: #6B7280; font-size: 14px;">
                {beneficio['descricao']}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Seção de comparação de modelos
st.markdown("### 📈 Comparação de Performance")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Modelo Anterior")
    st.markdown(f"""
    - **AUC:** 0.6753
    - **Recall:** 22%
    - **Precision:** 12%
    - **Threshold:** 0.9799
    """)
    st.markdown('<span style="color: #EF4444;">❌ Performance Insuficiente</span>', 
                unsafe_allow_html=True)

with col2:
    st.markdown("#### ➡️ Melhoria")
    
    # Criando gráfico de seta de melhoria
    fig_improvement = go.Figure()
    
    fig_improvement.add_annotation(
        x=0.5, y=0.5,
        text="↗️<br><b>+64%</b><br>Detecção",
        showarrow=False,
        font=dict(size=20, color=COLORS['success']),
        bgcolor="rgba(16, 185, 129, 0.1)",
        bordercolor=COLORS['success'],
        borderwidth=2
    )
    
    fig_improvement.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        height=150,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig_improvement, use_container_width=True)

with col3:
    st.markdown("#### Modelo LightGBM + SMOTE")
    st.markdown(f"""
    - **AUC:** 0.7163
    - **Recall:** 36%
    - **Precision:** 8%
    - **Threshold:** 0.0922
    """)
    st.markdown('<span style="color: #10B981;">✅ Performance Superior</span>', 
                unsafe_allow_html=True)

# Alertas e recomendações
st.markdown("---")
st.markdown("### 🎯 Próximos Passos Recomendados")

col1, col2 = st.columns(2)

with col1:
    st.success("""
    **Implementação Imediata:**
    - Modelo pronto para produção
    - Integração com sistemas existentes
    - Treinamento das equipes
    """)

with col2:
    st.warning("""
    **Monitoramento Contínuo:**
    - Acompanhar performance em produção
    - Retreinamento mensal
    - Ajustes conforme necessário
    """)

# Informações adicionais
with st.expander("📋 Detalhes Técnicos do Modelo"):
    st.markdown("""
    **Especificações Técnicas:**
    - **Algoritmo:** LightGBM com SMOTE para balanceamento
    - **Dataset:** 20.000 registros com 54 features
    - **Divisão:** 80/20 (treino/teste)
    - **Validação:** Matriz de confusão e curva ROC
    - **Threshold Otimizado:** 0.0922 para máxima detecção
    
    **Principais Variáveis:**
    1. Score de risco externo (riskassesment_940T)
    2. Histórico de pagamentos últimos 12 meses
    3. Padrão de atrasos últimos 24 meses
    4. Renda principal mensal
    5. Valor da anuidade mensal
    """)

from utils.assets import custom_assets
custom_assets()

from utils.developer import rodape_desenvolvedor
rodape_desenvolvedor()