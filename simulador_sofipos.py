"""
    main()
    },
    "Finsus": {
        "logo": "🦁",
        "productos": {
            "Finsus+ (A la vista)": {
                "tasa_base": 8.09,
                "liquidez": "Inmediata",
                "minimo": 0,
                "tipo": "vista"
            },
            "Apartados": {
                "tasa_base": 4.00,
                "liquidez": "Inmediata",
                "minimo": 0,
                "tipo": "vista"
            },
            "Plazo Fijo 7 días": {
                "tasa_base": 8.00,
                "liquidez": "7 días",
                "minimo": 100,
                "tipo": "plazo",
                "plazo_dias": 7
            },
            "Plazo Fijo 30 días": {
                "tasa_base": 8.09,
                "liquidez": "30 días",
                "minimo": 100,
                "tipo": "plazo",
                "plazo_dias": 30
            },
            "Plazo Fijo 90 días": {
                "tasa_base": 8.39,
                "liquidez": "90 días",
                "minimo": 100,
                "tipo": "plazo",
                "plazo_dias": 90
            },
            "Plazo Fijo 180 días": {
                "tasa_base": 8.59,
                "liquidez": "180 días",
                "minimo": 100,
                "tipo": "plazo",
                "plazo_dias": 180
            },
            "Plazo Fijo 360 días": {
                "tasa_base": 10.09,
                "liquidez": "360 días",
                "minimo": 100,
                "tipo": "plazo",
                "plazo_dias": 360
            }
        },
        "color": "#4CAF50",
        "descripcion": "SOFIPO enfocada en inclusión financiera y sustentabilidad"
    },
            "Plazo Fijo 30 días": {
                "tasa_base": 8.09,
                "liquidez": "30 días",
                "minimo": 100,
                "tipo": "plazo",
                "plazo_dias": 30
            },
            "Plazo Fijo 90 días": {
                "tasa_base": 8.39,
                "liquidez": "90 días",
                "minimo": 100,
                "tipo": "plazo",
                "plazo_dias": 90
            },
            "Plazo Fijo 180 días": {
                "tasa_base": 8.59,
                "liquidez": "180 días",
                "minimo": 100,
                "tipo": "plazo",
                "plazo_dias": 180
            },
            "Plazo Fijo 360 días": {
                "tasa_base": 10.09,
                "liquidez": "360 días",
                "minimo": 100,
                "tipo": "plazo",
                "plazo_dias": 360
            }
        },
        "color": "#4CAF50",
        "descripcion": "SOFIPO enfocada en inclusión financiera y sustentabilidad"
    }
}
Simulador de Inversiones Multi-SOFIPO Interactivo
Desarrollado para analizar y comparar rendimientos de SOFIPOs mexicanas
Autor: Experto Fintech MÃ©xico
Fecha: Noviembre 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# ConfiguraciÃ³n de la pÃ¡gina
st.set_page_config(
    page_title="Simulador Multi-SOFIPO MÃ©xico",
    page_icon="ðŸ’°",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados - DiseÃ±o Premium
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
    
    /* Tarjetas de SOFIPO - DiseÃ±o Fresh y Minimalista */
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
    
    /* Cajas de advertencia y Ã©xito - Minimalista */
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
    
    /* Tarjetas de mÃ©tricas - Fresh Design */
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
    
    /* Inputs numÃ©ricos */
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
    "Nu MÃ©xico": {
        "logo": "ðŸŸ£",
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
            "Plazo Fijo 7 dÃ­as": {
                "tasa_base": 7.55,
                "liquidez": "7 dÃ­as",
                "minimo": 100,
                "tipo": "plazo",
                "plazo_dias": 7
            },
            "Plazo Fijo 28 dÃ­as": {
                "tasa_base": 7.60,
                "liquidez": "28 dÃ­as",
                "minimo": 100,
                "tipo": "plazo",
                "plazo_dias": 28
            },
            "Plazo Fijo 90 dÃ­as": {
                "tasa_base": 7.70,
                "liquidez": "90 dÃ­as",
                "minimo": 100,
                "tipo": "plazo",
                "plazo_dias": 90
            },
            "Plazo Fijo 180 dÃ­as": {
                "tasa_base": 7.80,
                "liquidez": "180 dÃ­as",
                "minimo": 100,
                "tipo": "plazo",
                "plazo_dias": 180
            }
        },
        "color": "#8A05BE",
        "descripcion": "SOFIPO lÃ­der en MÃ©xico con 13+ millones de clientes"
    },
    "DiDi": {
        "logo": "ðŸ§¡",
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
        "descripcion": "Hasta 16% en primeros $10,000, despuÃ©s 8.5%"
    },
    "Stori": {
        "logo": "ðŸ’™",
        "productos": {
            "Stori Cuenta+ (Sin tarjeta)": {
                "tasa_base": 8.00,
                "liquidez": "Inmediata",
                "minimo": 0,
                "tipo": "vista",
                "requisito": False
            },
            "Stori Cuenta+ (Con tarjeta)": {
                "tasa_base": 13.50,
                "liquidez": "Inmediata",
                "minimo": 0,
                "tipo": "vista",
                "requisito": True
            }
        },
        "color": "#0066FF",
        "descripcion": "Requiere tarjeta de crÃ©dito Stori para mejores tasas"
    },
    "Klar": {
        "logo": "ðŸ’š",
        "productos": {
            "Cuenta Klar": {
                "tasa_base": 8.50,
                "liquidez": "Inmediata",
                "minimo": 100,
                "tipo": "vista"
            },
            "InversiÃ³n Flexible Max": {
                "tasa_base": 15.00,
                "liquidez": "Inmediata",
                "minimo": 100,
                "tipo": "vista",
                "requisito": "Plus o Platino",
                "descripcion_extra": "Requiere membresÃ­a Plus o Platino"
            }
        },
        "color": "#00D98C",
        "descripcion": "SOFIPO regulada por CNBV con mÃ¡s de 2M usuarios"
    },
    "UalÃ¡": {
        "logo": "ðŸ’³",
        "productos": {
            "UalÃ¡ Ahorro": {
                "tasa_base": 10.00,
                "liquidez": "Inmediata",
                "minimo": 0,
                "tipo": "vista"
            },
            "UalÃ¡ Plazo Fijo 28 dÃ­as": {
                "tasa_base": 11.00,
                "liquidez": "28 dÃ­as",
                "minimo": 100,
                "tipo": "plazo",
                "plazo_dias": 28
            }
        },
        "color": "#00D4FF",
        "descripcion": "Fintech argentina consolidada en MÃ©xico"
    },
    "Mercado Pago": {
        "logo": "ðŸ’µ",
        "productos": {
            "Rendimientos MP": {
                "tasa_base": 12.50,
                "liquidez": "Inmediata",
                "minimo": 0,
                "tipo": "vista"
            }
        },
        "color": "#00AAFF",
        "descripcion": "Respaldo del ecosistema Mercado Libre"
    },
    "Finsus": {
        "logo": "🦁",
        "productos": {
            "Finsus+ (A la vista)": {
                "tasa_base": 8.09,
                "liquidez": "Inmediata",
                "minimo": 0,
                "tipo": "vista"
            },
            "Apartados": {
                "tasa_base": 4.00,
                "liquidez": "Inmediata",
                "minimo": 0,
                "tipo": "vista"
            },
            "Plazo Fijo 7 días": {
                "tasa_base": 8.00,
                "liquidez": "7 días",
                "minimo": 100,
                "tipo": "plazo",
                "plazo_dias": 7
            },
            "Plazo Fijo 30 días": {
                "tasa_base": 8.09,
                "liquidez": "30 días",
                "minimo": 100,
                "tipo": "plazo",
                "plazo_dias": 30
            },
            "Plazo Fijo 90 días": {
                "tasa_base": 8.39,
                "liquidez": "90 días",
                "minimo": 100,
                "tipo": "plazo",
                "plazo_dias": 90
            },
            "Plazo Fijo 180 días": {
                "tasa_base": 8.59,
                "liquidez": "180 días",
                "minimo": 100,
                "tipo": "plazo",
                "plazo_dias": 180
            },
            "Plazo Fijo 360 días": {
                "tasa_base": 10.09,
                "liquidez": "360 días",
                "minimo": 100,
                "tipo": "plazo",
                "plazo_dias": 360
            }
        },
        "color": "#4CAF50",
        "descripcion": "SOFIPO enfocada en inclusión financiera y sustentabilidad"
    }
}

# ============================================================================
# FUNCIONES DE CÃLCULO
# ============================================================================

def calcular_rendimiento_hibrido_didi(monto, tasa_premium, limite_premium, tasa_base, dias):
    """
    Calcula el rendimiento con estructura hÃ­brida de DiDi
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
    Calcula interÃ©s compuesto con diferentes frecuencias
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
    Calcula interÃ©s simple para inversiones a plazo fijo
    """
    tasa_decimal = tasa_anual / 100
    interes = capital * tasa_decimal * (dias / 365)
    return interes

def generar_proyeccion_mensual(capital, tasa_anual, tipo_calculo, meses=12):
    """
    Genera proyecciÃ³n mes a mes del crecimiento de la inversiÃ³n
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
    Analiza el nivel de diversificaciÃ³n y genera recomendaciones
    """
    total_invertido = sum([inv["monto"] for inv in inversiones_dict.values()])
    
    if total_invertido == 0:
        return None
    
    # Calcular concentraciÃ³n
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

def generar_recomendaciones(analisis, rendimiento_ponderado):
    """
    Genera recomendaciones personalizadas basadas en el anÃ¡lisis
    """
    recomendaciones = []
    
    if analisis is None:
        return ["âš ï¸ Agrega al menos una inversiÃ³n para recibir recomendaciones"]
    
    # Evaluar diversificaciÃ³n
    if analisis["num_sofipos"] == 1:
        recomendaciones.append(
            "ðŸŽ¯ **Alta ConcentraciÃ³n**: EstÃ¡s invirtiendo en una sola SOFIPO. "
            "Considera diversificar en al menos 3-4 instituciones para reducir riesgo."
        )
    elif analisis["max_concentracion"] > 70:
        recomendaciones.append(
            f"âš ï¸ **ConcentraciÃ³n Elevada**: {analisis['max_concentracion']:.1f}% en una sola instituciÃ³n. "
            "Lo ideal es no superar el 40-50% por SOFIPO."
        )
    elif analisis["num_sofipos"] >= 3 and analisis["max_concentracion"] < 50:
        recomendaciones.append(
            "âœ… **Buena DiversificaciÃ³n**: Tu capital estÃ¡ bien distribuido entre mÃºltiples SOFIPOs."
        )
    
    # Evaluar liquidez
    if analisis["porcentaje_liquido"] < 20:
        recomendaciones.append(
            f"ðŸ’§ **Baja Liquidez**: Solo {analisis['porcentaje_liquido']:.1f}% estÃ¡ disponible de forma inmediata. "
            "Considera mantener al menos 20-30% en inversiones lÃ­quidas para emergencias."
        )
    elif analisis["porcentaje_liquido"] > 80:
        recomendaciones.append(
            f"ðŸ’° **Alta Liquidez**: {analisis['porcentaje_liquido']:.1f}% estÃ¡ disponible inmediatamente. "
            "PodrÃ­as mejorar rendimientos moviendo parte a plazos fijos."
        )
    else:
        recomendaciones.append(
            f"âœ… **Balance de Liquidez Adecuado**: {analisis['porcentaje_liquido']:.1f}% lÃ­quido "
            "es un buen equilibrio entre accesibilidad y rendimiento."
        )
    
    # Evaluar rendimiento
    if rendimiento_ponderado < 10:
        recomendaciones.append(
            f"ðŸ“Š **Rendimiento Bajo**: Tu GAT ponderado es {rendimiento_ponderado:.2f}%. "
            "Considera productos como Nu MÃ©xico (15%) o DiDi (16% primeros $10k) para mejorar."
        )
    elif rendimiento_ponderado >= 14:
        recomendaciones.append(
            f"ðŸš€ **Excelente Rendimiento**: Tu GAT ponderado de {rendimiento_ponderado:.2f}% "
            "estÃ¡ por encima del promedio del mercado."
        )
    
    # Recomendaciones especÃ­ficas de protecciÃ³n
    recomendaciones.append(
        "ðŸ›¡ï¸ **ProtecciÃ³n IPAB**: Recuerda que cada SOFIPO estÃ¡ protegida hasta 25,000 UDIs (~200,000 MXN) "
        "por el IPAB. Si inviertes mÃ¡s, distribuye entre varias instituciones."
    )
    
    # Sugerencias de optimizaciÃ³n
    if "Nu MÃ©xico" not in [k for k, v in analisis["concentraciones"].items() if v > 0]:
        recomendaciones.append(
            "ðŸ’¡ **Sugerencia**: Nu MÃ©xico ofrece 15% anual con liquidez inmediata, "
            "una de las mejores combinaciones del mercado."
        )
    
    if analisis["total_invertido"] >= 10000:
        tiene_didi = any("DiDi" in k for k in analisis["concentraciones"].keys() if analisis["concentraciones"][k] > 0)
        if not tiene_didi:
            recomendaciones.append(
                "ðŸ’¡ **Sugerencia DiDi**: Con capital suficiente, considera DiDi para aprovechar "
                "el 16% en los primeros $10,000 MXN."
            )
    
    return recomendaciones

# ============================================================================
# INTERFAZ PRINCIPAL
# ============================================================================

def main():
    # Header principal
    st.markdown('<h1 class="main-header">ðŸ’° Simulador de Inversiones</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Compara rendimientos de SOFIPOs mexicanas en tiempo real</p>', unsafe_allow_html=True)
    
    # ========================================================================
    # CONFIGURACIÃ“N RÃPIDA
    # ========================================================================
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### ðŸŽ¯ Â¿CuÃ¡nto quieres invertir?")
        monto_total = st.number_input(
            "Monto total disponible (MXN)",
            min_value=1000,
            value=50000,
            step=5000,
            help="Este es el capital que tienes disponible para distribuir entre SOFIPOs"
        )
    
    with col2:
        st.markdown("### ðŸ“… Plazo")
        periodo_simulacion = st.selectbox(
            "Simular a:",
            options=[3, 6, 12, 24],
            index=2,
            format_func=lambda x: f"{x} meses"
        )
    
    st.divider()
    
    # ========================================================================
    # SELECCIÃ“N SIMPLE DE SOFIPOS
    # ========================================================================
    
    st.markdown("### ðŸ’³ Selecciona las SOFIPOs donde invertirÃ¡s")
    
    inversiones_seleccionadas = {}
    
    # Placeholder para el indicador de dinero restante (se actualizarÃ¡ al final)
    indicador_restante = st.empty()
    
    # Crear tabs para cada SOFIPO
    sofipos_names = list(SOFIPOS_DATA.keys())
    tabs = st.tabs([f"{SOFIPOS_DATA[s]['logo']} {s}" for s in sofipos_names])
    
    for idx, (sofipo_name, tab) in enumerate(zip(sofipos_names, tabs)):
        with tab:
            sofipo_data = SOFIPOS_DATA[sofipo_name]
            
            # DescripciÃ³n breve
            st.info(f"**{sofipo_data['descripcion']}**")
            
            # Checkbox para incluir esta SOFIPO
            incluir = st.checkbox(
                f"âœ… Quiero invertir en {sofipo_name}",
                key=f"check_{sofipo_name}"
            )
            
            if incluir:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Selector de producto
                    productos = list(sofipo_data['productos'].keys())
                    producto_seleccionado = st.selectbox(
                        "ðŸ“¦ Elige el producto:",
                        options=productos,
                        key=f"prod_{sofipo_name}",
                        help="Selecciona el tipo de inversiÃ³n"
                    )
                    
                    producto_info = sofipo_data['productos'][producto_seleccionado]
                    
                    # Mostrar tasa
                    if producto_info.get("tipo") == "vista_hibrida":
                        st.success(f"**ðŸ“Š GAT: {producto_info['tasa_premium']}%** (primeros ${producto_info['limite_premium']:,})")
                        st.caption(f"DespuÃ©s: {producto_info['tasa_base']}%")
                    elif producto_info.get("limite_max"):
                        st.success(f"**ðŸ“Š GAT: {producto_info['tasa_base']}%** (hasta ${producto_info['limite_max']:,})")
                    else:
                        st.success(f"**ðŸ“Š GAT: {producto_info['tasa_base']}%**")
                    
                    st.caption(f"ðŸ’§ Liquidez: {producto_info['liquidez']}")
                
                with col2:
                    # Selector de modo: Monto o Porcentaje
                    modo_input = st.radio(
                        "Ingresar como:",
                        ["ðŸ’µ Monto ($)", "ðŸ“Š Porcentaje (%)"],
                        key=f"modo_{sofipo_name}",
                        horizontal=True
                    )
                    
                    if modo_input == "ðŸ’µ Monto ($)":
                        # Monto a invertir
                        monto = st.number_input(
                            "Â¿CuÃ¡nto invertirÃ¡s aquÃ­?",
                            min_value=producto_info['minimo'],
                            value=min(max(10000, producto_info['minimo']), monto_total),
                            step=1000,
                            key=f"monto_{sofipo_name}_{producto_seleccionado}",
                            help=f"MÃ­nimo: ${producto_info['minimo']:,} MXN"
                        )
                        
                        # Porcentaje del total
                        porcentaje = (monto / monto_total * 100) if monto_total > 0 else 0
                        st.caption(f"ðŸ“Š Representa el **{porcentaje:.1f}%** de tu capital total")
                    else:
                        # Input de porcentaje
                        porcentaje_input = st.number_input(
                            "Â¿QuÃ© % de tu capital invertirÃ¡s aquÃ­?",
                            min_value=0.0,
                            max_value=100.0,
                            value=10.0,
                            step=5.0,
                            key=f"pct_{sofipo_name}_{producto_seleccionado}",
                            help="Porcentaje de tu capital total"
                        )
                        
                        # Calcular monto desde porcentaje
                        monto = int(monto_total * porcentaje_input / 100)
                        
                        # Validar mÃ­nimo
                        if monto < producto_info['minimo']:
                            st.warning(f"âš ï¸ El {porcentaje_input}% equivale a ${monto:,}, pero el mÃ­nimo es ${producto_info['minimo']:,}")
                            monto = producto_info['minimo']
                        
                        st.caption(f"ðŸ’µ InvertirÃ¡s **${monto:,.0f}**")
                    
                    # Requisitos especiales
                    cumple_requisito = True
                    if producto_info.get("requisito") is not None:
                        if producto_info.get("requisito") == True:
                            cumple_requisito = st.checkbox(
                                "Â¿Tienes tarjeta de crÃ©dito Stori?",
                                value=True,
                                key=f"req_{sofipo_name}_{producto_seleccionado}",
                                help="Necesitas la tarjeta para obtener esta tasa"
                            )
                        elif producto_info.get("requisito") == "Plus o Platino":
                            cumple_requisito = st.checkbox(
                                "Â¿Tienes membresÃ­a Klar Plus o Platino?",
                                value=True,
                                key=f"req_{sofipo_name}_{producto_seleccionado}",
                                help="Necesitas membresÃ­a Plus o Platino para obtener el 15%"
                            )
                
                # Guardar inversiÃ³n
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
    
    # Mostrar indicador visual con color segÃºn el estado
    with indicador_restante.container():
        if dinero_restante > 0:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("ðŸ’° Dinero asignado", f"${total_asignado_actual:,.0f}", f"{porcentaje_asignado:.1f}%")
            with col2:
                st.metric("ðŸ”“ Dinero disponible", f"${dinero_restante:,.0f}", f"{porcentaje_restante:.1f}%")
            with col3:
                st.metric("ðŸ“Š Total", f"${monto_total:,.0f}", "100%")
        elif dinero_restante == 0:
            st.success(f"âœ… **Perfecto!** Has distribuido todo tu dinero: ${monto_total:,.0f} (100%)")
        else:
            st.error(f"âš ï¸ **Â¡Cuidado!** Te has pasado ${abs(dinero_restante):,.0f}. Ajusta los montos.")
    
    st.divider()
    
    # ========================================================================
    # CÃLCULOS Y RESULTADOS
    # ========================================================================
    
    if len(inversiones_seleccionadas) > 0:
        st.divider()
        st.markdown("## ðŸ“Š Tus Resultados")
        
        # Validar que no exceda el monto total
        total_asignado = sum([inv["monto"] for inv in inversiones_seleccionadas.values()])
        
        if total_asignado > monto_total:
            st.error(f"âš ï¸ **Cuidado:** Has asignado ${total_asignado:,.0f} pero solo tienes ${monto_total:,.0f}. Ajusta los montos.")
            return
        
        diferencia = monto_total - total_asignado
        if diferencia > 0:
            st.warning(f"ðŸ’¡ Tienes **${diferencia:,.0f}** sin asignar. Â¿Quieres agregarlo a alguna SOFIPO?")
        
        # Calcular rendimientos para cada inversiÃ³n
        resultados = []
        proyecciones_todas = []
        
        for inversion_key, inversion in inversiones_seleccionadas.items():
            monto = inversion['monto']
            producto_info = inversion['producto_info']
            tipo = producto_info['tipo']
            
            # Determinar tasa efectiva
            if tipo == "vista_hibrida":
                # DiDi con estructura hÃ­brida
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
                # A la vista con interÃ©s compuesto
                tasa_efectiva = producto_info['tasa_base']
                tipo_interes = "Compuesto (Diario)"
                
            elif tipo == "plazo":
                # Plazo fijo con interÃ©s simple
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
                "Ganancia/DÃ­a": f"${ganancia_dia:.2f}",
                "Ganancia/Mes": f"${ganancia_mes:.2f}",
                "Ganancia/AÃ±o": f"${ganancia_anio:.2f}",
                f"Total ({periodo_simulacion} meses)": f"${monto + ganancia_periodo:,.2f}",
                "Ganancia Total": f"${ganancia_periodo:,.2f}",
                "Tipo InterÃ©s": tipo_interes
            })
            
            # Generar proyecciÃ³n mensual
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
        
        # MÃ©tricas principales en cards grandes
        st.markdown("### ðŸ’° Resultado de tu inversiÃ³n")
        
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
        st.success(f"ðŸ“Š **Tu tasa promedio ponderada es: {rendimiento_ponderado:.2f}% anual**")
        
        # Tabla detallada en expander
        with st.expander("ï¿½ Ver desglose detallado por SOFIPO"):
            df_resultados = pd.DataFrame(resultados)
            st.dataframe(df_resultados, width="stretch", hide_index=True)
        
        # ====================================================================
        # GRÃFICO PRINCIPAL
        # ====================================================================
        
        if len(proyecciones_todas) > 0:
            st.subheader("ðŸ“ˆ ProyecciÃ³n de Crecimiento Total")
            
            # Combinar todas las proyecciones
            df_proyecciones_completo = pd.concat(proyecciones_todas, ignore_index=True)
            
            # Agrupar por mes y sumar TODO (capital + intereses de todas las SOFIPOs)
            df_total = df_proyecciones_completo.groupby('Mes').agg({
                'Capital Inicial': 'sum',
                'Intereses Generados': 'sum',
                'Total Acumulado': 'sum'
            }).reset_index()
            
            # Crear grÃ¡fico de lÃ­nea Ãºnica con el TOTAL
            fig = go.Figure()
            
            # LÃ­nea principal: Total acumulado de TODAS las inversiones
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
            
            # LÃ­nea de referencia: Capital inicial (sin intereses)
            fig.add_trace(go.Scatter(
                x=df_total['Mes'],
                y=[total_invertido] * len(df_total),
                mode='lines',
                name='Capital Inicial',
                line=dict(width=2, color='gray', dash='dash'),
                hovertemplate='Capital: $%{y:,.0f}<extra></extra>'
            ))
            
            fig.update_layout(
                title=f"Crecimiento total de tu portafolio a {periodo_simulacion} meses",
                xaxis_title="Meses",
                yaxis_title="Monto Total (MXN)",
                hovermode='x unified',
                template="plotly_white",
                height=500,
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # GrÃ¡fico de Ã¡rea apilada (Capital vs Intereses)
            st.subheader("ðŸ’µ Desglose: Capital vs Intereses")
            
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
                title="ComposiciÃ³n del patrimonio total",
                xaxis_title="Meses",
                yaxis_title="Monto (MXN)",
                hovermode='x unified',
                template="plotly_white",
                height=400
            )
            
            st.plotly_chart(fig_area, use_container_width=True)
            st.subheader("ðŸ“‹ Desglose Mensual Detallado")
            
            for inversion_key, df_proyeccion in zip(
                df_proyecciones_completo['SOFIPO'].unique(),
                proyecciones_todas
            ):
                with st.expander(f"ðŸ“Š {inversion_key}"):
                    # Formatear el dataframe
                    df_display = df_proyeccion.copy()
                    df_display['Capital Inicial'] = df_display['Capital Inicial'].apply(lambda x: f"${x:,.2f}")
                    df_display['Intereses Generados'] = df_display['Intereses Generados'].apply(lambda x: f"${x:,.2f}")
                    df_display['Total Acumulado'] = df_display['Total Acumulado'].apply(lambda x: f"${x:,.2f}")
                    df_display = df_display.drop('SOFIPO', axis=1)
                    
                    st.dataframe(df_display, width="stretch", hide_index=True)
        
        # ====================================================================
        # ANÃLISIS Y RECOMENDACIONES
        # ====================================================================
        
        st.divider()
        st.header("3ï¸âƒ£ AnÃ¡lisis de Riesgo y Recomendaciones")
        
        # Realizar anÃ¡lisis de diversificaciÃ³n
        analisis = analizar_diversificacion(inversiones_seleccionadas)
        if analisis:
            recomendaciones = generar_recomendaciones(analisis, rendimiento_ponderado)
            
            # Mostrar mÃ©tricas de diversificaciÃ³n
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "ðŸŽ¯ SOFIPOs utilizadas",
                    f"{analisis['num_sofipos']}/6",
                    help="NÃºmero de SOFIPOs diferentes en tu portafolio"
                )
            
            with col2:
                st.metric(
                    "âš–ï¸ ConcentraciÃ³n mÃ¡xima",
                    f"{analisis['max_concentracion']:.1f}%",
                    delta="Ã“ptimo: <50%" if analisis['max_concentracion'] < 50 else "Alto riesgo",
                    delta_color="normal" if analisis['max_concentracion'] < 50 else "inverse"
                )
            
            with col3:
                st.metric(
                    "ðŸ’§ Liquidez inmediata",
                    f"{analisis['porcentaje_liquido']:.1f}%",
                    help="Porcentaje disponible sin penalizaciÃ³n"
                )
        
            # GrÃ¡fico de distribuciÃ³n
            st.subheader("ðŸ“Š DistribuciÃ³n de tu portafolio")
            
            df_concentracion = pd.DataFrame([
                {"SOFIPO": k, "Porcentaje": v, "Monto": inversiones_seleccionadas[k]["monto"]}
                for k, v in analisis["concentraciones"].items()
                if v > 0
            ])
            
            fig_pie = px.pie(
                df_concentracion,
                values='Porcentaje',
                names='SOFIPO',
                title='DistribuciÃ³n por SOFIPO',
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
            
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # Mostrar recomendaciones
            st.subheader("ðŸ’¡ Recomendaciones Personalizadas")
            
            for i, recomendacion in enumerate(recomendaciones, 1):
                if "âœ…" in recomendacion:
                    st.markdown(f'<div class="success-box">{recomendacion}</div>', unsafe_allow_html=True)
                elif "âš ï¸" in recomendacion or "ðŸŽ¯" in recomendacion:
                    st.markdown(f'<div class="warning-box">{recomendacion}</div>', unsafe_allow_html=True)
                else:
                    st.info(recomendacion)
        
        # ====================================================================
        # ESTRATEGIAS SUGERIDAS
        # ====================================================================
        
        st.divider()
        st.header("4ï¸âƒ£ Estrategias de OptimizaciÃ³n")
        
        tab1, tab2, tab3 = st.tabs(["ðŸ›¡ï¸ Conservadora", "âš–ï¸ Balanceada", "ðŸš€ Agresiva"])
        
        with tab1:
            st.markdown("""
            ### Estrategia Conservadora (Menor Riesgo)
            
            **Perfil**: Prioriza seguridad y liquidez sobre rendimiento mÃ¡ximo.
            
            **DistribuciÃ³n sugerida**:
            - 30% Nu MÃ©xico (Cajita Turbo) - 15% GAT (hasta $25k)
            - 25% Mercado Pago - 12.5% GAT
            - 20% UalÃ¡ Ahorro - 10% GAT
            - 15% Klar Cuenta - 8.5% GAT
            - 10% Nu MÃ©xico (Dinero en Cajita) - 7.5% GAT (emergencias)
            
            **Ventajas**:
            - âœ… MÃ¡xima liquidez inmediata (100%)
            - âœ… DiversificaciÃ³n en 4 instituciones sÃ³lidas
            - âœ… Rendimiento promedio ~11% anual
            
            **Consideraciones**:
            - Todas las opciones tienen liquidez inmediata
            - Ideal para fondos de emergencia
            - Sin requisitos especiales ni membresÃ­as
            """)
        
        with tab2:
            st.markdown("""
            ### Estrategia Balanceada (Riesgo Moderado)
            
            **Perfil**: Balance entre rendimiento, liquidez y diversificaciÃ³n.
            
            **DistribuciÃ³n sugerida**:
            - 20% DiDi (hasta $10k) - 16% GAT (despuÃ©s 8.5%)
            - 25% Nu MÃ©xico (Cajita Turbo) - 15% GAT
            - 20% Klar InversiÃ³n Max - 15% GAT (requiere Plus/Platino)
            - 20% Stori Cuenta+ (con tarjeta) - 13.5% GAT
            - 15% Mercado Pago - 12.5% GAT
            
            **Ventajas**:
            - âœ… Excelente diversificaciÃ³n (5 SOFIPOs)
            - âœ… 100% con liquidez inmediata
            - âœ… Rendimiento optimizado (~14% ponderado)
            
            **Consideraciones**:
            - Requiere tarjeta Stori y membresÃ­a Klar Plus/Platino
            - Balance perfecto entre liquidez y rendimiento
            - Ideal para la mayorÃ­a de inversores
            """)
        
        with tab3:
            st.markdown("""
            ### ðŸš€ Estrategia Agresiva - Maximizar Rendimientos
            
            **Objetivo**: Obtener el **mÃ¡ximo rendimiento posible** sin importar el riesgo ni la liquidez.
            
            **FilosofÃ­a**: Toda tu inversiÃ³n trabaja al mÃ¡ximo, aprovechando las mejores tasas de mercado.
            """)
            
            # Calcular distribuciÃ³n agresiva con montos especÃ­ficos
            st.subheader("ðŸ’° DistribuciÃ³n Recomendada para tu Capital")
            
            # Estrategia: Maximizar tasas - DiDi (16%), Klar Max (15%), Nu Turbo (15%), Stori (13.5%)
            distribucion_agresiva = []
            
            # 1. DiDi Ahorro: Invertir hasta $10,000 al 16% (MÃXIMA PRIORIDAD)
            monto_didi = min(10000, monto_total)
            distribucion_agresiva.append({
                "sofipo": "DiDi",
                "producto": "DiDi Ahorro",
                "monto": monto_didi,
                "tasa": 16.0,
                "razon": "ðŸ¥‡ MÃ¡xima tasa del mercado (primeros $10k, despuÃ©s 8.5%)"
            })
            
            saldo_restante = monto_total - monto_didi
            
            # 2. Klar InversiÃ³n Flexible Max: 15% (requiere Plus/Platino)
            if saldo_restante > 0:
                monto_klar = int(saldo_restante * 0.40)  # 40% del restante
                if monto_klar >= 100:
                    distribucion_agresiva.append({
                        "sofipo": "Klar",
                        "producto": "InversiÃ³n Flexible Max",
                        "monto": monto_klar,
                        "tasa": 15.0,
                        "razon": "ðŸ¥ˆ 15% con liquidez inmediata (requiere Plus/Platino)"
                    })
                    saldo_restante -= monto_klar
            
            # 3. Nu MÃ©xico Cajita Turbo: Hasta $25,000 al 15%
            if saldo_restante > 0:
                monto_nu_turbo = min(25000, saldo_restante)
                if monto_nu_turbo > 0:
                    distribucion_agresiva.append({
                        "sofipo": "Nu MÃ©xico",
                        "producto": "Cajita Turbo",
                        "monto": monto_nu_turbo,
                        "tasa": 15.0,
                        "razon": "ï¿½ 15% hasta $25k con liquidez inmediata"
                    })
                    saldo_restante -= monto_nu_turbo
            
            # 4. Stori Cuenta+ (con tarjeta): Al 13.5%
            if saldo_restante > 0:
                distribucion_agresiva.append({
                    "sofipo": "Stori",
                    "producto": "Stori Cuenta+ (Con tarjeta)",
                    "monto": saldo_restante,
                    "tasa": 13.5,
                    "razon": "ðŸ¥‰ 13.5% (requiere tarjeta de crÃ©dito Stori)"
                })
            
            # Mostrar tabla con montos exactos
            st.markdown("**ðŸ’µ Montos especÃ­ficos sugeridos:**")
            
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
            
            st.success(f"ðŸŽ¯ **Con esta estrategia agresiva obtendrÃ¡s:**")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Tasa ponderada", f"{tasa_ponderada_agresiva:.2f}%")
            with col2:
                st.metric("Ganancia estimada (12 meses)", f"${ganancia_12m:,.0f}")
            
            st.warning("""
            **âš ï¸ Consideraciones importantes:**
            - Esta estrategia prioriza SOLO rendimiento mÃ¡ximo
            - Parte del capital quedarÃ¡ en plazos fijos (menor liquidez)
            - Requiere tarjeta de crÃ©dito Stori para obtener el 13.5%
            - No es recomendable para fondos de emergencia
            - DiversificaciÃ³n limitada a favor de mejores tasas
            """)
        
        # ====================================================================
        # INFORMACIÃ“N ADICIONAL
        # ====================================================================
        
        st.divider()
        
        with st.expander("ðŸ“– Glosario y Conceptos Clave"):
            st.markdown("""
            **GAT Nominal**: Ganancia Anual Total antes de impuestos. Es la tasa de rendimiento anual.
            
            **GAT Real**: Ganancia Anual Total despuÃ©s de restar inflaciÃ³n.
            
            **InterÃ©s Simple**: InterÃ©s calculado solo sobre el capital inicial.
            
            **InterÃ©s Compuesto**: InterÃ©s calculado sobre capital + intereses previos.
            
            **IPAB**: Instituto para la ProtecciÃ³n al Ahorro Bancario. Protege hasta 25,000 UDIs (~$200,000 MXN) por persona por instituciÃ³n.
            
            **SOFIPO**: Sociedad Financiera Popular regulada por CNBV.
            
            **Liquidez**: Facilidad para convertir la inversiÃ³n en efectivo sin penalizaciÃ³n.
            """)
        
        with st.expander("âš–ï¸ Aspectos Legales y Fiscales"):
            st.markdown("""
            ### RegulaciÃ³n
            - Todas las SOFIPOs mostradas estÃ¡n reguladas por CNBV
            - Supervisadas por Banco de MÃ©xico y CONDUSEF
            - Sujetas a la Ley de Ahorro y CrÃ©dito Popular
            
            ### ProtecciÃ³n IPAB
            - Cobertura: Hasta 25,000 UDIs por persona por instituciÃ³n
            - Equivalente aproximado: ~$200,000 MXN (varÃ­a con UDI)
            - Aplica a depÃ³sitos en SOFIPOs reguladas
            
            ### Impuestos
            - Los intereses generados estÃ¡n sujetos a ISR
            - Las SOFIPOs retienen impuestos automÃ¡ticamente
            - Tasa de retenciÃ³n: 1.04% mensual (aprox)
            - DeclaraciÃ³n anual puede generar saldo a favor
            
            **Nota**: Consulta con un contador para tu situaciÃ³n especÃ­fica.
            """)
    
    else:
        st.info("ðŸ‘† Selecciona al menos una SOFIPO arriba para comenzar la simulaciÃ³n")
        
        # Mostrar tabla comparativa de tasas
        st.subheader("ðŸ“Š Tabla Comparativa de Tasas (Referencia)")
        
        tabla_comparativa = []
        for sofipo_name, sofipo_data in SOFIPOS_DATA.items():
            for producto_name, producto_info in sofipo_data['productos'].items():
                tabla_comparativa.append({
                    "SOFIPO": f"{sofipo_data['logo']} {sofipo_name}",
                    "Producto": producto_name,
                    "GAT Nominal": f"{producto_info['tasa_base']}%",
                    "Liquidez": producto_info['liquidez'],
                    "MÃ­nimo": f"${producto_info['minimo']:,}"
                })
        
        df_comparativa = pd.DataFrame(tabla_comparativa)
        st.dataframe(df_comparativa, width="stretch", hide_index=True)
    
    # Footer
    st.divider()
    st.markdown("""
    ---
    <div style='text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 20px; color: white; margin-top: 2rem;'>
        <h3 style='margin: 0; font-weight: 700;'>ðŸ’° Simulador de Inversiones Multi-SOFIPO</h3>
        <p style='margin: 1rem 0; opacity: 0.9;'>âš ï¸ Este simulador es una herramienta educativa. Las tasas pueden variar.<br>
        Verifica siempre las condiciones vigentes con cada instituciÃ³n.</p>
        <p style='margin: 0.5rem 0;'><span class="badge">ðŸ“… Tasas actualizadas: Noviembre 2025</span></p>
        <p style='margin-top: 1rem; font-size: 1.1rem;'>Desarrollado con â¤ï¸ para inversionistas mexicanos ðŸ‡²ðŸ‡½</p>
    </div>
    """, unsafe_allow_html=True)


# Mostrar fecha de última actualización al final
st.markdown("---")
st.markdown('<div style="text-align: center; font-size: 0.7rem; color: #999; padding: 1rem;"> Última actualización de tasas: 20 de Noviembre, 2025</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
