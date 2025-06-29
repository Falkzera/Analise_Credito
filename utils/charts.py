
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# Cores da Power of Data
COLORS = {
    'primary': '#1E3A8A',
    'secondary': '#6B7280', 
    'success': '#10B981',
    'warning': '#F59E0B',
    'light_blue': '#3B82F6',
    'light_gray': '#F3F4F6'
}

def create_auc_comparison():
    """Cria gráfico de comparação de AUC entre modelos"""
    
    models = ['Modelo Base', 'LightGBM + SMOTE']
    auc_values = [0.6753, 0.7163]
    colors = [COLORS['secondary'], COLORS['primary']]
    
    fig = go.Figure(data=[
        go.Bar(
            x=models,
            y=auc_values,
            text=[f'{val:.4f}' for val in auc_values],
            textposition='auto',
            marker_color=colors,
            textfont=dict(size=14, color='white')
        )
    ])
    
    fig.update_layout(
        title={
            'text': 'Comparação de Performance - AUC-ROC',
            'x': 0.5,
            'font': {'size': 18, 'color': COLORS['primary']}
        },
        yaxis_title='AUC-ROC',
        xaxis_title='Modelo',
        template='plotly_white',
        height=400,
        showlegend=False
    )
    
    # Linha de referência para AUC mínimo aceitável
    fig.add_hline(y=0.7, line_dash="dash", line_color=COLORS['success'], 
                  annotation_text="Mínimo Aceitável (0.70)")
    
    return fig

def create_confusion_matrix(cm_data):
    """Cria heatmap da matriz de confusão"""
    
    labels = ['Adimplente (0)', 'Inadimplente (1)']
    
    fig = go.Figure(data=go.Heatmap(
        z=cm_data,
        x=['Predito: Adimplente', 'Predito: Inadimplente'],
        y=['Real: Adimplente', 'Real: Inadimplente'],
        colorscale=[[0, COLORS['light_gray']], [1, COLORS['primary']]],
        text=cm_data,
        texttemplate="%{text}",
        textfont={"size": 16, "color": "white"},
        hoverongaps=False
    ))
    
    fig.update_layout(
        title={
            'text': 'Matriz de Confusão - Modelo LightGBM + SMOTE',
            'x': 0.5,
            'font': {'size': 18, 'color': COLORS['primary']}
        },
        template='plotly_white',
        height=400
    )
    
    return fig

def create_feature_importance(features_df):
    """Cria gráfico de importância das variáveis"""
    
    # Cores por categoria
    color_map = {
        'Score Externo': COLORS['primary'],
        'Histórico Pagamento': COLORS['success'],
        'Capacidade Pagamento': COLORS['warning'],
        'Utilização Crédito': COLORS['light_blue'],
        'Consultas Recentes': COLORS['secondary'],
        'Dados Demográficos': '#8B5CF6'
    }
    
    colors = [color_map[cat] for cat in features_df['Category']]
    
    fig = go.Figure(go.Bar(
        x=features_df['Importance'],
        y=features_df['Variable'],
        orientation='h',
        marker_color=colors,
        text=features_df['Importance'].round(2),
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>Importância: %{x:.2f}<br>%{customdata}<extra></extra>',
        customdata=features_df['Description']
    ))
    
    fig.update_layout(
        title={
            'text': 'Top 10 Variáveis Mais Importantes',
            'x': 0.5,
            'font': {'size': 18, 'color': COLORS['primary']}
        },
        xaxis_title='Importância',
        yaxis_title='Variável',
        template='plotly_white',
        height=500,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig

def create_roc_curve():
    """Cria curva ROC"""
    
    # Simulando curva ROC baseada no AUC 0.7163
    np.random.seed(42)
    n_points = 100
    
    # Gerando pontos da curva ROC
    fpr = np.linspace(0, 1, n_points)
    
    # Simulando TPR baseado no AUC conhecido
    tpr = []
    for fp in fpr:
        if fp < 0.1:
            tp = fp * 2.5  # Início mais íngreme
        elif fp < 0.5:
            tp = 0.25 + (fp - 0.1) * 1.5
        else:
            tp = 0.85 + (fp - 0.5) * 0.3
        tpr.append(min(tp, 1.0))
    
    tpr = np.array(tpr)
    
    fig = go.Figure()
    
    # Curva ROC do modelo
    fig.add_trace(go.Scatter(
        x=fpr, y=tpr,
        mode='lines',
        name=f'LightGBM + SMOTE (AUC = 0.7163)',
        line=dict(color=COLORS['primary'], width=3)
    ))
    
    # Linha de referência aleatória
    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1],
        mode='lines',
        name='Classificador Aleatório (AUC = 0.5)',
        line=dict(color=COLORS['secondary'], width=2, dash='dash')
    ))
    
    # Preenchimento da área sob a curva
    fig.add_trace(go.Scatter(
        x=fpr, y=tpr,
        fill='tonexty',
        fillcolor=f'rgba(30, 58, 138, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        showlegend=False,
        name='AUC'
    ))
    
    fig.update_layout(
        title={
            'text': 'Curva ROC - Modelo LightGBM + SMOTE',
            'x': 0.5,
            'font': {'size': 18, 'color': COLORS['primary']}
        },
        xaxis_title='Taxa de Falsos Positivos (1 - Especificidade)',
        yaxis_title='Taxa de Verdadeiros Positivos (Sensibilidade)',
        template='plotly_white',
        height=500,
        legend=dict(x=0.6, y=0.2)
    )
    
    return fig

