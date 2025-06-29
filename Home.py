import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Power of Data - Análise de Risco de Crédito",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


import streamlit as st
import pandas as pd
from utils.charts import create_risk_gauge, COLORS
from utils.calculations import simulate_credit_risk, format_currency


st.markdown('<h2 class="section-header">🔍 Simulador de Risco de Crédito Individual</h2>', 
            unsafe_allow_html=True)

st.markdown("""
**Simule a análise de risco para diferentes perfis de clientes usando o Threshold obtido através da análise do Modelo.**  
Insira os dados do cliente e veja a classificação de risco em tempo real.
""")

st.markdown("---")

# Formulário de entrada de dados
st.markdown("### 📋 Dados do Cliente")

with st.form("risk_analysis_form"):
    # Informações pessoais
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 👤 Informações Pessoais")
        
        idade = st.number_input(
            "Idade",
            min_value=18,
            max_value=80,
            value=35,
            help="Idade do solicitante"
        )
        
        renda_mensal = st.number_input(
            "Renda Mensal (R$)",
            min_value=1000,
            max_value=50000,
            value=5000,
            step=100,
            help="Renda mensal comprovada"
        )
        
        historico_credito = st.selectbox(
            "Histórico de Crédito",
            ["Excelente", "Bom", "Regular", "Ruim"],
            index=1,
            help="Histórico de pagamentos e relacionamento com instituições financeiras"
        )
    
    with col2:
        st.markdown("#### 💰 Informações do Empréstimo")
        
        valor_emprestimo = st.number_input(
            "Valor do Empréstimo (R$)",
            min_value=1000,
            max_value=500000,
            value=25000,
            step=1000,
            help="Valor solicitado para o empréstimo"
        )
        
        finalidade_emprestimo = st.selectbox(
            "Finalidade do Empréstimo",
            [
                "Compra de veículo",
                "Reforma/construção", 
                "Consolidação de dívidas",
                "Capital de giro",
                "Outros"
            ],
            index=0,
            help="Principal finalidade do empréstimo"
        )
        
        # Calculando automaticamente a relação empréstimo/renda
        relacao_emprestimo_renda = valor_emprestimo / (renda_mensal * 12)
        
        st.metric(
            "Relação Empréstimo/Renda Anual",
            f"{relacao_emprestimo_renda:.1f}x",
            help="Quantas vezes a renda anual representa o valor do empréstimo"
        )
    
    # Botão de análise
    st.markdown("---")
    analisar = st.form_submit_button(
        "🔍 Analisar Risco",
        use_container_width=True,
        type="primary"
    )

