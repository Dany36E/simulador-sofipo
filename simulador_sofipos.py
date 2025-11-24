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
        "logo": "💜",
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
        "logo": "🚗",
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
        "logo": "🟦",
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
        "logo": "⚡",
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
        "logo": "🔴",
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
        "logo": "💙",
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
        "logo": "🟢",
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
# FUNCIONES DE CÁLCULO FINANCIERO
# ============================================================================
# 
# CONVENCIONES FINANCIERAS DEL SISTEMA:
# -------------------------------------
# 1. AÑO COMERCIAL: 360 días (12 meses × 30 días)
#    - Estándar bancario mexicano para cálculos de interés
#    - Usado en: interés simple, conversión de periodos
#
# 2. CAPITALIZACIÓN DIARIA: 365 días/año
#    - Para productos a la vista (Nu, Klar, DiDi, Stori, Ualá, Mercado Pago)
#    - Fórmula: M = C * (1 + r/365)^días
#
# 3. CAPITALIZACIÓN MENSUAL: 12 periodos/año
#    - Para algunos productos según especificaciones
#    - Fórmula: M = C * (1 + r/12)^(n*t) donde t en años
#
# 4. INTERÉS SIMPLE: Para plazos fijos
#    - Fórmula: I = C * r * (días/360)
#    - Sin capitalización, interés se paga al vencimiento
#
# 5. RENDIMIENTO PONDERADO:
#    - Tasa efectiva anual considerando todas las inversiones
#    - Para periodos < 12 meses: tasa equivalente anualizada
#    - Fórmula: r_anual = (1 + r_periodo)^(12/periodo) - 1
#
# ============================================================================

def calcular_rendimiento_hibrido_didi(monto, tasa_premium, limite_premium, tasa_base, dias):
    """
    Calcula el rendimiento con estructura híbrida de DiDi con capitalización diaria
    16% sobre primeros $10,000 y tasa base sobre el resto
    
    CORRECCIÓN FINANCIERA: DiDi capitaliza diariamente, no usa interés simple
    """
    if monto <= limite_premium:
        # Todo el monto está en tasa premium con capitalización diaria
        tasa_decimal = tasa_premium / 100
        monto_final = monto * (1 + tasa_decimal / 365) ** dias
        return monto_final - monto
    else:
        # Capitalización diaria separada para cada tramo
        tasa_premium_decimal = tasa_premium / 100
        tasa_base_decimal = tasa_base / 100
        
        # Interés compuesto sobre el límite premium
        monto_final_premium = limite_premium * (1 + tasa_premium_decimal / 365) ** dias
        interes_premium = monto_final_premium - limite_premium
        
        # Interés compuesto sobre el excedente
        excedente = monto - limite_premium
        monto_final_excedente = excedente * (1 + tasa_base_decimal / 365) ** dias
        interes_excedente = monto_final_excedente - excedente
        
        return interes_premium + interes_excedente

def calcular_interes_compuesto(capital, tasa_anual, dias, compounding="diario"):
    """
    Calcula interés compuesto con diferentes frecuencias de capitalización
    
    Fórmula: M = C * (1 + r/n)^(n*t)
    Donde:
    - M = Monto final
    - C = Capital inicial
    - r = Tasa anual (decimal)
    - n = Número de capitalizaciones por año
    - t = Tiempo en años
    
    CORRECCIÓN FINANCIERA: Uso de fórmulas estándar de interés compuesto
    """
    tasa_decimal = tasa_anual / 100
    
    if compounding == "diario":
        # Capitalización diaria: n=365, periodos en días
        n = 365
        t = dias / 365  # Tiempo en años
        monto_final = capital * (1 + tasa_decimal / n) ** (n * t)
    elif compounding == "mensual":
        # Capitalización mensual: n=12, periodos en meses
        n = 12
        t = dias / 360  # Usar año comercial (360 días) como hace el sistema
        monto_final = capital * (1 + tasa_decimal / n) ** (n * t)
    else:  # anual
        # Capitalización anual
        t = dias / 365
        monto_final = capital * (1 + tasa_decimal) ** t
    
    return monto_final - capital

def calcular_interes_simple(capital, tasa_anual, dias):
    """
    Calcula interés simple para inversiones a plazo fijo
    
    Fórmula: I = C * r * t
    Donde:
    - I = Interés
    - C = Capital
    - r = Tasa anual (decimal)
    - t = Tiempo en años
    
    CORRECCIÓN FINANCIERA: Usar año comercial (360 días) para consistencia
    con el estándar bancario mexicano
    """
    tasa_decimal = tasa_anual / 100
    interes = capital * tasa_decimal * (dias / 360)  # Año comercial
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

def calcular_distribucion_aportaciones(inversiones_seleccionadas, aportacion_monto, estrategia, total_invertido):
    """
    Calcula cómo distribuir cada aportación entre los productos, respetando límites máximos
    
    Args:
        inversiones_seleccionadas: Dict con las inversiones actuales
        aportacion_monto: Monto de cada aportación
        estrategia: Estrategia de distribución seleccionada
        total_invertido: Capital inicial total
    
    Returns:
        Dict con la distribución de la aportación y lista de mensajes explicativos
    """
    distribucion = {}
    mensajes = []
    monto_restante = aportacion_monto
    
    if estrategia == "Misma distribución que capital inicial":
        # Intentar distribuir proporcionalmente, respetando límites
        for sofipo_key, inv_data in inversiones_seleccionadas.items():
            porcentaje = (inv_data['monto'] / total_invertido) if total_invertido > 0 else 0
            monto_proporcional = aportacion_monto * porcentaje
            
            # Verificar si el producto tiene límite máximo
            producto_info = inv_data['producto_info']
            # Buscar limite_maximo, limite_max, o limite_premium (para DiDi)
            limite_maximo = producto_info.get('limite_maximo', producto_info.get('limite_max', producto_info.get('limite_premium', None)))
            monto_actual = inv_data['monto']
            
            if limite_maximo and monto_actual >= limite_maximo:
                # Ya alcanzó el límite, no puede recibir más
                distribucion[sofipo_key] = 0
                mensajes.append(f"⚠️ {inv_data['sofipo']} - {inv_data['producto']}: Ya alcanzó el límite de ${limite_maximo:,.0f}")
            elif limite_maximo and (monto_actual + monto_proporcional) > limite_maximo:
                # Puede recibir solo hasta el límite
                monto_asignable = limite_maximo - monto_actual
                distribucion[sofipo_key] = monto_asignable
                mensajes.append(f"⚠️ {inv_data['sofipo']} - {inv_data['producto']}: Solo puede recibir ${monto_asignable:,.0f} más (límite: ${limite_maximo:,.0f})")
            else:
                # Puede recibir el monto proporcional completo
                distribucion[sofipo_key] = monto_proporcional
                mensajes.append(f"✅ {inv_data['sofipo']} - {inv_data['producto']}: ${monto_proporcional:,.0f} ({porcentaje*100:.1f}%)")
        
        # Si hay sobrante por límites alcanzados, redistribuir proporcionalmente entre los que pueden recibir más
        monto_asignado = sum(distribucion.values())
        if monto_asignado < aportacion_monto:
            sobrante = aportacion_monto - monto_asignado
            productos_disponibles = {k: v for k, v in distribucion.items() if v > 0}
            
            if productos_disponibles:
                mensajes.append(f"\n💡 Redistribuyendo ${sobrante:,.0f} sobrante entre productos disponibles:")
                for sofipo_key in productos_disponibles:
                    porcentaje_disponible = distribucion[sofipo_key] / monto_asignado if monto_asignado > 0 else 0
                    distribucion[sofipo_key] += sobrante * porcentaje_disponible
                    mensajes.append(f"   • {inversiones_seleccionadas[sofipo_key]['sofipo']}: +${sobrante * porcentaje_disponible:,.0f}")
    
    elif estrategia == "Solo productos de mayor rendimiento":
        # Ordenar por tasa y llenar hasta el límite
        inversiones_ordenadas = sorted(
            inversiones_seleccionadas.items(),
            key=lambda x: x[1]['producto_info']['tasa_base'],
            reverse=True
        )
        
        mensajes.append("📈 Priorizando productos con mejores tasas:")
        for sofipo_key, inv_data in inversiones_ordenadas:
            if monto_restante <= 0:
                break
            
            producto_info = inv_data['producto_info']
            limite_maximo = producto_info.get('limite_maximo', producto_info.get('limite_max', producto_info.get('limite_premium', None)))
            monto_actual = inv_data['monto']
            tasa = producto_info['tasa_base']
            
            if limite_maximo and monto_actual >= limite_maximo:
                distribucion[sofipo_key] = 0
                mensajes.append(f"⚠️ {inv_data['sofipo']} ({tasa}%): Límite alcanzado")
            elif limite_maximo:
                espacio_disponible = limite_maximo - monto_actual
                monto_asignar = min(monto_restante, espacio_disponible)
                distribucion[sofipo_key] = monto_asignar
                monto_restante -= monto_asignar
                mensajes.append(f"✅ {inv_data['sofipo']} ({tasa}%): ${monto_asignar:,.0f}")
            else:
                # Sin límite, asignar todo lo que queda
                distribucion[sofipo_key] = monto_restante
                mensajes.append(f"✅ {inv_data['sofipo']} ({tasa}%): ${monto_restante:,.0f}")
                monto_restante = 0
    
    else:  # Distribución inteligente automática
        mensajes.append("🤖 Aplicando distribución inteligente (simulada):")
        mensajes.append("   • Maximizando rendimiento")
        mensajes.append("   • Respetando límites por producto")
        mensajes.append("   • Manteniendo diversificación")
        
        # Por ahora, usar la misma lógica que "mayor rendimiento"
        inversiones_ordenadas = sorted(
            inversiones_seleccionadas.items(),
            key=lambda x: x[1]['producto_info']['tasa_base'],
            reverse=True
        )
        
        for sofipo_key, inv_data in inversiones_ordenadas:
            if monto_restante <= 0:
                break
            
            producto_info = inv_data['producto_info']
            limite_maximo = producto_info.get('limite_maximo', producto_info.get('limite_max', producto_info.get('limite_premium', None)))
            monto_actual = inv_data['monto']
            
            if limite_maximo and monto_actual >= limite_maximo:
                distribucion[sofipo_key] = 0
            elif limite_maximo:
                espacio_disponible = limite_maximo - monto_actual
                monto_asignar = min(monto_restante, espacio_disponible)
                distribucion[sofipo_key] = monto_asignar
                monto_restante -= monto_asignar
            else:
                distribucion[sofipo_key] = monto_restante
                monto_restante = 0
    
    return distribucion, mensajes

