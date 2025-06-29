
import streamlit as st
import pandas as pd
from utils.data_loader import load_roi_scenarios
from utils.charts import create_roi_timeline, COLORS
from utils.calculations import calculate_roi, format_currency, format_percentage


st.markdown('<h2 class="section-header">💰 Calculadora de ROI Interativa</h2>', 
            unsafe_allow_html=True)

# Cenários pré-definidos
scenarios = load_roi_scenarios()

# Seletor de cenário ou personalizado
st.markdown("### 🎯 Escolha o Cenário de Análise")

col1, col2 = st.columns([1, 2])

with col1:
    scenario_type = st.selectbox(
        "Tipo de Cenário:",
        ["Personalizado", "Conservador", "Moderado", "Agressivo"],
        help="Selecione um cenário pré-definido ou configure manualmente"
    )

with col2:
    if scenario_type != "Personalizado":
        scenario_map = {
            "Conservador": "Conservative",
            "Moderado": "Moderate", 
            "Agressivo": "Aggressive"
        }
        selected_scenario = scenarios[scenario_map[scenario_type]]
        
        st.info(f"""
        **Cenário {scenario_type} Selecionado:**
        - Volume Mensal: {format_currency(selected_scenario['volume_mensal'])}
        - Taxa de Juros: {selected_scenario['taxa_juros']}%
        - Taxa de Inadimplência Atual: {selected_scenario['taxa_inadimplencia_atual']}%
        - Redução Esperada: {selected_scenario['reducao_inadimplencia']}%
        """)

st.markdown("---")

# Formulário de entrada
st.markdown("### ⚙️ Configurações do Cálculo")

