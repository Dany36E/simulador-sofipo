# -*- coding: utf-8 -*-
"""
Simulador de Inversiones Multi-SOFIPO Interactivo
Desarrollado para analizar y comparar rendimientos de SOFIPOs mexicanas
Autor: Experto Fintech México
Fecha: Noviembre 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import base64

# Configuración de la página
st.set_page_config(
    page_title="Simulador Multi-SOFIPO México",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================================================
# FUNCIONES DE GUARDAR/CARGAR SIMULACIÓN
# ========================================================================

def guardar_simulacion():
    """Captura el estado actual de la simulación y retorna un diccionario"""
    simulacion = {
        "fecha_guardado": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "monto_total": st.session_state.get("monto_total_input", 50000),
        "periodo_simulacion": st.session_state.get("periodo_simulacion", 12),
        "preferencias": {
            "cumple_klar_plus": st.session_state.get("cumple_klar_plus", False),
            "cumple_mercadopago": st.session_state.get("cumple_mercadopago", False),
            "cumple_uala_plus": st.session_state.get("cumple_uala_plus", False),
            "usa_nu": st.session_state.get("usa_nu", True),
            "usa_didi": st.session_state.get("usa_didi", True),
            "usa_stori": st.session_state.get("usa_stori", True),
            "usa_klar": st.session_state.get("usa_klar", True),
            "usa_uala": st.session_state.get("usa_uala", True),
            "usa_mp": st.session_state.get("usa_mp", True),
            "usa_finsus": st.session_state.get("usa_finsus", True),
            "solo_vista": st.session_state.get("solo_vista", False)
        },
        "inversiones": {}
    }
    
    # Capturar inversiones manuales (checkboxes y montos)
    sofipos = ["Nu México", "DiDi", "Stori", "Klar", "Ualá", "Mercado Pago", "Finsus"]
    for sofipo in sofipos:
        check_key = f"check_{sofipo}"
        if st.session_state.get(check_key, False):
            prod_key = f"prod_{sofipo}"
            producto = st.session_state.get(prod_key, "")
            if producto:
                monto_key = f"monto_{sofipo}_{producto}"
                monto = st.session_state.get(monto_key, 0)
                simulacion["inversiones"][sofipo] = {
                    "producto": producto,
                    "monto": monto
                }
    
    return simulacion

def cargar_simulacion(simulacion_data):
    """Carga una simulación guardada al session_state"""
    try:
        # Cargar configuración básica
        st.session_state["monto_total_input"] = simulacion_data.get("monto_total", 50000)
        st.session_state["periodo_simulacion"] = simulacion_data.get("periodo_simulacion", 12)
        
        # Cargar preferencias
        preferencias = simulacion_data.get("preferencias", {})
        for key, value in preferencias.items():
            st.session_state[key] = value
        
        # Cargar inversiones
        inversiones = simulacion_data.get("inversiones", {})
        for sofipo, datos in inversiones.items():
            st.session_state[f"check_{sofipo}"] = True
            st.session_state[f"prod_{sofipo}"] = datos["producto"]
            st.session_state[f"monto_{sofipo}_{datos['producto']}"] = datos["monto"]
        
        return True
    except Exception as e:
        st.error(f"Error al cargar simulación: {str(e)}")
        return False

def exportar_json(simulacion):
    """Convierte la simulación a JSON para descarga"""
    json_str = json.dumps(simulacion, indent=2, ensure_ascii=False)
    b64 = base64.b64encode(json_str.encode()).decode()
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    return json_str, b64, fecha

# Estilos CSS personalizados - Diseño Premium
st.markdown("""
<style>
    /* Importar fuentes modernas */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@600;700;800&display=swap');
    
    /* Estilos globales */
    .main {
        background: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header principal - Fresh & Clean */
    .main-header {
        font-size: 3rem;
        font-family: 'Poppins', sans-serif;
        color: #1a1a2e;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #64748b;
        margin-bottom: 3rem;
        font-weight: 400;
    }
    
    /* Tarjetas de SOFIPO - Diseño Fresh y Minimalista */
    .sofipo-section {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        border: 1px solid #e8eaed;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        transition: all 0.3s ease;
        position: relative;
        overflow: visible;
    }
    
    .sofipo-section::before {
        content: '';
        position: absolute;
        top: -1px;
        left: -1px;
        right: -1px;
        bottom: -1px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        opacity: 0;
        z-index: -1;
        transition: opacity 0.3s ease;
    }
    
    .sofipo-section:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.12);
        border-color: transparent;
    }
    
    .sofipo-section:hover::before {
        opacity: 1;
    }
    
    /* Cajas de advertencia y éxito - Minimalista */
    .warning-box {
        background: #fef3c7;
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        border-left: 3px solid #f59e0b;
        margin: 1rem 0;
        color: #92400e;
        font-size: 0.95rem;
    }
    
    .success-box {
        background: #d1fae5;
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        border-left: 3px solid #10b981;
        margin: 1rem 0;
        color: #065f46;
        font-size: 0.95rem;
    }
    
    .info-box {
        background: #dbeafe;
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        border-left: 3px solid #3b82f6;
        margin: 1rem 0;
        color: #1e40af;
        font-size: 0.95rem;
    }
    
    /* Tarjetas de métricas - Fresh Design */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
        transition: all 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
    }
    
    /* Botones personalizados - Clean */
    .stButton>button {
        background: #667eea;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.7rem 1.8rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
    }
    
    .stButton>button:hover {
        background: #5568d3;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    /* Checkboxes mejorados */
    .stCheckbox {
        font-size: 1.1rem;
        font-weight: 500;
    }
    
    /* Inputs numéricos */
    .stNumberInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #e0e7ff;
        padding: 0.75rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stNumberInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Selectbox mejorado */
    .stSelectbox>div>div {
        border-radius: 10px;
        border: 2px solid #e0e7ff;
    }
    
    /* Dataframe personalizado */
    .dataframe {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    
    /* Sidebar mejorado */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Animaciones sutiles */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Badge moderno */
    .badge {
        display: inline-block;
        padding: 0.35rem 0.8rem;
        font-size: 0.875rem;
        font-weight: 600;
        border-radius: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin: 0.25rem;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
    }
    
    /* Separador estilizado */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 2rem 0;
    }
    
    /* Tabs personalizados */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f8f9ff;
        padding: 0.5rem;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Expander mejorado */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8f9ff 0%, #e8eeff 100%);
        border-radius: 10px;
        font-weight: 600;
        padding: 1rem;
    }
    
    /* Tooltip personalizado */
    .tooltip {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted #667eea;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATOS DE LAS SOFIPOS (Tasas actualizadas a Noviembre 2025)
# ============================================================================

SOFIPOS_DATA = {
    "Nu México": {
        "logo": "🟣",
        "productos": {
            "Cajita Turbo": {
                "tasa_base": 15.00,
                "liquidez": "Inmediata",
                "minimo": 0,
                "tipo": "vista",
                "limite_max": 25000,
                "descripcion_extra": "Hasta $25,000 MXN"
            },
            "Dinero en Cajita (disponible)": {
                "tasa_base": 7.50,
                "liquidez": "Inmediata",
                "minimo": 0,
                "tipo": "vista"
            },
            "Plazo Fijo 7 días": {
                "tasa_base": 7.55,
                "liquidez": "7 días",
                "minimo": 100,
                "tipo": "plazo",
                "plazo_dias": 7
            },
            "Plazo Fijo 28 días": {
                "tasa_base": 7.60,
                "liquidez": "28 días",
                "minimo": 100,
                "tipo": "plazo",
                "plazo_dias": 28
            },
            "Plazo Fijo 90 días": {
                "tasa_base": 7.70,
                "liquidez": "90 días",
                "minimo": 100,
                "tipo": "plazo",
                "plazo_dias": 90
            },
            "Plazo Fijo 180 días": {
                "tasa_base": 7.80,
                "liquidez": "180 días",
                "minimo": 100,
                "tipo": "plazo",
                "plazo_dias": 180
            }
        },
        "color": "#8A05BE",
        "descripcion": "SOFIPO líder en México con 13+ millones de clientes"
    },
    "DiDi": {
        "logo": "🧡",
        "productos": {
            "DiDi Ahorro": {
                "tasa_base": 8.50,
                "tasa_premium": 16.00,
                "limite_premium": 10000,
                "liquidez": "Inmediata",
                "minimo": 0,
                "tipo": "vista_hibrida"
            }
        },
        "color": "#FF6600",
        "descripcion": "Hasta 16% en primeros $10,000, después 8.5%"
    },
    "Stori": {
        "logo": "💙",
        "productos": {
            "Sin plazo": {
                "tasa_base": 8.00,
                "liquidez": "Inmediata",
                "minimo": 0,
                "tipo": "vista",
                "plazo_dias": 0
            },
            "30 días": {
                "tasa_base": 8.05,
                "liquidez": "30 días",
                "minimo": 0,
                "tipo": "plazo",
                "plazo_dias": 30
            },
            "90 días": {
                "tasa_base": 10.00,
                "liquidez": "90 días",
                "minimo": 0,
                "tipo": "plazo",
                "plazo_dias": 90
            },
            "180 días": {
                "tasa_base": 7.50,
                "liquidez": "180 días",
                "minimo": 0,
                "tipo": "plazo",
                "plazo_dias": 180
            },
            "360 días": {
                "tasa_base": 7.00,
                "liquidez": "360 días",
                "minimo": 0,
                "tipo": "plazo",
                "plazo_dias": 360
            }
        },
        "color": "#0066FF",
        "descripcion": "Inversiones con y sin plazo (requiere cuenta Stori)"
    },
    "Klar": {
        "logo": "💚",
        "productos": {
            "Cuenta Klar": {
                "tasa_base": 8.50,
                "liquidez": "Inmediata",
                "minimo": 100,
                "tipo": "vista"
            },
            "Inversión Flexible Max": {
                "tasa_base": 15.00,
                "liquidez": "Inmediata",
                "minimo": 100,
                "tipo": "vista",
                "requisito": "Plus o Platino",
                "descripcion_extra": "Requiere membresía Plus o Platino"
            }
        },
        "color": "#00D98C",
        "descripcion": "SOFIPO regulada por CNBV con más de 2M usuarios"
    },
    "Ualá": {
        "logo": "💳",
        "productos": {
            "Cuenta con Rendimiento (Base)": {
                "tasa_base": 7.75,
                "liquidez": "Inmediata",
                "minimo": 0,
                "tipo": "vista",
                "limite_max": 30000,
                "descripcion_extra": "7.75% hasta $30,000"
            },
            "Cuenta con Rendimiento Plus": {
                "tasa_base": 16.00,
                "liquidez": "Inmediata",
                "minimo": 0,
                "tipo": "vista",
                "limite_max": 50000,
                "requisito": "Plus",
                "requisito_deposito": 3000,
                "descripcion_extra": "16% hasta $50k (requiere $3k/mes en consumos o nómina)"
            },
            "Reserva 7 días": {
                "tasa_base": 7.80,
                "liquidez": "7 días",
                "minimo": 0,
                "tipo": "plazo",
                "plazo_dias": 7
            },
            "Reserva 14 días": {
                "tasa_base": 7.85,
                "liquidez": "14 días",
                "minimo": 0,
                "tipo": "plazo",
                "plazo_dias": 14
            },
            "Reserva 28 días": {
                "tasa_base": 7.90,
                "liquidez": "28 días",
                "minimo": 0,
                "tipo": "plazo",
                "plazo_dias": 28
            },
            "Reserva 90 días": {
                "tasa_base": 8.00,
                "liquidez": "90 días",
                "minimo": 0,
                "tipo": "plazo",
                "plazo_dias": 90
            },
            "Reserva 180 días": {
                "tasa_base": 8.10,
                "liquidez": "180 días",
                "minimo": 0,
                "tipo": "plazo",
                "plazo_dias": 180
            },
            "Reserva 1 año": {
                "tasa_base": 8.15,
                "liquidez": "365 días",
                "minimo": 0,
                "tipo": "plazo",
                "plazo_dias": 365
            }
        },
        "color": "#00D4FF",
        "descripcion": "Hasta 16% con Tasa Plus (requiere $3k/mes en consumos/nómina)"
    },
    "Mercado Pago": {
        "logo": "💵",
        "productos": {
            "Rendimientos MP": {
                "tasa_base": 13.00,
                "liquidez": "Inmediata",
                "minimo": 3000,
                "tipo": "vista",
                "limite_max": 25000,
                "requisito_deposito": 3000,
                "descripcion_extra": "Requiere depositar $3,000/mes, máximo $25,000"
            }
        },
        "color": "#00AAFF",
        "descripcion": "13% anual (requiere $3k/mes, máx $25k)"
    },
    "Finsus": {
        "logo": "🏦",
        "productos": {
            "Finsus+ (a la vista)": {
                "tasa_base": 8.09,
                "liquidez": "Inmediata",
                "minimo": 0,
                "tipo": "vista"
            },
            "Apartados": {
                "tasa_base": 4.00,
                "liquidez": "Inmediata",
                "minimo": 0,
                "tipo": "vista",
                "descripcion_extra": "Ideal para metas de ahorro"
            },
            "Plazo Fijo 7 días": {
                "tasa_base": 8.00,
                "liquidez": "7 días",
                "minimo": 0,
                "tipo": "plazo",
                "plazo_dias": 7
            },
            "Plazo Fijo 30 días": {
                "tasa_base": 8.09,
                "liquidez": "30 días",
                "minimo": 0,
                "tipo": "plazo",
                "plazo_dias": 30
            },
            "Plazo Fijo 90 días": {
                "tasa_base": 8.39,
                "liquidez": "90 días",
                "minimo": 0,
                "tipo": "plazo",
                "plazo_dias": 90
            },
            "Plazo Fijo 180 días": {
                "tasa_base": 8.59,
                "liquidez": "180 días",
                "minimo": 0,
                "tipo": "plazo",
                "plazo_dias": 180
            },
            "Plazo Fijo 360 días": {
                "tasa_base": 10.09,
                "liquidez": "360 días",
                "minimo": 0,
                "tipo": "plazo",
                "plazo_dias": 360
            },
            "Plazo Fijo 720 días": {
                "tasa_base": 8.19,
                "liquidez": "720 días",
                "minimo": 0,
                "tipo": "plazo",
                "plazo_dias": 720
            },
            "Plazo Fijo 1080 días": {
                "tasa_base": 7.59,
                "liquidez": "1080 días",
                "minimo": 0,
                "tipo": "plazo",
                "plazo_dias": 1080
            },
            "Plazo Fijo 1440 días": {
                "tasa_base": 7.29,
                "liquidez": "1440 días",
                "minimo": 0,
                "tipo": "plazo",
                "plazo_dias": 1440
            },
            "Plazo Fijo 1800 días": {
                "tasa_base": 6.89,
                "liquidez": "1800 días",
                "minimo": 0,
                "tipo": "plazo",
                "plazo_dias": 1800
            }
        },
        "color": "#4CAF50",
        "descripcion": "Ahorro sustentable a la vista y plazos fijos hasta 1800 días"
    }
}

# ============================================================================
# FUNCIONES DE CÁLCULO
# ============================================================================

def calcular_rendimiento_hibrido_didi(monto, tasa_premium, limite_premium, tasa_base, dias):
    """
    Calcula el rendimiento con estructura híbrida de DiDi
    16% sobre primeros $10,000 y tasa base sobre el resto
    """
    if monto <= limite_premium:
        interes_diario = (monto * tasa_premium / 100) / 365
    else:
        interes_premium = (limite_premium * tasa_premium / 100) / 365
        excedente = monto - limite_premium
        interes_excedente = (excedente * tasa_base / 100) / 365
        interes_diario = interes_premium + interes_excedente
    
    return interes_diario * dias

def calcular_interes_compuesto(capital, tasa_anual, dias, compounding="diario"):
    """
    Calcula interés compuesto con diferentes frecuencias
    """
    tasa_decimal = tasa_anual / 100
    
    if compounding == "diario":
        n = 365
        periodos = dias
        monto_final = capital * (1 + tasa_decimal / n) ** periodos
    elif compounding == "mensual":
        n = 12
        periodos = dias / 30.42
        monto_final = capital * (1 + tasa_decimal / n) ** periodos
    else:  # anual
        periodos = dias / 365
        monto_final = capital * (1 + tasa_decimal) ** periodos
    
    return monto_final - capital

def calcular_interes_simple(capital, tasa_anual, dias):
    """
    Calcula interés simple para inversiones a plazo fijo
    """
    tasa_decimal = tasa_anual / 100
    interes = capital * tasa_decimal * (dias / 365)
    return interes

def generar_proyeccion_mensual(capital, tasa_anual, tipo_calculo, meses=12):
    """
    Genera proyección mes a mes del crecimiento de la inversión
    """
    proyeccion = []
    capital_actual = capital
    
    for mes in range(meses + 1):
        dias = mes * 30
        
        if tipo_calculo == "compuesto":
            interes_acumulado = calcular_interes_compuesto(capital, tasa_anual, dias)
        else:
            interes_acumulado = calcular_interes_simple(capital, tasa_anual, dias)
        
        proyeccion.append({
            "Mes": mes,
            "Capital Inicial": capital,
            "Intereses Generados": interes_acumulado,
            "Total Acumulado": capital + interes_acumulado
        })
    
    return pd.DataFrame(proyeccion)

def analizar_diversificacion(inversiones_dict):
    """
    Analiza el nivel de diversificación y genera recomendaciones
    """
    total_invertido = sum([inv["monto"] for inv in inversiones_dict.values()])
    
    if total_invertido == 0:
        return None
    
    # Calcular concentración
    concentraciones = {
        sofipo: (inv["monto"] / total_invertido * 100) 
        for sofipo, inv in inversiones_dict.items()
    }
    
    max_concentracion = max(concentraciones.values())
    num_sofipos = len([c for c in concentraciones.values() if c > 0])
    
    # Calcular liquidez total
    liquidez_inmediata = sum([
        inv["monto"] for inv in inversiones_dict.values() 
        if inv.get("liquidez") == "Inmediata"
    ])
    
    porcentaje_liquido = (liquidez_inmediata / total_invertido * 100) if total_invertido > 0 else 0
    
    return {
        "total_invertido": total_invertido,
        "concentraciones": concentraciones,
        "max_concentracion": max_concentracion,
        "num_sofipos": num_sofipos,
        "liquidez_inmediata": liquidez_inmediata,
        "porcentaje_liquido": porcentaje_liquido
    }

def generar_recomendaciones(analisis, rendimiento_ponderado, cumple_klar=False, cumple_mp=False, cumple_uala=False):
    """
    Genera recomendaciones personalizadas basadas en el análisis y preferencias del usuario
    """
    recomendaciones = []
    
    if analisis is None:
        return ["⚠️ Agrega al menos una inversión para recibir recomendaciones"]
    
    # Evaluar diversificación
    if analisis["num_sofipos"] == 1:
        recomendaciones.append(
            "🎯 **Alta Concentración**: Estás invirtiendo en una sola SOFIPO. "
            "Considera diversificar en al menos 3-4 instituciones para reducir riesgo."
        )
    elif analisis["max_concentracion"] > 70:
        recomendaciones.append(
            f"⚠️ **Concentración Elevada**: {analisis['max_concentracion']:.1f}% en una sola institución. "
            "Lo ideal es no superar el 40-50% por SOFIPO."
        )
    elif analisis["num_sofipos"] >= 3 and analisis["max_concentracion"] < 50:
        recomendaciones.append(
            "✅ **Buena Diversificación**: Tu capital está bien distribuido entre múltiples SOFIPOs."
        )
    
    # Evaluar liquidez
    if analisis["porcentaje_liquido"] < 20:
        recomendaciones.append(
            f"💧 **Baja Liquidez**: Solo {analisis['porcentaje_liquido']:.1f}% está disponible de forma inmediata. "
            "Considera mantener al menos 20-30% en inversiones líquidas para emergencias."
        )
    elif analisis["porcentaje_liquido"] > 80:
        recomendaciones.append(
            f"💰 **Alta Liquidez**: {analisis['porcentaje_liquido']:.1f}% está disponible inmediatamente. "
            "Podrías mejorar rendimientos moviendo parte a plazos fijos."
        )
    else:
        recomendaciones.append(
            f"✅ **Balance de Liquidez Adecuado**: {analisis['porcentaje_liquido']:.1f}% líquido "
            "es un buen equilibrio entre accesibilidad y rendimiento."
        )
    
    # Evaluar rendimiento
    if rendimiento_ponderado < 10:
        recomendaciones.append(
            f"📊 **Rendimiento Bajo**: Tu GAT ponderado es {rendimiento_ponderado:.2f}%. "
            "Considera productos como Nu México (15%) o DiDi (16% primeros $10k) para mejorar."
        )
    elif rendimiento_ponderado >= 14:
        recomendaciones.append(
            f"🚀 **Excelente Rendimiento**: Tu GAT ponderado de {rendimiento_ponderado:.2f}% "
            "está por encima del promedio del mercado."
        )
    
    # Recomendaciones específicas de protección
    recomendaciones.append(
        "🛡️ **Protección IPAB**: Recuerda que cada SOFIPO está protegida hasta 25,000 UDIs (~200,000 MXN) "
        "por el IPAB. Si inviertes más, distribuye entre varias instituciones."
    )
    
    # Sugerencias de optimización
    if "Nu México" not in [k for k, v in analisis["concentraciones"].items() if v > 0]:
        recomendaciones.append(
            "💡 **Sugerencia**: Nu México ofrece 15% anual con liquidez inmediata, "
            "una de las mejores combinaciones del mercado."
        )
    
    if analisis["total_invertido"] >= 10000:
        tiene_didi = any("DiDi" in k for k in analisis["concentraciones"].keys() if analisis["concentraciones"][k] > 0)
        if not tiene_didi:
            recomendaciones.append(
                "💡 **Sugerencia DiDi**: Con capital suficiente, considera DiDi para aprovechar "
                "el 16% en los primeros $10,000 MXN."
            )
    
    # Recomendaciones basadas en preferencias del usuario
    st.markdown("---")
    recomendaciones.append("### 🎯 Oportunidades según tus preferencias:")
    
    # Lista de opciones disponibles ordenadas por tasa
    opciones_disponibles = []
    
    # DiDi siempre disponible (sin requisitos especiales)
    if not any("DiDi" in k for k in analisis["concentraciones"].keys() if analisis["concentraciones"][k] > 0):
        opciones_disponibles.append({
            "sofipo": "DiDi",
            "producto": "DiDi Ahorro",
            "tasa": 16.0,
            "limite": 10000,
            "requisito": None,
            "texto": "**DiDi Ahorro** - 16% primeros $10k, luego 8.5% (sin requisitos especiales)"
        })
    
    # Ualá - depende de si cumple requisitos
    tiene_uala = any("Ualá" in k for k in analisis["concentraciones"].keys() if analisis["concentraciones"][k] > 0)
    
    if not tiene_uala:
        if cumple_uala:
            # SÍ cumple requisitos → recomendar Ualá Plus 16%
            opciones_disponibles.append({
                "sofipo": "Ualá",
                "producto": "Plus",
                "tasa": 16.0,
                "limite": 50000,
                "requisito": "✅ Ya cumples",
                "texto": "**Ualá Plus** - 16% hasta $50k ✅ Cumples requisito de $3k/mes"
            })
        else:
            # NO cumple requisitos → recomendar Ualá Base 7.75%
            opciones_disponibles.append({
                "sofipo": "Ualá",
                "producto": "Base",
                "tasa": 7.75,
                "limite": 30000,
                "requisito": "❌ No cumples",
                "texto": "**Ualá Base** - 7.75% hasta $30k (sin requisitos especiales)"
            })
    
    # Klar - depende de si cumple requisitos
    tiene_klar = any("Klar" in k for k in analisis["concentraciones"].keys() if analisis["concentraciones"][k] > 0)
    
    if not tiene_klar:
        if cumple_klar:
            # SÍ cumple requisitos → recomendar Klar Max 15%
            opciones_disponibles.append({
                "sofipo": "Klar",
                "producto": "Inversión Max",
                "tasa": 15.0,
                "limite": None,
                "requisito": "✅ Ya cumples",
                "texto": "**Klar Inversión Max** - 15% liquidez inmediata ✅ Tienes Plus/Platino"
            })
        else:
            # NO cumple requisitos → recomendar Klar Cuenta 8.5%
            opciones_disponibles.append({
                "sofipo": "Klar",
                "producto": "Cuenta",
                "tasa": 8.5,
                "limite": None,
                "requisito": "❌ No cumples",
                "texto": "**Klar Cuenta** - 8.5% (sin requisitos especiales)"
            })
    
    # Nu México siempre disponible
    if not any("Nu" in k and "Turbo" in k for k in analisis["concentraciones"].keys() if analisis["concentraciones"][k] > 0):
        opciones_disponibles.append({
            "sofipo": "Nu México",
            "producto": "Cajita Turbo",
            "tasa": 15.0,
            "limite": 25000,
            "requisito": None,
            "texto": "**Nu México Cajita Turbo** - 15% hasta $25k con liquidez inmediata"
        })
    
    # Mercado Pago - solo si cumple requisitos
    tiene_mp = any("Mercado Pago" in k for k in analisis["concentraciones"].keys() if analisis["concentraciones"][k] > 0)
    
    if cumple_mp and not tiene_mp:
        # SÍ cumple requisitos → recomendar Mercado Pago 13%
        opciones_disponibles.append({
            "sofipo": "Mercado Pago",
            "producto": "Rendimientos",
            "tasa": 13.0,
            "limite": 25000,
            "requisito": "✅ Ya cumples",
            "texto": "**Mercado Pago** - 13% hasta $25k ✅ Cumples requisito de $3k/mes"
        })
    # Si NO cumple, no lo recomendamos (no tiene versión "base" sin requisitos)
    
    # Stori 90 días (mejor plazo sin requisitos)
    if not any("Stori" in k and "90" in k for k in analisis["concentraciones"].keys() if analisis["concentraciones"][k] > 0):
        opciones_disponibles.append({
            "sofipo": "Stori",
            "producto": "90 días",
            "tasa": 10.0,
            "limite": None,
            "requisito": None,
            "texto": "**Stori 90 días** - 10% a plazo fijo (sin requisitos)"
        })
    
    # Ordenar por tasa descendente
    opciones_disponibles.sort(key=lambda x: x["tasa"], reverse=True)
    
    # Mostrar top 3 opciones
    if len(opciones_disponibles) > 0:
        recomendaciones.append("\n**🌟 Mejores opciones disponibles para ti:**\n")
        for i, opcion in enumerate(opciones_disponibles[:3], 1):
            recomendaciones.append(f"{i}. {opcion['texto']}")
    
    return recomendaciones

# ============================================================================
# INTERFAZ PRINCIPAL
# ============================================================================

def main():
    # Crear espacio para el toggle en la esquina superior derecha
    col_spacer, col_toggle = st.columns([6, 1])
    
    with col_toggle:
        modo_oscuro = st.toggle("🌙", value=False, key="dark_mode", help="Modo Oscuro")
    
    # Aplicar estilos según el modo
    if modo_oscuro:
        st.markdown("""
        <style>
            /* ============================================ */
            /* MODO OSCURO COMPLETO */
            /* ============================================ */
            
            /* Fondo principal y contenedor */
            .stApp, .main, .block-container {
                background-color: #0d1117 !important;
                color: #c9d1d9 !important;
            }
            
            /* Headers y títulos */
            .main-header {
                color: #f0f6fc !important;
                text-shadow: 0 0 20px rgba(139, 92, 246, 0.3);
                text-align: center !important;
            }
            
            .subtitle {
                color: #8b949e !important;
                text-align: center !important;
            }
            
            h1, h2, h3, h4, h5, h6 {
                color: #f0f6fc !important;
            }
            
            /* Texto general */
            p, span, label, div, li {
                color: #c9d1d9 !important;
            }
            
            /* Tarjetas de SOFIPO */
            .sofipo-section {
                background: #161b22 !important;
                border: 1px solid #30363d !important;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
            }
            
            .sofipo-section:hover {
                background: #1c2128 !important;
                border-color: #667eea !important;
                box-shadow: 0 8px 24px rgba(102, 126, 234, 0.2) !important;
            }
            
            /* Métricas */
            [data-testid="stMetric"] {
                background-color: #161b22 !important;
                border: 1px solid #30363d !important;
                border-radius: 12px !important;
                padding: 1rem !important;
            }
            
            [data-testid="stMetricValue"] {
                color: #58a6ff !important;
            }
            
            [data-testid="stMetricLabel"] {
                color: #8b949e !important;
            }
            
            [data-testid="stMetricDelta"] {
                color: #3fb950 !important;
            }
            
            .metric-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            }
            
            /* Inputs - Mejorados con brillo en focus */
            input, textarea, select {
                background-color: #0d1117 !important;
                color: #c9d1d9 !important;
                border: 2px solid #30363d !important;
                transition: all 0.3s ease !important;
            }
            
            input:focus, textarea:focus, select:focus {
                border-color: #58a6ff !important;
                box-shadow: 0 0 0 4px rgba(88, 166, 255, 0.15), 0 0 12px rgba(88, 166, 255, 0.3) !important;
                outline: none !important;
                transform: translateY(-1px) !important;
            }
            
            .stNumberInput input {
                background-color: #0d1117 !important;
                color: #c9d1d9 !important;
                border: 2px solid #30363d !important;
                transition: all 0.3s ease !important;
            }
            
            .stNumberInput input:focus {
                border-color: #58a6ff !important;
                box-shadow: 0 0 0 4px rgba(88, 166, 255, 0.15), 0 0 12px rgba(88, 166, 255, 0.3) !important;
            }
            
            /* Selectbox */
            [data-baseweb="select"] {
                background-color: #0d1117 !important;
            }
            
            [data-baseweb="select"] > div {
                background-color: #0d1117 !important;
                border-color: #30363d !important;
            }
            
            /* Checkbox y Toggle */
            [data-testid="stCheckbox"] label {
                color: #c9d1d9 !important;
            }
            
            /* Radio buttons */
            [data-testid="stRadio"] label {
                color: #c9d1d9 !important;
            }
            
            /* Tabs - Mejorados con mejor contraste */
            .stTabs [data-baseweb="tab-list"] {
                background-color: #161b22 !important;
                border-radius: 12px !important;
                padding: 0.5rem !important;
                border: 1px solid #30363d !important;
            }
            
            .stTabs [data-baseweb="tab"] {
                background-color: transparent !important;
                color: #8b949e !important;
                border-radius: 10px !important;
                padding: 0.75rem 1.5rem !important;
                font-weight: 600 !important;
                transition: all 0.3s ease !important;
            }
            
            .stTabs [data-baseweb="tab"]:hover {
                background-color: #21262d !important;
                color: #c9d1d9 !important;
                transform: translateY(-2px) !important;
            }
            
            .stTabs [aria-selected="true"] {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                color: #ffffff !important;
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4), 0 0 20px rgba(102, 126, 234, 0.2) !important;
                transform: scale(1.02) !important;
            }
            
            /* Expander - Diseño profesional */
            [data-testid="stExpander"] {
                background-color: #0d1117 !important;
                border: 1px solid #30363d !important;
                border-radius: 12px !important;
                margin-bottom: 1rem !important;
                transition: all 0.3s ease !important;
            }
            
            [data-testid="stExpander"] summary {
                background-color: #161b22 !important;
                color: #c9d1d9 !important;
                padding: 1rem !important;
                border-radius: 12px !important;
                font-weight: 600 !important;
                cursor: pointer !important;
            }
            
            [data-testid="stExpander"] summary:hover {
                background-color: #1c2128 !important;
                color: #58a6ff !important;
            }
            
            [data-testid="stExpander"]:hover {
                border-color: #58a6ff !important;
                box-shadow: 0 4px 12px rgba(88, 166, 255, 0.15) !important;
            }
            
            [data-testid="stExpander"] > div:last-child {
                background-color: #0d1117 !important;
                padding: 1rem !important;
            }
            
            /* DataFrames y Tablas - Diseño profesional sin fondos blancos */
            [data-testid="stDataFrame"] {
                background-color: transparent !important;
                border-radius: 12px !important;
                overflow: hidden !important;
            }
            
            /* Iframe de la tabla (contiene Glide Data Grid) */
            [data-testid="stDataFrame"] iframe {
                background-color: #0d1117 !important;
                border: 1px solid #30363d !important;
                border-radius: 8px !important;
            }
            
            /* Estilo para tablas HTML estándar si las hay */
            .dataframe {
                background-color: #0d1117 !important;
                border: 1px solid #30363d !important;
                border-radius: 8px !important;
                overflow: hidden !important;
            }
            
            .dataframe thead tr th {
                background-color: #161b22 !important;
                color: #58a6ff !important;
                border-bottom: 2px solid #30363d !important;
                font-weight: 600 !important;
                padding: 12px 16px !important;
                text-align: left !important;
            }
            
            .dataframe tbody tr {
                background-color: #0d1117 !important;
                border-bottom: 1px solid #21262d !important;
                transition: background-color 0.2s ease !important;
            }
            
            .dataframe tbody tr:hover {
                background-color: #161b22 !important;
            }
            
            .dataframe tbody tr td {
                color: #c9d1d9 !important;
                background-color: transparent !important;
                padding: 10px 16px !important;
                border-right: 1px solid #21262d !important;
            }
            
            .dataframe tbody tr td:last-child {
                border-right: none !important;
            }
            
            /* Alertas y cajas de mensaje */
            .stAlert, [data-testid="stNotification"] {
                background-color: #161b22 !important;
                border: 1px solid #30363d !important;
                color: #c9d1d9 !important;
            }
            
            .warning-box {
                background-color: #3d2a00 !important;
                border-left: 4px solid #f59e0b !important;
                color: #fbbf24 !important;
            }
            
            .success-box {
                background-color: #002d1a !important;
                border-left: 4px solid #10b981 !important;
                color: #34d399 !important;
            }
            
            .info-box {
                background-color: #001d3d !important;
                border-left: 4px solid #3b82f6 !important;
                color: #60a5fa !important;
            }
            
            /* Divisores */
            hr {
                border-color: #30363d !important;
                background: linear-gradient(90deg, transparent, #30363d, transparent) !important;
            }
            
            /* Botones */
            .stButton > button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                color: white !important;
                border: none !important;
            }
            
            .stButton > button:hover {
                background: linear-gradient(135deg, #5568d3 0%, #643a8d 100%) !important;
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4) !important;
            }
            
            /* Sidebar (si se usa) */
            [data-testid="stSidebar"] {
                background-color: #0d1117 !important;
            }
            
            [data-testid="stSidebarNav"] {
                background-color: #161b22 !important;
            }
            
            /* Gráficas Plotly - Profesional y limpio */
            [data-testid="stPlotlyChart"] {
                background-color: transparent !important;
                border-radius: 12px !important;
                padding: 1rem !important;
            }
            
            /* Contenedor de gráfica con borde sutil */
            .js-plotly-plot {
                border: 1px solid #30363d !important;
                border-radius: 12px !important;
                overflow: hidden !important;
            }
            
            /* Modebar (botones de interacción) */
            .modebar-container, .modebar {
                background-color: rgba(22, 27, 34, 0.9) !important;
            }
            
            .modebar-btn {
                color: #8b949e !important;
            }
            
            .modebar-btn:hover {
                background-color: #30363d !important;
                color: #58a6ff !important;
            }
            
            /* Caption y textos pequeños */
            .stCaption, small {
                color: #8b949e !important;
            }
            
            /* Footer */
            footer {
                background-color: #0d1117 !important;
                color: #8b949e !important;
            }
            
            /* Markdown y código */
            code {
                background-color: #161b22 !important;
                color: #ff7b72 !important;
                border: 1px solid #30363d !important;
            }
            
            /* Progress bars */
            [data-testid="stProgressBar"] > div > div {
                background-color: #667eea !important;
            }
            
            /* Spinner */
            [data-testid="stSpinner"] > div {
                border-color: #667eea transparent transparent transparent !important;
            }
            
            /* Markdown containers */
            .element-container {
                color: #c9d1d9 !important;
            }
            
            /* Info, warning, error, success messages de Streamlit */
            .stInfo {
                background-color: #001d3d !important;
                color: #60a5fa !important;
            }
            
            .stWarning {
                background-color: #3d2a00 !important;
                color: #fbbf24 !important;
            }
            
            .stError {
                background-color: #3d0000 !important;
                color: #ff7b72 !important;
            }
            
            .stSuccess {
                background-color: #002d1a !important;
                color: #34d399 !important;
            }
            
            /* Links */
            a {
                color: #58a6ff !important;
            }
            
            a:hover {
                color: #79c0ff !important;
            }
            
            /* Badge */
            .badge {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                color: white !important;
                box-shadow: 0 2px 10px rgba(102, 126, 234, 0.4) !important;
            }
            
            /* Efectos adicionales de hover para mejor UX */
            .stButton > button:active {
                transform: scale(0.98) !important;
            }
            
            /* Scrollbar personalizado para modo oscuro */
            ::-webkit-scrollbar {
                width: 12px;
                height: 12px;
            }
            
            ::-webkit-scrollbar-track {
                background: #0d1117 !important;
            }
            
            ::-webkit-scrollbar-thumb {
                background: #30363d !important;
                border-radius: 6px !important;
                border: 2px solid #0d1117 !important;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: #484f58 !important;
            }
            
            /* Animaciones suaves */
            * {
                transition: background-color 0.2s ease, border-color 0.2s ease !important;
            }
            
            /* Selectbox mejorado */
            [data-baseweb="select"] > div:hover {
                border-color: #58a6ff !important;
                box-shadow: 0 0 0 2px rgba(88, 166, 255, 0.1) !important;
            }
            
            /* Mejora visual del toggle de modo oscuro */
            [data-testid="stCheckbox"] input:checked ~ div {
                background-color: #667eea !important;
            }
        </style>
        """, unsafe_allow_html=True)
    
    # Encabezado centrado
    st.markdown('<h1 class="main-header">💰 Simulador de Inversiones</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Compara rendimientos de SOFIPOs mexicanas en tiempo real</p>', unsafe_allow_html=True)
    
    # ========================================================================
    # GUARDAR/CARGAR SIMULACIONES
    # ========================================================================
    
    with st.expander("💾 Guardar/Cargar Simulación", expanded=False):
        st.markdown("**Guarda tu simulación actual o carga una anterior**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Botón para guardar simulación
            if st.button("💾 Guardar Simulación Actual", use_container_width=True):
                simulacion = guardar_simulacion()
                json_str, b64, fecha = exportar_json(simulacion)
                st.session_state["ultima_simulacion"] = simulacion
                st.success("✅ Simulación guardada en memoria")
        
        with col2:
            # Descargar como JSON
            if "ultima_simulacion" in st.session_state:
                json_str, b64, fecha = exportar_json(st.session_state["ultima_simulacion"])
                st.download_button(
                    label="📥 Descargar JSON",
                    data=json_str,
                    file_name=f"simulacion_sofipo_{fecha}.json",
                    mime="application/json",
                    use_container_width=True
                )
            else:
                st.button("📥 Descargar JSON", disabled=True, use_container_width=True, help="Primero guarda una simulación")
        
        with col3:
            # Cargar desde archivo
            uploaded_file = st.file_uploader("📤 Cargar desde archivo", type=['json'], label_visibility="collapsed")
            if uploaded_file is not None:
                try:
                    simulacion_data = json.load(uploaded_file)
                    if cargar_simulacion(simulacion_data):
                        st.success(f"✅ Simulación cargada: {simulacion_data.get('fecha_guardado', 'Sin fecha')}")
                        st.rerun()
                except Exception as e:
                    st.error(f"❌ Error al cargar archivo: {str(e)}")
        
        # Mostrar información de la última simulación guardada
        if "ultima_simulacion" in st.session_state:
            sim = st.session_state["ultima_simulacion"]
            st.info(f"📊 **Última simulación guardada:** {sim['fecha_guardado']} | Monto: ${sim['monto_total']:,.0f} | Inversiones: {len(sim['inversiones'])}")
    
    st.divider()
    
    # ========================================================================
    # CONFIGURACIÓN RÁPIDA
    # ========================================================================
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎯 ¿Cuánto quieres invertir?")
        monto_total = st.number_input(
            "Monto total disponible (MXN)",
            min_value=1000,
            value=st.session_state.get("monto_total_input", 50000),
            step=5000,
            help="Este es el capital que tienes disponible para distribuir entre SOFIPOs",
            key="monto_total_input"
        )
    
    with col2:
        st.markdown("### 📅 Plazo")
        periodo_options = [3, 6, 12, 24]
        default_periodo = st.session_state.get("periodo_simulacion", 12)
        default_index = periodo_options.index(default_periodo) if default_periodo in periodo_options else 2
        periodo_simulacion = st.selectbox(
            "Simular a:",
            options=periodo_options,
            index=default_index,
            format_func=lambda x: f"{x} meses",
            key="periodo_simulacion"
        )
    
    st.divider()
    
    # ========================================================================
    # PREFERENCIAS DEL USUARIO
    # ========================================================================
    
    st.markdown("### ⚙️ Tus preferencias de inversión")
    
    with st.expander("🔧 Configurar requisitos que SÍ puedo cumplir", expanded=False):
        st.markdown("**Marca las opciones que SÍ cumples para obtener mejores recomendaciones:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            cumple_klar_plus = st.checkbox(
                "✅ Tengo membresía Klar Plus o Platino",
                value=st.session_state.get("cumple_klar_plus", False),
                help="Necesaria para Klar Inversión Max (15%)",
                key="cumple_klar_plus"
            )
            
            cumple_mercadopago = st.checkbox(
                "✅ Puedo depositar $3,000/mes en Mercado Pago",
                value=st.session_state.get("cumple_mercadopago", False),
                help="Necesario para obtener el 13% en Mercado Pago",
                key="cumple_mercadopago"
            )
        
        with col2:
            cumple_uala_plus = st.checkbox(
                "✅ Puedo consumir $3k/mes con Ualá o domiciliar nómina",
                value=st.session_state.get("cumple_uala_plus", False),
                help="Necesario para Ualá Plus (16% hasta $50k)",
                key="cumple_uala_plus"
            )
    
    with st.expander("🚫 Excluir SOFIPOs que NO quiero usar", expanded=False):
        st.markdown("**Desmarca las SOFIPOs que NO quieres que aparezcan en las recomendaciones:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            usa_nu = st.checkbox("🟣 Nu México", value=True, key="usa_nu")
            usa_didi = st.checkbox("🧡 DiDi", value=True, key="usa_didi")
            usa_stori = st.checkbox("💙 Stori", value=True, key="usa_stori")
            usa_klar = st.checkbox("💚 Klar", value=True, key="usa_klar")
        
        with col2:
            usa_uala = st.checkbox("💜 Ualá", value=True, key="usa_uala")
            usa_mp = st.checkbox("💵 Mercado Pago", value=True, key="usa_mp")
            usa_finsus = st.checkbox("🔵 Finsus", value=True, key="usa_finsus")
    
    with st.expander("💧 Preferencias de liquidez", expanded=False):
        st.markdown("**Configura si solo quieres productos con disponibilidad inmediata:**")
        solo_vista = st.checkbox(
            "💰 Solo productos A LA VISTA (sin plazo fijo)",
            value=st.session_state.get("solo_vista", False),
            help="Activar para excluir productos con plazos fijos y solo ver rendimientos líquidos disponibles",
            key="solo_vista"
        )
    
    st.divider()
    
    # ========================================================================
    # CALCULADORA DE OBJETIVO INVERSO (CON TASAS REALES)
    # ========================================================================
    
    with st.expander("🎯 Calculadora de Objetivo: ¿Cuánto necesito invertir?", expanded=False):
        st.markdown("**Calcula cuánto capital necesitas para alcanzar tu meta de ganancia usando tasas reales y tus preferencias**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💰 Tu Meta de Ganancia")
            objetivo_tipo = st.radio(
                "Quiero ganar:",
                options=["mensual", "anual"],
                format_func=lambda x: "💵 Por mes" if x == "mensual" else "📅 Por año",
                horizontal=True
            )
            
            objetivo_ganancia = st.number_input(
                f"Ganancia deseada ({objetivo_tipo})",
                min_value=100,
                value=1000 if objetivo_tipo == "mensual" else 12000,
                step=100 if objetivo_tipo == "mensual" else 1000,
                help=f"¿Cuánto quieres ganar {'al mes' if objetivo_tipo == 'mensual' else 'al año'}?"
            )
        
        with col2:
            st.markdown("#### 📊 Perfil de Inversión")
            st.info("💡 La calculadora usará **tus preferencias actuales** (SOFIPOs excluidas, requisitos, liquidez)")
        
        # Convertir ganancia a anual
        if objetivo_tipo == "mensual":
            ganancia_anual_objetivo = objetivo_ganancia * 12
        else:
            ganancia_anual_objetivo = objetivo_ganancia
        
        # Función para calcular distribución y tasa ponderada con un monto dado
        def calcular_tasa_ponderada_real(monto_prueba):
            """Simula la distribución agresiva y calcula la tasa ponderada real"""
            distribucion = []
            saldo = monto_prueba
            
            # 1. DiDi 16% hasta $10k
            if usa_didi and saldo > 0:
                monto_didi = min(10000, saldo)
                distribucion.append({"monto": monto_didi, "tasa": 16.0})
                saldo -= monto_didi
            
            # 2. Ualá Plus 16% hasta $50k (si cumple requisitos)
            if usa_uala and cumple_uala_plus and saldo > 0:
                monto_uala = min(50000, saldo)
                distribucion.append({"monto": monto_uala, "tasa": 16.0})
                saldo -= monto_uala
            
            # 3. Klar Max 15% (si cumple requisitos)
            if usa_klar and cumple_klar_plus and saldo > 0:
                distribucion.append({"monto": saldo, "tasa": 15.0})
                saldo = 0
            
            # 4. Nu Turbo 15% hasta $25k
            if usa_nu and saldo > 0:
                monto_nu = min(25000, saldo)
                distribucion.append({"monto": monto_nu, "tasa": 15.0})
                saldo -= monto_nu
            
            # 5. Mercado Pago 13% hasta $25k (si cumple requisitos)
            if usa_mp and cumple_mercadopago and saldo > 0:
                monto_mp = min(25000, saldo)
                distribucion.append({"monto": monto_mp, "tasa": 13.0})
                saldo -= monto_mp
            
            # 6. DiDi Base 8.5% (resto)
            if usa_didi and saldo > 0 and not solo_vista:
                distribucion.append({"monto": saldo, "tasa": 8.5})
                saldo = 0
            
            # 7. Stori 10% (plazo fijo - solo si NO está en modo vista)
            if not solo_vista and usa_stori and saldo > 0:
                distribucion.append({"monto": saldo, "tasa": 10.0})
                saldo = 0
            
            # 8. Finsus 10.09% (plazo fijo - solo si NO está en modo vista)
            if not solo_vista and usa_finsus and saldo > 0:
                distribucion.append({"monto": saldo, "tasa": 10.09})
                saldo = 0
            
            # Calcular tasa ponderada
            if distribucion:
                rendimiento_total = sum([d["monto"] * d["tasa"] / 100 for d in distribucion])
                tasa_ponderada = (rendimiento_total / monto_prueba) * 100 if monto_prueba > 0 else 0
                return tasa_ponderada, distribucion
            else:
                return 0, []
        
        # Buscar el capital necesario mediante aproximación binaria
        capital_min = 1000
        capital_max = 10000000
        capital_necesario = capital_min
        iteraciones = 0
        max_iteraciones = 50
        
        while iteraciones < max_iteraciones:
            capital_prueba = (capital_min + capital_max) / 2
            tasa_ponderada, dist = calcular_tasa_ponderada_real(capital_prueba)
            
            if tasa_ponderada == 0:
                st.error("❌ No hay SOFIPOs disponibles con tu configuración actual. Activa al menos una SOFIPO.")
                break
            
            ganancia_estimada = capital_prueba * tasa_ponderada / 100
            
            if abs(ganancia_estimada - ganancia_anual_objetivo) < 100:  # Precisión de $100
                capital_necesario = capital_prueba
                break
            elif ganancia_estimada < ganancia_anual_objetivo:
                capital_min = capital_prueba
            else:
                capital_max = capital_prueba
            
            capital_necesario = capital_prueba
            iteraciones += 1
        
        # Calcular valores finales
        tasa_real, distribucion_final = calcular_tasa_ponderada_real(capital_necesario)
        ganancia_anual_real = capital_necesario * tasa_real / 100
        ganancia_mensual_real = ganancia_anual_real / 12
        
        st.markdown("---")
        st.markdown("### 🎯 Resultado de tu Objetivo (Con Tasas Reales)")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "💼 Capital Necesario",
                f"${capital_necesario:,.0f}",
                help="Monto que necesitas invertir"
            )
        
        with col2:
            st.metric(
                "📅 Ganancia Anual",
                f"${ganancia_anual_real:,.0f}",
                delta=f"{tasa_real:.2f}%"
            )
        
        with col3:
            st.metric(
                "💵 Ganancia Mensual",
                f"${ganancia_mensual_real:,.0f}",
                delta=f"~{ganancia_mensual_real/capital_necesario*100:.2f}% mensual"
            )
        
        with col4:
            sofipos_count = len(set([d.get("sofipo", "") for d in distribucion_final if d.get("sofipo")]))
            if sofipos_count == 0:
                sofipos_count = len(distribucion_final)
            st.metric(
                "🏦 SOFIPOs en distribución",
                f"{sofipos_count}",
                help="Según tu configuración"
            )
        
        # Mostrar distribución detallada
        if distribucion_final:
            st.markdown("#### 📊 Distribución Sugerida")
            for i, item in enumerate(distribucion_final, 1):
                porcentaje = (item["monto"] / capital_necesario * 100)
                ganancia_item = item["monto"] * item["tasa"] / 100
                st.caption(f"{i}. ${item['monto']:,.0f} al {item['tasa']}% = **${ganancia_item:,.0f}/año** ({porcentaje:.1f}% del total)")
        
        # Mostrar advertencias según el monto
        if capital_necesario > 1000000:
            st.warning("⚠️ **Capital alto**: Considera diversificar en múltiples SOFIPOs para no exceder el límite IPAB de $400k por institución.")
        elif capital_necesario < 5000:
            st.info("💡 **Capital bajo**: Puedes empezar con 1-2 SOFIPOs y diversificar conforme aumentes tu capital.")
        
        # Mostrar advertencias de configuración
        if solo_vista:
            st.info("💧 **Modo A LA VISTA activado**: Solo se incluyen productos líquidos (sin plazo fijo)")
        
        excluidas = []
        if not usa_nu: excluidas.append("Nu")
        if not usa_didi: excluidas.append("DiDi")
        if not usa_stori: excluidas.append("Stori")
        if not usa_klar: excluidas.append("Klar")
        if not usa_uala: excluidas.append("Ualá")
        if not usa_mp: excluidas.append("Mercado Pago")
        if not usa_finsus: excluidas.append("Finsus")
        
        if excluidas:
            st.warning(f"🚫 **SOFIPOs excluidas**: {', '.join(excluidas)}")
        
        # Botón para aplicar el objetivo al simulador (FIJO)
        st.markdown("---")
        if st.button("📊 Copiar este monto", use_container_width=True, key="btn_copiar_objetivo"):
            st.code(f"{int(capital_necesario)}", language=None)
            st.success(f"✅ **Copia ${capital_necesario:,.0f}** y pégalo arriba en 'Monto total disponible'")
    
    st.divider()
    
    # ========================================================================
    # ESTRATEGIAS DE OPTIMIZACIÓN (ANTES DE SELECCIONAR)
    # ========================================================================
    
    st.header("💡 Recomendaciones de Inversión")
    st.markdown("Basadas en tu capital y preferencias, estas son las estrategias optimizadas:")
    
    tab1, tab2, tab3 = st.tabs(["🛡️ Conservadora", "⚖️ Balanceada", "🚀 Agresiva"])
    
    with tab1:
        st.markdown("""
        ### Estrategia Conservadora (Menor Riesgo)
        
        **Perfil**: Prioriza seguridad y liquidez sobre rendimiento máximo.
        
        **Distribución sugerida**:
        - 30% Nu México (Cajita Turbo) - 15% GAT (hasta $25k)
        - 25% Mercado Pago - 13% GAT (requiere $3k/mes)
        - 20% Ualá Base - 7.75% GAT (hasta $30k)
        - 15% Klar Cuenta - 8.5% GAT
        - 10% Nu México (Dinero en Cajita) - 7.5% GAT (emergencias)
        
        **Ventajas**:
        - ✅ Máxima liquidez inmediata (100%)
        - ✅ Diversificación en 4 instituciones sólidas
        - ✅ Rendimiento promedio ~11.3% anual
        
        **Consideraciones**:
        - Todas las opciones tienen liquidez inmediata
        - Ideal para fondos de emergencia
        - Mercado Pago requiere $3k/mes, resto sin requisitos especiales
        """)
    
    with tab2:
        st.markdown("""
        ### Estrategia Balanceada (Riesgo Moderado)
        
        **Perfil**: Balance entre rendimiento, liquidez y diversificación.
        
        **Distribución sugerida**:
        - 20% DiDi (hasta $10k) - 16% GAT (después 8.5%)
        - 25% Nu México (Cajita Turbo) - 15% GAT
        - 20% Klar Inversión Max - 15% GAT (requiere Plus/Platino)
        - 15% Mercado Pago - 13% GAT (requiere $3k/mes)
        - 20% Stori 90 días - 10% GAT
        
        **Ventajas**:
        - ✅ Excelente diversificación (5 SOFIPOs)
        - ✅ 80% con liquidez inmediata
        - ✅ Rendimiento optimizado (~13.8% ponderado)
        
        **Consideraciones**:
        - Requiere membresía Klar Plus/Platino
        - Mercado Pago requiere depositar al menos $3,000/mes
        - 20% a plazo fijo de 90 días en Stori
        - Balance perfecto entre liquidez y rendimiento
        - Ideal para la mayoría de inversores
        """)
    
    with tab3:
        st.markdown("""
        ### 🚀 Estrategia Agresiva - Maximizar Rendimientos
        
        **Objetivo**: Obtener el **máximo rendimiento posible** sin importar el riesgo ni la liquidez.
        
        **Filosofía**: Toda tu inversión trabaja al máximo, aprovechando las mejores tasas de mercado.
        """)
        
        # Calcular distribución agresiva con montos específicos
        st.subheader("💰 Distribución Recomendada para tu Capital")
        
        # Mostrar filtro activo si está en modo solo vista
        if solo_vista:
            st.info("💧 **Modo A LA VISTA activado**: Solo se mostrarán productos sin plazo fijo")
        
        # Estrategia: Maximizar tasas según tus preferencias Y exclusiones
        distribucion_agresiva = []
        saldo_restante = monto_total
        
        # 1. DiDi Ahorro: Invertir hasta $10,000 al 16% (PRIORIDAD 1 - A LA VISTA)
        if usa_didi and saldo_restante > 0:
            monto_didi = min(10000, saldo_restante)
            distribucion_agresiva.append({
                "sofipo": "DiDi",
                "producto": "DiDi Ahorro",
                "monto": monto_didi,
                "tasa": 16.0,
                "razon": "🥇 16% primeros $10k (después 8.5%) 💧 A LA VISTA"
            })
            saldo_restante -= monto_didi
        
        # 2. Ualá Plus: SOLO si cumples requisitos (PRIORIDAD 2 - A LA VISTA)
        if usa_uala and cumple_uala_plus and saldo_restante > 0:
            monto_uala = min(50000, saldo_restante)
            distribucion_agresiva.append({
                "sofipo": "Ualá",
                "producto": "Cuenta Plus",
                "monto": monto_uala,
                "tasa": 16.0,
                "razon": "🥇 16% hasta $50k ✅ Cumples requisito de $3k/mes 💧 A LA VISTA"
            })
            saldo_restante -= monto_uala
        
        # 3. Klar Inversión Flexible Max: SOLO si cumples requisitos (PRIORIDAD 3 - A LA VISTA)
        if usa_klar and cumple_klar_plus and saldo_restante > 0:
            monto_klar = saldo_restante
            if monto_klar >= 100:
                distribucion_agresiva.append({
                    "sofipo": "Klar",
                    "producto": "Inversión Flexible Max",
                    "monto": monto_klar,
                    "tasa": 15.0,
                    "razon": "🥈 15% liquidez inmediata ✅ Tienes Plus/Platino 💧 A LA VISTA"
                })
                saldo_restante -= monto_klar
        
        # 4. Nu México Cajita Turbo: Hasta $25,000 al 15% (PRIORIDAD 4 - A LA VISTA)
        if usa_nu and saldo_restante > 0:
            monto_nu_turbo = min(25000, saldo_restante)
            if monto_nu_turbo > 0:
                distribucion_agresiva.append({
                    "sofipo": "Nu México",
                    "producto": "Cajita Turbo",
                    "monto": monto_nu_turbo,
                    "tasa": 15.0,
                    "razon": "🥈 15% hasta $25k liquidez inmediata 💧 A LA VISTA"
                })
                saldo_restante -= monto_nu_turbo
        
        # 5. Mercado Pago: SOLO si cumples requisitos al 13% (PRIORIDAD 5 - A LA VISTA)
        if usa_mp and cumple_mercadopago and saldo_restante > 0:
            monto_mp = min(25000, saldo_restante)
            distribucion_agresiva.append({
                "sofipo": "Mercado Pago",
                "producto": "Cuenta Remunerada",
                "monto": monto_mp,
                "tasa": 13.0,
                "razon": "🥈 13% hasta $25k ✅ Cumples requisito de $3k/mes 💧 A LA VISTA"
            })
            saldo_restante -= monto_mp
        
        # 6. DiDi Ahorro Base: Después de los primeros $10k al 8.5% (PRIORIDAD 6 - A LA VISTA)
        if usa_didi and saldo_restante > 0:
            distribucion_agresiva.append({
                "sofipo": "DiDi",
                "producto": "DiDi Ahorro",
                "monto": saldo_restante,
                "tasa": 8.5,
                "razon": "🥉 8.5% después de $10k 💧 A LA VISTA"
            })
            saldo_restante -= saldo_restante
        
        # 7. Stori 90 días: Al 10% (PRIORIDAD 7 - PLAZO FIJO - solo si NO está en modo vista)
        if not solo_vista and usa_stori and saldo_restante > 0:
            distribucion_agresiva.append({
                "sofipo": "Stori",
                "producto": "90 días",
                "monto": saldo_restante,
                "tasa": 10.0,
                "razon": "🥉 10% plazo 90 días ⏰ PLAZO FIJO"
            })
            saldo_restante -= saldo_restante
        
        # 8. Finsus: Si aún queda saldo y otras opciones están excluidas (RESPALDO - PLAZO FIJO - solo si NO está en modo vista)
        if not solo_vista and usa_finsus and saldo_restante > 0:
            distribucion_agresiva.append({
                "sofipo": "Finsus",
                "producto": "Apartado 360 días",
                "monto": saldo_restante,
                "tasa": 10.09,
                "razon": "🥉 10.09% plazo 360 días ⏰ PLAZO FIJO"
            })
            saldo_restante -= saldo_restante
        
        # Advertencia si quedan fondos sin asignar
        if saldo_restante > 0:
            if solo_vista:
                st.warning(f"⚠️ Quedan **${saldo_restante:,.0f}** sin asignar. En modo A LA VISTA, los productos a plazo fijo están excluidos. Desactiva el modo A LA VISTA o activa más SOFIPOs para distribuir todo tu capital.")
            else:
                st.warning(f"⚠️ Quedan **${saldo_restante:,.0f}** sin asignar. Has excluido demasiadas SOFIPOs. Activa al menos una más para distribuir todo tu capital.")
        
        # Mostrar tabla con montos exactos
        if distribucion_agresiva:
            st.markdown("**💵 Montos específicos sugeridos:**")
        else:
            st.error("❌ No hay recomendaciones disponibles. Has excluido todas las SOFIPOs. Activa al menos una para ver recomendaciones.")
        
        for i, dist in enumerate(distribucion_agresiva, 1):
            porcentaje = (dist['monto'] / monto_total * 100)
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.markdown(f"**{i}. {dist['sofipo']}** - {dist['producto']}")
                st.caption(dist['razon'])
            
            with col2:
                st.metric(
                    "Monto",
                    f"${dist['monto']:,.0f}",
                    delta=f"{porcentaje:.1f}% del total"
                )
            
            with col3:
                st.metric("GAT", f"{dist['tasa']}%")
        
        # Calcular rendimiento proyectado de esta estrategia
        rendimiento_agresivo = sum([d['monto'] * d['tasa'] / 100 for d in distribucion_agresiva])
        tasa_ponderada_agresiva = (rendimiento_agresivo / monto_total) * 100
        ganancia_12m = int(rendimiento_agresivo)
        
        st.success(f"🎯 **Con esta estrategia agresiva obtendrás:**")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Tasa ponderada", f"{tasa_ponderada_agresiva:.2f}%")
        with col2:
            st.metric("Ganancia estimada (12 meses)", f"${ganancia_12m:,.0f}")
        
        # Botón para aplicar estrategia
        st.markdown("---")
        if st.button("✨ Aplicar esta estrategia a mi simulación", key="btn_aplicar_agresiva", type="primary"):
            # Guardar la distribución en session_state
            st.session_state['estrategia_aplicada'] = distribucion_agresiva
            st.session_state['aplicar_estrategia'] = True
            st.success("✅ Estrategia aplicada! Desplázate hacia abajo para ver los cambios.")
            st.rerun()
        
        # Advertencias dinámicas según preferencias
        advertencias = ["**⚠️ Consideraciones importantes:**"]
        advertencias.append(f"- Esta estrategia alcanza un rendimiento ponderado de ~{tasa_ponderada_agresiva:.1f}%")
        
        # Advertencias sobre requisitos incluidos
        if cumple_mercadopago:
            advertencias.append("- ✅ Incluye Mercado Pago 13% (cumples requisito de $3k/mes)")
        else:
            advertencias.append("- ℹ️ Podrías mejorar con Mercado Pago 13% si puedes depositar $3k/mes")
        
        if cumple_uala_plus:
            advertencias.append("- ✅ Incluye Ualá Plus 16% (cumples requisito de $3k/mes)")
        else:
            advertencias.append("- ℹ️ Podrías mejorar con Ualá Plus 16% si puedes consumir $3k/mes")
        
        if cumple_klar_plus:
            advertencias.append("- ✅ Incluye Klar Max 15% (tienes membresía Plus/Platino)")
        else:
            advertencias.append("- ℹ️ Podrías mejorar con Klar Max 15% si tienes membresía Plus/Platino")
        
        advertencias.append("- Parte del capital puede quedar en plazos fijos (menor liquidez)")
        advertencias.append("- No es recomendable para fondos de emergencia")
        
        st.warning("\n".join(advertencias))
    
    st.divider()
    
    # ========================================================================
    # SELECCIÓN SIMPLE DE SOFIPOS
    # ========================================================================
    
    st.markdown("### 💳 Selecciona las SOFIPOs donde invertirás (o aplica una estrategia arriba)")
    
    # Verificar si se aplicó una estrategia y pre-cargar valores en session_state
    if 'aplicar_estrategia' in st.session_state and st.session_state['aplicar_estrategia']:
        estrategia_aplicada = st.session_state.get('estrategia_aplicada', [])
        
        # Pre-cargar todos los valores en session_state
        for item in estrategia_aplicada:
            sofipo_name = item['sofipo']
            # Marcar checkbox
            st.session_state[f"check_{sofipo_name}"] = True
            # Seleccionar producto
            st.session_state[f"prod_{sofipo_name}"] = item['producto']
            # Establecer monto
            st.session_state[f"monto_{sofipo_name}_{item['producto']}"] = item['monto']
        
        # Limpiar el flag
        st.session_state['aplicar_estrategia'] = False
        st.info("📋 **Estrategia aplicada automáticamente.** Los valores han sido cargados en las pestañas de cada SOFIPO.")
    
    estrategia_a_aplicar = None
    
    inversiones_seleccionadas = {}
    
    # Placeholder para el indicador de dinero restante (se actualizará al final)
    indicador_restante = st.empty()
    
    # Crear tabs para cada SOFIPO
    sofipos_names = list(SOFIPOS_DATA.keys())
    tabs = st.tabs([f"{SOFIPOS_DATA[s]['logo']} {s}" for s in sofipos_names])
    
    for idx, (sofipo_name, tab) in enumerate(zip(sofipos_names, tabs)):
        with tab:
            sofipo_data = SOFIPOS_DATA[sofipo_name]
            
            # Descripción breve
            st.info(f"**{sofipo_data['descripcion']}**")
            
            # Checkbox para incluir esta SOFIPO
            incluir = st.checkbox(
                f"✅ Quiero invertir en {sofipo_name}",
                key=f"check_{sofipo_name}"
            )
            
            if incluir:
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Selector de producto
                    productos = list(sofipo_data['productos'].keys())
                    
                    producto_seleccionado = st.selectbox(
                        "📦 Elige el producto:",
                        options=productos,
                        key=f"prod_{sofipo_name}",
                        help="Selecciona el tipo de inversión"
                    )
                    
                    producto_info = sofipo_data['productos'][producto_seleccionado]
                    
                    # Mostrar tasa
                    if producto_info.get("tipo") == "vista_hibrida":
                        st.success(f"**📊 GAT: {producto_info['tasa_premium']}%** (primeros ${producto_info['limite_premium']:,})")
                        st.caption(f"Después: {producto_info['tasa_base']}%")
                    elif producto_info.get("limite_max"):
                        st.success(f"**📊 GAT: {producto_info['tasa_base']}%** (hasta ${producto_info['limite_max']:,})")
                    else:
                        st.success(f"**📊 GAT: {producto_info['tasa_base']}%**")
                    
                    st.caption(f"💧 Liquidez: {producto_info['liquidez']}")
                
                with col2:
                    # Selector de modo: Monto o Porcentaje
                    modo_input = st.radio(
                        "Ingresar como:",
                        ["💵 Monto ($)", "📊 Porcentaje (%)"],
                        key=f"modo_{sofipo_name}",
                        horizontal=True
                    )
                    
                    if modo_input == "💵 Monto ($)":
                        # Monto a invertir
                        monto = st.number_input(
                            "¿Cuánto invertirás aquí?",
                            min_value=producto_info['minimo'],
                            value=min(max(10000, producto_info['minimo']), monto_total),
                            step=1000,
                            key=f"monto_{sofipo_name}_{producto_seleccionado}",
                            help=f"Mínimo: ${producto_info['minimo']:,} MXN"
                        )
                        
                        # Porcentaje del total
                        porcentaje = (monto / monto_total * 100) if monto_total > 0 else 0
                        st.caption(f"📊 Representa el **{porcentaje:.1f}%** de tu capital total")
                    else:
                        # Input de porcentaje
                        porcentaje_input = st.number_input(
                            "¿Qué % de tu capital invertirás aquí?",
                            min_value=0.0,
                            max_value=100.0,
                            value=10.0,
                            step=5.0,
                            key=f"pct_{sofipo_name}_{producto_seleccionado}",
                            help="Porcentaje de tu capital total"
                        )
                        
                        # Calcular monto desde porcentaje
                        monto = int(monto_total * porcentaje_input / 100)
                        
                        # Validar mínimo
                        if monto < producto_info['minimo']:
                            st.warning(f"⚠️ El {porcentaje_input}% equivale a ${monto:,}, pero el mínimo es ${producto_info['minimo']:,}")
                            monto = producto_info['minimo']
                        
                        st.caption(f"💵 Invertirás **${monto:,.0f}**")
                
                # Advertencias especiales por SOFIPO
                if sofipo_name == "Mercado Pago":
                    if monto > 25000:
                        st.warning("⚠️ Mercado Pago tiene un límite de $25,000 para obtener el 13%")
                    st.info("ℹ️ Requieres depositar al menos $3,000 MXN mensuales para mantener la tasa del 13%")
                
                if sofipo_name == "Ualá":
                    if "Plus" in producto_seleccionado:
                        if monto > 50000:
                            st.warning("⚠️ Ualá Plus tiene un límite de $50,000 para obtener el 16%")
                        st.info("ℹ️ Requieres consumir $3,000/mes con tarjetas Ualá o domiciliar tu nómina")
                    elif "Base" in producto_seleccionado and monto > 30000:
                        st.warning("⚠️ La tasa base del 7.75% aplica solo hasta $30,000")
                
                # Requisitos especiales
                cumple_requisito = True
                if producto_info.get("requisito") is not None:
                        if producto_info.get("requisito") == "Plus o Platino":
                            cumple_requisito = st.checkbox(
                                "¿Tienes membresía Klar Plus o Platino?",
                                value=True,
                                key=f"req_{sofipo_name}_{producto_seleccionado}",
                                help="Necesitas membresía Plus o Platino para obtener el 15%"
                            )
                
                # Guardar inversión
                inversiones_seleccionadas[f"{sofipo_name} - {producto_seleccionado}"] = {
                    "sofipo": sofipo_name,
                    "producto": producto_seleccionado,
                    "monto": monto,
                    "producto_info": producto_info,
                    "cumple_requisito": cumple_requisito,
                    "liquidez": producto_info['liquidez'],
                    "tipo": producto_info['tipo']
                }
    
    # ========================================================================
    # INDICADOR DE DINERO RESTANTE
    # ========================================================================
    
    # Calcular total asignado
    total_asignado_actual = sum([inv["monto"] for inv in inversiones_seleccionadas.values()])
    dinero_restante = monto_total - total_asignado_actual
    porcentaje_restante = (dinero_restante / monto_total * 100) if monto_total > 0 else 0
    porcentaje_asignado = (total_asignado_actual / monto_total * 100) if monto_total > 0 else 0
    
    # Mostrar indicador visual con color según el estado
    with indicador_restante.container():
        if dinero_restante > 0:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("💰 Dinero asignado", f"${total_asignado_actual:,.0f}", f"{porcentaje_asignado:.1f}%")
            with col2:
                st.metric("🔓 Dinero disponible", f"${dinero_restante:,.0f}", f"{porcentaje_restante:.1f}%")
            with col3:
                st.metric("📊 Total", f"${monto_total:,.0f}", "100%")
        elif dinero_restante == 0:
            st.success(f"✅ **Perfecto!** Has distribuido todo tu dinero: ${monto_total:,.0f} (100%)")
        else:
            st.error(f"⚠️ **¡Cuidado!** Te has pasado ${abs(dinero_restante):,.0f}. Ajusta los montos.")
    
    st.divider()
    
    # ========================================================================
    # CÁLCULOS Y RESULTADOS
    # ========================================================================
    
    if len(inversiones_seleccionadas) > 0:
        st.divider()
        st.markdown("## 📊 Tus Resultados")
        
        # Validar que no exceda el monto total
        total_asignado = sum([inv["monto"] for inv in inversiones_seleccionadas.values()])
        
        if total_asignado > monto_total:
            st.error(f"⚠️ **Cuidado:** Has asignado ${total_asignado:,.0f} pero solo tienes ${monto_total:,.0f}. Ajusta los montos.")
            return
        
        diferencia = monto_total - total_asignado
        if diferencia > 0:
            st.warning(f"💡 Tienes **${diferencia:,.0f}** sin asignar. ¿Quieres agregarlo a alguna SOFIPO?")
        
        # Calcular rendimientos para cada inversión
        resultados = []
        proyecciones_todas = []
        
        for inversion_key, inversion in inversiones_seleccionadas.items():
            monto = inversion['monto']
            producto_info = inversion['producto_info']
            tipo = producto_info['tipo']
            
            # Determinar tasa efectiva
            if tipo == "vista_hibrida":
                # DiDi con estructura híbrida
                interes_anual = calcular_rendimiento_hibrido_didi(
                    monto,
                    producto_info['tasa_premium'],
                    producto_info['limite_premium'],
                    producto_info['tasa_base'],
                    365
                )
                tasa_efectiva = (interes_anual / monto) * 100
                tipo_interes = "Compuesto (Diario)"
                
            elif tipo == "vista":
                # A la vista con interés compuesto
                tasa_efectiva = producto_info['tasa_base']
                tipo_interes = "Compuesto (Diario)"
                
            elif tipo == "plazo":
                # Plazo fijo con interés simple
                tasa_efectiva = producto_info['tasa_base']
                tipo_interes = "Simple"
            
            # Calcular rendimientos
            dias_simulacion = periodo_simulacion * 30
            
            if tipo == "vista_hibrida":
                ganancia_periodo = calcular_rendimiento_hibrido_didi(
                    monto,
                    producto_info['tasa_premium'],
                    producto_info['limite_premium'],
                    producto_info['tasa_base'],
                    dias_simulacion
                )
            elif tipo == "vista" or tipo_interes == "Compuesto (Diario)":
                ganancia_periodo = calcular_interes_compuesto(monto, tasa_efectiva, dias_simulacion)
            else:
                ganancia_periodo = calcular_interes_simple(monto, tasa_efectiva, dias_simulacion)
            
            ganancia_dia = ganancia_periodo / dias_simulacion
            ganancia_mes = ganancia_dia * 30
            ganancia_anio = ganancia_dia * 365
            
            resultados.append({
                "SOFIPO": inversion['sofipo'],
                "Producto": inversion['producto'],
                "Monto Invertido": f"${monto:,.2f}",
                "GAT Efectivo": f"{tasa_efectiva:.2f}%",
                "Ganancia/Día": f"${ganancia_dia:.2f}",
                "Ganancia/Mes": f"${ganancia_mes:.2f}",
                "Ganancia/Año": f"${ganancia_anio:.2f}",
                f"Total ({periodo_simulacion} meses)": f"${monto + ganancia_periodo:,.2f}",
                "Ganancia Total": f"${ganancia_periodo:,.2f}",
                "Tipo Interés": tipo_interes
            })
            
            # Generar proyección mensual
            if tipo == "vista" or tipo_interes == "Compuesto (Diario)":
                proyeccion = generar_proyeccion_mensual(
                    monto, tasa_efectiva, "compuesto", periodo_simulacion
                )
            else:
                proyeccion = generar_proyeccion_mensual(
                    monto, tasa_efectiva, "simple", periodo_simulacion
                )
            
            proyeccion['SOFIPO'] = inversion_key
            proyecciones_todas.append(proyeccion)
        
        # ====================================================================
        # RESUMEN VISUAL SIMPLIFICADO
        # ====================================================================
        
        total_invertido = sum([inv['monto'] for inv in inversiones_seleccionadas.values()])
        
        # Calcular ganancia total ponderada
        ganancia_total = 0
        for resultado in resultados:
            ganancia_str = resultado["Ganancia Total"].replace("$", "").replace(",", "")
            ganancia_total += float(ganancia_str)
        
        rendimiento_ponderado = (ganancia_total / total_invertido) * (12 / periodo_simulacion) * 100
        
        # Métricas principales en cards grandes
        st.markdown("### 💰 Resultado de tu inversión")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Inviertes", f"${total_invertido:,.0f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric(f"Ganas en {periodo_simulacion} meses", f"${ganancia_total:,.0f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Terminas con", f"${total_invertido + ganancia_total:,.0f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # GAT Ponderado destacado
        st.success(f"📊 **Tu tasa promedio ponderada es: {rendimiento_ponderado:.2f}% anual**")
        
        # Tabla detallada en expander
        with st.expander("� Ver desglose detallado por SOFIPO"):
            df_resultados = pd.DataFrame(resultados)
            st.dataframe(df_resultados, width="stretch", hide_index=True)
        
        # ====================================================================
        # GRÁFICO PRINCIPAL
        # ====================================================================
        
        if len(proyecciones_todas) > 0:
            st.subheader("📈 Proyección de Crecimiento Total")
            
            # Combinar todas las proyecciones
            df_proyecciones_completo = pd.concat(proyecciones_todas, ignore_index=True)
            
            # Agrupar por mes y sumar TODO (capital + intereses de todas las SOFIPOs)
            df_total = df_proyecciones_completo.groupby('Mes').agg({
                'Capital Inicial': 'sum',
                'Intereses Generados': 'sum',
                'Total Acumulado': 'sum'
            }).reset_index()
            
            # Crear gráfico de línea única con el TOTAL
            fig = go.Figure()
            
            # Línea principal: Total acumulado de TODAS las inversiones
            fig.add_trace(go.Scatter(
                x=df_total['Mes'],
                y=df_total['Total Acumulado'],
                mode='lines+markers',
                name='Total Portafolio',
                line=dict(width=4, color='#667eea'),
                marker=dict(size=8),
                fill='tonexty',
                fillcolor='rgba(102, 126, 234, 0.1)',
                hovertemplate='<b>Total Acumulado</b><br>' +
                              'Mes: %{x}<br>' +
                              'Total: $%{y:,.0f}<br>' +
                              '<extra></extra>'
            ))
            
            # Línea de referencia: Capital inicial (sin intereses)
            fig.add_trace(go.Scatter(
                x=df_total['Mes'],
                y=[total_invertido] * len(df_total),
                mode='lines',
                name='Capital Inicial',
                line=dict(width=2, color='gray', dash='dash'),
                hovertemplate='Capital: $%{y:,.0f}<extra></extra>'
            ))
            
            fig.update_layout(
                title=dict(
                    text=f"Crecimiento total de tu portafolio a {periodo_simulacion} meses",
                    font=dict(size=18, color='#c9d1d9' if modo_oscuro else '#333333')
                ),
                xaxis_title="Meses",
                yaxis_title="Monto Total (MXN)",
                hovermode='x unified',
                template="plotly_dark" if modo_oscuro else "plotly_white",
                height=500,
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5,
                    bgcolor='rgba(22, 27, 34, 0.8)' if modo_oscuro else 'rgba(255, 255, 255, 0.8)',
                    bordercolor='#30363d' if modo_oscuro else '#e0e0e0',
                    borderwidth=1
                ),
                paper_bgcolor='#0d1117' if modo_oscuro else 'white',
                plot_bgcolor='#161b22' if modo_oscuro else '#f8f9fa',
                font=dict(color='#c9d1d9' if modo_oscuro else '#333333'),
                xaxis=dict(
                    gridcolor='#30363d' if modo_oscuro else '#e0e0e0',
                    color='#8b949e' if modo_oscuro else '#666666'
                ),
                yaxis=dict(
                    gridcolor='#30363d' if modo_oscuro else '#e0e0e0',
                    color='#8b949e' if modo_oscuro else '#666666'
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Gráfico de área apilada (Capital vs Intereses)
            st.subheader("💵 Desglose: Capital vs Intereses")
            
            # Sumar todos los capitales e intereses por mes
            df_agregado = df_proyecciones_completo.groupby('Mes').agg({
                'Capital Inicial': 'sum',
                'Intereses Generados': 'sum',
                'Total Acumulado': 'sum'
            }).reset_index()
            
            fig_area = go.Figure()
            
            fig_area.add_trace(go.Scatter(
                x=df_agregado['Mes'],
                y=df_agregado['Capital Inicial'],
                mode='lines',
                name='Capital Inicial',
                line=dict(width=0),
                fillcolor='rgba(102, 126, 234, 0.5)',
                fill='tozeroy',
                hovertemplate='Capital: $%{y:,.2f}<extra></extra>'
            ))
            
            fig_area.add_trace(go.Scatter(
                x=df_agregado['Mes'],
                y=df_agregado['Intereses Generados'],
                mode='lines',
                name='Intereses Generados',
                line=dict(width=0),
                fillcolor='rgba(118, 75, 162, 0.5)',
                fill='tonexty',
                hovertemplate='Intereses: $%{y:,.2f}<extra></extra>'
            ))
            
            fig_area.update_layout(
                title=dict(
                    text="Composición del patrimonio total",
                    font=dict(size=18, color='#c9d1d9' if modo_oscuro else '#333333')
                ),
                xaxis_title="Meses",
                yaxis_title="Monto (MXN)",
                hovermode='x unified',
                template="plotly_dark" if modo_oscuro else "plotly_white",
                height=400,
                paper_bgcolor='#0d1117' if modo_oscuro else 'white',
                plot_bgcolor='#161b22' if modo_oscuro else '#f8f9fa',
                font=dict(color='#c9d1d9' if modo_oscuro else '#333333'),
                xaxis=dict(
                    gridcolor='#30363d' if modo_oscuro else '#e0e0e0',
                    color='#8b949e' if modo_oscuro else '#666666'
                ),
                yaxis=dict(
                    gridcolor='#30363d' if modo_oscuro else '#e0e0e0',
                    color='#8b949e' if modo_oscuro else '#666666'
                )
            )
            
            st.plotly_chart(fig_area, use_container_width=True)
            st.subheader("📋 Desglose Mensual Detallado")
            
            for inversion_key, df_proyeccion in zip(
                df_proyecciones_completo['SOFIPO'].unique(),
                proyecciones_todas
            ):
                with st.expander(f"📊 {inversion_key}"):
                    # Formatear el dataframe
                    df_display = df_proyeccion.copy()
                    df_display['Capital Inicial'] = df_display['Capital Inicial'].apply(lambda x: f"${x:,.2f}")
                    df_display['Intereses Generados'] = df_display['Intereses Generados'].apply(lambda x: f"${x:,.2f}")
                    df_display['Total Acumulado'] = df_display['Total Acumulado'].apply(lambda x: f"${x:,.2f}")
                    df_display = df_display.drop('SOFIPO', axis=1)
                    
                    st.dataframe(df_display, width="stretch", hide_index=True)
        
        # ====================================================================
        # ANÁLISIS Y RECOMENDACIONES
        # ====================================================================
        
        st.divider()
        st.header("3️⃣ Análisis de Riesgo y Recomendaciones")
        
        # Realizar análisis de diversificación
        analisis = analizar_diversificacion(inversiones_seleccionadas)
        if analisis:
            recomendaciones = generar_recomendaciones(
                analisis, 
                rendimiento_ponderado,
                cumple_klar_plus,
                cumple_mercadopago,
                cumple_uala_plus
            )
            
            # Mostrar métricas de diversificación
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "🎯 SOFIPOs utilizadas",
                    f"{analisis['num_sofipos']}/7",
                    help="Número de SOFIPOs diferentes en tu portafolio"
                )
            
            with col2:
                st.metric(
                    "⚖️ Concentración máxima",
                    f"{analisis['max_concentracion']:.1f}%",
                    delta="Óptimo: <50%" if analisis['max_concentracion'] < 50 else "Alto riesgo",
                    delta_color="normal" if analisis['max_concentracion'] < 50 else "inverse"
                )
            
            with col3:
                st.metric(
                    "💧 Liquidez inmediata",
                    f"{analisis['porcentaje_liquido']:.1f}%",
                    help="Porcentaje disponible sin penalización"
                )
        
            # Gráfico de distribución
            st.subheader("📊 Distribución de tu portafolio")
            
            df_concentracion = pd.DataFrame([
                {"SOFIPO": k, "Porcentaje": v, "Monto": inversiones_seleccionadas[k]["monto"]}
                for k, v in analisis["concentraciones"].items()
                if v > 0
            ])
            
            fig_pie = px.pie(
                df_concentracion,
                values='Porcentaje',
                names='SOFIPO',
                title='Distribución por SOFIPO',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            fig_pie.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>' +
                              'Porcentaje: %{percent}<br>' +
                              '<extra></extra>'
            )
            
            fig_pie.update_layout(
                title=dict(
                    text='Distribución por SOFIPO',
                    font=dict(size=18, color='#c9d1d9' if modo_oscuro else '#333333')
                ),
                template="plotly_dark" if modo_oscuro else "plotly_white",
                paper_bgcolor='#0d1117' if modo_oscuro else 'white',
                plot_bgcolor='#161b22' if modo_oscuro else '#f8f9fa',
                font=dict(color='#c9d1d9' if modo_oscuro else '#333333'),
                legend=dict(
                    bgcolor='rgba(22, 27, 34, 0.8)' if modo_oscuro else 'rgba(255, 255, 255, 0.8)',
                    bordercolor='#30363d' if modo_oscuro else '#e0e0e0',
                    borderwidth=1
                )
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # Mostrar recomendaciones
            st.subheader("💡 Recomendaciones Personalizadas")
            
            for i, recomendacion in enumerate(recomendaciones, 1):
                if "✅" in recomendacion:
                    st.markdown(f'<div class="success-box">{recomendacion}</div>', unsafe_allow_html=True)
                elif "⚠️" in recomendacion or "🎯" in recomendacion:
                    st.markdown(f'<div class="warning-box">{recomendacion}</div>', unsafe_allow_html=True)
                else:
                    st.info(recomendacion)
        
        # ====================================================================
        # INFORMACIÓN ADICIONAL
        # ====================================================================
        
        st.divider()
        
        with st.expander("📖 Glosario y Conceptos Clave"):
            st.markdown("""
            **GAT Nominal**: Ganancia Anual Total antes de impuestos. Es la tasa de rendimiento anual.
            
            **GAT Real**: Ganancia Anual Total después de restar inflación.
            
            **Interés Simple**: Interés calculado solo sobre el capital inicial.
            
            **Interés Compuesto**: Interés calculado sobre capital + intereses previos.
            
            **IPAB**: Instituto para la Protección al Ahorro Bancario. Protege hasta 25,000 UDIs (~$200,000 MXN) por persona por institución.
            
            **SOFIPO**: Sociedad Financiera Popular regulada por CNBV.
            
            **Liquidez**: Facilidad para convertir la inversión en efectivo sin penalización.
            """)
        
        with st.expander("⚖️ Aspectos Legales y Fiscales"):
            st.markdown("""
            ### Regulación
            - Todas las SOFIPOs mostradas están reguladas por CNBV
            - Supervisadas por Banco de México y CONDUSEF
            - Sujetas a la Ley de Ahorro y Crédito Popular
            
            ### Protección IPAB
            - Cobertura: Hasta 25,000 UDIs por persona por institución
            - Equivalente aproximado: ~$200,000 MXN (varía con UDI)
            - Aplica a depósitos en SOFIPOs reguladas
            
            ### Impuestos
            - Los intereses generados están sujetos a ISR
            - Las SOFIPOs retienen impuestos automáticamente
            - Tasa de retención: 1.04% mensual (aprox)
            - Declaración anual puede generar saldo a favor
            
            **Nota**: Consulta con un contador para tu situación específica.
            """)
    
    else:
        st.info("👆 Selecciona al menos una SOFIPO arriba para comenzar la simulación")
        
        # Mostrar tabla comparativa de tasas
        st.subheader("📊 Tabla Comparativa de Tasas (Referencia)")
        
        tabla_comparativa = []
        for sofipo_name, sofipo_data in SOFIPOS_DATA.items():
            for producto_name, producto_info in sofipo_data['productos'].items():
                tabla_comparativa.append({
                    "SOFIPO": f"{sofipo_data['logo']} {sofipo_name}",
                    "Producto": producto_name,
                    "GAT Nominal": f"{producto_info['tasa_base']}%",
                    "Liquidez": producto_info['liquidez'],
                    "Mínimo": f"${producto_info['minimo']:,}"
                })
        
        df_comparativa = pd.DataFrame(tabla_comparativa)
        st.dataframe(df_comparativa, width="stretch", hide_index=True)
    
    # Footer
    st.divider()
    st.markdown("""
    ---
    <div style='text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin-top: 2rem;'>
        <h3 style='margin: 0; font-weight: 700;'>💰 Simulador de Inversiones Multi-SOFIPO</h3>
        <p style='margin: 1rem 0; opacity: 0.9;'>⚠️ Este simulador es una herramienta educativa. Las tasas pueden variar.<br>
        Verifica siempre las condiciones vigentes con cada institución.</p>
        <p style='margin: 0.5rem 0;'><span class="badge">📅 Tasas actualizadas: Noviembre 2025</span></p>
        <p style='margin-top: 1rem; font-size: 1.1rem;'>Desarrollado con ❤️ para inversionistas mexicanos 🇲🇽</p>
    </div>
    """, unsafe_allow_html=True)


    # Fecha de última actualización
    st.markdown("---")
    st.markdown('<div style="text-align: center; font-size: 0.7rem; color: #999; padding: 1rem;">📅 Última actualización de tasas: 21 de Noviembre, 2025</div>', unsafe_allow_html=True)
if __name__ == "__main__":
    main()
