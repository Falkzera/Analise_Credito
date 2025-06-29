
import numpy as np
import pandas as pd

def calculate_roi(volume_mensal, taxa_juros, taxa_inadimplencia_atual, reducao_inadimplencia, 
                  investimento_inicial=500000, meses=12):
    """
    Calcula ROI baseado nos parâmetros de negócio
    
    Args:
        volume_mensal: Volume de empréstimos por mês em R$
        taxa_juros: Taxa de juros mensal em %
        taxa_inadimplencia_atual: Taxa de inadimplência atual em %
        reducao_inadimplencia: Redução esperada na inadimplência em %
        investimento_inicial: Custo de implementação do modelo
        meses: Período de análise em meses
    
    Returns:
        dict: Métricas de ROI calculadas
    """
    
    # Convertendo percentuais
    taxa_juros = taxa_juros / 100
    taxa_inad_atual = taxa_inadimplencia_atual / 100
    reducao = reducao_inadimplencia / 100
    
    # Cálculos mensais
    volume_total = volume_mensal * meses
    
    # Perdas atuais
    perdas_atuais = volume_total * taxa_inad_atual
    
    # Nova taxa de inadimplência com o modelo
    nova_taxa_inad = taxa_inad_atual * (1 - reducao)
    perdas_com_modelo = volume_total * nova_taxa_inad
    
    # Economia gerada
    economia_total = perdas_atuais - perdas_com_modelo
    
    # ROI
    roi_percentual = ((economia_total - investimento_inicial) / investimento_inicial) * 100
    
    # Payback em meses
    economia_mensal = economia_total / meses
    payback_meses = investimento_inicial / economia_mensal if economia_mensal > 0 else float('inf')
    
    return {
        'volume_total': volume_total,
        'perdas_atuais': perdas_atuais,
        'perdas_com_modelo': perdas_com_modelo,
        'economia_total': economia_total,
        'economia_mensal': economia_mensal,
        'roi_percentual': roi_percentual,
        'payback_meses': payback_meses,
        'nova_taxa_inadimplencia': nova_taxa_inad * 100
    }

def calculate_business_impact(modelo_atual_auc=0.6753, novo_modelo_auc=0.7163, 
                             carteira_valor=100_000_000):
    """
    Calcula impacto de negócio da melhoria do modelo
    
    Args:
        modelo_atual_auc: AUC do modelo atual
        novo_modelo_auc: AUC do novo modelo
        carteira_valor: Valor total da carteira em R$
    
    Returns:
        dict: Métricas de impacto
    """
    
    # Melhoria percentual no AUC
    melhoria_auc = ((novo_modelo_auc - modelo_atual_auc) / modelo_atual_auc) * 100
    
    # Assumindo que melhoria no AUC se traduz em redução proporcional de perdas
    # Esta é uma aproximação para fins de demonstração
    reducao_perdas_estimada = melhoria_auc * 0.4  # Fator de conversão conservador
    
    # Estimando perdas com inadimplência (assumindo 5% da carteira)
    taxa_inadimplencia_estimada = 0.05
    perdas_atuais = carteira_valor * taxa_inadimplencia_estimada
    
    # Economia estimada
    economia_estimada = perdas_atuais * (reducao_perdas_estimada / 100)
    
    return {
        'melhoria_auc_percentual': melhoria_auc,
        'reducao_perdas_estimada': reducao_perdas_estimada,
        'perdas_atuais_estimadas': perdas_atuais,
        'economia_estimada': economia_estimada,
        'valor_carteira': carteira_valor
    }