def generar_proyeccion_con_aportaciones(
    capital_inicial, 
    tasa_anual, 
    tipo_calculo, 
    meses=12, 
    aportacion=0, 
    frecuencia="Mensual"
):
    """
    Genera proyección considerando aportaciones recurrentes
    
    Args:
        capital_inicial: Capital inicial a invertir
        tasa_anual: Tasa de interés anual promedio ponderada
        tipo_calculo: "compuesto" o "simple"
        meses: Número de meses a simular
        aportacion: Monto de cada aportación
        frecuencia: "Semanal", "Quincenal", o "Mensual"
    
    Returns:
        DataFrame con proyección detallada mes a mes
    """
    proyeccion = []
    
    # Calcular número de aportaciones por mes según frecuencia
    aportaciones_por_mes = {
        "Semanal": 4.33,      # ~4.33 semanas por mes
        "Quincenal": 2,
        "Mensual": 1
    }
    
    aportacion_mensual_equivalente = aportacion * aportaciones_por_mes.get(frecuencia, 1)
    
    capital_acumulado = capital_inicial
    total_aportaciones = 0
    
    for mes in range(meses + 1):
        # Calcular intereses del mes sobre el capital acumulado
        if mes > 0:
            dias_mes = 30
            if tipo_calculo == "compuesto":
                intereses_mes = calcular_interes_compuesto(capital_acumulado, tasa_anual, dias_mes)
            else:
                intereses_mes = calcular_interes_simple(capital_acumulado, tasa_anual, dias_mes)
            
            capital_acumulado += intereses_mes
            
            # Agregar aportación al final del mes
            capital_acumulado += aportacion_mensual_equivalente
            total_aportaciones += aportacion_mensual_equivalente
        
        # Calcular intereses totales acumulados
        intereses_totales = capital_acumulado - capital_inicial - total_aportaciones
        
        proyeccion.append({
            "Mes": mes,
            "Capital Inicial": capital_inicial,
            "Aportaciones Acumuladas": total_aportaciones,
            "Intereses Generados": intereses_totales,
            "Total Acumulado": capital_acumulado
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
    Genera recomendaciones personalizadas estructuradas: alertas críticas y oportunidades
    """
    if analisis is None:
        return {"alertas": [], "oportunidades": []}
    
    alertas = []
    oportunidades = []
    
    # ========================================================================
    # ALERTAS CRÍTICAS (solo problemas importantes)
    # ========================================================================
    
    # Alerta de concentración extrema
    if analisis["max_concentracion"] > 85:
        alertas.append({
            "tipo": "critico",
            "emoji": "⚠️",
            "titulo": "**Concentración Elevada**",
            "mensaje": f"{analisis['max_concentracion']:.1f}% en una sola institución. Lo ideal es no superar el 40-50% por SOFIPO."
        })
    
    # Alerta de liquidez muy baja
    if analisis["porcentaje_liquido"] < 20:
        alertas.append({
            "tipo": "warning",
            "emoji": "⚠️",
            "titulo": "**Baja Liquidez**",
            "mensaje": f"Solo {analisis['porcentaje_liquido']:.1f}% está disponible inmediatamente. Considera mantener al menos 20-30% en inversiones líquidas para emergencias."
        })
    
    # Alerta de muy poca diversificación
    if analisis["num_sofipos"] == 1 and analisis["total_invertido"] > 50000:
        alertas.append({
            "tipo": "warning",
            "emoji": "⚠️",
            "titulo": "**Alta Concentración**",
            "mensaje": f"Inviertes en una sola SOFIPO. Considera diversificar en al menos 3-4 instituciones para reducir riesgo."
        })
    
    # ========================================================================
    # OPORTUNIDADES (productos que NO tiene y podrían mejorar rendimiento)
    # ========================================================================
    
    sofipos_actuales = [k for k, v in analisis["concentraciones"].items() if v > 0]
    
    # 1. Nu México Cajita Turbo - 15% liquidez inmediata (SIEMPRE disponible)
    if not any("Nu México" in s and "Turbo" in s for s in sofipos_actuales):
        oportunidades.append({
            "orden": 1,
            "tasa": 15.0,
            "sofipo": "Nu México",
            "producto": "Cajita Turbo",
            "detalle": "15% hasta $25k con liquidez inmediata",
            "requisito": None
        })
    
    # 2. DiDi Ahorro - 16% primeros $10k (SIEMPRE disponible)
    if not any("DiDi" in s for s in sofipos_actuales):
        oportunidades.append({
            "orden": 2,
            "tasa": 16.0,
            "sofipo": "DiDi",
            "producto": "Ahorro",
            "detalle": "16% primeros $10k, luego 8.5%",
            "requisito": None
        })
    
    # 3. Ualá Plus vs Base (depende de si cumple requisitos)
    if not any("Ualá" in s for s in sofipos_actuales):
        if cumple_uala:
            oportunidades.append({
                "orden": 3,
                "tasa": 16.0,
                "sofipo": "Ualá",
                "producto": "Plus",
                "detalle": "16% hasta $50k",
                "requisito": "✅ Cumples requisito de $3k/mes"
            })
        else:
            oportunidades.append({
                "orden": 7,
                "tasa": 7.75,
                "sofipo": "Ualá",
                "producto": "Base",
                "detalle": "7.75% hasta $30k",
                "requisito": None
            })
    
    # 4. Klar Max vs Cuenta (depende de si tiene tarjeta Plus/Platino)
    if not any("Klar" in s for s in sofipos_actuales):
        if cumple_klar:
            oportunidades.append({
                "orden": 4,
                "tasa": 15.0,
                "sofipo": "Klar",
                "producto": "Inversión Max",
                "detalle": "15% con liquidez inmediata",
                "requisito": "✅ Tienes tarjeta Plus/Platino"
            })
        else:
            oportunidades.append({
                "orden": 8,
                "tasa": 8.5,
                "sofipo": "Klar",
                "producto": "Cuenta",
                "detalle": "8.5% sin requisitos",
                "requisito": None
            })
    
    # 5. Mercado Pago - 13% (solo si cumple requisitos)
    if cumple_mp and not any("Mercado Pago" in s for s in sofipos_actuales):
        oportunidades.append({
            "orden": 5,
            "tasa": 13.0,
            "sofipo": "Mercado Pago",
            "producto": "Rendimientos",
            "detalle": "13% hasta $25k",
            "requisito": "✅ Cumples requisito de $3k/mes"
        })
    
    # 6. Stori 90 días - 10% plazo (SIEMPRE disponible)
    if not any("Stori" in s and "90" in s for s in sofipos_actuales):
        oportunidades.append({
            "orden": 6,
            "tasa": 10.0,
            "sofipo": "Stori",
            "producto": "90 días",
            "detalle": "10% a plazo fijo (sin requisitos)",
            "requisito": None
        })
    
    # Ordenar por tasa descendente y tomar top 3
    oportunidades.sort(key=lambda x: (-x["tasa"], x["orden"]))
    oportunidades = oportunidades[:3]
    
    return {"alertas": alertas, "oportunidades": oportunidades}

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
            uploaded_file = st.file_uploader("📂 Cargar desde archivo", type=['json'], label_visibility="collapsed")
            if uploaded_file is not None:
                try:
                    simulacion_data = json.load(uploaded_file)
                    if cargar_simulacion(simulacion_data):
                        st.success(f"✅ Simulación cargada: {simulacion_data.get('fecha_guardado', 'Sin fecha')}")
                        st.rerun()
                except Exception as e:
                    st.error(f"? Error al cargar archivo: {str(e)}")
        
        # Mostrar información de la última simulación guardada
        if "ultima_simulacion" in st.session_state:
            sim = st.session_state["ultima_simulacion"]
            st.info(f"ℹ️ **Última simulación guardada:** {sim['fecha_guardado']} | Monto: ${sim['monto_total']:,.0f} | Inversiones: {len(sim['inversiones'])}")
    
    st.divider()
    # ========================================================================
    # APLICAR ESTRATEGIA OBJETIVO SI ESTÁ PENDIENTE
    # ========================================================================
    
    if "estrategia_objetivo_pendiente" in st.session_state:
        estrategia = st.session_state["estrategia_objetivo_pendiente"]
        
        # SIEMPRE actualizar el capital cuando se aplica una estrategia
        st.session_state["monto_total_input"] = estrategia["capital"]
        
        # Limpiar selecciones previas
        for sofipo in ["Nu México", "DiDi", "Stori", "Klar", "Ualá", "Mercado Pago", "Finsus"]:
            st.session_state[f"check_{sofipo}"] = False
        
        # Aplicar cada producto de la distribución
        for item in estrategia["distribucion"]:
            sofipo_nombre = item["sofipo"]
            producto_nombre = item["producto"]
            monto = item["monto"]
            
            # Activar el checkbox de la SOFIPO
            st.session_state[f"check_{sofipo_nombre}"] = True
            
            # Validar que el producto existe en esta SOFIPO
            if sofipo_nombre in SOFIPOS_DATA:
                productos_disponibles = list(SOFIPOS_DATA[sofipo_nombre]['productos'].keys())
                
                # Si el producto existe exactamente, usarlo
                if producto_nombre in productos_disponibles:
                    producto_valido = producto_nombre
                else:
                    # Si no existe, intentar encontrar uno similar o usar el primero
                    producto_valido = productos_disponibles[0]
                    # Buscar por coincidencia parcial
                    for prod in productos_disponibles:
                        if producto_nombre.lower() in prod.lower() or prod.lower() in producto_nombre.lower():
                            producto_valido = prod
                            break
                
                # Seleccionar el producto validado
                st.session_state[f"prod_{sofipo_nombre}"] = producto_valido
                
                # Asignar el monto con el nombre validado
                st.session_state[f"monto_{sofipo_nombre}_{producto_valido}"] = int(monto)
        
        # Limpiar la estrategia pendiente
        del st.session_state["estrategia_objetivo_pendiente"]
        
        st.success(f" **Estrategia aplicada:** ${estrategia['capital']:,.0f} distribuidos en {len(estrategia['distribucion'])} productos")
    
    
    # ========================================================================
    # CONFIGURACIÓN RÁPIDA
    # ========================================================================
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎯 ¿Cuánto quieres invertir?")
        monto_total = st.number_input(
            "Monto total disponible (MXN)",
            min_value=0,
            value=st.session_state.get("monto_total_input", 50000),
            step=5000,
            help="Capital inicial disponible. Puedes empezar desde $0 si solo quieres simular aportaciones recurrentes",
            key="monto_total_input"
        )
        
        # Mostrar mensaje informativo si está en $0
        if monto_total == 0:
            st.info("💡 **Modo: Solo Aportaciones Recurrentes** - Activa las aportaciones abajo para simular crecimiento desde cero")
    
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
    
    # ========================================================================
    # APORTACIONES RECURRENTES
    # ========================================================================
    
    st.markdown("### 💰 Aportaciones Recurrentes (Opcional)")
    
    col_activar, col_monto, col_frecuencia, col_estrategia = st.columns([1.5, 2, 2, 2.5])
    
    with col_activar:
        aportaciones_activas = st.checkbox(
            "Activar aportaciones",
            value=st.session_state.get("aportaciones_activas", False),
            help="Simula el efecto de agregar dinero periódicamente",
            key="aportaciones_activas"
        )
    
    with col_monto:
        aportacion_monto = st.number_input(
            "Monto por aportación",
            min_value=0,
            value=st.session_state.get("aportacion_monto", 2000),
            step=500,
            disabled=not aportaciones_activas,
            key="aportacion_monto"
        )
    
    with col_frecuencia:
        frecuencia_aportacion = st.selectbox(
            "Frecuencia",
            options=["Semanal", "Quincenal", "Mensual"],
            index=2,  # Default: Mensual
            disabled=not aportaciones_activas,
            key="frecuencia_aportacion"
        )
    
    with col_estrategia:
        estrategia_aportacion = st.selectbox(
            "Estrategia de inversión",
            options=[
                "Misma distribución que capital inicial",
                "Solo productos de mayor rendimiento",
                "Distribución inteligente automática"
            ],
            index=0,
            disabled=not aportaciones_activas,
            help="Define cómo se invertirán las aportaciones recurrentes",
            key="estrategia_aportacion"
        )
    
    st.divider()
    
    # ========================================================================
    # PREFERENCIAS DEL USUARIO
    # ========================================================================
    
    st.markdown("### ⚙️ Tus preferencias de inversión")
    
    with st.expander("✅ Configurar requisitos que SÍ puedo cumplir", expanded=False):
        st.markdown("**Marca las opciones que SÍ cumples para obtener mejores recomendaciones:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            cumple_klar_plus = st.checkbox(
                "💳 Tengo membresía Klar Plus o Platino",
                value=st.session_state.get("cumple_klar_plus", False),
                help="Necesaria para Klar Inversión Max (15%)",
                key="cumple_klar_plus"
            )
            
            cumple_mercadopago = st.checkbox(
                "💰 Puedo depositar $3,000/mes en Mercado Pago",
                value=st.session_state.get("cumple_mercadopago", False),
                help="Necesario para obtener el 13% en Mercado Pago",
                key="cumple_mercadopago"
            )
        
        with col2:
            cumple_uala_plus = st.checkbox(
                "💸 Puedo consumir $3k/mes con Ualá o domiciliar nómina",
                value=st.session_state.get("cumple_uala_plus", False),
                help="Necesario para Ualá Plus (16% hasta $50k)",
                key="cumple_uala_plus"
            )
    
    with st.expander("🚫 Excluir SOFIPOs que NO quiero usar", expanded=False):
        st.markdown("**Desmarca las SOFIPOs que NO quieres que aparezcan en las recomendaciones:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            usa_nu = st.checkbox("💜 Nu México", value=True, key="usa_nu")
            usa_didi = st.checkbox("🚗 DiDi", value=True, key="usa_didi")
            usa_stori = st.checkbox("🟦 Stori", value=True, key="usa_stori")
            usa_klar = st.checkbox("⚡ Klar", value=True, key="usa_klar")
        
        with col2:
            usa_uala = st.checkbox("🔴 Ualá", value=True, key="usa_uala")
            usa_mp = st.checkbox("💙 Mercado Pago", value=True, key="usa_mp")
            usa_finsus = st.checkbox("🟢 Finsus", value=True, key="usa_finsus")
    
    with st.expander("💧 Preferencias de liquidez", expanded=False):
        st.markdown("**Configura si solo quieres productos con disponibilidad inmediata:**")
        solo_vista = st.checkbox(
            "💧 Solo productos A LA VISTA (sin plazo fijo)",
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
            st.markdown("#### 🎯 Tu Meta de Ganancia")
            objetivo_tipo = st.radio(
                "Quiero ganar:",
                options=["mensual", "anual"],
                format_func=lambda x: "📅 Por mes" if x == "mensual" else "📅 Por año",
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
            st.markdown("#### ⚙️ Perfil de Inversión")
            st.info("ℹ️ La calculadora usará **tus preferencias actuales** (SOFIPOs excluidas, requisitos, liquidez)")
        
        # Convertir ganancia a anual
        if objetivo_tipo == "mensual":
            ganancia_anual_objetivo = objetivo_ganancia * 12
        else:
            ganancia_anual_objetivo = objetivo_ganancia
        
        # Función para calcular distribución ÓPTIMA con TODAS las tasas disponibles
        def calcular_tasa_ponderada_real(monto_prueba):
            """Calcula la mejor distribución usando TODOS los productos del catálogo"""
            
            # Construir catálogo completo de productos disponibles
            productos_disponibles = []
            
            # Nu México
            if usa_nu:
                productos_disponibles.append({"sofipo": "Nu México", "producto": "Cajita Turbo", "tasa": 15.0, "maximo": 25000, "tipo": "vista", "requisito": None})
                productos_disponibles.append({"sofipo": "Nu México", "producto": "Dinero en Cajita", "tasa": 7.5, "maximo": None, "tipo": "vista", "requisito": None})
            
            # DiDi
            if usa_didi:
                productos_disponibles.append({"sofipo": "DiDi", "producto": "DiDi Ahorro (primeros $10k)", "tasa": 16.0, "maximo": 10000, "tipo": "vista", "requisito": None})
                productos_disponibles.append({"sofipo": "DiDi", "producto": "DiDi Ahorro (después de $10k)", "tasa": 8.5, "maximo": None, "tipo": "vista", "requisito": None})
            
            # Stori
            if usa_stori and not solo_vista:
                productos_disponibles.append({"sofipo": "Stori", "producto": "28 días", "tasa": 9.5, "maximo": None, "tipo": "plazo", "requisito": None})
                productos_disponibles.append({"sofipo": "Stori", "producto": "90 días", "tasa": 10.0, "maximo": None, "tipo": "plazo", "requisito": None})
                productos_disponibles.append({"sofipo": "Stori", "producto": "180 días", "tasa": 10.5, "maximo": None, "tipo": "plazo", "requisito": None})
                productos_disponibles.append({"sofipo": "Stori", "producto": "360 días", "tasa": 11.0, "maximo": None, "tipo": "plazo", "requisito": None})
            
            # Klar
            if usa_klar:
                productos_disponibles.append({"sofipo": "Klar", "producto": "Cuenta (Base)", "tasa": 8.5, "maximo": None, "tipo": "vista", "requisito": None})
                if cumple_klar_plus:
                    productos_disponibles.append({"sofipo": "Klar", "producto": "Inversión Flexible Max", "tasa": 15.0, "maximo": None, "tipo": "vista", "requisito": "Klar Plus"})
            
            # Ualá
            if usa_uala:
                productos_disponibles.append({"sofipo": "Ualá", "producto": "Cuenta Base", "tasa": 7.75, "maximo": 30000, "tipo": "vista", "requisito": None})
                if cumple_uala_plus:
                    productos_disponibles.append({"sofipo": "Ualá", "producto": "Cuenta Plus", "tasa": 16.0, "maximo": 50000, "tipo": "vista", "requisito": "Ualá Plus"})
            
            # Mercado Pago
            if usa_mp:
                if cumple_mercadopago:
                    productos_disponibles.append({"sofipo": "Mercado Pago", "producto": "Cuenta Remunerada", "tasa": 13.0, "maximo": 25000, "tipo": "vista", "requisito": "$3k/mes"})
                else:
                    productos_disponibles.append({"sofipo": "Mercado Pago", "producto": "Cuenta Remunerada Base", "tasa": 10.0, "maximo": None, "tipo": "vista", "requisito": None})
            
            # Finsus
            if usa_finsus and not solo_vista:
                productos_disponibles.append({"sofipo": "Finsus", "producto": "Apartado 28 días", "tasa": 9.5, "maximo": None, "tipo": "plazo", "requisito": None})
                productos_disponibles.append({"sofipo": "Finsus", "producto": "Apartado 91 días", "tasa": 10.09, "maximo": None, "tipo": "plazo", "requisito": None})
                productos_disponibles.append({"sofipo": "Finsus", "producto": "Apartado 360 días", "tasa": 10.09, "maximo": None, "tipo": "plazo", "requisito": None})
            
            if not productos_disponibles:
                return 0, []
            
            # Ordenar productos por tasa (de mayor a menor)
            productos_ordenados = sorted(productos_disponibles, key=lambda x: x["tasa"], reverse=True)
            
            # Distribuir el capital en los productos con mejores tasas
            distribucion = []
            saldo = monto_prueba
            
            for producto in productos_ordenados:
                if saldo <= 0:
                    break
                
                if producto["maximo"] is not None:
                    monto_asignar = min(producto["maximo"], saldo)
                else:
                    # Si no tiene máximo, asignar todo el saldo restante
                    monto_asignar = saldo
                
                if monto_asignar > 0:
                    distribucion.append({
                        "sofipo": producto["sofipo"],
                        "producto": producto["producto"],
                        "monto": monto_asignar,
                        "tasa": producto["tasa"],
                        "tipo": producto["tipo"],
                        "requisito": producto["requisito"]
                    })
                    saldo -= monto_asignar
                    
                    # Si el producto no tiene máximo, ya asignamos todo
                    if producto["maximo"] is None:
                        break
            
            # Calcular tasa ponderada usando el MISMO método que los resultados
            if distribucion:
                rendimiento_total = 0
                dias_simulacion = 12 * 30  # 360 días (igual que en los resultados)
                for d in distribucion:
                    # Usar el mismo cálculo que en la simulación principal
                    interes = calcular_interes_compuesto(d["monto"], d["tasa"], dias_simulacion)
                    rendimiento_total += interes
                tasa_ponderada = (rendimiento_total / monto_prueba) * 100 if monto_prueba > 0 else 0
                return tasa_ponderada, distribucion
            else:
                return 0, []
        
        # Calcular tasa ponderada de referencia con $100k
        tasa_referencia, _ = calcular_tasa_ponderada_real(100000)
        
        if tasa_referencia == 0:
            st.error("? No hay SOFIPOs disponibles con tu configuración actual. Activa al menos una SOFIPO.")
            capital_necesario = 0
            tasa_real = 0
            distribucion_final = []
            ganancia_anual_real = 0
            ganancia_mensual_real = 0
        else:
            # Estimación inicial simple
            capital_estimado = (ganancia_anual_objetivo / tasa_referencia) * 100
            
            # Buscar el capital necesario mediante aproximación binaria
            capital_min = max(1000, capital_estimado * 0.5)
            capital_max = capital_estimado * 2
            capital_necesario = capital_estimado
            iteraciones = 0
            max_iteraciones = 30
            
            while iteraciones < max_iteraciones and capital_max - capital_min > 10:
                capital_prueba = (capital_min + capital_max) / 2
                tasa_ponderada, dist = calcular_tasa_ponderada_real(capital_prueba)
                
                ganancia_estimada = capital_prueba * tasa_ponderada / 100
                
                diferencia = abs(ganancia_estimada - ganancia_anual_objetivo)
                
                if diferencia < 10:  # Precisión de $10
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
        
        if tasa_referencia > 0:
            st.markdown("### 🎯 Resultado de tu Objetivo (Con Tasas Reales)")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "💰 Capital Necesario",
                    f"${capital_necesario:,.0f}",
                    help="Monto que necesitas invertir"
                )
            
            with col2:
                st.metric(
                    "💵 Ganancia Anual",
                    f"${ganancia_anual_real:,.0f}",
                    delta=f"{tasa_real:.2f}%"
                )
            
            with col3:
                st.metric(
                    "📅 Ganancia Mensual",
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
                    # Calcular ganancia con el mismo método que los resultados (360 días)
                    dias_simulacion = 12 * 30
                    ganancia_item = calcular_interes_compuesto(item["monto"], item["tasa"], dias_simulacion)
                    
                    # Construir descripción
                    nombre_completo = f"{item['sofipo']} - {item['producto']}"
                    tipo_icon = "💧" if item.get("tipo") == "vista" else "📅"
                    requisito_text = f" ✅ {item['requisito']}" if item.get("requisito") else ""
                    
                    st.markdown(f"{i}. {tipo_icon} **{nombre_completo}** {requisito_text}")
                    st.markdown(f"   +- **\${item['monto']:,.0f}** al **{item['tasa']}%** = **\${ganancia_item:,.0f}/año** *({porcentaje:.1f}% del total)*")
            
            # Mostrar advertencias según el monto
            if capital_necesario > 1000000:
                st.warning("⚠️ **Capital alto**: Considera diversificar en múltiples SOFIPOs para no exceder el límite IPAB de $400k por institución.")
            elif capital_necesario < 5000:
                st.info("ℹ️ **Capital bajo**: Puedes empezar con 1-2 SOFIPOs y diversificar conforme aumentes tu capital.")
            
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
                st.warning(f"⚠️ **SOFIPOs excluidas**: {', '.join(excluidas)}")
            
            # Botón para aplicar toda la estrategia al simulador
            st.markdown("---")
            if st.button("🚀 Aplicar esta estrategia a la simulación", use_container_width=True, key="btn_aplicar_estrategia_objetivo", type="primary"):
                # Actualizar el monto total
                # Guardar la estrategia para aplicarla en el próximo render
                st.session_state["estrategia_objetivo_pendiente"] = {
                    "capital": int(capital_necesario),
                    "distribucion": distribucion_final
                }
                st.success(f" **Estrategia lista:** ${capital_necesario:,.0f} distribuidos en {len(distribucion_final)} productos")
                st.rerun()
    st.divider()
    
    # ========================================================================
    # ESTRATEGIAS DE OPTIMIZACIÓN (ANTES DE SELECCIONAR)
    # ========================================================================
    
    # Solo mostrar recomendaciones si hay capital disponible
    if monto_total > 0:
        with st.expander("💡 Recomendaciones de Inversión", expanded=False):
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
            - ? Máxima liquidez inmediata (100%)
            - ? Diversificación en 4 instituciones sólidas
            - ? Rendimiento promedio ~11.3% anual
            
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
            - ? Excelente diversificación (5 SOFIPOs)
            - ? 80% con liquidez inmediata
            - ? Rendimiento optimizado (~13.8% ponderado)
            
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
            
            # ================================================================
            # ALGORITMO INTELIGENTE DE OPTIMIZACIÓN DE RENDIMIENTO
            # ================================================================
            
            # Construir lista de todas las opciones disponibles con sus límites y tasas
            opciones_disponibles = []
            
            # DiDi Ahorro (16% hasta $10k, luego 8.5%)
            if usa_didi:
                opciones_disponibles.append({
                    "sofipo": "DiDi",
                    "producto": "DiDi Ahorro",
                    "tasa": 16.0,
                    "limite": 10000,
                    "minimo": 0,
                    "prioridad": 1,  # Máxima prioridad por mejor tasa
                    "liquidez": "Inmediata",
                    "tipo": "vista",
                    "razon": "🚗 16% primeros $10k 💧 A LA VISTA",
                    "emoji": "🚗"
                })
            
            # Ualá Plus (16% hasta $50k) - SOLO si cumple requisitos
            if usa_uala and cumple_uala_plus:
                opciones_disponibles.append({
                    "sofipo": "Ualá",
                    "producto": "Cuenta Plus",
                    "tasa": 16.0,
                    "limite": 50000,
                    "minimo": 0,
                    "prioridad": 2,
                    "liquidez": "Inmediata",
                    "tipo": "vista",
                    "razon": "🔴 16% hasta $50k ✅ Cumples $3k/mes 💧 A LA VISTA",
                    "emoji": "🔴"
                })
            
            # Nu México Cajita Turbo (15% hasta $25k)
            if usa_nu:
                opciones_disponibles.append({
                    "sofipo": "Nu México",
                    "producto": "Cajita Turbo",
                    "tasa": 15.0,
                    "limite": 25000,
                    "minimo": 0,
                    "prioridad": 3,
                    "liquidez": "Inmediata",
                    "tipo": "vista",
                    "razon": "💜 15% hasta $25k 💧 A LA VISTA",
                    "emoji": "💜"
                })
            
            # Klar Inversión Max (15%) - SOLO si cumple requisitos
            if usa_klar and cumple_klar_plus:
                opciones_disponibles.append({
                    "sofipo": "Klar",
                    "producto": "Inversión Flexible Max",
                    "tasa": 15.0,
                    "limite": None,  # Sin límite
                    "minimo": 100,
                    "prioridad": 4,
                    "liquidez": "Inmediata",
                    "tipo": "vista",
                    "razon": "⚡ 15% sin límite ✅ Tienes Plus/Platino 💧 A LA VISTA",
                    "emoji": "⚡"
                })
            
            # Mercado Pago (13% hasta $25k) - SOLO si cumple requisitos
            if usa_mp and cumple_mercadopago:
                opciones_disponibles.append({
                    "sofipo": "Mercado Pago",
                    "producto": "Cuenta Remunerada",
                    "tasa": 13.0,
                    "limite": 25000,
                    "minimo": 0,
                    "prioridad": 5,
                    "liquidez": "Inmediata",
                    "tipo": "vista",
                    "razon": "� 13% hasta $25k ✅ Cumples $3k/mes 💧 A LA VISTA",
                    "emoji": "💙"
                })
            
            # Stori 90 días (10%) - Solo si NO está en modo solo_vista
            if not solo_vista and usa_stori:
                opciones_disponibles.append({
                    "sofipo": "Stori",
                    "producto": "90 días",
                    "tasa": 10.0,
                    "limite": None,
                    "minimo": 1000,
                    "prioridad": 6,
                    "liquidez": "90 días",
                    "tipo": "plazo",
                    "razon": "🟦 10% plazo 90 días 📅 PLAZO FIJO",
                    "emoji": "🟦"
                })
            
            # Finsus 360 días (10.09%) - Solo si NO está en modo solo_vista
            if not solo_vista and usa_finsus:
                opciones_disponibles.append({
                    "sofipo": "Finsus",
                    "producto": "Apartado 360 días",
                    "tasa": 10.09,
                    "limite": None,
                    "minimo": 1000,
                    "prioridad": 7,
                    "liquidez": "360 días",
                    "tipo": "plazo",
                    "razon": "🟢 10.09% plazo 360 días � PLAZO FIJO",
                    "emoji": "🟢"
                })
            
            # Ualá Base (7.75%) - Solo si NO tiene Ualá Plus
            if usa_uala and not cumple_uala_plus:
                opciones_disponibles.append({
                    "sofipo": "Ualá",
                    "producto": "Cuenta Base",
                    "tasa": 7.75,
                    "limite": 30000,
                    "minimo": 0,
                    "prioridad": 8,
                    "liquidez": "Inmediata",
                    "tipo": "vista",
                    "razon": "� 7.75% hasta $30k 💧 A LA VISTA",
                    "emoji": "🔴"
                })
            
            # Klar Cuenta (8.5%) - Solo si NO tiene Klar Max
            if usa_klar and not cumple_klar_plus:
                opciones_disponibles.append({
                    "sofipo": "Klar",
                    "producto": "Inversión Flexible",
                    "tasa": 8.5,
                    "limite": None,
                    "minimo": 100,
                    "prioridad": 9,
                    "liquidez": "Inmediata",
                    "tipo": "vista",
                    "razon": "⚡ 8.5% sin límite 💧 A LA VISTA",
                    "emoji": "⚡"
                })
            
            # ================================================================
            # DISTRIBUIR CAPITAL OPTIMIZANDO RENDIMIENTO
            # ================================================================
            
            # Ordenar opciones por tasa descendente (no por prioridad fija)
            opciones_disponibles.sort(key=lambda x: (-x['tasa'], x['prioridad']))
            
            distribucion_agresiva = []
            saldo_restante = monto_total
            
            for opcion in opciones_disponibles:
                if saldo_restante <= 0:
                    break
                
                # Verificar si cumple mínimo
                if saldo_restante < opcion['minimo']:
                    continue
                
                # Calcular cuánto asignar
                if opcion['limite'] is None:
                    # Sin límite: asignar todo el saldo restante
                    monto_asignar = saldo_restante
                else:
                    # Con límite: asignar hasta el límite o lo que quede
                    monto_asignar = min(opcion['limite'], saldo_restante)
                
                # Agregar a la distribución
                distribucion_agresiva.append({
                    "sofipo": opcion['sofipo'],
                    "producto": opcion['producto'],
                    "monto": monto_asignar,
                    "tasa": opcion['tasa'],
                    "razon": opcion['razon'],
                    "emoji": opcion['emoji']
                })
                
                saldo_restante -= monto_asignar
            
            # Advertencia si quedan fondos sin asignar
            if saldo_restante > 0:
                if solo_vista:
                    st.warning(f"⚠️ Quedan **${saldo_restante:,.0f}** sin asignar. En modo A LA VISTA, los productos a plazo fijo están excluidos. Desactiva el modo A LA VISTA o activa más SOFIPOs para distribuir todo tu capital.")
                else:
                    st.warning(f"⚠️ Quedan **${saldo_restante:,.0f}** sin asignar. Has excluido demasiadas SOFIPOs. Activa al menos una más para distribuir todo tu capital.")
            
            # Mostrar tabla con montos exactos
            if distribucion_agresiva:
                st.markdown("**💰 Montos específicos sugeridos:**")
            else:
                st.error("⚠️ No hay recomendaciones disponibles. Has excluido todas las SOFIPOs. Activa al menos una para ver recomendaciones.")
            
            for i, dist in enumerate(distribucion_agresiva, 1):
                porcentaje = (dist['monto'] / monto_total * 100) if monto_total > 0 else 0
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
            
            # Calcular rendimiento proyectado de esta estrategia usando el MISMO método que los resultados
            ganancia_12m = 0
            dias_simulacion = 12 * 30  # 360 días (igual que en los resultados)
            for d in distribucion_agresiva:
                # Usar el mismo cálculo que en la simulación principal
                interes = calcular_interes_compuesto(d['monto'], d['tasa'], dias_simulacion)
                ganancia_12m += interes
            
            ganancia_12m = int(ganancia_12m)
            tasa_ponderada_agresiva = (ganancia_12m / monto_total * 100) if monto_total > 0 else 0
            
            st.success(f"🎯 **Con esta estrategia agresiva obtendrás:**")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Tasa ponderada", f"{tasa_ponderada_agresiva:.2f}%")
            with col2:
                st.metric("Ganancia estimada (12 meses)", f"${ganancia_12m:,.0f}")
            
            # Botón para aplicar estrategia
            st.markdown("---")
            if st.button("🚀 Aplicar esta estrategia a mi simulación", key="btn_aplicar_agresiva", type="primary"):
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
                advertencias.append("- 💡 Podrías mejorar con Mercado Pago 13% si puedes depositar $3k/mes")
            
            if cumple_uala_plus:
                advertencias.append("- ✅ Incluye Ualá Plus 16% (cumples requisito de $3k/mes)")
            else:
                advertencias.append("- 💡 Podrías mejorar con Ualá Plus 16% si puedes consumir $3k/mes")
            
            if cumple_klar_plus:
                advertencias.append("- ✅ Incluye Klar Max 15% (tienes membresía Plus/Platino)")
            else:
                advertencias.append("- 💡 Podrías mejorar con Klar Max 15% si tienes membresía Plus/Platino")
            
            advertencias.append("- Parte del capital puede quedar en plazos fijos (menor liquidez)")
            advertencias.append("- No es recomendable para fondos de emergencia")
            
            st.warning("\n".join(advertencias))
    
    st.divider()
    
    # ========================================================================
    # SELECCIÓN SIMPLE DE SOFIPOS
    # ========================================================================
    
    st.markdown("### 🏦 Selecciona las SOFIPOs donde invertirás (o aplica una estrategia arriba)")
    
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
        st.info("✅ **Estrategia aplicada automáticamente.** Los valores han sido cargados en las pestañas de cada SOFIPO.")
    
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
                f"? Quiero invertir en {sofipo_name}",
                key=f"check_{sofipo_name}"
            )
            
            if incluir:
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Selector de producto
                    productos = list(sofipo_data['productos'].keys())
                    
                    # Validar que el producto guardado existe, si no usar el primero
                    producto_guardado = st.session_state.get(f"prod_{sofipo_name}", productos[0])
                    if producto_guardado not in productos:
                        producto_guardado = productos[0]
                    
                    producto_seleccionado = st.selectbox(
                        "📦 Elige el producto:",
                        options=productos,
                        index=productos.index(producto_guardado) if producto_guardado in productos else 0,
                        key=f"prod_{sofipo_name}",
                        help="Selecciona el tipo de inversión"
                    )
                    
                    producto_info = sofipo_data['productos'][producto_seleccionado]
                    
                    # Mostrar tasa
                    if producto_info.get("tipo") == "vista_hibrida":
                        st.success(f"**📈 GAT: {producto_info['tasa_premium']}%** (primeros ${producto_info['limite_premium']:,})")
                        st.caption(f"Después: {producto_info['tasa_base']}%")
                    elif producto_info.get("limite_max"):
                        st.success(f"**📈 GAT: {producto_info['tasa_base']}%** (hasta ${producto_info['limite_max']:,})")
                    else:
                        st.success(f"**📈 GAT: {producto_info['tasa_base']}%**")
                    
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
                st.metric("💵 Dinero asignado", f"${total_asignado_actual:,.0f}", f"{porcentaje_asignado:.1f}%")
            with col2:
                st.metric("💰 Dinero disponible", f"${dinero_restante:,.0f}", f"{porcentaje_restante:.1f}%")
            with col3:
                st.metric("💯 Total", f"${monto_total:,.0f}", "100%")
        elif dinero_restante == 0:
            st.success(f"✅ **Perfecto!** Has distribuido todo tu dinero: ${monto_total:,.0f} (100%)")
        else:
            st.error(f"⚠️ **¡Cuidado!** Te has pasado ${abs(dinero_restante):,.0f}. Ajusta los montos.")
    
    st.divider()
    
    # ========================================================================
    # CÁLCULOS Y RESULTADOS
    # ========================================================================
    
    # Verificar si hay algo que simular (inversiones O aportaciones)
    tiene_inversiones = len(inversiones_seleccionadas) > 0
    tiene_aportaciones = aportaciones_activas and aportacion_monto > 0
    
    if tiene_inversiones or (monto_total == 0 and tiene_aportaciones):
        st.divider()
        st.markdown("## 📊 Tus Resultados")
        
        # Si hay capital inicial, validar distribución
        if monto_total > 0:
            # Validar que no exceda el monto total
            total_asignado = sum([inv["monto"] for inv in inversiones_seleccionadas.values()])
            
            if total_asignado > monto_total:
                st.error(f"⚠️ **Cuidado:** Has asignado ${total_asignado:,.0f} pero solo tienes ${monto_total:,.0f}. Ajusta los montos.")
                return
            
            diferencia = monto_total - total_asignado
            if diferencia > 0:
                st.warning(f"ℹ️ Tienes **${diferencia:,.0f}** sin asignar. ¿Quieres agregarlo a alguna SOFIPO?")
        elif not tiene_inversiones and tiene_aportaciones:
            # Modo solo aportaciones: crear una inversión virtual para proyección
            st.info("💡 **Simulación desde $0** - Se proyectará el crecimiento solo con aportaciones recurrentes. Selecciona productos arriba para ver dónde se invertirán las aportaciones.")
        
        # Calcular rendimientos para cada inversión (skip si no hay inversiones)
        resultados = []
        proyecciones_todas = []
        total_invertido = sum([inv["monto"] for inv in inversiones_seleccionadas.values()]) if inversiones_seleccionadas else 0
        
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
        
        total_invertido = sum([inv['monto'] for inv in inversiones_seleccionadas.values()]) if inversiones_seleccionadas else 0
        
        # Calcular ganancia total y GAT ponderado
        ganancia_total = 0
        for resultado in resultados:
            ganancia_str = resultado["Ganancia Total"].replace("$", "").replace(",", "")
            ganancia_total += float(ganancia_str)
        
        # CORRECCIÓN FINANCIERA: Calcular la tasa efectiva anualizada correctamente
        # Si el periodo es < 12 meses, necesitamos calcular la tasa equivalente anual
        if total_invertido > 0:
            if periodo_simulacion == 12:
                # Para 12 meses, es directo
                rendimiento_ponderado = (ganancia_total / total_invertido) * 100
            else:
                # Para otros periodos, calcular tasa equivalente anual
                # (1 + r_periodo) = (1 + r_anual)^(periodo/12)
                # r_anual = (1 + r_periodo)^(12/periodo) - 1
                rendimiento_periodo = ganancia_total / total_invertido
                rendimiento_ponderado = ((1 + rendimiento_periodo) ** (12 / periodo_simulacion) - 1) * 100
        else:
            # Modo $0: Sin capital inicial, solo aportaciones
            rendimiento_ponderado = 0
        
        # Métricas principales en cards grandes
        st.markdown("### 📈 Resultado de tu inversión")
        
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
        
        # GAT Ponderado destacado (solo si hay capital invertido)
        if total_invertido > 0:
            st.success(f"📊 **Tu tasa promedio ponderada es: {rendimiento_ponderado:.2f}% anual**")
        
        # Tabla detallada en expander (solo si hay productos)
        if resultados:
            with st.expander("🔍 Ver desglose detallado por SOFIPO"):
                df_resultados = pd.DataFrame(resultados)
                st.dataframe(df_resultados, width="stretch", hide_index=True)
        
        # ====================================================================
        # 📊 DASHBOARD EJECUTIVO - TU PORTAFOLIO EN 30 SEGUNDOS
        # ====================================================================
        
        # Solo mostrar Dashboard Ejecutivo si hay capital invertido
        if total_invertido > 0:
            st.markdown("---")
            st.markdown("### 📊 Dashboard Ejecutivo")
            st.caption("🚀 Tu portafolio en 30 segundos")
            
            # Calcular métricas para el score
            num_sofipos = len(inversiones_seleccionadas)
            
            # Calcular montos por SOFIPO para verificar protección IPAB
            montos_por_sofipo = {}
            for inversion_key, inversion in inversiones_seleccionadas.items():
                sofipo = inversion['sofipo']
                monto = inversion['monto']
                if sofipo not in montos_por_sofipo:
                    montos_por_sofipo[sofipo] = 0
                montos_por_sofipo[sofipo] += monto
            
            proteccion_ipab_completa = all(monto <= 200000 for monto in montos_por_sofipo.values())
            
            # Calcular porcentaje de liquidez
            monto_liquido = sum(
                inv['monto'] for inv in inversiones_seleccionadas.values() 
                if inv['producto_info']['tipo'] in ['vista', 'vista_hibrida']
            )
            porcentaje_liquidez = (monto_liquido / total_invertido * 100) if total_invertido > 0 else 0
            
            # ====================================================================
            # SISTEMA DE SCORE INTELIGENTE (0-100)
            # ====================================================================
            
            score_total = 0
            componentes_score = []
            
            # 1. RENDIMIENTO (40 puntos máximo) - El más importante
            if rendimiento_ponderado >= 15:
                score_rendimiento = 40
                nivel_rendimiento = "Excelente"
            elif rendimiento_ponderado >= 14:
                score_rendimiento = 35
                nivel_rendimiento = "Muy Bueno"
            elif rendimiento_ponderado >= 13:
                score_rendimiento = 30
                nivel_rendimiento = "Bueno"
            elif rendimiento_ponderado >= 12:
                score_rendimiento = 25
                nivel_rendimiento = "Aceptable"
            else:
                score_rendimiento = int((rendimiento_ponderado / 12) * 25)
                nivel_rendimiento = "Mejorable"
            
            score_total += score_rendimiento
            componentes_score.append(("Rendimiento", score_rendimiento, 40, nivel_rendimiento))
            
            # 2. PROTECCIÓN IPAB (25 puntos máximo)
            if proteccion_ipab_completa:
                score_ipab = 25
                nivel_ipab = "100% Protegido"
            else:
                # Calcular qué porcentaje del total está protegido
                monto_protegido = sum(min(m, 200000) for m in montos_por_sofipo.values())
                porcentaje_protegido = (monto_protegido / total_invertido * 100) if total_invertido > 0 else 0
                score_ipab = int((porcentaje_protegido / 100) * 25)
                nivel_ipab = f"{porcentaje_protegido:.0f}% Protegido"
            
            score_total += score_ipab
            componentes_score.append(("Protección IPAB", score_ipab, 25, nivel_ipab))
            
            # 3. LIQUIDEZ (20 puntos máximo)
            if porcentaje_liquidez >= 80:
                score_liquidez = 20
                nivel_liquidez = "Muy Alta"
            elif porcentaje_liquidez >= 50:
                score_liquidez = 15
                nivel_liquidez = "Balanceada"
            elif porcentaje_liquidez >= 30:
                score_liquidez = 10
                nivel_liquidez = "Moderada"
            else:
                score_liquidez = int((porcentaje_liquidez / 30) * 10)
                nivel_liquidez = "Baja"
            
            score_total += score_liquidez
            componentes_score.append(("Liquidez", score_liquidez, 20, nivel_liquidez))
            
            # 4. DIVERSIFICACIÓN (15 puntos máximo) - Peso reducido para no penalizar tanto
            if num_sofipos >= 5:
                score_diversificacion = 15
                nivel_diversificacion = "Excelente"
            elif num_sofipos >= 3:
                score_diversificacion = 12
                nivel_diversificacion = "Buena"
            elif num_sofipos >= 2:
                score_diversificacion = 9
                nivel_diversificacion = "Aceptable"
            else:
                score_diversificacion = 6
                nivel_diversificacion = "Básica"
            
            score_total += score_diversificacion
            componentes_score.append(("Diversificación", score_diversificacion, 15, nivel_diversificacion))
            
            # ====================================================================
            # SEMÁFORO DE RIESGO
            # ====================================================================
            
            if score_total >= 85:
                semaforo = "🟢"
                semaforo_texto = "EXCELENTE"
                semaforo_color = "#22c55e"
                mensaje_riesgo = "Tu portafolio está muy bien optimizado"
            elif score_total >= 70:
                semaforo = "🟢"
                semaforo_texto = "BUENO"
                semaforo_color = "#84cc16"
                mensaje_riesgo = "Portafolio sólido con buen balance"
            elif score_total >= 55:
                semaforo = "🟡"
                semaforo_texto = "ACEPTABLE"
                semaforo_color = "#eab308"
                mensaje_riesgo = "Considera mejorar algunos aspectos"
            else:
                semaforo = "🔴"
                semaforo_texto = "MEJORABLE"
                semaforo_color = "#ef4444"
                mensaje_riesgo = "Hay áreas importantes que optimizar"
            
            # ====================================================================
            # MOSTRAR DASHBOARD EN TARJETA ÚNICA (VERSIÓN NATIVA STREAMLIT)
            # ====================================================================
            
            # Contenedor principal con estilo
            dashboard_container = st.container()
            
            with dashboard_container:
                # Header del dashboard
                col_score, col_msg = st.columns([1, 2])
                
                with col_score:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 20px; background: {semaforo_color}15; border-radius: 10px; border: 2px solid {semaforo_color};">
                        <div style="font-size: 48px; font-weight: bold; color: {semaforo_color};">
                            {score_total}/100
                        </div>
                        <div style="font-size: 18px; font-weight: bold; color: {semaforo_color}; margin-top: 10px;">
                            {semaforo} {semaforo_texto}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_msg:
                    st.info(f"**Score de Calidad del Portafolio**\n\n{mensaje_riesgo}")
                
                # Desglose del score
                st.markdown("---")
                st.markdown("### 📋 Desglose del Score")
                
                for comp in componentes_score:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{comp[0]}**")
                        st.progress(comp[1] / comp[2])
                    with col2:
                        st.metric(
                            label="Puntos",
                            value=f"{comp[1]}/{comp[2]}",
                            delta=comp[3]
                        )
                    st.caption(f"_{comp[3]}_")
                    st.markdown("")  # Espacio
            
            # ====================================================================
            # KPIs PRINCIPALES EN FORMATO COMPACTO
            # ====================================================================
            
            col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
            
            with col_kpi1:
                st.metric(
                    label="📈 GAT Ponderado",
                    value=f"{rendimiento_ponderado:.2f}%",
                    delta="Anual"
                )
            
            with col_kpi2:
                st.metric(
                    label="🏦 SOFIPOs",
                    value=f"{num_sofipos}",
                    delta=nivel_diversificacion
                )
            
            with col_kpi3:
                st.metric(
                    label="🛡️ IPAB",
                    value=f"{nivel_ipab}",
                    delta="Protección"
                )
            
            with col_kpi4:
                st.metric(
                    label="💧 Liquidez",
                    value=f"{porcentaje_liquidez:.0f}%",
                    delta=nivel_liquidez
                )
            
            st.markdown("---")
        
        # ====================================================================
        # VISUALIZACIONES PROFESIONALES
        # ====================================================================
        
        # Mostrar visualizaciones si hay proyecciones o aportaciones activas
        if len(proyecciones_todas) > 0 or (total_invertido == 0 and aportaciones_activas and aportacion_monto > 0):
            st.markdown("---")
            st.markdown("## 📊 Visualización de tu Inversión")
            
            # Caso especial: Solo aportaciones sin capital inicial
            if total_invertido == 0 and aportaciones_activas and aportacion_monto > 0:
                st.info(f"💡 **Simulación desde $0** - Proyectando con aportaciones {frecuencia_aportacion.lower()}es de ${aportacion_monto:,.0f} a tasa promedio del mercado (15% anual)")
                
                # Generar proyección solo con aportaciones
                # Usar la tasa más alta disponible de los productos habilitados
                tasa_referencia = 15.0  # Tasa promedio conservadora
                
                df_total_con_aportaciones = generar_proyeccion_con_aportaciones(
                    capital_inicial=0,
                    tasa_anual=tasa_referencia,
                    tipo_calculo="compuesto",
                    meses=periodo_simulacion,
                    aportacion=aportacion_monto,
                    frecuencia=frecuencia_aportacion
                )
                # No hay proyección sin aportaciones, por lo que df_total será None
                df_total = None
            
            # Caso normal: Hay capital inicial
            elif len(proyecciones_todas) > 0:
                # Combinar todas las proyecciones
                df_proyecciones_completo = pd.concat(proyecciones_todas, ignore_index=True)
                
                # Agrupar por mes y sumar TODO
                df_total = df_proyecciones_completo.groupby('Mes').agg({
                    'Capital Inicial': 'sum',
                    'Intereses Generados': 'sum',
                    'Total Acumulado': 'sum'
                }).reset_index()
                
                # Si hay aportaciones activas, generar proyección con aportaciones
                if aportaciones_activas and aportacion_monto > 0:
                    df_total_con_aportaciones = generar_proyeccion_con_aportaciones(
                        capital_inicial=total_invertido,
                        tasa_anual=rendimiento_ponderado,
                        tipo_calculo="compuesto",
                        meses=periodo_simulacion,
                        aportacion=aportacion_monto,
                        frecuencia=frecuencia_aportacion
                    )
                else:
                    df_total_con_aportaciones = None
            else:
                df_total = None
                df_total_con_aportaciones = None
            
            # Dos columnas para las visualizaciones
            col_viz1, col_viz2 = st.columns([1.5, 1])
            
            with col_viz1:
                titulo_grafica = "### 📈 Proyección de Crecimiento"
                if aportaciones_activas and aportacion_monto > 0:
                    # Calcular frecuencia para mostrar
                    frecuencias_texto = {
                        "Semanal": f"${aportacion_monto:,.0f}/semana",
                        "Quincenal": f"${aportacion_monto:,.0f}/quincena",
                        "Mensual": f"${aportacion_monto:,.0f}/mes"
                    }
                    titulo_grafica += f" (+ {frecuencias_texto[frecuencia_aportacion]})"
                
                st.markdown(titulo_grafica)
                
                # Crear gráfico profesional con gradiente
                fig = go.Figure()
                
                # Si hay aportaciones, mostrar comparación
                if aportaciones_activas and aportacion_monto > 0:
                    # Área de relleno para CON aportaciones
                    fig.add_trace(go.Scatter(
                        x=df_total_con_aportaciones['Mes'],
                        y=df_total_con_aportaciones['Total Acumulado'],
                        mode='lines',
                        name='Con Aportaciones (área)',
                        line=dict(width=0),
                        fillcolor='rgba(67, 233, 123, 0.3)',
                        fill='tozeroy',
                        showlegend=False,
                        hoverinfo='skip'
                    ))
                    
                    # Línea principal CON aportaciones
                    fig.add_trace(go.Scatter(
                        x=df_total_con_aportaciones['Mes'],
                        y=df_total_con_aportaciones['Total Acumulado'],
                        mode='lines+markers',
                        name='Con Aportaciones',
                        line=dict(
                            width=3.5,
                            color='#43e97b',
                            shape='spline',
                        ),
                        marker=dict(
                            size=9,
                            color='#43e97b',
                            symbol='circle',
                            line=dict(color='white', width=2)
                        ),
                        hovertemplate=(
                            '<b style="color:#43e97b;">Con Aportaciones</b><br>' +
                            '<b>Mes %{x}</b><br>' +
                            'Total: <b>$%{y:,.0f}</b><br>' +
                            '<extra></extra>'
                        )
                    ))
                    
                    # Línea SIN aportaciones (para comparar) - solo si hay capital inicial
                    if df_total is not None:
                        fig.add_trace(go.Scatter(
                            x=df_total['Mes'],
                            y=df_total['Total Acumulado'],
                            mode='lines+markers',
                            name='Sin Aportaciones',
                            line=dict(
                                width=2.5,
                                color='#667eea',
                                shape='spline',
                                dash='dash'
                            ),
                            marker=dict(
                                size=7,
                                color='#667eea',
                                symbol='circle',
                                line=dict(color='white', width=1.5)
                            ),
                            hovertemplate=(
                                '<b style="color:#667eea;">Sin Aportaciones</b><br>' +
                                '<b>Mes %{x}</b><br>' +
                                'Total: <b>$%{y:,.0f}</b><br>' +
                                '<extra></extra>'
                            )
                        ))
                else:
                    # Gráfico normal sin aportaciones
                    # Área de relleno con gradiente
                    fig.add_trace(go.Scatter(
                        x=df_total['Mes'],
                        y=df_total['Total Acumulado'],
                        mode='lines',
                        name='Crecimiento',
                        line=dict(width=0),
                        fillcolor='rgba(102, 126, 234, 0.3)',
                        fill='tozeroy',
                        showlegend=False,
                        hoverinfo='skip'
                    ))
                    
                    # Línea principal con gradiente profesional
                    fig.add_trace(go.Scatter(
                        x=df_total['Mes'],
                        y=df_total['Total Acumulado'],
                        mode='lines+markers',
                        name='Total del Portafolio',
                        line=dict(
                            width=3.5,
                            color='#667eea',
                            shape='spline',  # Línea suavizada
                        ),
                        marker=dict(
                            size=9,
                            color='#667eea',
                            symbol='circle',
                            line=dict(color='white', width=2)
                        ),
                        hovertemplate=(
                            '<b style="color:#667eea;">Total Acumulado</b><br>' +
                            '<b>Mes %{x}</b><br>' +
                            'Monto: <b>$%{y:,.0f}</b><br>' +
                            '<extra></extra>'
                        )
                    ))
                
                # Línea de capital inicial (más sutil) - solo si hay capital
                if total_invertido > 0 and df_total is not None:
                    fig.add_trace(go.Scatter(
                        x=df_total['Mes'],
                        y=[total_invertido] * len(df_total),
                        mode='lines',
                        name='Capital Inicial',
                        line=dict(
                            width=2,
                            color='rgba(150, 150, 150, 0.4)',
                            dash='dot'
                        ),
                        hovertemplate='Capital Inicial: $%{y:,.0f}<extra></extra>'
                    ))
                
                # Anotación profesional al final
                if aportaciones_activas and aportacion_monto > 0:
                    # Anotación para CON aportaciones
                    total_final_con_aport = df_total_con_aportaciones['Total Acumulado'].iloc[-1]
                    aportaciones_totales = df_total_con_aportaciones['Aportaciones Acumuladas'].iloc[-1]
                    intereses_con_aport = df_total_con_aportaciones['Intereses Generados'].iloc[-1]
                    
                    fig.add_annotation(
                        x=df_total_con_aportaciones['Mes'].iloc[-1],
                        y=total_final_con_aport,
                        text=f"<b>${total_final_con_aport:,.0f}</b><br>+${intereses_con_aport:,.0f} intereses",
                        showarrow=True,
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor="#43e97b",
                        ax=40,
                        ay=-50,
                        font=dict(size=12, color="#43e97b", family="Arial"),
                        bgcolor="rgba(255,255,255,0.9)",
                        bordercolor="#43e97b",
                        borderwidth=2,
                        borderpad=4
                    )
                    
                    # Anotación para SIN aportaciones (más pequeña) - solo si hay capital inicial
                    if df_total is not None:
                        total_final_correcto = total_invertido + ganancia_total
                        fig.add_annotation(
                            x=df_total['Mes'].iloc[-1],
                            y=df_total['Total Acumulado'].iloc[-1],
                            text=f"<b>${total_final_correcto:,.0f}</b>",
                            showarrow=True,
                            arrowhead=2,
                            arrowsize=1,
                            arrowwidth=2,
                            arrowcolor="#667eea",
                            ax=-40,
                            ay=30,
                            font=dict(size=11, color="#667eea", family="Arial"),
                            bgcolor="rgba(255,255,255,0.85)",
                            bordercolor="#667eea",
                            borderwidth=1.5,
                            borderpad=3
                        )
                else:
                    # Anotación normal sin aportaciones
                    if df_total is not None:
                        total_final_correcto = total_invertido + ganancia_total
                        
                        fig.add_annotation(
                            x=df_total['Mes'].iloc[-1],
                            y=df_total['Total Acumulado'].iloc[-1],
                            text=f"<b>${total_final_correcto:,.0f}</b><br>+${ganancia_total:,.0f}",
                            showarrow=True,
                            arrowhead=2,
                            arrowsize=1,
                            arrowwidth=2,
                            arrowcolor="#667eea",
                            ax=40,
                            ay=-40,
                            font=dict(size=12, color="#667eea", family="Arial"),
                            bgcolor="rgba(255,255,255,0.9)",
                            bordercolor="#667eea",
                            borderwidth=2,
                            borderpad=4
                        )
                
                fig.update_layout(
                    height=450,
                    margin=dict(l=20, r=20, t=40, b=20),
                    hovermode='x unified',
                    template="plotly_white" if not modo_oscuro else "plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(
                        size=12,
                        color='#333333' if not modo_oscuro else '#c9d1d9',
                        family="Arial"
                    ),
                    xaxis=dict(
                        title="<b>Periodo (Meses)</b>",
                        showgrid=True,
                        gridwidth=1,
                        gridcolor='rgba(200,200,200,0.2)',
                        zeroline=False,
                        showline=True,
                        linewidth=2,
                        linecolor='rgba(200,200,200,0.3)'
                    ),
                    yaxis=dict(
                        title="<b>Monto Total (MXN)</b>",
                        showgrid=True,
                        gridwidth=1,
                        gridcolor='rgba(200,200,200,0.2)',
                        zeroline=False,
                        showline=True,
                        linewidth=2,
                        linecolor='rgba(200,200,200,0.3)',
                        tickformat="$,.0f"
                    ),
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="top",
                        y=-0.15,
                        xanchor="center",
                        x=0.5,
                        bgcolor='rgba(255,255,255,0.8)' if not modo_oscuro else 'rgba(30,30,30,0.8)',
                        bordercolor='rgba(200,200,200,0.3)',
                        borderwidth=1,
                        font=dict(size=11)
                    )
                )
                
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            with col_viz2:
                st.markdown("### 🎯 Distribución del Portafolio")
                
                # Calcular distribución por SOFIPO
                distribucion_sofipos = {}
                for inv_key, inv_data in inversiones_seleccionadas.items():
                    sofipo = inv_data['sofipo']
                    monto = inv_data['monto']
                    if sofipo not in distribucion_sofipos:
                        distribucion_sofipos[sofipo] = 0
                    distribucion_sofipos[sofipo] += monto
                
                # Crear pie chart profesional
                colores_profesionales = [
                    '#667eea', '#764ba2', '#f093fb', '#4facfe',
                    '#43e97b', '#fa709a', '#fee140', '#30cfd0'
                ]
                
                fig_pie = go.Figure(data=[go.Pie(
                    labels=list(distribucion_sofipos.keys()),
                    values=list(distribucion_sofipos.values()),
                    hole=0.5,  # Donut chart
                    marker=dict(
                        colors=colores_profesionales[:len(distribucion_sofipos)],
                        line=dict(color='white', width=3)
                    ),
                    textinfo='label+percent',
                    textfont=dict(size=13, color='white', family="Arial"),
                    hovertemplate=(
                        '<b>%{label}</b><br>' +
                        'Monto: $%{value:,.0f}<br>' +
                        'Porcentaje: %{percent}<br>' +
                        '<extra></extra>'
                    ),
                    pull=[0.05] * len(distribucion_sofipos)  # Separar ligeramente
                )])
                
                # Anotación central del donut
                fig_pie.add_annotation(
                    text=f"<b>${total_invertido:,.0f}</b><br><span style='font-size:11px;'>Total Invertido</span>",
                    x=0.5, y=0.5,
                    font=dict(size=16, color='#667eea', family="Arial"),
                    showarrow=False
                )
                
                fig_pie.update_layout(
                    height=450,
                    margin=dict(l=20, r=20, t=20, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12, family="Arial"),
                    showlegend=True,
                    legend=dict(
                        orientation="v",
                        yanchor="middle",
                        y=0.5,
                        xanchor="left",
                        x=1.05,
                        bgcolor='rgba(255,255,255,0.8)' if not modo_oscuro else 'rgba(30,30,30,0.8)',
                        bordercolor='rgba(200,200,200,0.3)',
                        borderwidth=1,
                        font=dict(size=11)
                    )
                )
                
                st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
            
            # ====================================================================
            # DESGLOSE DETALLADO (OPCIONAL - EN EXPANDER)
            # ====================================================================
            
            # Solo mostrar desglose si hay inversiones (no solo aportaciones)
            if len(proyecciones_todas) > 0 and total_invertido > 0:
                st.markdown("---")
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
            # IMPACTO DE APORTACIONES RECURRENTES
            # ====================================================================
            
            # Mostrar impacto de aportaciones si están activas
            if aportaciones_activas and aportacion_monto > 0:
                st.markdown("---")
                st.markdown("### 💰 Impacto de Aportaciones Recurrentes")
                
                # Calcular datos finales
                total_final_sin_aport = total_invertido + ganancia_total
                total_final_con_aport = df_total_con_aportaciones['Total Acumulado'].iloc[-1]
                aportaciones_totales = df_total_con_aportaciones['Aportaciones Acumuladas'].iloc[-1]
                intereses_con_aport = df_total_con_aportaciones['Intereses Generados'].iloc[-1]
                
                # Si hay capital inicial, calcular ganancia extra; si no, solo mostrar total acumulado
                if total_invertido > 0:
                    ganancia_extra_por_aportaciones = total_final_con_aport - total_final_sin_aport
                else:
                    ganancia_extra_por_aportaciones = total_final_con_aport  # Todo es ganancia desde $0
                
                col_a1, col_a2, col_a3, col_a4 = st.columns(4)
                
                with col_a1:
                    st.metric(
                        "Total Aportado",
                        f"${aportaciones_totales:,.0f}",
                        help=f"Suma de todas tus aportaciones {frecuencia_aportacion.lower()}es"
                    )
                
                with col_a2:
                    st.metric(
                        "Intereses Generados",
                        f"${intereses_con_aport:,.0f}",
                        help="Intereses sobre capital inicial + aportaciones"
                    )
                
                with col_a3:
                    if total_invertido > 0:
                        st.metric(
                            "Total Final",
                            f"${total_final_con_aport:,.0f}",
                            delta=f"+${ganancia_extra_por_aportaciones:,.0f} vs sin aportaciones",
                            delta_color="normal"
                        )
                    else:
                        st.metric(
                            "Total Final",
                            f"${total_final_con_aport:,.0f}",
                            help="Capital acumulado desde $0 con aportaciones"
                        )
                
                with col_a4:
                    if total_invertido > 0:
                        porcentaje_extra = (ganancia_extra_por_aportaciones / total_final_sin_aport * 100) if total_final_sin_aport > 0 else 0
                        st.metric(
                            "Crecimiento Extra",
                            f"{porcentaje_extra:.1f}%",
                            help="Cuánto más ganas con aportaciones vs solo capital inicial"
                        )
                    else:
                        rendimiento_efectivo = (intereses_con_aport / aportaciones_totales * 100) if aportaciones_totales > 0 else 0
                        st.metric(
                            "Rendimiento",
                            f"{rendimiento_efectivo:.1f}%",
                            help="Intereses generados sobre aportaciones totales"
                        )
                
                # Mensaje con formato corregido (sin itálicas accidentales)
                if total_invertido > 0:
                    st.info(f"💡 Con aportaciones {frecuencia_aportacion.lower()}es de ${aportacion_monto:,.0f}, ganarías ${ganancia_extra_por_aportaciones:,.0f} MÁS en {periodo_simulacion} meses")
                else:
                    st.info(f"💡 Iniciando desde $0 con aportaciones {frecuencia_aportacion.lower()}es de ${aportacion_monto:,.0f}, acumularías ${total_final_con_aport:,.0f} en {periodo_simulacion} meses ({aportaciones_totales:,.0f} aportado + ${intereses_con_aport:,.0f} intereses)")
                
                # Explicar estrategia de distribución de aportaciones
                st.markdown("##### 📋 Estrategia de Distribución de Aportaciones")
                
                # Calcular distribución real respetando límites
                distribucion_aportacion, mensajes_distribucion = calcular_distribucion_aportaciones(
                    inversiones_seleccionadas,
                    aportacion_monto,
                    estrategia_aportacion,
                    total_invertido
                )
                
                # Mostrar estrategia seleccionada
                if estrategia_aportacion == "Misma distribución que capital inicial":
                    st.caption("🔄 **Estrategia Seleccionada:** Misma distribución que capital inicial")
                elif estrategia_aportacion == "Solo productos de mayor rendimiento":
                    st.caption("📈 **Estrategia Seleccionada:** Solo productos de mayor rendimiento")
                else:
                    st.caption("🤖 **Estrategia Seleccionada:** Distribución inteligente automática")
                
                # Mostrar distribución detallada en expander
                with st.expander("🔍 Ver distribución detallada de cada aportación", expanded=False):
                    st.markdown(f"**Monto por aportación:** ${aportacion_monto:,.0f}")
                    st.markdown("---")
                    
                    # Mostrar cada mensaje de la distribución
                    for mensaje in mensajes_distribucion:
                        st.markdown(mensaje)
                    
                    # Resumen de la distribución
                    st.markdown("---")
                    st.markdown("**📊 Resumen de distribución:**")
                    total_distribuido = sum(distribucion_aportacion.values())
                    
                    for sofipo_key, monto_aport in distribucion_aportacion.items():
                        if monto_aport > 0:
                            inv_data = inversiones_seleccionadas[sofipo_key]
                            porcentaje_aport = (monto_aport / total_distribuido * 100) if total_distribuido > 0 else 0
                            st.markdown(f"• **{inv_data['sofipo']} - {inv_data['producto']}**: ${monto_aport:,.0f} ({porcentaje_aport:.1f}%)")
                    
                    if total_distribuido < aportacion_monto:
                        st.warning(f"⚠️ Solo se pueden distribuir ${total_distribuido:,.0f} de ${aportacion_monto:,.0f} debido a límites máximos de productos.")
        
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
                    "🏦 SOFIPOs utilizadas",
                    f"{analisis['num_sofipos']}/7",
                    help="Número de SOFIPOs diferentes en tu portafolio"
                )
            
            with col2:
                st.metric(
                    "📊 Concentración máxima",
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
            
            # Mostrar alertas críticas (si hay)
            if recomendaciones["alertas"]:
                st.markdown("### ⚠️ Alertas Importantes")
                for alerta in recomendaciones["alertas"]:
                    st.markdown(f'<div class="warning-box">{alerta["emoji"]} {alerta["titulo"]}: {alerta["mensaje"]}</div>', unsafe_allow_html=True)
                st.markdown("")
            
            # Mostrar oportunidades (top 3)
            if recomendaciones["oportunidades"]:
                st.markdown("### 💡 Oportunidades según tus preferencias:")
                
                oportunidades_html = ""
                for i, opp in enumerate(recomendaciones["oportunidades"], 1):
                    requisito_txt = f" · {opp['requisito']}" if opp['requisito'] else ""
                    oportunidades_html += f"**{i}.** **{opp['sofipo']} {opp['producto']}** - {opp['detalle']}{requisito_txt}\n\n"
                
                st.markdown(oportunidades_html)
        
        # ====================================================================
        # INFORMACIÓN ADICIONAL
        # ====================================================================
        
        st.divider()
        
        with st.expander("📚 Glosario y Conceptos Clave"):
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
        st.info("ℹ️ Selecciona al menos una SOFIPO arriba para comenzar la simulación")
        
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
        <p style='margin: 1rem 0; opacity: 0.9;'>ℹ️ Este simulador es una herramienta educativa. Las tasas pueden variar.<br>
        Verifica siempre las condiciones vigentes con cada institución.</p>
        <p style='margin: 0.5rem 0;'><span class="badge">📅 Tasas actualizadas: Noviembre 2025</span></p>
        <p style='margin-top: 1rem; font-size: 1.1rem;'>Desarrollado con 💚 para inversionistas mexicanos 🇲🇽</p>
    </div>
    """, unsafe_allow_html=True)


    # Fecha de última actualización
    st.markdown("---")
    st.markdown('<div style="text-align: center; font-size: 0.7rem; color: #999; padding: 1rem;">📅 Última actualización de tasas: 21 de Noviembre, 2025</div>', unsafe_allow_html=True)
if __name__ == "__main__":
    main()


