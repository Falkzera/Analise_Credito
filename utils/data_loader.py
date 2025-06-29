
import pandas as pd
import numpy as np

def load_model_data():
    """Carrega dados dos modelos baseados no relatório"""
    
    # Dados de performance dos modelos
    model_performance = {
        'Modelo': ['Base (Sem Balanceamento)', 'LightGBM com SMOTE'],
        'AUC': [0.6753, 0.7163],
        'Accuracy': [0.92, 0.84],
        'Precision_Classe_1': [0.12, 0.08],
        'Recall_Classe_1': [0.22, 0.36],
        'Threshold': [0.9799, 0.0922]
    }
    
    return pd.DataFrame(model_performance)

def load_business_metrics():
    """Carrega métricas de negócio"""
    
    # KPIs principais baseados no relatório
    kpis = {
        'auc_atual': 0.7163,
        'melhoria_deteccao': 64,  # % melhoria no recall
        'roi_projetado': 740,  # % ROI primeiro ano
        'reducao_inadimplencia': 25  # % estimado
    }
    
    return kpis

def load_feature_importance():
    """Carrega importância das variáveis baseada no relatório"""
    
    features = {
        'Variable': [
            'riskassesment_940T',
            'avgpmtlast12m_4525200A', 
            'avgdbddpdlast24m_3658932P',
            'maininc_215A',
            'maxdpdlast24m_143P',
            'annuity_780A',
            'numactivecreds_622L',
            'currdebt_22A',
            'applications30d_658L',
            'education_1103M'
        ],
        'Importance': [0.85, 0.78, 0.72, 0.68, 0.65, 0.61, 0.58, 0.55, 0.51, 0.48],
        'Category': [
            'Score Externo',
            'Histórico Pagamento',
            'Histórico Pagamento', 
            'Capacidade Pagamento',
            'Histórico Pagamento',
            'Capacidade Pagamento',
            'Utilização Crédito',
            'Utilização Crédito',
            'Consultas Recentes',
            'Dados Demográficos'
        ],
        'Description': [
            'Score de risco externo',
            'Pagamento médio últimos 12 meses',
            'Média dias atraso últimos 24 meses',
            'Renda principal mensal',
            'Máximo dias atraso 24 meses',
            'Valor anuidade mensal',
            'Número créditos ativos',
            'Dívida atual total',
            'Aplicações últimos 30 dias',
            'Nível de escolaridade'
        ]
    }
    
    return pd.DataFrame(features)

def load_confusion_matrix_data():
    """Carrega dados da matriz de confusão"""
    
    # Simulando matriz de confusão baseada nas métricas do relatório
    # Para um dataset de teste de 4000 registros com 3.14% inadimplentes
    total_test = 4000
    inadimplentes = int(total_test * 0.0314)  # 126 inadimplentes
    adimplentes = total_test - inadimplentes  # 3874 adimplentes
    
    # Com recall de 36% e precision de 8%
    recall = 0.36
    precision = 0.08
    
    tp = int(inadimplentes * recall)  # 45 verdadeiros positivos
    fn = inadimplentes - tp  # 81 falsos negativos
    
    # Calculando com base na precision
    fp = int(tp / precision) - tp  # 517 falsos positivos
    tn = adimplentes - fp  # 3357 verdadeiros negativos
    
    confusion_matrix = np.array([
        [tn, fp],  # Linha 0: Adimplentes (classe 0)
        [fn, tp]   # Linha 1: Inadimplentes (classe 1)
    ])
    
    return confusion_matrix

def generate_sample_portfolio():
    """Gera amostra da carteira para análises"""
    
    np.random.seed(42)
    n_samples = 1000
    
    # Simulando distribuição de risco baseada no modelo
    risk_scores = np.random.beta(2, 8, n_samples)  # Distribuição beta para scores de risco
    
    # Categorizando risco
    risk_categories = []
    for score in risk_scores:
        if score < 0.1:
            risk_categories.append('Baixo Risco')
        elif score < 0.3:
            risk_categories.append('Médio Risco')
        else:
            risk_categories.append('Alto Risco')
    
    portfolio = pd.DataFrame({
        'risk_score': risk_scores,
        'risk_category': risk_categories,
        'loan_amount': np.random.normal(50000, 20000, n_samples),
        'monthly_income': np.random.normal(8000, 3000, n_samples),
        'age': np.random.randint(18, 70, n_samples)
    })
    
    return portfolio

def load_roi_scenarios():
    """Carrega cenários para análise de ROI"""
    
    scenarios = {
        'Conservative': {
            'volume_mensal': 10_000_000,
            'taxa_juros': 2.5,
            'taxa_inadimplencia_atual': 8.0,
            'reducao_inadimplencia': 15
        },
        'Moderate': {
            'volume_mensal': 25_000_000,
            'taxa_juros': 3.0,
            'taxa_inadimplencia_atual': 6.5,
            'reducao_inadimplencia': 25
        },
        'Aggressive': {
            'volume_mensal': 50_000_000,
            'taxa_juros': 3.5,
            'taxa_inadimplencia_atual': 5.0,
            'reducao_inadimplencia': 35
        }
    }
    
    return scenarios