def simulate_credit_risk(idade, renda_mensal, valor_emprestimo, historico_credito, 
                        finalidade_emprestimo):
    """
    Simula análise de risco de crédito para um perfil individual
    
    Args:
        idade: Idade do solicitante
        renda_mensal: Renda mensal em R$
        valor_emprestimo: Valor solicitado em R$
        historico_credito: Histórico de crédito (Excelente, Bom, Regular, Ruim)
        finalidade_emprestimo: Finalidade do empréstimo
    
    Returns:
        dict: Resultado da análise
    """
    
    # Simulação de score baseada nas variáveis mais importantes do modelo real
    score = 0.5  # Score base
    
    # Ajuste por idade (curva U invertida)
    if 25 <= idade <= 55:
        score -= 0.1  # Idade ótima
    else:
        score += 0.05
    
    # Ajuste por renda
    if renda_mensal >= 10000:
        score -= 0.15
    elif renda_mensal >= 5000:
        score -= 0.05
    else:
        score += 0.1
    
    # Ajuste por histórico de crédito (variável mais importante)
    historico_map = {
        'Excelente': -0.2,
        'Bom': -0.1,
        'Regular': 0.05,
        'Ruim': 0.25
    }
    score += historico_map.get(historico_credito, 0)
    
    # Ajuste por relação empréstimo/renda
    relacao_emprestimo_renda = valor_emprestimo / (renda_mensal * 12)
    if relacao_emprestimo_renda > 5:
        score += 0.2
    elif relacao_emprestimo_renda > 3:
        score += 0.1
    elif relacao_emprestimo_renda < 1:
        score -= 0.05
    
    # Ajuste por finalidade
    finalidade_map = {
        'Compra de veículo': -0.02,
        'Reforma/construção': -0.01,
        'Consolidação de dívidas': 0.05,
        'Capital de giro': 0.03,
        'Outros': 0.02
    }
    score += finalidade_map.get(finalidade_emprestimo, 0)
    
    # Garantindo que score esteja entre 0 e 1
    score = max(0, min(1, score))
    
    # Determinando decisão com base no threshold otimizado (0.0922)
    threshold = 0.0922
    aprovado = score <= threshold
    
    # Classificação de risco
    if score <= 0.1:
        risco = "Baixo"
        cor_risco = "#10B981"
    elif score <= 0.3:
        risco = "Médio-Baixo"
        cor_risco = "#84CC16"
    elif score <= 0.5:
        risco = "Médio"
        cor_risco = "#F59E0B"
    elif score <= 0.7:
        risco = "Médio-Alto"
        cor_risco = "#EF4444"
    else:
        risco = "Alto"
        cor_risco = "#DC2626"
    
    return {
        'score': score,
        'aprovado': aprovado,
        'classificacao_risco': risco,
        'cor_risco': cor_risco,
        'confianca': min(95, 70 + (abs(score - threshold) * 100)),
        'motivo_principal': get_main_reason(idade, renda_mensal, valor_emprestimo, 
                                          historico_credito, relacao_emprestimo_renda)
    }

def get_main_reason(idade, renda_mensal, valor_emprestimo, historico_credito, relacao_emprestimo_renda):
    """Determina o principal motivo para a decisão"""
    
    reasons = []
    
    if historico_credito in ['Excelente', 'Bom']:
        reasons.append("Histórico de crédito positivo")
    elif historico_credito == 'Ruim':
        reasons.append("Histórico de crédito negativo")
    
    if renda_mensal >= 10000:
        reasons.append("Renda mensal elevada")
    elif renda_mensal < 3000:
        reasons.append("Renda mensal baixa")
    
    if relacao_emprestimo_renda > 5:
        reasons.append("Valor do empréstimo muito alto em relação à renda")
    elif relacao_emprestimo_renda < 1:
        reasons.append("Valor do empréstimo adequado à renda")
    
    if 25 <= idade <= 55:
        reasons.append("Faixa etária de menor risco")
    
    return reasons[0] if reasons else "Perfil geral do solicitante"

def format_currency(value):
    """Formata valor em moeda brasileira"""
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_percentage(value):
    """Formata porcentagem"""
    return f"{value:.1f}%"

def calculate_model_metrics(tp, tn, fp, fn):
    """
    Calcula métricas do modelo a partir da matriz de confusão
    
    Args:
        tp: Verdadeiros positivos
        tn: Verdadeiros negativos  
        fp: Falsos positivos
        fn: Falsos negativos
        
    Returns:
        dict: Métricas calculadas
    """
    
    total = tp + tn + fp + fn
    
    accuracy = (tp + tn) / total
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'specificity': specificity,
        'f1_score': f1_score,
        'true_positive_rate': recall,
        'false_positive_rate': 1 - specificity
    }