with st.form("roi_calculator"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if scenario_type == "Personalizado":
            volume_mensal = st.number_input(
                "Volume Mensal de Empréstimos (R$)",
                min_value=1_000_000,
                max_value=200_000_000,
                value=25_000_000,
                step=1_000_000,
                help="Volume total de empréstimos por mês"
            )
            
            taxa_juros = st.number_input(
                "Taxa de Juros Mensal (%)",
                min_value=0.5,
                max_value=10.0,
                value=3.0,
                step=0.1,
                help="Taxa de juros cobrada nos empréstimos"
            )
        else:
            selected = scenarios[scenario_map[scenario_type]]
            volume_mensal = selected['volume_mensal']
            taxa_juros = selected['taxa_juros']
            
            st.metric("Volume Mensal", format_currency(volume_mensal))
            st.metric("Taxa de Juros", f"{taxa_juros}%")
    
    with col2:
        if scenario_type == "Personalizado":
            taxa_inadimplencia = st.number_input(
                "Taxa de Inadimplência Atual (%)",
                min_value=1.0,
                max_value=20.0,
                value=6.5,
                step=0.1,
                help="Taxa atual de inadimplência da carteira"
            )
            
            reducao_inadimplencia = st.number_input(
                "Redução Esperada (%)",
                min_value=5.0,
                max_value=50.0,
                value=25.0,
                step=1.0,
                help="Redução percentual na inadimplência com o modelo"
            )
        else:
            taxa_inadimplencia = selected['taxa_inadimplencia_atual']
            reducao_inadimplencia = selected['reducao_inadimplencia']
            
            st.metric("Taxa Inadimplência Atual", f"{taxa_inadimplencia}%")
            st.metric("Redução Esperada", f"{reducao_inadimplencia}%")
    
    with col3:
        investimento_inicial = st.number_input(
            "Investimento Inicial (R$)",
            min_value=100_000,
            max_value=2_000_000,
            value=500_000,
            step=50_000,
            help="Custo de implementação do modelo"
        )
        
        periodo_analise = st.number_input(
            "Período de Análise (meses)",
            min_value=6,
            max_value=36,
            value=12,
            step=1,
            help="Período para cálculo do ROI"
        )
    
    # Botão de cálculo
    calcular = st.form_submit_button("🚀 Calcular ROI", use_container_width=True)

# Cálculos e resultados
if calcular:
    # Realizando cálculos
    resultado = calculate_roi(
        volume_mensal=volume_mensal,
        taxa_juros=taxa_juros,
        taxa_inadimplencia_atual=taxa_inadimplencia,
        reducao_inadimplencia=reducao_inadimplencia,
        investimento_inicial=investimento_inicial,
        meses=periodo_analise
    )
    
    st.markdown("---")
    st.markdown("### 📊 Resultados da Análise")
    
    # KPIs principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        roi_color = COLORS['success'] if resultado['roi_percentual'] > 0 else '#EF4444'
        st.metric(
            "ROI Total",
            f"{resultado['roi_percentual']:.1f}%",
            delta="Retorno sobre investimento",
            help=f"ROI em {periodo_analise} meses"
        )
    
    with col2:
        st.metric(
            "Economia Total",
            format_currency(resultado['economia_total']),
            delta="Redução de perdas",
            help="Economia total no período"
        )
    
    with col3:
        st.metric(
            "Economia Mensal",
            format_currency(resultado['economia_mensal']),
            delta="Fluxo de caixa",
            help="Economia média por mês"
        )
    
    with col4:
        payback_text = f"{resultado['payback_meses']:.1f} meses" if resultado['payback_meses'] < 100 else "N/A"
        st.metric(
            "Payback",
            payback_text,
            delta="Tempo de retorno",
            help="Tempo para recuperar o investimento"
        )
    
    # Detalhamento dos cálculos
    st.markdown("---")
    st.markdown("### 🔍 Detalhamento dos Cálculos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📈 Cenário Atual vs Novo Modelo")
        
        comparison_data = {
            'Métrica': [
                'Volume Total',
                'Taxa de Inadimplência',
                'Perdas Estimadas',
                'Investimento Modelo',
                'Resultado Líquido'
            ],
            'Cenário Atual': [
                format_currency(resultado['volume_total']),
                f"{taxa_inadimplencia}%",
                format_currency(resultado['perdas_atuais']),
                "R$ 0,00",
                format_currency(-resultado['perdas_atuais'])
            ],
            'Com Novo Modelo': [
                format_currency(resultado['volume_total']),
                f"{resultado['nova_taxa_inadimplencia']:.1f}%",
                format_currency(resultado['perdas_com_modelo']),
                format_currency(investimento_inicial),
                format_currency(resultado['economia_total'] - investimento_inicial)
            ]
        }
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("#### 💡 Análise de Sensibilidade")
        
        # Análise de sensibilidade simples
        scenarios_sensitivity = []
        for factor in [0.5, 0.75, 1.0, 1.25, 1.5]:
            roi_temp = calculate_roi(
                volume_mensal=volume_mensal,
                taxa_juros=taxa_juros,
                taxa_inadimplencia_atual=taxa_inadimplencia,
                reducao_inadimplencia=reducao_inadimplencia * factor,
                investimento_inicial=investimento_inicial,
                meses=periodo_analise
            )
            scenarios_sensitivity.append({
                'Cenário': f"{factor*100:.0f}% da redução",
                'ROI': f"{roi_temp['roi_percentual']:.1f}%"
            })
        
        sensitivity_df = pd.DataFrame(scenarios_sensitivity)
        st.dataframe(sensitivity_df, use_container_width=True, hide_index=True)
        
        st.info("""
        **💭 Análise de Sensibilidade:**
        Mostra como o ROI varia conforme diferentes níveis de eficácia do modelo.
        """)
    
    # Gráfico de timeline ROI
    st.markdown("---")
    st.markdown("### 📈 Evolução do ROI ao Longo do Tempo")
    
    # Criando dados para timeline
    timeline_scenarios = {
        'Atual': {
            'volume_mensal': volume_mensal,
            'taxa_juros': taxa_juros,
            'taxa_inadimplencia_atual': taxa_inadimplencia,
            'reducao_inadimplencia': reducao_inadimplencia
        }
    }
    
    fig_timeline = create_roi_timeline(timeline_scenarios)
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Insights e recomendações
    st.markdown("---")
    st.markdown("### 🎯 Insights e Recomendações")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if resultado['roi_percentual'] > 200:
            st.success(f"""
            **🚀 ROI Excepcional ({resultado['roi_percentual']:.1f}%)**
            
            - Implementação altamente recomendada
            - Payback em {resultado['payback_meses']:.1f} meses
            - Economia de {format_currency(resultado['economia_mensal'])} por mês
            - Projeto prioritário para execução
            """)
        elif resultado['roi_percentual'] > 50:
            st.info(f"""
            **✅ ROI Positivo ({resultado['roi_percentual']:.1f}%)**
            
            - Implementação recomendada
            - Retorno adequado sobre o investimento
            - Redução significativa de perdas
            - Monitorar performance em produção
            """)
        else:
            st.warning(f"""
            **⚠️ ROI Baixo ({resultado['roi_percentual']:.1f}%)**
            
            - Revisar premissas do cálculo
            - Considerar otimizações do modelo
            - Avaliar redução de custos de implementação
            - Analisar cenários alternativos
            """)
    
    with col2:
        st.markdown("#### 📋 Próximos Passos")
        
        if resultado['roi_percentual'] > 100:
            st.markdown("""
            **Implementação Imediata:**
            1. ✅ Aprovação executiva do projeto
            2. 🔧 Preparação da infraestrutura técnica
            3. 👥 Treinamento das equipes
            4. 📊 Implementação piloto (10% da carteira)
            5. 📈 Rollout completo em 3 meses
            """)
        else:
            st.markdown("""
            **Análise Adicional:**
            1. 🔍 Validação das premissas
            2. 📊 Análise de cenários alternativos
            3. 💰 Otimização de custos de implementação
            4. 🎯 Refinamento do modelo
            5. 📈 Reavaliação após melhorias
            """)
    
    # Exportar resultados
    st.markdown("---")
    
    # Dados para download
    export_data = {
        'Métrica': ['ROI Total (%)', 'Economia Total (R$)', 'Economia Mensal (R$)', 
                    'Payback (meses)', 'Nova Taxa Inadimplência (%)'],
        'Valor': [
            f"{resultado['roi_percentual']:.2f}",
            f"{resultado['economia_total']:.2f}",
            f"{resultado['economia_mensal']:.2f}",
            f"{resultado['payback_meses']:.2f}",
            f"{resultado['nova_taxa_inadimplencia']:.2f}"
        ]
    }
    
    export_df = pd.DataFrame(export_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv_data = export_df.to_csv(index=False)
        st.download_button(
            label="📥 Baixar Resultados (CSV)",
            data=csv_data,
            file_name=f"roi_analysis_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        st.info("""
        **💡 Dica:**
        Use os resultados exportados para apresentações executivas e documentação do projeto.
        """)

# Cenários de exemplo para demonstração

with st.expander("📋 Cenários de Referência"):
    st.markdown("""
    **Cenário Conservador:**
    - Instituição pequena/média
    - Volume: R$ 10M/mês
    - Taxa inadimplência: 8%
    - Redução esperada: 15%
    
    **Cenário Moderado:**
    - Instituição média/grande
    - Volume: R$ 25M/mês  
    - Taxa inadimplência: 6.5%
    - Redução esperada: 25%
    
    **Cenário Agressivo:**
    - Instituição grande
    - Volume: R$ 50M/mês
    - Taxa inadimplência: 5%
    - Redução esperada: 35%
    """)

from utils.assets import custom_assets
custom_assets()

from utils.developer import rodape_desenvolvedor
rodape_desenvolvedor()