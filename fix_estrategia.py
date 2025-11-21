#!/usr/bin/env python3
# -*- coding: utf-8 -*-

with open('c:\\Users\\daniel.gonzalez\\simulador_sofipos.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Insertar el código en la línea 1430 (después de st.divider())
insert_pos = 1430
new_code = '''    # ========================================================================
    # APLICAR ESTRATEGIA OBJETIVO SI ESTÁ PENDIENTE
    # ========================================================================
    
    if "estrategia_objetivo_pendiente" in st.session_state:
        estrategia = st.session_state["estrategia_objetivo_pendiente"]
        
        # Aplicar el capital (esto se reflejará en el widget)
        if "monto_total_input" not in st.session_state:
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
            
            # Seleccionar el producto
            st.session_state[f"prod_{sofipo_nombre}"] = producto_nombre
            
            # Asignar el monto
            st.session_state[f"monto_{sofipo_nombre}_{producto_nombre}"] = int(monto)
        
        # Limpiar la estrategia pendiente
        del st.session_state["estrategia_objetivo_pendiente"]
        
        st.success(f"✅ **Estrategia aplicada:** ${estrategia['capital']:,.0f} distribuidos en {len(estrategia['distribucion'])} productos")
    
'''

lines.insert(insert_pos, new_code)

with open('c:\\Users\\daniel.gonzalez\\simulador_sofipos.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ Código insertado correctamente")