# Resultados da análise
if analisar:
    # Executando simulação
    resultado = simulate_credit_risk(
        idade=idade,
        renda_mensal=renda_mensal,
        valor_emprestimo=valor_emprestimo,
        historico_credito=historico_credito,
        finalidade_emprestimo=finalidade_emprestimo
    )
    
    st.markdown("---")
    st.markdown("### 📊 Resultado da Análise")
    
    # Layout principal dos resultados
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Medidor de risco
        fig_gauge = create_risk_gauge(resultado['score'])
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        # Score numérico
        st.metric(
            "Score de Risco",
            f"{resultado['score']:.3f}",
            help="Score entre 0 (menor risco) e 1 (maior risco)"
        )
    
    with col2:
        # Decisão principal
        if resultado['aprovado']:
            st.success(f"""
            ### ✅ CRÉDITO APROVADO
            
            **Classificação:** {resultado['classificacao_risco']} Risco  
            **Confiança:** {resultado['confianca']:.0f}%  
            **Motivo Principal:** {resultado['motivo_principal']}
            """)
        else:
            st.error(f"""
            ### ❌ CRÉDITO NEGADO
            
            **Classificação:** {resultado['classificacao_risco']} Risco  
            **Confiança:** {resultado['confianca']:.0f}%  
            **Motivo Principal:** {resultado['motivo_principal']}
            """)
        
        # Informações adicionais
        st.info(f"""
        **Detalhes da Análise:**
        - Threshold do modelo: 0.0922
        - Score calculado: {resultado['score']:.4f}
        - Algoritmo: LightGBM com SMOTE
        """)
    
    st.markdown("---")
    
    # Análise detalhada dos fatores
    st.markdown("### 🔍 Análise Detalhada dos Fatores de Risco")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 👤 Perfil Demográfico")
        
        # Análise da idade
        if 25 <= idade <= 55:
            idade_status = "✅ Faixa etária de menor risco"
            idade_color = COLORS['success']
        else:
            idade_status = "⚠️ Faixa etária de maior atenção"
            idade_color = COLORS['warning']
        
        st.markdown(f"""
        **Idade:** {idade} anos  
        <span style="color: {idade_color};">{idade_status}</span>
        
        **Renda Mensal:** {format_currency(renda_mensal)}
        """, unsafe_allow_html=True)
        
        # Classificação da renda
        if renda_mensal >= 10000:
            renda_status = "✅ Renda elevada - fator protetor"
        elif renda_mensal >= 5000:
            renda_status = "✅ Renda adequada"
        else:
            renda_status = "⚠️ Renda baixa - maior atenção"
        
        st.markdown(renda_status)
    
    with col2:
        st.markdown("#### 💳 Histórico de Crédito")
        
        # Análise do histórico
        historico_analysis = {
            'Excelente': ('✅ Excelente histórico', COLORS['success'], 'Fator muito positivo'),
            'Bom': ('✅ Bom histórico', COLORS['success'], 'Fator positivo'),
            'Regular': ('⚠️ Histórico regular', COLORS['warning'], 'Requer atenção'),
            'Ruim': ('❌ Histórico negativo', '#EF4444', 'Fator de alto risco')
        }
        
        status, color, descricao = historico_analysis[historico_credito]
        
        st.markdown(f"""
        **Status:** <span style="color: {color};">{status}</span>  
        **Impacto:** {descricao}
        
        **Observação:** Histórico de pagamento é a variável mais importante do modelo (85% de importância).
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("#### 💰 Análise Financeira")
        
        st.markdown(f"""
        **Valor Solicitado:** {format_currency(valor_emprestimo)}  
        **Finalidade:** {finalidade_emprestimo}  
        **Relação Empréstimo/Renda:** {relacao_emprestimo_renda:.1f}x
        """)
        
        # Análise da relação empréstimo/renda
        if relacao_emprestimo_renda > 5:
            relacao_status = "❌ Muito alto - risco elevado"
            relacao_color = '#EF4444'
        elif relacao_emprestimo_renda > 3:
            relacao_status = "⚠️ Alto - requer atenção"
            relacao_color = COLORS['warning']
        elif relacao_emprestimo_renda < 1:
            relacao_status = "✅ Baixo - fator protetor"
            relacao_color = COLORS['success']
        else:
            relacao_status = "✅ Adequado"
            relacao_color = COLORS['success']
        
        st.markdown(f'<span style="color: {relacao_color};">{relacao_status}</span>', 
                    unsafe_allow_html=True)
    
    # Recomendações baseadas no resultado
    st.markdown("---")
    st.markdown("### 🎯 Recomendações")
    
    if resultado['aprovado']:
        col1, col2 = st.columns(2)
        
        with col1:
            st.success("""
            **✅ Recomendações para Aprovação:**
            
            1. **Prosseguir com aprovação** conforme análise
            2. **Monitorar** o comportamento de pagamento
            3. **Oferecer** produtos adicionais se apropriado
            4. **Revisar** periodicamente o perfil de risco
            """)
        
        with col2:
            st.info("""
            **📋 Condições Sugeridas:**
            
            - Taxa de juros padrão para o perfil
            - Prazo adequado à capacidade de pagamento  
            - Possibilidade de refinanciamento futuro
            - Acompanhamento mensal inicial
            """)
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.error("""
            **❌ Motivos para Negação:**
            
            1. **Score de risco** acima do threshold aceitável
            2. **Histórico de crédito** inadequado
            3. **Capacidade de pagamento** insuficiente
            4. **Relação empréstimo/renda** muito alta
            """)
        
        with col2:
            st.warning("""
            **🔄 Alternativas Possíveis:**
            
            - Reduzir o valor do empréstimo
            - Aguardar melhoria do histórico
            - Apresentar comprovante de renda adicional
            - Incluir avalista ou garantia real
            """)
    
    # Comparação com outros perfis
    st.markdown("---")
    st.markdown("### 📊 Comparação com Outros Perfis")
    
    # Gerando perfis de comparação
    perfis_comparacao = [
        {
            'nome': 'Perfil Baixo Risco',
            'idade': 40,
            'renda': 15000,
            'valor': 30000,
            'historico': 'Excelente',
            'finalidade': 'Compra de veículo'
        },
        {
            'nome': 'Perfil Médio Risco', 
            'idade': 28,
            'renda': 6000,
            'valor': 20000,
            'historico': 'Bom',
            'finalidade': 'Reforma/construção'
        },
        {
            'nome': 'Perfil Alto Risco',
            'idade': 22,
            'renda': 2500,
            'valor': 15000,
            'historico': 'Ruim',
            'finalidade': 'Consolidação de dívidas'
        }
    ]
    
    resultados_comparacao = []
    for perfil in perfis_comparacao:
        resultado_comp = simulate_credit_risk(
            idade=perfil['idade'],
            renda_mensal=perfil['renda'],
            valor_emprestimo=perfil['valor'],
            historico_credito=perfil['historico'],
            finalidade_emprestimo=perfil['finalidade']
        )
        resultados_comparacao.append({
            'Perfil': perfil['nome'],
            'Score': f"{resultado_comp['score']:.3f}",
            'Classificação': resultado_comp['classificacao_risco'],
            'Decisão': 'Aprovado' if resultado_comp['aprovado'] else 'Negado',
            'Renda': format_currency(perfil['renda']),
            'Valor': format_currency(perfil['valor'])
        })
    
    # Adicionando perfil atual
    resultados_comparacao.append({
        'Perfil': '👤 Seu Perfil',
        'Score': f"{resultado['score']:.3f}",
        'Classificação': resultado['classificacao_risco'],
        'Decisão': 'Aprovado' if resultado['aprovado'] else 'Negado',
        'Renda': format_currency(renda_mensal),
        'Valor': format_currency(valor_emprestimo)
    })
    
    df_comparacao = pd.DataFrame(resultados_comparacao)
    st.dataframe(df_comparacao, use_container_width=True, hide_index=True)
    
    # Observações finais
    with st.expander("ℹ️ Sobre o Modelo de Análise"):
        st.markdown("""
        **Threshold Obtido através da análise do Modelo- Especificações:**
        
        **Performance:**
        - AUC-ROC: 0.7163
        - Recall: 36% (detecção de inadimplentes)
        - Threshold otimizado: 0.0922
        
        **Variáveis Mais Importantes:**
        1. Histórico de crédito e pagamentos (85% importância)
        2. Capacidade de pagamento e renda (68% importância)  
        3. Relação empréstimo/renda (estimativa)
        4. Perfil demográfico (48% importância)
        
        **Limitações:**
        - Simulação baseada em variáveis limitadas
        - Modelo real utiliza 54 variáveis
        - Resultados para fins demonstrativos
        
        **Precisão:**
        - Modelo treinado com 20.000 registros
        - Validação em dataset de teste
        - Performance superior ao modelo base em 64%
        """)

from utils.assets import custom_assets
custom_assets()

from utils.developer import rodape_desenvolvedor
rodape_desenvolvedor()