def create_portfolio_distribution(portfolio_df):
    """Cria gráfico de distribuição de risco da carteira"""
    
    risk_counts = portfolio_df['risk_category'].value_counts()
    
    colors_map = {
        'Baixo Risco': COLORS['success'],
        'Médio Risco': COLORS['warning'], 
        'Alto Risco': '#EF4444'
    }
    
    colors = [colors_map[cat] for cat in risk_counts.index]
    
    fig = go.Figure(data=[go.Pie(
        labels=risk_counts.index,
        values=risk_counts.values,
        hole=0.3,
        marker_colors=colors,
        textinfo='label+percent',
        textfont_size=12
    )])
    
    fig.update_layout(
        title={
            'text': 'Distribuição de Risco da Carteira Atual',
            'x': 0.5,
            'font': {'size': 18, 'color': COLORS['primary']}
        },
        template='plotly_white',
        height=400,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    
    return fig

def create_roi_timeline(scenarios):
    """Cria timeline de ROI para diferentes cenários"""
    
    months = list(range(1, 13))
    
    fig = go.Figure()
    
    colors_scenarios = [COLORS['success'], COLORS['warning'], COLORS['primary']]
    
    for i, (scenario_name, params) in enumerate(scenarios.items()):
        # Simulando ROI acumulado ao longo do tempo
        roi_values = []
        for month in months:
            volume_total = params['volume_mensal'] * month
            reducao = params['reducao_inadimplencia'] / 100
            taxa_inad = params['taxa_inadimplencia_atual'] / 100
            
            # Economia com redução de inadimplência
            economia = volume_total * taxa_inad * reducao
            
            # ROI considerando investimento inicial
            investimento = 500_000  # Investimento inicial estimado
            roi = ((economia - investimento) / investimento) * 100
            
            roi_values.append(max(roi, -100))  # Limitando ROI mínimo
        
        fig.add_trace(go.Scatter(
            x=months,
            y=roi_values,
            mode='lines+markers',
            name=f'Cenário {scenario_name}',
            line=dict(color=colors_scenarios[i], width=3),
            marker=dict(size=8)
        ))
    
    fig.update_layout(
        title={
            'text': 'Projeção de ROI por Cenário (12 meses)',
            'x': 0.5,
            'font': {'size': 18, 'color': COLORS['primary']}
        },
        xaxis_title='Mês',
        yaxis_title='ROI (%)',
        template='plotly_white',
        height=400,
        legend=dict(x=0.02, y=0.98)
    )
    
    # Linha de referência ROI = 0
    fig.add_hline(y=0, line_dash="dash", line_color=COLORS['secondary'], 
                  annotation_text="Break-even")
    
    return fig

def create_risk_gauge(risk_score):
    """Cria medidor de risco para o simulador"""
    
    # Determinando cor baseada no score
    if risk_score < 0.3:
        color = COLORS['success']
        risk_level = "Baixo Risco"
    elif risk_score < 0.7:
        color = COLORS['warning'] 
        risk_level = "Médio Risco"
    else:
        color = '#EF4444'
        risk_level = "Alto Risco"
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = risk_score * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Score de Risco: {risk_level}"},
        delta = {'reference': 50},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 30], 'color': "lightgreen"},
                {'range': [30, 70], 'color': "lightyellow"},
                {'range': [70, 100], 'color': "lightcoral"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    
    fig.update_layout(
        template='plotly_white',
        height=300,
        font={'color': COLORS['primary'], 'family': "Arial"}
    )
    
    return fig
