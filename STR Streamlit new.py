# ==========================================
# STOCK TRANSFER DASHBOARD - PHASE 3 FINAL
# L2 Warm Cream + Orange Theme
# ==========================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import io
import time
import warnings
import re
warnings.filterwarnings('ignore')

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Talabat Stock Transfer",
    page_icon="🧡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== PLOTLY THEME ====================
pio.templates["warm_cream"] = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#3D2415', family='Inter', size=13),
        xaxis=dict(gridcolor='rgba(44,24,16,0.08)', zeroline=False,
                   linecolor='rgba(44,24,16,0.15)', color='#3D2415'),
        yaxis=dict(gridcolor='rgba(44,24,16,0.08)', zeroline=False,
                   linecolor='rgba(44,24,16,0.15)', color='#3D2415'),
        colorway=['#FF6F00','#22c55e','#f59e0b','#ef4444',
                  '#8b5cf6','#06b6d4','#3b82f6','#f97316']
    )
)
pio.templates.default = "warm_cream"

# ==================== CSS - L2 WARM CREAM THEME ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp {
        background: linear-gradient(135deg, #FDF8F0 0%, #FFF5E6 50%, #FDF8F0 100%);
        color: #3D2415;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2C1810 0%, #3D2415 100%);
        border-right: none;
        box-shadow: 4px 0 20px rgba(44,24,16,0.15);
    }
    [data-testid="stSidebar"] * { color: #FFE0C0 !important; }
    [data-testid="stSidebar"] .stMarkdown p { color: #FFE0C0 !important; }
    [data-testid="stSidebar"] label { color: #FFE0C0 !important; }
    h1, h2, h3, h4, h5, h6 { color: #2C1810 !important; font-weight: 800 !important; }
    .stMarkdown, p, span, label, div { color: #3D2415 !important; }

    /* TABS */
    .stTabs {
        position: sticky !important; top: 0 !important; z-index: 999 !important;
        background: linear-gradient(180deg, #FDF8F0 0%, #FFF5E6 100%) !important;
        padding: 18px 0 22px 0 !important;
        border-bottom: 3px solid rgba(255,111,0,0.25) !important;
        box-shadow: 0 4px 15px rgba(44,24,16,0.06);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        background: rgba(255,111,0,0.05) !important;
        border-radius: 22px !important;
        padding: 12px 20px !important;
        border: 2px solid rgba(255,111,0,0.15) !important;
        justify-content: center !important;
        flex-wrap: wrap !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.6) !important;
        color: #8B7355 !important;
        border-radius: 14px !important;
        padding: 12px 20px !important;
        font-weight: 700 !important;
        font-size: 13px !important;
        min-width: 120px !important;
        border: 1px solid rgba(44,24,16,0.08) !important;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255,111,0,0.1) !important;
        color: #FF6F00 !important;
        border-color: rgba(255,111,0,0.3) !important;
        transform: translateY(-3px) !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FF6F00 0%, #FF9A3C 100%) !important;
        color: #FFFFFF !important;
        border-color: #FF9A3C !important;
        box-shadow: 0 10px 30px rgba(255,111,0,0.35) !important;
        transform: translateY(-4px) scale(1.03) !important;
        font-weight: 800 !important;
    }
    .stTabs [data-baseweb="tab-panel"] { padding-top: 25px !important; }
    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] { display: none !important; }

    /* BUTTONS */
    .stButton>button {
        background: linear-gradient(135deg, #FF6F00 0%, #FF9A3C 100%) !important;
        color: #FFFFFF !important;
        border-radius: 14px !important;
        padding: 14px 30px !important;
        font-weight: 700 !important;
        border: none !important;
        box-shadow: 0 6px 20px rgba(255,111,0,0.3) !important;
    }
    .stButton>button:hover { transform: translateY(-2px) !important; }
    .stDownloadButton>button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: #ffffff !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricValue"] { font-size: 28px !important; font-weight: 800 !important; color: #FF6F00 !important; }
    [data-testid="stMetricLabel"] { color: #8B7355 !important; font-size: 13px !important; }

    /* INPUTS */
    .stNumberInput input, .stTextInput input {
        background: #FFFFFF !important; color: #3D2415 !important;
        border-radius: 8px !important; border: 1px solid #E8D5C0 !important;
    }
    .stSelectbox > div > div {
        background: #FFFFFF !important; border-radius: 8px !important;
        border: 1px solid #E8D5C0 !important;
    }
    .stSelectbox > div > div > div { color: #3D2415 !important; font-weight: 600 !important; }
    .stMultiSelect > div > div {
        background: #FFFFFF !important; border-radius: 8px !important;
        border: 1px solid #E8D5C0 !important;
    }
    .stMultiSelect > div > div > div { color: #3D2415 !important; }
    [role="listbox"] [role="option"] { color: #3D2415 !important; background: #FFFFFF !important; }
    [data-baseweb="menu"] * { color: #3D2415 !important; }
    [data-baseweb="popover"] * { color: #3D2415 !important; }

    /* DATA TABLE */
    [data-testid="stDataFrame"] {
        background: rgba(255,255,255,0.92) !important;
        border-radius: 14px !important;
        border: 1px solid rgba(44,24,16,0.08) !important;
        box-shadow: 0 2px 12px rgba(44,24,16,0.05) !important;
    }
    .stExpander {
        background: rgba(255,255,255,0.92) !important;
        border: 1px solid rgba(44,24,16,0.08) !important;
        border-radius: 14px !important;
    }
    hr { border-color: rgba(44,24,16,0.1) !important; margin: 25px 0 !important; }
    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: #FDF8F0; }
    ::-webkit-scrollbar-thumb { background: #FF6F00; border-radius: 8px; }
    .stAlert { border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
def init_session_state():
    defaults = {
        'calculation_done': False, 'sales_data': None, 'sku_master': None,
        'stock_status': None, 'promo_calendar': None, 'sales_enhanced': None,
        'final_results': None, 'filtered_results': None,
        'calc_time': None, 'calc_date': None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
init_session_state()

# ==================== COLOR PALETTE ====================
STATUS_COLORS = {'OOS':'#7f1d1d','Critical':'#ef4444','Low':'#f59e0b','OK':'#22c55e','Overstock':'#3b82f6'}
COV_COLORS = {'OOS':'#7f1d1d','Critical':'#ef4444','Very Low':'#f97316','Low':'#f59e0b','OK':'#22c55e','Overstock':'#3b82f6'}
KPI_COLORS = {
    'primary':'#FF6F00','primary_light':'#FF9A3C',
    'success':'#059669','danger':'#dc2626','danger_dark':'#7f1d1d',
    'warning':'#d97706','info':'#2563eb','purple':'#7c3aed',
    'orange':'#ea580c','teal':'#0d9488','slate':'#475569',
    'pink':'#db2777','indigo':'#4f46e5',
}
CHART_TEXT = '#3D2415'
CHART_GRID = 'rgba(44,24,16,0.06)'

# ==================== HELPER FUNCTIONS ====================
def create_colored_kpi(title, value, subtitle="", icon="📊", bg_color="#FF6F00"):
    return f"""
    <div style='background:{bg_color}; padding:18px; border-radius:14px; text-align:center;
                box-shadow:0 6px 25px rgba(0,0,0,0.15); margin:4px;
                border:1px solid rgba(255,255,255,0.15);'>
        <p style='color:rgba(255,255,255,0.85); margin:0; font-size:10px;
                  font-weight:600; text-transform:uppercase; letter-spacing:0.5px;'>{icon} {title}</p>
        <h2 style='color:#FFFFFF; margin:6px 0; font-size:22px; font-weight:900;'>{value}</h2>
        <p style='color:rgba(255,255,255,0.9); margin:0; font-size:11px; font-weight:600;'>{subtitle}</p>
    </div>"""

def create_action_card(icon, title, value, action_text, bg_color="#FF6F00"):
    return f"""
    <div style='background:linear-gradient(135deg, {bg_color} 0%, {bg_color}dd 100%);
                padding:18px; border-radius:14px; text-align:center;
                box-shadow:0 6px 25px rgba(0,0,0,0.15); margin:4px;
                border:1px solid rgba(255,255,255,0.15);'>
        <p style='color:#FFFFFF; margin:0; font-size:28px;'>{icon}</p>
        <h3 style='color:#FFFFFF !important; margin:6px 0; font-size:16px; font-weight:800;'>{title}</h3>
        <p style='color:#FFFFFF; margin:4px 0; font-size:20px; font-weight:900;'>{value}</p>
        <p style='color:rgba(255,255,255,0.85); margin:4px 0 0 0; font-size:11px;
                  font-weight:600; background:rgba(0,0,0,0.2); padding:4px 10px;
                  border-radius:8px; display:inline-block;'>{action_text}</p>
    </div>"""

def info_card(text):
    return f"""
    <div style='background:rgba(255,111,0,0.06); border:1px solid rgba(255,111,0,0.2);
                border-radius:12px; padding:14px; margin-bottom:12px;'>
        <span style='color:#3D2415; font-size:12px;'>{text}</span>
    </div>"""

def fmt(num, prefix="", suffix=""):
    if pd.isna(num): return f"{prefix}0{suffix}"
    num = float(num)
    if abs(num) >= 1000000: return f"{prefix}{num/1000000:.1f}M{suffix}"
    elif abs(num) >= 1000: return f"{prefix}{num/1000:.1f}K{suffix}"
    return f"{prefix}{num:,.0f}{suffix}"

def clean_number(val):
    if pd.isna(val): return 0.0
    if isinstance(val, (int, float)): return float(val)
    if isinstance(val, str):
        val = val.replace('AED','').replace(',','').replace(' ','').strip()
        try: return float(val)
        except: return 0.0
    return 0.0

def safe_div(a, b, default=0):
    try:
        if b == 0 or pd.isna(b): return default
        return a / b
    except: return default

# ==================== STOCK STATUS & COVERAGE ====================
def get_stock_status(row):
    cs=row['Current_Stock']; mn=row['Final_Min_Stock']
    ideal=row['Final_Ideal_Stock']; mx=row['Final_Max_Stock']
    if cs==0: return 'OOS'
    if cs<mn*0.5: return 'Critical'
    if cs<ideal: return 'Low'
    if cs<=mx: return 'OK'
    return 'Overstock'

def get_coverage_category(row):
    cs=row['Current_Stock']; ideal=row['Final_Ideal_Stock']; mx=row['Final_Max_Stock']
    if cs==0: return 'OOS'
    if cs>mx: return 'Overstock'
    if ideal<=0: return 'OK'
    cov=cs/ideal*100
    if cov<=25: return 'Critical'
    if cov<=50: return 'Very Low'
    if cov<=75: return 'Low'
    return 'OK'

def get_coverage_pct(row):
    ideal=row['Final_Ideal_Stock']
    if ideal<=0: return 0
    return round(row['Current_Stock']/ideal*100,1)

def get_dos_category(row):
    if row['Current_Stock']==0: return 'OOS (0 days)'
    target=row['Final_Ideal_Stock'] if row['Final_Ideal_Stock']>0 else 1
    hp=(row['Current_Stock']/target)*100
    if hp<=25: return 'Critical (<1 day)'
    elif hp<=50: return 'Very Low (1-3 days)'
    elif hp<=70: return 'Low (3-7 days)'
    elif hp<=130: return 'OK (7-14 days)'
    return 'High Stock (>30 days)'

# ==================== SKU EXTRACTION (Same as before) ====================
def extract_sku_values(name):
    clean=name.lower().replace('×','x').replace('*','x')
    has_mult='none'; pack_count=1; size_raw='unknown'; unit='unknown'
    m=re.search(r'pack of (\d+)',clean)
    if m: has_mult='pack_of'; pack_count=int(m.group(1))
    else:
        m=re.search(r'(\d+)\s*pk\b',clean)
        if m: has_mult='pk'; pack_count=int(m.group(1))
        else:
            m=re.search(r'(\d+)-pack',clean)
            if m: has_mult='dash_pack'; pack_count=int(m.group(1))
            else:
                m=re.search(r'(\d+)\s+pack\b',clean)
                if m: has_mult='space_pack'; pack_count=int(m.group(1))
                else:
                    m=re.search(r'(\d+)[xX](\d)',clean)
                    if m: has_mult='x_pattern'; pack_count=int(m.group(1))
                    else:
                        m=re.search(r'(\d+)\s[xX]\s(\d)',clean)
                        if m: has_mult='x_space_pattern'; pack_count=int(m.group(1))
    patterns=[(r'(\d+\.?\d*)\s*millilitre','ml'),(r'(\d+\.?\d*)\s*milliliter','ml'),(r'(\d+\.?\d*)\s*litre','l'),(r'(\d+\.?\d*)\s*liter','l'),(r'(\d+\.?\d*)\s*kilogram','kg'),(r'(\d+\.?\d*)\s*kilo\b','kg'),(r'(\d+\.?\d*)\s*gram[s]?\b','g'),(r'(\d+\.?\d*)\s*ltr\b','l'),(r'(\d+\.?\d*)\s*lt\b','l'),(r'(\d+\.?\d*)\s*ml\b','ml'),(r'(\d+\.?\d*)\s*mg\b','mg'),(r'(\d+\.?\d*)\s*gm\b','g'),(r'(\d+\.?\d*)\s*kg\b','kg'),(r'(\d+\.?\d*)\s*cl\b','cl'),(r'(\d+\.?\d*)\s*oz\b','oz'),(r'(\d+\.?\d*)\s*lb[s]?\b','lb'),(r'(\d+\.?\d*)\s*l\b','l'),(r'(\d+\.?\d*)\s*g\b','g'),(r'(\d+)\s*pcs\b','pcs'),(r'(\d+)\s*pieces\b','pcs'),(r'(\d+)\s*bags\b','pcs'),(r'(\d+)\s*rolls\b','pcs'),(r'(\d+)\s*sheets\b','pcs'),(r'(\d+)\s*tabs\b','pcs'),(r'(\d+)\s*tablets\b','pcs'),(r'(\d+)\s*sachets\b','pcs')]
    if has_mult in ['x_pattern','x_space_pattern']:
        m=re.search(r'[xX]\s*(\d+\.?\d*)',clean)
        if m:
            val=float(m.group(1)); size_raw=int(val) if val==int(val) else val
            rest=clean[clean.find(m.group(0))+len(m.group(0)):]
            for pat,u in patterns:
                mu=re.search(pat,rest)
                if mu: unit=u; break
            if unit=='unknown': unit='ml'
            return has_mult,pack_count,size_raw,unit
    for pat,u in patterns:
        m=re.search(pat,clean)
        if m: val=float(m.group(1)); size_raw=int(val) if val==int(val) else val; unit=u; break
    return has_mult,pack_count,size_raw,unit

def convert_to_size_ml(size_raw,unit):
    if size_raw=='unknown': return 0
    val=float(size_raw)
    conv={'ml':val,'l':val*1000,'cl':val*10,'oz':round(val*29.5735),'kl':val*1000000,'g':val,'kg':val*1000,'mg':val/1000,'lb':round(val*453.592),'pcs':val,'unknown':val}
    return conv.get(unit,val)

def get_pack_size_display(size_ml,unit):
    if size_ml==0: return 'unknown'
    if unit in ['ml','l','cl','oz','kl']:
        if size_ml>=1000: v=size_ml/1000; return f"{int(v)}L" if v==int(v) else f"{round(v,2)}L"
        return f"{int(size_ml)}ml" if size_ml==int(size_ml) else f"{size_ml}ml"
    if unit in ['g','kg','mg','lb']:
        if size_ml>=1000: v=size_ml/1000; return f"{int(v)}kg" if v==int(v) else f"{round(v,2)}kg"
        return f"{int(size_ml)}g" if size_ml==int(size_ml) else f"{size_ml}g"
    if unit in ['pcs','sheets','rolls','bags']: return f"{int(size_ml)}pcs"
    return 'unknown'

def get_shelf_life_category(days):
    if days<=3: return 'Very Short'
    if days<=7: return 'Short'
    if days<=14: return 'Medium'
    if days<=30: return 'Long'
    return 'Very Long'

def find_competitors(current_sku,all_skus_df,sku_sizes):
    my_code=current_sku['SKU_Code']; my_cat=current_sku['Category']
    my_subcat=current_sku['Sub_Category']; my_price=current_sku['Base_Price']
    my_size=sku_sizes.get(my_code,0)
    if my_size==0: return [('NONE','NONE','NONE')]*3
    matches=[]
    for _,row in all_skus_df.iterrows():
        if row['SKU_Code']==my_code: continue
        if row['Category']!=my_cat or row['Sub_Category']!=my_subcat: continue
        other_size=sku_sizes.get(row['SKU_Code'],0)
        if other_size==0: continue
        if not (other_size>=my_size*0.8 and other_size<=my_size*1.2): continue
        if not (row['Base_Price']>=my_price*0.7 and row['Base_Price']<=my_price*1.3): continue
        matches.append({'code':row['SKU_Code'],'name':row['SKU_Name'],'group':row['Category']+'_'+row['Sub_Category'],'l30':row.get('L30_Sales',0)})
    matches.sort(key=lambda x:x['l30'],reverse=True)
    result=[]
    for i in range(3):
        if i<len(matches): result.append((matches[i]['code'],matches[i]['name'],matches[i]['group']))
        else: result.append(('NONE','NONE','NONE'))
    return result

# ==================== SAMPLE DATA ====================
def generate_sample_data():
    import random; random.seed(42)
    skus=[
        {'code':'SKU001','name':'Nestle Pure Life 6x500ml','brand':'Nestle','category':'Beverages','sub_category':'Water','cbm':0.002,'shelf_life':180,'price':4.50,'base_sales':150},
        {'code':'SKU002','name':'Masafi 6x500ml Pack','brand':'Masafi','category':'Beverages','sub_category':'Water','cbm':0.002,'shelf_life':180,'price':4.20,'base_sales':130},
        {'code':'SKU003','name':'Aquafina 6x500ml Pack','brand':'Aquafina','category':'Beverages','sub_category':'Water','cbm':0.002,'shelf_life':180,'price':4.00,'base_sales':110},
        {'code':'SKU004','name':'Masafi Water 1.5L','brand':'Masafi','category':'Beverages','sub_category':'Water','cbm':0.002,'shelf_life':180,'price':2.50,'base_sales':100},
        {'code':'SKU005','name':'Aquafina Water 1.5L','brand':'Aquafina','category':'Beverages','sub_category':'Water','cbm':0.002,'shelf_life':180,'price':2.50,'base_sales':90},
        {'code':'SKU006','name':'Evian Water 1.5 Litre','brand':'Evian','category':'Beverages','sub_category':'Water','cbm':0.002,'shelf_life':180,'price':3.50,'base_sales':60},
        {'code':'SKU007','name':'Masafi Water 500ml','brand':'Masafi','category':'Beverages','sub_category':'Water','cbm':0.001,'shelf_life':180,'price':1.00,'base_sales':250},
        {'code':'SKU008','name':'Aquafina Water 500ml','brand':'Aquafina','category':'Beverages','sub_category':'Water','cbm':0.001,'shelf_life':180,'price':1.00,'base_sales':200},
        {'code':'SKU009','name':'Al Ain Water 500ml','brand':'Al Ain','category':'Beverages','sub_category':'Water','cbm':0.001,'shelf_life':180,'price':0.90,'base_sales':180},
        {'code':'SKU010','name':'Pepsi 330ml Can','brand':'Pepsi','category':'Beverages','sub_category':'Soft Drinks','cbm':0.001,'shelf_life':120,'price':2.50,'base_sales':180},
        {'code':'SKU011','name':'Coca Cola 330ml Can','brand':'Coca Cola','category':'Beverages','sub_category':'Soft Drinks','cbm':0.001,'shelf_life':120,'price':2.50,'base_sales':200},
        {'code':'SKU012','name':'Fanta 330ml Can','brand':'Fanta','category':'Beverages','sub_category':'Soft Drinks','cbm':0.001,'shelf_life':120,'price':2.50,'base_sales':120},
        {'code':'SKU013','name':'Sprite 330ml Can','brand':'Sprite','category':'Beverages','sub_category':'Soft Drinks','cbm':0.001,'shelf_life':120,'price':2.50,'base_sales':100},
        {'code':'SKU014','name':'Pepsi 6x330ml Pack','brand':'Pepsi','category':'Beverages','sub_category':'Soft Drinks','cbm':0.003,'shelf_life':120,'price':12.50,'base_sales':80},
        {'code':'SKU015','name':'Coca Cola 6x330ml Pack','brand':'Coca Cola','category':'Beverages','sub_category':'Soft Drinks','cbm':0.003,'shelf_life':120,'price':12.00,'base_sales':90},
        {'code':'SKU016','name':'Fanta 6x330ml Pack','brand':'Fanta','category':'Beverages','sub_category':'Soft Drinks','cbm':0.003,'shelf_life':120,'price':11.50,'base_sales':65},
        {'code':'SKU017','name':'Al Marai Full Cream Milk 1L','brand':'Al Marai','category':'Dairy','sub_category':'Fresh Milk','cbm':0.001,'shelf_life':5,'price':6.50,'base_sales':120},
        {'code':'SKU018','name':'Al Rawabi Fresh Milk 1L','brand':'Al Rawabi','category':'Dairy','sub_category':'Fresh Milk','cbm':0.001,'shelf_life':5,'price':6.00,'base_sales':100},
        {'code':'SKU019','name':'Nada Fresh Milk 1L','brand':'Nada','category':'Dairy','sub_category':'Fresh Milk','cbm':0.001,'shelf_life':5,'price':5.50,'base_sales':80},
        {'code':'SKU020','name':'Al Marai Full Cream Milk 2L','brand':'Al Marai','category':'Dairy','sub_category':'Fresh Milk','cbm':0.003,'shelf_life':5,'price':12.50,'base_sales':100},
        {'code':'SKU021','name':'Al Rawabi Fresh Milk 2L','brand':'Al Rawabi','category':'Dairy','sub_category':'Fresh Milk','cbm':0.003,'shelf_life':5,'price':11.50,'base_sales':80},
        {'code':'SKU022','name':'Nada Fresh Milk 2L','brand':'Nada','category':'Dairy','sub_category':'Fresh Milk','cbm':0.003,'shelf_life':5,'price':10.50,'base_sales':65},
        {'code':'SKU023','name':'Lays Classic 150g','brand':'Lays','category':'Snacks','sub_category':'Chips','cbm':0.002,'shelf_life':90,'price':7.00,'base_sales':80},
        {'code':'SKU024','name':'Pringles Original 165g','brand':'Pringles','category':'Snacks','sub_category':'Chips','cbm':0.002,'shelf_life':90,'price':8.50,'base_sales':70},
        {'code':'SKU025','name':'Doritos Nacho 160g','brand':'Doritos','category':'Snacks','sub_category':'Chips','cbm':0.002,'shelf_life':90,'price':7.50,'base_sales':60},
        {'code':'SKU026','name':'Nescafe Classic 200g','brand':'Nescafe','category':'Beverages','sub_category':'Coffee','cbm':0.002,'shelf_life':365,'price':55.00,'base_sales':40},
        {'code':'SKU027','name':'Nescafe Gold 200g','brand':'Nescafe','category':'Beverages','sub_category':'Coffee','cbm':0.002,'shelf_life':365,'price':65.00,'base_sales':35},
        {'code':'SKU028','name':'Jacobs Coffee 200g','brand':'Jacobs','category':'Beverages','sub_category':'Coffee','cbm':0.002,'shelf_life':365,'price':58.00,'base_sales':30},
        {'code':'SKU029','name':'Ariel 3kg Powder','brand':'Ariel','category':'Household','sub_category':'Detergent','cbm':0.005,'shelf_life':730,'price':38.00,'base_sales':35},
        {'code':'SKU030','name':'Tide 3kg Powder','brand':'Tide','category':'Household','sub_category':'Detergent','cbm':0.005,'shelf_life':730,'price':36.00,'base_sales':30},
        {'code':'SKU031','name':'OMO 3kg Powder','brand':'OMO','category':'Household','sub_category':'Detergent','cbm':0.005,'shelf_life':730,'price':35.00,'base_sales':25},
        {'code':'SKU032','name':'Lurpak Butter 200g','brand':'Lurpak','category':'Dairy','sub_category':'Butter','cbm':0.001,'shelf_life':30,'price':22.00,'base_sales':30},
        {'code':'SKU033','name':'Anchor Butter 250g','brand':'Anchor','category':'Dairy','sub_category':'Butter','cbm':0.001,'shelf_life':30,'price':20.00,'base_sales':28},
        {'code':'SKU034','name':'Kerrygold Butter 200g','brand':'Kerrygold','category':'Dairy','sub_category':'Butter','cbm':0.001,'shelf_life':30,'price':24.00,'base_sales':22},
        {'code':'SKU035','name':'Lipton Yellow Label 100pcs','brand':'Lipton','category':'Beverages','sub_category':'Tea','cbm':0.003,'shelf_life':365,'price':18.00,'base_sales':35},
        {'code':'SKU036','name':'Tetley Tea 100pcs','brand':'Tetley','category':'Beverages','sub_category':'Tea','cbm':0.003,'shelf_life':365,'price':17.00,'base_sales':30},
        {'code':'SKU037','name':'Tapal Tea 100pcs','brand':'Tapal','category':'Beverages','sub_category':'Tea','cbm':0.003,'shelf_life':365,'price':15.00,'base_sales':25},
        {'code':'SKU038','name':'Galaxy Chocolate 90g','brand':'Galaxy','category':'Snacks','sub_category':'Chocolate','cbm':0.001,'shelf_life':180,'price':8.50,'base_sales':45},
        {'code':'SKU039','name':'KitKat Chocolate 85g','brand':'KitKat','category':'Snacks','sub_category':'Chocolate','cbm':0.001,'shelf_life':180,'price':7.50,'base_sales':40},
        {'code':'SKU040','name':'Cadbury Dairy Milk 90g','brand':'Cadbury','category':'Snacks','sub_category':'Chocolate','cbm':0.001,'shelf_life':180,'price':8.00,'base_sales':42},
    ]
    stores=[{'code':'DS_JLT','factor':1.4},{'code':'DS_MARINA','factor':1.2},{'code':'DS_DEIRA','factor':0.9},{'code':'DS_SILICON','factor':0.5}]
    today=pd.Timestamp.now().normalize(); dates=[today-pd.Timedelta(days=59)+pd.Timedelta(days=i) for i in range(60)]
    canni_config={'SKU001':{'promo_days':list(range(20,35)),'loss_pct':0.25},'SKU010':{'promo_days':list(range(25,40)),'loss_pct':0.22},'SKU017':{'promo_days':list(range(30,48)),'loss_pct':0.28},'SKU023':{'promo_days':list(range(15,30)),'loss_pct':0.20}}
    subs_config={'SKU008':{'oos_days':list(range(35,50)),'gain_pct':0.55},'SKU011':{'oos_days':list(range(40,55)),'gain_pct':0.45},'SKU018':{'oos_days':list(range(45,58)),'gain_pct':0.38}}
    comp_groups={'SKU001':['SKU002','SKU003'],'SKU002':['SKU001','SKU003'],'SKU003':['SKU001','SKU002'],'SKU004':['SKU005','SKU006'],'SKU005':['SKU004','SKU006'],'SKU006':['SKU004','SKU005'],'SKU007':['SKU008','SKU009'],'SKU008':['SKU007','SKU009'],'SKU009':['SKU007','SKU008'],'SKU010':['SKU011','SKU012','SKU013'],'SKU011':['SKU010','SKU012','SKU013'],'SKU012':['SKU010','SKU011','SKU013'],'SKU013':['SKU010','SKU011','SKU012'],'SKU017':['SKU018','SKU019'],'SKU018':['SKU017','SKU019'],'SKU019':['SKU017','SKU018'],'SKU020':['SKU021','SKU022'],'SKU021':['SKU020','SKU022'],'SKU022':['SKU020','SKU021'],'SKU023':['SKU024','SKU025'],'SKU024':['SKU023','SKU025'],'SKU025':['SKU023','SKU024'],'SKU038':['SKU039','SKU040'],'SKU039':['SKU038','SKU040'],'SKU040':['SKU038','SKU039']}
    sales_rows=[]; row_id=1
    for day_idx,date in enumerate(dates):
        for store in stores:
            for sku in skus:
                is_wknd=date.dayofweek in [5,6]; sq=int(sku['base_sales']*store['factor']*(1.35 if is_wknd else 1.0)*random.uniform(0.85,1.15))
                if sku['code'] in canni_config and day_idx in canni_config[sku['code']]['promo_days']: sp=round(sku['price']*(1-random.choice([0.20,0.25,0.30,0.35])),2)
                elif random.random()<0.08: sp=round(sku['price']*(1-random.choice([0.10,0.12,0.18,0.25])),2)
                else: sp=sku['price']
                for ok,cfg in subs_config.items():
                    if sku['code']==ok and day_idx in cfg['oos_days']: sq=random.randint(0,5)
                for ok,cfg in subs_config.items():
                    if ok in comp_groups and sku['code'] in comp_groups.get(ok,[]) and day_idx in cfg['oos_days']: sq=int(sq*(1+cfg['gain_pct']))
                for pk,cfg in canni_config.items():
                    if pk in comp_groups and sku['code'] in comp_groups.get(pk,[]) and day_idx in cfg['promo_days']: sq=int(sq*(1-cfg['loss_pct']))
                sales_rows.append({'Row_ID':row_id,'Date':date,'Store_Code':store['code'],'SKU_Code':sku['code'],'Sales_Qty':max(0,sq),'Selling_Price':sp,'Sales_Value':max(0,sq)*sp}); row_id+=1
    sales_df=pd.DataFrame(sales_rows)
    sku_master_df=pd.DataFrame([{'SKU_Code':s['code'],'SKU_Name':s['name'],'Brand':s['brand'],'Category':s['category'],'Sub_Category':s['sub_category'],'Base_Price':s['price'],'CBM_Per_Unit':s['cbm'],'Shelf_Life_Days':s['shelf_life']} for s in skus])
    stock_scenarios={('DS_DEIRA','SKU017'):{'current':20,'warehouse':2500},('DS_SILICON','SKU018'):{'current':15,'warehouse':2200},('DS_JLT','SKU008'):{'current':8,'warehouse':150},('DS_MARINA','SKU008'):{'current':5,'warehouse':150},('DS_DEIRA','SKU008'):{'current':3,'warehouse':150},('DS_JLT','SKU011'):{'current':10,'warehouse':200},('DS_DEIRA','SKU011'):{'current':5,'warehouse':200},('DS_JLT','SKU026'):{'current':950,'warehouse':5000},('DS_MARINA','SKU035'):{'current':880,'warehouse':4500},('DS_JLT','SKU029'):{'current':750,'warehouse':3500},('DS_SILICON','SKU017'):{'current':0,'warehouse':2000},('DS_DEIRA','SKU020'):{'current':0,'warehouse':1500}}
    stock_rows=[]
    for store in stores:
        for sku in skus:
            key=(store['code'],sku['code'])
            if key in stock_scenarios: c=stock_scenarios[key]['current']; w=stock_scenarios[key]['warehouse']
            else: c=random.randint(180,450); w=random.randint(2000,4500)
            stock_rows.append({'Date':today,'Store_Code':store['code'],'SKU_Code':sku['code'],'Current_Stock':c,'Warehouse_Stock':w})
    stock_df=pd.DataFrame(stock_rows)
    tomorrow=today+pd.Timedelta(days=1)
    promos=[('DS_JLT','SKU001',today,today+pd.Timedelta(days=5),4.50,3.15),('DS_MARINA','SKU001',tomorrow,tomorrow+pd.Timedelta(days=4),4.50,3.38),('DS_JLT','SKU010',tomorrow,tomorrow+pd.Timedelta(days=3),2.50,1.75),('DS_MARINA','SKU010',tomorrow,tomorrow+pd.Timedelta(days=4),2.50,1.88),('DS_MARINA','SKU017',tomorrow,tomorrow+pd.Timedelta(days=5),6.50,4.55),('DS_JLT','SKU017',tomorrow,tomorrow+pd.Timedelta(days=4),6.50,4.23),('DS_DEIRA','SKU023',tomorrow,tomorrow+pd.Timedelta(days=4),7.00,4.90),('DS_JLT','SKU023',tomorrow,tomorrow+pd.Timedelta(days=3),7.00,4.55),('DS_JLT','SKU014',tomorrow,tomorrow+pd.Timedelta(days=4),12.50,8.75),('DS_DEIRA','SKU029',tomorrow,tomorrow+pd.Timedelta(days=5),38.00,26.60),('DS_MARINA','SKU035',tomorrow,tomorrow+pd.Timedelta(days=4),18.00,12.60),('DS_JLT','SKU038',tomorrow,tomorrow+pd.Timedelta(days=3),8.50,5.95)]
    promo_df=pd.DataFrame([{'Promo_ID':i+1,'Store_Code':p[0],'SKU_Code':p[1],'Start_Date':p[2],'End_Date':p[3],'Regular_Price':p[4],'Promo_Price':p[5]} for i,p in enumerate(promos)])
    return sales_df,sku_master_df,stock_df,promo_df
# ==================== CALCULATION ENGINE ====================
def calculate_sku_master_full(sku_raw, sales_data):
    today=pd.Timestamp.now().normalize(); sku=sku_raw.copy()
    l30=sales_data[(sales_data['Date']>=today-pd.Timedelta(days=30))&(sales_data['Date']<=today-pd.Timedelta(days=1))].groupby('SKU_Code')['Sales_Qty'].sum().to_dict()
    sku['L30_Sales']=sku['SKU_Code'].map(l30).fillna(0).astype(int)
    sku['Lower_Name']=sku['SKU_Name'].str.lower(); sku['Clean_Name']=sku['Lower_Name'].str.replace('×','x').str.replace('*','x').str.replace('  ',' ')
    extracted=sku['SKU_Name'].apply(extract_sku_values)
    sku['Has_Multiplier']=extracted.apply(lambda x:x[0]); sku['Pack_Count']=extracted.apply(lambda x:x[1])
    sku['Size_Raw']=extracted.apply(lambda x:x[2]); sku['_unit']=extracted.apply(lambda x:x[3])
    sku['L_Position']=0; sku['Unit_Position']=0; sku['Unit_Found']=sku['_unit']
    sku['Size_ML']=sku.apply(lambda r:int(convert_to_size_ml(r['Size_Raw'],r['_unit'])),axis=1)
    def gus(u):
        if u in ['ml','l','cl','oz','kl']: return 'ml'
        if u in ['g','kg','mg','lb']: return 'g'
        if u in ['pcs','sheets','rolls','bags','caps','tabs']: return 'pcs'
        return 'unknown'
    sku['Unit_Standard']=sku['_unit'].apply(gus)
    sku['Pack_Size']=sku.apply(lambda r:get_pack_size_display(r['Size_ML'],r['_unit']),axis=1)
    sku['Total_ML']=sku['Pack_Count']*sku['Size_ML']
    sku_sizes=dict(zip(sku['SKU_Code'],sku['Size_ML']))
    comp_results={}
    for _,row in sku.iterrows(): comp_results[row['SKU_Code']]=find_competitors(row,sku,sku_sizes)
    for cn in [1,2,3]:
        sku[f'Comp{cn}_SKU']=sku['SKU_Code'].apply(lambda c:comp_results[c][cn-1][0])
        sku[f'Comp{cn}_Name']=sku['SKU_Code'].apply(lambda c:comp_results[c][cn-1][1])
        sku[f'Comp{cn}_Group']=sku['SKU_Code'].apply(lambda c:comp_results[c][cn-1][2])
    sku['Size_Category']=sku['Size_ML'].apply(lambda s:'Mini' if s<=250 else ('Small' if s<=500 else ('Medium' if s<=1000 else 'Large')))
    sku['Units_Per_Pallet']=sku['CBM_Per_Unit'].apply(lambda x:int(round(1/x)) if x>0 else 0)
    sku['Shelf_Life_Category']=sku['Shelf_Life_Days'].apply(get_shelf_life_category)
    sku['Base_Price_Dup']=sku['Base_Price']; sku=sku.drop('_unit',axis=1)
    store_sku_listed=sales_data.groupby(['Store_Code','SKU_Code']).size().reset_index()[['Store_Code','SKU_Code']]
    store_sku_listed['Is_Listed']=1
    listed_pivot=store_sku_listed.pivot_table(index='SKU_Code',columns='Store_Code',values='Is_Listed',fill_value=0)
    sku=sku.merge(listed_pivot.reset_index(),on='SKU_Code',how='left')
    stores_in_data=sales_data['Store_Code'].unique().tolist()
    for s in stores_in_data:
        if s not in sku.columns: sku[s]=0
        sku[s]=sku[s].fillna(0).astype(int)
    return sku,comp_results,stores_in_data

def calculate_promo_calendar_full(pc_raw,tomorrow):
    pc=pc_raw.copy()
    pc['Discount_%']=((pc['Regular_Price']-pc['Promo_Price'])/pc['Regular_Price'].clip(lower=0.01)).fillna(0)
    pc['Promo_Type']=pc['Discount_%'].apply(lambda d:'Big Deal' if d>=0.30 else ('High Discount' if d>=0.20 else ('Medium Discount' if d>=0.10 else 'Light Discount')))
    tomorrow_ts=pd.Timestamp(tomorrow)
    pc['Is_Active_Tomorrow']=pc.apply(lambda r:'Yes' if r['Start_Date']<=tomorrow_ts<=r['End_Date'] else 'No',axis=1)
    return pc

def calculate_sales_data_enhanced(sales_raw,sku_master_calc):
    df=sales_raw.copy(); df=df.sort_values(['Date','Store_Code','SKU_Code']).reset_index(drop=True)
    sku_lkp=sku_master_calc.set_index('SKU_Code').to_dict('index')
    df['Avg_Price_L60']=df.groupby(['Store_Code','SKU_Code'])['Selling_Price'].transform('mean')
    df['Discount_%']=((df['Avg_Price_L60']-df['Selling_Price'])/df['Avg_Price_L60'].clip(lower=0.01)).fillna(0).clip(lower=0)
    df['Promo_Flag']=df['Discount_%'].apply(lambda x:'Yes' if x>=0.10 else 'No')
    def pt(row):
        if row['Promo_Flag']=='No': return ''
        d=row['Discount_%']
        if d>=0.30: return 'Big Deal'
        if d>=0.20: return 'High Discount'
        if d>=0.10: return 'Medium Discount'
        return 'Light Discount'
    df['Promo_Type']=df.apply(pt,axis=1)
    df['Day_Name']=df['Date'].dt.day_name(); df['Day_Type']=df['Date'].dt.dayofweek.apply(lambda x:'Weekend' if x in [5,6] else 'Weekday')
    df['Week_Start']=df['Date'].dt.to_period('W-MON').apply(lambda p:p.start_time)
    df['Day_Num']=df['Date'].dt.day; df['Month']=df['Date'].dt.month; df['Year']=df['Date'].dt.year
    df['Is_Weekend']=df['Day_Type'].apply(lambda x:1 if x=='Weekend' else 0)
    df['Median_L60']=df.groupby(['Store_Code','SKU_Code'])['Sales_Qty'].transform('mean')
    df['_abs_dev']=abs(df['Sales_Qty']-df['Median_L60'])
    df['Sum_Abs_Dev']=df.groupby(['Store_Code','SKU_Code'])['_abs_dev'].transform('sum')
    df['Count_L60']=df.groupby(['Store_Code','SKU_Code'])['Sales_Qty'].transform('count')
    df['MAD_L60']=df.apply(lambda r:max(r['Sum_Abs_Dev']/max(r['Count_L60'],1),r['Median_L60']*0.05,5),axis=1).fillna(10)
    df['Deviation']=df['Sales_Qty']-df['Median_L60']
    df['Modified_Z']=(0.6745*df['Deviation']/df['MAD_L60'].clip(lower=1)).fillna(0)
    df['Is_Outlier']=df.apply(lambda r:'Yes' if (abs(r['Modified_Z'])>3.5 or r['Sales_Qty']<r['Median_L60']*0.1 or r['Sales_Qty']>r['Median_L60']*5) else 'No',axis=1)
    def ot(r):
        if r['Is_Outlier']=='No': return 'Normal'
        if r['Modified_Z']>3.5 or r['Sales_Qty']>r['Median_L60']*5: return 'Spike'
        if r['Modified_Z']<-3.5 or r['Sales_Qty']<r['Median_L60']*0.1: return 'Stockout'
        return 'Outlier'
    df['Outlier_Type']=df.apply(ot,axis=1)
    df['Clean_Sales']=df.apply(lambda r:round(r['Median_L60']) if r['Is_Outlier']=='Yes' else r['Sales_Qty'],axis=1)
    df['OOS_Flag']=df.apply(lambda r:1 if r['Sales_Qty']<r['Median_L60']*0.5 else 0,axis=1)
    promo_set=set(); oos_set=set()
    for _,row in df.iterrows():
        key=(row['Store_Code'],row['SKU_Code'],row['Date'])
        if row['Promo_Flag']=='Yes': promo_set.add(key)
        if row['OOS_Flag']==1: oos_set.add(key)
    def cp(row,cc):
        comp=sku_lkp.get(row['SKU_Code'],{}).get(cc,'NONE')
        if not comp or comp=='NONE' or pd.isna(comp): return ''
        return 'Yes' if (row['Store_Code'],str(comp),row['Date']) in promo_set else 'No'
    def co(row,cc):
        comp=sku_lkp.get(row['SKU_Code'],{}).get(cc,'NONE')
        if not comp or comp=='NONE' or pd.isna(comp): return ''
        return 'OOS' if (row['Store_Code'],str(comp),row['Date']) in oos_set else 'In Stock'
    for cn in [1,2,3]:
        df[f'Comp{cn}_Promo_Flag']=df.apply(lambda r:cp(r,f'Comp{cn}_SKU'),axis=1)
        df[f'Comp{cn}_OOS_Flag']=df.apply(lambda r:co(r,f'Comp{cn}_SKU'),axis=1)
    df=df.drop('_abs_dev',axis=1)
    return df

def calculate_final_calculation(sales_calc,sku_master_calc,stock_status,promo_cal,calc_date=None):
    today=pd.Timestamp(calc_date).normalize() if calc_date else pd.Timestamp.now().normalize()
    tomorrow=today+pd.Timedelta(days=1)
    sku_lkp=sku_master_calc.set_index('SKU_Code').to_dict('index')
    stores=sorted(sales_calc['Store_Code'].unique()); skus=sku_master_calc['SKU_Code'].tolist()
    stock_dict=stock_status.set_index(['Store_Code','SKU_Code'])['Current_Stock'].to_dict()
    wh_dict=stock_status.groupby('SKU_Code')['Warehouse_Stock'].first().to_dict()
    rows=[{'Store_Code':s,'SKU_Code':k} for s in stores for k in skus]
    df=pd.DataFrame(rows); df['Row_ID']=range(1,len(df)+1); df['Calc_Date']=today; df['Tomorrow_Date']=tomorrow
    for col,key in [('SKU_Name','SKU_Name'),('Brand','Brand'),('Category','Category'),('Sub_Category','Sub_Category'),('Size_ML','Size_ML'),('CBM_Per_Unit','CBM_Per_Unit'),('Units_Per_Pallet','Units_Per_Pallet'),('Shelf_Life_Days','Shelf_Life_Days'),('Shelf_Life_Category','Shelf_Life_Category'),('Base_Price','Base_Price')]:
        df[col]=df['SKU_Code'].apply(lambda x:sku_lkp.get(x,{}).get(key,''))
    df['Comp1_SKU']=df['SKU_Code'].apply(lambda x:sku_lkp.get(x,{}).get('Comp1_SKU','NONE'))
    df['Comp1_Name']=df['SKU_Code'].apply(lambda x:sku_lkp.get(x,{}).get('Comp1_Name','NONE'))
    df['Canni_Subs_Group']=df['SKU_Code'].apply(lambda x:sku_lkp.get(x,{}).get('Comp1_Group',''))
    df['Tomorrow_Day_Name']=tomorrow.day_name()
    df['Tomorrow_Day_Type']='Weekend' if tomorrow.dayofweek in [5,6] else 'Weekday'
    df['Tomorrow_Is_Weekend']='Yes' if tomorrow.dayofweek in [5,6] else 'No'
    promo_dict={}; promo_price_dict={}
    for _,row in promo_cal.iterrows():
        if row['Start_Date']<=tomorrow<=row['End_Date']:
            promo_dict[(row['Store_Code'],row['SKU_Code'])]='Yes'; promo_price_dict[(row['Store_Code'],row['SKU_Code'])]=row['Promo_Price']
    df['Promo_Tomorrow']=df.apply(lambda r:promo_dict.get((r['Store_Code'],r['SKU_Code']),'No'),axis=1)
    df['Promo_Price_Tomorrow']=df.apply(lambda r:promo_price_dict.get((r['Store_Code'],r['SKU_Code']),r['Base_Price']),axis=1)
    df['Promo_Discount_%']=((df['Base_Price']-df['Promo_Price_Tomorrow'])/df['Base_Price'].clip(lower=0.01)).fillna(0)
    yesterday=today-pd.Timedelta(days=1)
    yest=sales_calc[sales_calc['Date']==yesterday].set_index(['Store_Code','SKU_Code'])['Sales_Qty'].to_dict()
    df['Latest_Sales_Qty']=df.apply(lambda r:yest.get((r['Store_Code'],r['SKU_Code']),0),axis=1)
    grp=sales_calc.groupby(['Store_Code','SKU_Code'])
    mean_d=grp['Sales_Qty'].mean().to_dict(); outlier_d=grp['Is_Outlier'].apply(lambda x:(x=='Yes').sum()).to_dict(); count_d=grp.size().to_dict()
    df['Median_L60_Fixed']=df.apply(lambda r:mean_d.get((r['Store_Code'],r['SKU_Code']),0),axis=1); df['MAD_L60_Fixed']=10
    df['Outlier_Count_L60']=df.apply(lambda r:outlier_d.get((r['Store_Code'],r['SKU_Code']),0),axis=1)
    df['Total_Days_L60']=df.apply(lambda r:count_d.get((r['Store_Code'],r['SKU_Code']),0),axis=1)
    df['Outlier_%']=(df['Outlier_Count_L60']/df['Total_Days_L60'].clip(lower=1)).fillna(0)
    df['Is_Outlier_SKU']=df['Outlier_%'].apply(lambda x:'Yes' if x>0.05 else 'No')
    df['Outlier_Summary']=df.apply(lambda r:f"{int(r['Outlier_Count_L60'])} outliers ({r['Outlier_%']:.0%})" if r['Outlier_Count_L60']>0 else 'None',axis=1)
    def avg_f(day_type=None,promo=None,days=None):
        mask=pd.Series([True]*len(sales_calc),index=sales_calc.index)
        if day_type: mask&=sales_calc['Day_Type']==day_type
        if promo=='No': mask&=sales_calc['Promo_Flag']=='No'
        elif promo=='Yes': mask&=sales_calc['Promo_Flag']=='Yes'
        if days: mask&=(sales_calc['Date']>=today-pd.Timedelta(days=days))&(sales_calc['Date']<=today-pd.Timedelta(days=1))
        return sales_calc[mask].groupby(['Store_Code','SKU_Code'])['Clean_Sales'].mean().to_dict()
    l7=avg_f(days=7); l30=avg_f(days=30); l60=grp['Clean_Sales'].mean().to_dict()
    l7t=sales_calc[(sales_calc['Date']>=today-pd.Timedelta(days=7))&(sales_calc['Date']<=today-pd.Timedelta(days=1))].groupby(['Store_Code','SKU_Code'])['Clean_Sales'].sum().to_dict()
    l30t=sales_calc[(sales_calc['Date']>=today-pd.Timedelta(days=30))&(sales_calc['Date']<=today-pd.Timedelta(days=1))].groupby(['Store_Code','SKU_Code'])['Clean_Sales'].sum().to_dict()
    l30tv=sales_calc[(sales_calc['Date']>=today-pd.Timedelta(days=30))&(sales_calc['Date']<=today-pd.Timedelta(days=1))].groupby(['Store_Code','SKU_Code'])['Sales_Value'].sum().to_dict()
    l7tv=sales_calc[(sales_calc['Date']>=today-pd.Timedelta(days=7))&(sales_calc['Date']<=today-pd.Timedelta(days=1))].groupby(['Store_Code','SKU_Code'])['Sales_Value'].sum().to_dict()
    wkn_no=avg_f(day_type='Weekend',promo='No'); wkd_no=avg_f(day_type='Weekday',promo='No')
    wkn_yes=avg_f(day_type='Weekend',promo='Yes'); wkd_yes=avg_f(day_type='Weekday',promo='Yes')
    def g(d,r): return d.get((r['Store_Code'],r['SKU_Code']),0)
    df['L7_Avg']=df.apply(lambda r:g(l7,r),axis=1); df['L30_Avg']=df.apply(lambda r:g(l30,r),axis=1)
    df['L60_Avg']=df.apply(lambda r:g(l60,r),axis=1); df['L30_Total']=df.apply(lambda r:g(l30t,r),axis=1)
    df['L7_Total']=df.apply(lambda r:g(l7t,r),axis=1); df['L30_Total_Value']=df.apply(lambda r:g(l30tv,r),axis=1)
    df['L7_Total_Value']=df.apply(lambda r:g(l7tv,r),axis=1)
    df['Avg_Weekend_Normal']=df.apply(lambda r:wkn_no.get((r['Store_Code'],r['SKU_Code']),r['L30_Avg']),axis=1)
    df['Avg_Weekday_Normal']=df.apply(lambda r:wkd_no.get((r['Store_Code'],r['SKU_Code']),r['L30_Avg']),axis=1)
    df['Avg_Weekend_Promo']=df.apply(lambda r:wkn_yes.get((r['Store_Code'],r['SKU_Code']),r['Avg_Weekend_Normal']*1.25),axis=1)
    df['Avg_Weekday_Promo']=df.apply(lambda r:wkd_yes.get((r['Store_Code'],r['SKU_Code']),r['Avg_Weekday_Normal']*1.25),axis=1)
    df['Data_Points_Count']=df['Total_Days_L60']
    def sel_name(row):
        if row['Promo_Tomorrow']=='Yes': return 'Weekend_Promo' if row['Tomorrow_Is_Weekend']=='Yes' else 'Weekday_Promo'
        return 'Weekend_Normal' if row['Tomorrow_Is_Weekend']=='Yes' else 'Weekday_Normal'
    df['Selected_Avg_Name']=df.apply(sel_name,axis=1)
    def fba(row):
        m={'Weekend_Promo':row['Avg_Weekend_Promo'],'Weekday_Promo':row['Avg_Weekday_Promo'],'Weekend_Normal':row['Avg_Weekend_Normal'],'Weekday_Normal':row['Avg_Weekday_Normal']}
        return m[row['Selected_Avg_Name']]
    df['Final_Base_Avg']=df.apply(fba,axis=1)
    df['Trend_Ratio']=(df['L7_Avg']/df['L30_Avg'].clip(lower=0.01)).fillna(1)
    df['Trend_Change_%']=df['Trend_Ratio']-1; df['Trend_Multiplier']=df['Trend_Ratio'].clip(lower=0.85,upper=1.15)
    df['Trend_Flag']=df['Trend_Ratio'].apply(lambda r:'Surge' if r>1.15 else ('Growing' if r>1.05 else ('Dropping' if r<0.85 else ('Declining' if r<0.95 else 'Stable'))))
    df['Canni_Group_ID']=df['Canni_Subs_Group']
    # Cannibalization
    def get_canni(row,cn):
        cs=sku_lkp.get(row['SKU_Code'],{}).get(f'Comp{cn}_SKU','NONE'); cn2=sku_lkp.get(row['SKU_Code'],{}).get(f'Comp{cn}_Name','NONE')
        if cs=='NONE' or pd.isna(cs): return 'NONE',cn2,0,row['Final_Base_Avg'],row['Final_Base_Avg'],0.0
        hcol={1:'Comp1_Promo_Flag',2:'Comp2_Promo_Flag',3:'Comp3_Promo_Flag'}[cn]
        my=sales_calc[(sales_calc['Store_Code']==row['Store_Code'])&(sales_calc['SKU_Code']==row['SKU_Code'])]
        if len(my)==0: return cs,cn2,0,row['Final_Base_Avg'],row['Final_Base_Avg'],0.0
        pd_=int((my[hcol]=='Yes').sum()); norm=my.loc[my[hcol]=='No','Clean_Sales']; prom=my.loc[my[hcol]=='Yes','Clean_Sales']
        na=norm.mean() if len(norm)>0 else row['Final_Base_Avg']; pa=prom.mean() if len(prom)>0 else row['Final_Base_Avg']
        eff=0.0 if pd_<5 else min(0.40,max(0.0,(na-pa)/max(na,0.01)))
        return cs,cn2,pd_,na,pa,eff
    for cn in [1,2,3]:
        res=df.apply(lambda r:get_canni(r,cn),axis=1)
        df[f'Comp{cn}_SKU_Canni']=res.apply(lambda x:x[0]); df[f'Comp{cn}_Name_Canni']=res.apply(lambda x:x[1])
        df[f'Comp{cn}_Promo_Days']=res.apply(lambda x:x[2]); df[f'Comp{cn}_Avg_Sales_Normal']=res.apply(lambda x:x[3])
        df[f'Comp{cn}_Avg_Sales_Comp_Promo']=res.apply(lambda x:x[4]); df[f'Comp{cn}_Canni_Effect_%']=res.apply(lambda x:x[5])
    df['Max_Canni_Effect_%']=df[['Comp1_Canni_Effect_%','Comp2_Canni_Effect_%','Comp3_Canni_Effect_%']].max(axis=1)
    def bc(row):
        e={row['Comp1_SKU_Canni']:row['Comp1_Canni_Effect_%'],row['Comp2_SKU_Canni']:row['Comp2_Canni_Effect_%'],row['Comp3_SKU_Canni']:row['Comp3_Canni_Effect_%']}
        b=max(e,key=e.get); return b if b!='NONE' else 'NONE'
    df['Best_Canni_Comp_SKU']=df.apply(bc,axis=1)
    df['Comp_On_Promo_Tomorrow']=df.apply(lambda r:promo_dict.get((r['Store_Code'],r['Best_Canni_Comp_SKU']),'No') if r['Best_Canni_Comp_SKU']!='NONE' else 'No',axis=1)
    df['Has_Cannibalization']=df.apply(lambda r:'Yes' if (r['Best_Canni_Comp_SKU']!='NONE' and r['Max_Canni_Effect_%']>=0.15 and r['Comp_On_Promo_Tomorrow']=='Yes') else 'No',axis=1)
    df['Canni_Multiplier']=df.apply(lambda r:max(0.60,1-r['Max_Canni_Effect_%']) if r['Has_Cannibalization']=='Yes' else 1.0,axis=1)
    df['Canni_Status']=df['Comp_On_Promo_Tomorrow'].apply(lambda x:'On Promo Tomorrow' if x=='Yes' else 'Not On Promo')
    df['Canni_Loss_Qty']=df.apply(lambda r:round(r['Final_Base_Avg']*r['Max_Canni_Effect_%']) if r['Has_Cannibalization']=='Yes' else 0,axis=1)
    df['Canni_Loss_Value']=df['Canni_Loss_Qty']*df['Base_Price']
    df['Canni_Group_Info']=df.apply(lambda r:f"{r['Canni_Group_ID']}|{r['Best_Canni_Comp_SKU']}|-{r['Max_Canni_Effect_%']:.0%}|{r['Canni_Status']}" if r['Has_Cannibalization']=='Yes' else 'No Cannibalization',axis=1)
    # Substitution
    df['Subs_Group_ID']=df['Canni_Subs_Group']
    def get_subs(row,cn):
        cs=sku_lkp.get(row['SKU_Code'],{}).get(f'Comp{cn}_SKU','NONE'); cn2=sku_lkp.get(row['SKU_Code'],{}).get(f'Comp{cn}_Name','NONE')
        if cs=='NONE' or pd.isna(cs): return 'NONE',cn2,0,9999,100,'No',row['Final_Base_Avg'],row['Final_Base_Avg'],0.0
        hcol={1:'Comp1_OOS_Flag',2:'Comp2_OOS_Flag',3:'Comp3_OOS_Flag'}[cn]
        my=sales_calc[(sales_calc['Store_Code']==row['Store_Code'])&(sales_calc['SKU_Code']==row['SKU_Code'])]
        od=int((my[hcol]=='OOS').sum()); cur=stock_dict.get((row['Store_Code'],cs),9999)
        if len(my)==0: return cs,cn2,od,cur,100,'Pending',row['Final_Base_Avg'],row['Final_Base_Avg'],0.0
        norm=my.loc[my[hcol]=='In Stock','Clean_Sales']; oos_v=my.loc[my[hcol]=='OOS','Clean_Sales']
        na=norm.mean() if len(norm)>0 else row['Final_Base_Avg']; oa=oos_v.mean() if len(oos_v)>0 else row['Final_Base_Avg']
        eff=0.0 if od<5 else min(0.50,max(0.0,(oa-na)/max(na,0.01)))
        return cs,cn2,od,cur,100,'Pending',na,oa,eff
    for cn in [1,2,3]:
        res=df.apply(lambda r:get_subs(r,cn),axis=1)
        df[f'Comp{cn}_SKU_Subs']=res.apply(lambda x:x[0]); df[f'Comp{cn}_Name_Subs']=res.apply(lambda x:x[1])
        df[f'Comp{cn}_OOS_Days']=res.apply(lambda x:x[2]); df[f'Comp{cn}_Current_Stock']=res.apply(lambda x:x[3])
        df[f'Comp{cn}_Min_Stock']=res.apply(lambda x:x[4]); df[f'Comp{cn}_OOS_Tomorrow']=res.apply(lambda x:x[5])
        df[f'Comp{cn}_Avg_Sales_Normal_S']=res.apply(lambda x:x[6]); df[f'Comp{cn}_Avg_Sales_Comp_OOS']=res.apply(lambda x:x[7])
        df[f'Comp{cn}_Subs_Effect_%']=res.apply(lambda x:x[8])
    df['Max_Subs_Effect_%']=df[['Comp1_Subs_Effect_%','Comp2_Subs_Effect_%','Comp3_Subs_Effect_%']].max(axis=1)
    def bs(row):
        e={row['Comp1_SKU_Subs']:row['Comp1_Subs_Effect_%'],row['Comp2_SKU_Subs']:row['Comp2_Subs_Effect_%'],row['Comp3_SKU_Subs']:row['Comp3_Subs_Effect_%']}
        b=max(e,key=e.get); return b if b!='NONE' else 'NONE'
    df['Best_Subs_Comp_SKU']=df.apply(bs,axis=1)
    df['Comp_OOS_Tomorrow']='Pending'; df['Has_Substitution']='No'; df['Subs_Multiplier']=1.0
    df['Subs_Status']='In Stock'; df['Subs_Gain_Qty']=0; df['Subs_Gain_Value']=0.0; df['Subs_Group_Info']='No Substitution'
    # Shelf Life Days
    def min_d(sl):
        if sl<=3: return 1.0
        if sl<=7: return 1.5
        if sl<=14: return 2.0
        if sl<=30: return 2.5
        return 3.0
    def ideal_d(sl):
        if sl<=3: return 1.2
        if sl<=7: return 2.0
        if sl<=14: return 3.0
        if sl<=30: return 4.0
        return 4.5
    def max_d(sl):
        if sl<=3: return 1.4
        if sl<=7: return 3.0
        if sl<=14: return 4.5
        if sl<=30: return 6.0
        return 7.0
    df['Min_Days']=df['Shelf_Life_Days'].apply(lambda x:min_d(int(x))); df['Ideal_Days']=df['Shelf_Life_Days'].apply(lambda x:ideal_d(int(x)))
    df['Max_Days']=df['Shelf_Life_Days'].apply(lambda x:max_d(int(x))); df['Safety_Buffer']=df['Ideal_Days']-df['Min_Days']
    # Store Tier
    store_l30=sales_calc[(sales_calc['Date']>=today-pd.Timedelta(days=30))&(sales_calc['Date']<=today-pd.Timedelta(days=1))].groupby('Store_Code')['Clean_Sales'].sum().to_dict()
    df['Store_Sales_L30D']=df['Store_Code'].map(store_l30).fillna(0); all_s=sum(store_l30.values())
    df['All_Stores_Sales']=all_s; df['Store_Sales_%']=(df['Store_Sales_L30D']/max(all_s,1)).fillna(0)
    df['Store_Rank']=df['Store_Sales_L30D'].rank(ascending=False,method='dense')
    df['Store_Tier']=df['Store_Sales_%'].apply(lambda x:'Tier1' if x>=0.28 else ('Tier2' if x>=0.18 else 'Tier3'))
    df['Tier_Priority']=df['Store_Tier'].apply(lambda x:3 if x=='Tier1' else (2 if x=='Tier2' else 1)); df['Tier_Boost']=df['Tier_Priority']
    # ABC
    df['SKU_Revenue_L30D']=df['L30_Total_Value']
    cat_rev=df.groupby(['Category','Store_Code'])['L30_Total_Value'].sum().to_dict()
    df['Cat_Revenue_L30D']=df.apply(lambda r:cat_rev.get((r['Category'],r['Store_Code']),0),axis=1)
    df['SKU_Revenue_%']=(df['SKU_Revenue_L30D']/df['Cat_Revenue_L30D'].clip(lower=0.01)).fillna(0)
    df['SKU_Rank']=df.groupby(['Store_Code','Category'])['SKU_Revenue_L30D'].rank(ascending=False,method='dense')
    df['ABC_Class']=df['SKU_Revenue_%'].apply(lambda x:'A' if x>=0.25 else ('B' if x>=0.10 else 'C'))
    df['ABC_Priority']=df['ABC_Class'].apply(lambda x:3 if x=='A' else (2 if x=='B' else 1))
    df['ABC_Multiplier']=df['ABC_Class'].apply(lambda x:1.1 if x=='A' else 1.0)
    df['ABC_Label']=df['ABC_Class'].apply(lambda x:'Fast Moving' if x=='A' else ('Medium Moving' if x=='B' else 'Slow Moving'))
    # Forecast
    df['Target_Days']=df.apply(lambda r:r['Max_Days'] if r['Promo_Tomorrow']=='Yes' else r['Ideal_Days'],axis=1)
    df['Adjusted_Forecast']=(df['Final_Base_Avg']*df['Trend_Multiplier']*df['Canni_Multiplier']*df['Subs_Multiplier']).round()
    df['Base_Min_Stock']=(df['Adjusted_Forecast']*df['Min_Days']).round(); df['Base_Ideal_Stock']=(df['Adjusted_Forecast']*df['Ideal_Days']).round()
    df['Base_Max_Stock']=(df['Adjusted_Forecast']*df['Max_Days']).round()
    df['Final_Min_Stock']=(df['Base_Min_Stock']*df['ABC_Multiplier']).round(); df['Final_Ideal_Stock']=(df['Base_Ideal_Stock']*df['ABC_Multiplier']).round()
    df['Final_Max_Stock']=(df['Base_Max_Stock']*df['ABC_Multiplier']).round()
    df['Target_Stock']=df.apply(lambda r:r['Final_Max_Stock'] if r['Promo_Tomorrow']=='Yes' else r['Final_Ideal_Stock'],axis=1); df['DRR']=df['Adjusted_Forecast']
    # Pass 2 Subs
    min_lkp=df.set_index(['Store_Code','SKU_Code'])['Final_Min_Stock'].to_dict()
    for cn in [1,2,3]:
        cc=f'Comp{cn}_SKU_Subs'; cu=f'Comp{cn}_Current_Stock'; mc=f'Comp{cn}_Min_Stock'; oc=f'Comp{cn}_OOS_Tomorrow'
        def recalc(row,cc=cc,cu=cu,mc=mc):
            comp=row[cc]
            if comp=='NONE': return 'No'
            cm=min_lkp.get((row['Store_Code'],comp),100); df.at[row.name,mc]=cm
            return 'Yes' if row[cu]<cm*0.5 else 'No'
        df[oc]=df.apply(recalc,axis=1)
    def bo(row):
        comp=row['Best_Subs_Comp_SKU']
        if comp=='NONE': return 'No'
        cm=min_lkp.get((row['Store_Code'],comp),100); cur=stock_dict.get((row['Store_Code'],comp),9999)
        return 'Yes' if cur<cm*0.5 else 'No'
    df['Comp_OOS_Tomorrow']=df.apply(bo,axis=1)
    df['Has_Substitution']=df.apply(lambda r:'Yes' if (r['Best_Subs_Comp_SKU']!='NONE' and r['Max_Subs_Effect_%']>=0.15 and r['Comp_OOS_Tomorrow']=='Yes') else 'No',axis=1)
    df['Subs_Multiplier']=df.apply(lambda r:min(1.50,1+r['Max_Subs_Effect_%']) if r['Has_Substitution']=='Yes' else 1.0,axis=1)
    df['Subs_Status']=df['Comp_OOS_Tomorrow'].apply(lambda x:'Competitor OOS' if x=='Yes' else 'In Stock')
    df['Subs_Gain_Qty']=df.apply(lambda r:round(r['Final_Base_Avg']*r['Max_Subs_Effect_%']) if r['Has_Substitution']=='Yes' else 0,axis=1)
    df['Subs_Gain_Value']=df['Subs_Gain_Qty']*df['Base_Price']
    df['Subs_Group_Info']=df.apply(lambda r:f"{r['Subs_Group_ID']}|{r['Best_Subs_Comp_SKU']}|+{r['Max_Subs_Effect_%']:.0%}|OOS" if r['Has_Substitution']=='Yes' else 'No Substitution',axis=1)
    # Recalculate with Subs
    df['Adjusted_Forecast']=(df['Final_Base_Avg']*df['Trend_Multiplier']*df['Canni_Multiplier']*df['Subs_Multiplier']).round(); df['DRR']=df['Adjusted_Forecast']
    df['Base_Min_Stock']=(df['Adjusted_Forecast']*df['Min_Days']).round(); df['Base_Ideal_Stock']=(df['Adjusted_Forecast']*df['Ideal_Days']).round()
    df['Base_Max_Stock']=(df['Adjusted_Forecast']*df['Max_Days']).round()
    df['Final_Min_Stock']=(df['Base_Min_Stock']*df['ABC_Multiplier']).round(); df['Final_Ideal_Stock']=(df['Base_Ideal_Stock']*df['ABC_Multiplier']).round()
    df['Final_Max_Stock']=(df['Base_Max_Stock']*df['ABC_Multiplier']).round()
    df['Target_Stock']=df.apply(lambda r:r['Final_Max_Stock'] if r['Promo_Tomorrow']=='Yes' else r['Final_Ideal_Stock'],axis=1)
    # Stock Status
    df['Current_Stock']=df.apply(lambda r:stock_dict.get((r['Store_Code'],r['SKU_Code']),0),axis=1)
    df['Stock_Status']=df.apply(get_stock_status,axis=1); df['Coverage_%']=df.apply(get_coverage_pct,axis=1)
    df['Coverage_Category']=df.apply(get_coverage_category,axis=1); df['DoS_Category']=df.apply(get_dos_category,axis=1)
    df['Days_Of_Stock']=(df['Current_Stock']/df['DRR'].clip(lower=0.01)).fillna(99)
    df['Stock_vs_Min']=df['Current_Stock']-df['Final_Min_Stock']; df['Stock_vs_Target']=df['Current_Stock']-df['Target_Stock']
    df['OOS_Threshold']=(df['Final_Min_Stock']*0.5).round()
    df['Stock_Health_%']=(df['Current_Stock']/df['Final_Max_Stock'].clip(lower=0.01)).fillna(0)
    df['Is_OOS']=df['Stock_Status'].apply(lambda x:'Yes' if x=='OOS' else 'No'); df['Reorder_Point']=df['Target_Stock']
    # Transfer
    df['Ideal_Transfer']=(df['Target_Stock']-df['Current_Stock']).clip(lower=0); df['Min_Transfer']=(df['Final_Min_Stock']-df['Current_Stock']).clip(lower=0)
    df['Transfer_Urgency']=df.apply(lambda r:'Must Transfer' if r['Min_Transfer']>0 else ('Should Transfer' if r['Ideal_Transfer']>0 else 'No Transfer'),axis=1)
    df['Warehouse_Stock']=df['SKU_Code'].map(wh_dict).fillna(500)
    df['Total_Need']=df.groupby('SKU_Code')['Ideal_Transfer'].transform('sum')
    df['WH_Shortage']=df.apply(lambda r:'Yes' if r['Total_Need']>r['Warehouse_Stock'] else 'No',axis=1)
    df['WH_Fulfill_%']=(df['Warehouse_Stock']/df['Total_Need'].clip(lower=0.01)).clip(upper=1).fillna(1)
    df['Shortage_Qty']=(df['Total_Need']-df['Warehouse_Stock']).clip(lower=0); df['Shortage_Value']=df['Shortage_Qty']*df['Base_Price']
    df['Store_Daily_Runrate']=df['DRR']; df['Total_Daily_Runrate']=df.groupby('SKU_Code')['DRR'].transform('sum')
    df['Store_Contrib_%']=(df['Store_Daily_Runrate']/df['Total_Daily_Runrate'].clip(lower=0.01)).fillna(0.25)
    df['Allocated_Qty']=df.apply(lambda r:round(r['Warehouse_Stock']*r['Store_Contrib_%']) if r['WH_Shortage']=='Yes' else r['Ideal_Transfer'],axis=1)
    df['Transfer_Shortage_Qty']=(df['Ideal_Transfer']-df['Allocated_Qty']).clip(lower=0)
    df['Transfer_Shortage_Value']=df['Transfer_Shortage_Qty']*df['Base_Price']
    df['Urgency_Score']=df['Stock_Status'].apply(lambda x:4 if x in ['OOS','Critical'] else (2 if x=='Low' else 0))
    df['Promo_Score']=df['Promo_Tomorrow'].apply(lambda x:2 if x=='Yes' else 0)
    # Priority
    df['Priority_Score']=df['Tier_Priority']+df['ABC_Priority']+df['Urgency_Score']+df['Promo_Score']
    df['Priority_Rank']=df['Priority_Score'].rank(ascending=False,method='dense')
    df['Priority_Cat']=df['Priority_Score'].apply(lambda x:'Critical' if x>=9 else ('High' if x>=6 else ('Medium' if x>=3 else 'Low')))
    df['Priority_Remarks']=df['Priority_Score'].apply(lambda x:'Critical - Urgent' if x>=9 else ('High - Today' if x>=6 else ('Medium - Routine' if x>=3 else 'Low - Batch')))
    df['Final_Transfer']=df.apply(lambda r:min(r['Allocated_Qty'],r['Ideal_Transfer'],max(0,r['Final_Max_Stock']-r['Current_Stock'])),axis=1)
    df['Post_Stock']=df['Current_Stock']+df['Final_Transfer']; df['Post_Days']=(df['Post_Stock']/df['DRR'].clip(lower=0.01)).fillna(0)
    df['Transfer_Fulfill_%']=(df['Final_Transfer']/df['Ideal_Transfer'].clip(lower=0.01)).clip(upper=1).fillna(1)
    df['Transfer_CBM']=df['Final_Transfer']*df['CBM_Per_Unit']
    df['Pallets']=(df['Final_Transfer']/df['Units_Per_Pallet'].clip(lower=1)).apply(np.ceil).fillna(0)
    df['Cat_Stock']=df.groupby(['Category','Store_Code'])['Current_Stock'].transform('sum')
    df['Cat_Max']=df.groupby(['Category','Store_Code'])['Final_Max_Stock'].transform('sum')
    df['Cat_Stock_%']=(df['Cat_Stock']/df['Cat_Max'].clip(lower=0.01)).fillna(0)
    df['Cat_Status']=df['Cat_Stock_%'].apply(lambda x:'Overstock' if x>1.1 else ('Understock' if x<0.7 else 'OK'))
    # Flags
    df['Has_Transfer']=df['Final_Transfer'].apply(lambda x:'Yes' if x>0 else 'No')
    df['Is_Critical']=df['Stock_Status'].apply(lambda x:'Yes' if x in ['OOS','Critical'] else 'No')
    df['Is_Overstock']=df['Stock_Status'].apply(lambda x:'Yes' if x=='Overstock' else 'No')
    df['WH_OOS_Risk']=df.apply(lambda r:'Yes' if r['Warehouse_Stock']<r['Total_Need']*0.5 else 'No',axis=1)
    def ar(row):
        if row['Stock_Status']=='OOS': return 'Urgent Transfer - OOS!'
        if row['Is_Critical']=='Yes': return 'Urgent Transfer'
        if row['Has_Transfer']=='Yes': return 'Normal Transfer'
        if row['Is_Overstock']=='Yes': return 'Review Overstock'
        return 'No Action'
    df['Action_Required']=df.apply(ar,axis=1)
    # Assortment Gap
    listed=sales_calc.groupby(['Store_Code','SKU_Code']).size().reset_index()[['Store_Code','SKU_Code']]; listed['Is_Listed']=1
    all_combos=pd.MultiIndex.from_product([stores,skus],names=['Store_Code','SKU_Code']).to_frame(index=False)
    gap_df=all_combos.merge(listed,on=['Store_Code','SKU_Code'],how='left')
    gap_df['Is_Listed']=gap_df['Is_Listed'].fillna(0).astype(int); gap_df['Is_Gap']=(gap_df['Is_Listed']==0).astype(int)
    df=df.merge(gap_df[['Store_Code','SKU_Code','Is_Listed','Is_Gap']],on=['Store_Code','SKU_Code'],how='left')
    df['Is_Listed']=df['Is_Listed'].fillna(0).astype(int); df['Is_Gap']=df['Is_Gap'].fillna(0).astype(int)
    return df

# ==================== SIDEBAR ====================
with st.sidebar:
    # Talabat Logo
    col_l,col_m,col_r = st.columns([1,3,1])
    with col_m:
        try:
            st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRE3gAso9iaSgsjd-y9YXWeezeOq5MLqYzI8w&s",width=130)
        except:
            st.markdown("<div style='font-size:45px; text-align:center;'>🧡</div>",unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; padding:5px 0 10px 0;'>
        <h2 style='color:#FF8C00 !important; margin:4px 0; font-size:16px;'>Stock Transfer</h2>
        <p style='color:rgba(255,224,192,0.7); font-size:10px;'>Dashboard v3.0</p>
    </div>""",unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### 📁 Data Source")
    data_source=st.radio("",["🎯 Sample Data (Demo)","📤 Upload Excel"],label_visibility="collapsed")
    use_sample=data_source=="🎯 Sample Data (Demo)"; uploaded_files_valid=False

    if not use_sample:
        workbook_file=st.file_uploader("Upload workbook",type=['xlsx'],key="wb")
        if workbook_file:
            try:
                xl=pd.ExcelFile(workbook_file); required=['SKU_Master','Sales_Data','Stock_Status','Promo_Calendar']
                missing=[s for s in required if s not in xl.sheet_names]
                if missing: st.error(f"❌ Missing: {', '.join(missing)}")
                else:
                    st.success("✅ Validated!")
                    for s in required: st.markdown(f"• **{s}**: {len(pd.read_excel(workbook_file,sheet_name=s)):,} rows")
                    uploaded_files_valid=True; st.session_state.uploaded_workbook=workbook_file
            except Exception as e: st.error(f"❌ {e}")
    else:
        st.info("📊 Demo: 40 SKUs × 4 Stores × 60 days"); uploaded_files_valid=True

    st.markdown("---")
    calc_date=st.date_input("📅 Calculation Date",value=datetime.now().date())
    st.markdown("---")

    if st.session_state.calculation_done:
        n=len(st.session_state.final_results) if st.session_state.final_results is not None else 0
        t=f"{st.session_state.calc_time:.1f}" if st.session_state.calc_time else "0"
        st.markdown(f"""
        <div style='background:rgba(34,197,94,0.2); border:2px solid rgba(34,197,94,0.5);
                    border-radius:12px; padding:12px; text-align:center;'>
            <span style='color:#22c55e; font-size:20px;'>✅</span>
            <p style='color:#22c55e; margin:5px 0 0 0; font-weight:700;'>Complete!</p>
            <p style='color:rgba(255,224,192,0.8); margin:0; font-size:11px;'>{n:,} SKUs • {t}s</p>
        </div>""",unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background:rgba(255,140,0,0.15); border:2px solid rgba(255,140,0,0.4);
                    border-radius:12px; padding:12px; text-align:center;'>
            <span style='color:#FF8C00; font-size:20px;'>⏳</span>
            <p style='color:#FF8C00; margin:5px 0; font-weight:700;'>Ready</p>
        </div>""",unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    run_button=st.button("🚀 RUN CALCULATION" if not st.session_state.calculation_done else "🔄 RECALCULATE",
        disabled=not uploaded_files_valid,use_container_width=True,type="primary")

    if run_button:
        start_time=time.time(); prog=st.empty(); stat=st.empty()
        try:
            prog.progress(5,"📊 Loading...")
            if use_sample: sales_data,sku_master,stock_status_df,promo_calendar=generate_sample_data()
            else:
                wb=st.session_state.uploaded_workbook
                sales_data=pd.read_excel(wb,sheet_name='Sales_Data'); sku_master=pd.read_excel(wb,sheet_name='SKU_Master')
                stock_status_df=pd.read_excel(wb,sheet_name='Stock_Status'); promo_calendar=pd.read_excel(wb,sheet_name='Promo_Calendar')
            for df_c,cols in [(sales_data,{'Date':None,'Store_Code':str,'SKU_Code':str,'Sales_Qty':int,'Selling_Price':float,'Sales_Value':float}),(sku_master,{'SKU_Code':str,'Base_Price':float,'CBM_Per_Unit':float,'Shelf_Life_Days':int}),(stock_status_df,{'Store_Code':str,'SKU_Code':str,'Current_Stock':int,'Warehouse_Stock':int}),(promo_calendar,{'Store_Code':str,'SKU_Code':str,'Regular_Price':float,'Promo_Price':float})]:
                for col,dtype in cols.items():
                    if col in df_c.columns:
                        if col=='Date': df_c[col]=pd.to_datetime(df_c[col])
                        elif dtype==str: df_c[col]=df_c[col].astype(str).str.strip()
                        elif dtype==int: df_c[col]=df_c[col].apply(clean_number).astype(int)
                        elif dtype==float: df_c[col]=df_c[col].apply(clean_number)
            promo_calendar['Start_Date']=pd.to_datetime(promo_calendar['Start_Date']); promo_calendar['End_Date']=pd.to_datetime(promo_calendar['End_Date'])
            prog.progress(20,"🧮 SKU Master..."); sku_calc,_,stores_in_data=calculate_sku_master_full(sku_master,sales_data)
            prog.progress(35,"📅 Promo..."); promo_calc=calculate_promo_calendar_full(promo_calendar,pd.Timestamp(calc_date)+pd.Timedelta(days=1))
            prog.progress(55,"📈 Sales..."); sales_enh=calculate_sales_data_enhanced(sales_data,sku_calc)
            prog.progress(80,"🚚 Transfers..."); final=calculate_final_calculation(sales_enh,sku_calc,stock_status_df,promo_calc,calc_date)
            st.session_state.sales_data=sales_data; st.session_state.sku_master=sku_calc
            st.session_state.stock_status=stock_status_df; st.session_state.promo_calendar=promo_calc
            st.session_state.sales_enhanced=sales_enh; st.session_state.final_results=final
            st.session_state.filtered_results=final.copy()
            st.session_state.calc_time=time.time()-start_time; st.session_state.calc_date=calc_date
            st.session_state.calculation_done=True
            prog.progress(100,"✅ Done!"); time.sleep(0.3); prog.empty(); stat.empty()
            st.success(f"✅ {st.session_state.calc_time:.1f}s!"); st.balloons(); st.rerun()
        except Exception as e:
            prog.empty(); stat.empty(); st.error(f"❌ {e}")
            import traceback; st.code(traceback.format_exc())

    st.markdown("---")
    if st.session_state.calculation_done and st.session_state.final_results is not None:
        st.markdown("### 🎛️ Filters")
        df_f=st.session_state.final_results
        store_f=st.multiselect("🏪 Store",sorted(df_f['Store_Code'].unique()),placeholder="All")
        tier_f=st.multiselect("🏆 Tier",sorted(df_f['Store_Tier'].unique()),placeholder="All")
        cat_f=st.multiselect("📂 Category",sorted(df_f['Category'].unique()),placeholder="All")
        subcat_f=st.multiselect("📁 Sub-Cat",sorted(df_f['Sub_Category'].unique()),placeholder="All")
        brand_f=st.multiselect("🏷️ Brand",sorted(df_f['Brand'].unique()),placeholder="All")
        sku_f=st.multiselect("📦 SKU",sorted(df_f['SKU_Code'].unique()),placeholder="All")
        abc_f=st.multiselect("🔤 ABC",['A','B','C'],placeholder="All")
        status_f=st.multiselect("📊 Status",['OOS','Critical','Low','OK','Overstock'],placeholder="All")
        cov_f=st.multiselect("📉 Coverage",['OOS','Critical','Very Low','Low','OK','Overstock'],placeholder="All")
        filtered=df_f.copy()
        if store_f: filtered=filtered[filtered['Store_Code'].isin(store_f)]
        if tier_f: filtered=filtered[filtered['Store_Tier'].isin(tier_f)]
        if cat_f: filtered=filtered[filtered['Category'].isin(cat_f)]
        if subcat_f: filtered=filtered[filtered['Sub_Category'].isin(subcat_f)]
        if brand_f: filtered=filtered[filtered['Brand'].isin(brand_f)]
        if sku_f: filtered=filtered[filtered['SKU_Code'].isin(sku_f)]
        if abc_f: filtered=filtered[filtered['ABC_Class'].isin(abc_f)]
        if status_f: filtered=filtered[filtered['Stock_Status'].isin(status_f)]
        if cov_f: filtered=filtered[filtered['Coverage_Category'].isin(cov_f)]
        st.session_state.filtered_results=filtered
        st.markdown(f"""
        <div style='background:rgba(255,140,0,0.15); padding:10px; border-radius:10px;'>
            <p style='margin:3px 0; font-size:11px; color:#FFE0C0;'><b>Showing:</b> {len(filtered):,} SKUs</p>
            <p style='margin:3px 0; font-size:11px; color:#FFE0C0;'><b>Stores:</b> {filtered['Store_Code'].nunique()}</p>
            <p style='margin:3px 0; font-size:11px; color:#FFE0C0;'><b>Categories:</b> {filtered['Category'].nunique()}</p>
        </div>""",unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("### 📥 Downloads")
        tmpl=io.BytesIO()
        with pd.ExcelWriter(tmpl,engine='openpyxl') as writer:
            pd.DataFrame({'Row_ID':[1,2,3],'Date':['2026-01-01','2026-01-01','2026-01-02'],'Store_Code':['DS_JLT','DS_MARINA','DS_JLT'],'SKU_Code':['SKU001','SKU001','SKU001'],'Sales_Qty':[150,120,160],'Selling_Price':[4.50,4.50,4.50],'Sales_Value':[675,540,720]}).to_excel(writer,sheet_name='Sales_Data',index=False)
            pd.DataFrame({'SKU_Code':['SKU001','SKU002'],'SKU_Name':['Nestle Pure Life 6x500ml','Masafi 6x500ml Pack'],'Brand':['Nestle','Masafi'],'Category':['Beverages','Beverages'],'Sub_Category':['Water','Water'],'Base_Price':[4.50,4.20],'CBM_Per_Unit':[0.002,0.002],'Shelf_Life_Days':[180,180]}).to_excel(writer,sheet_name='SKU_Master',index=False)
            pd.DataFrame({'Date':['2026-01-15','2026-01-15'],'Store_Code':['DS_JLT','DS_MARINA'],'SKU_Code':['SKU001','SKU001'],'Current_Stock':[369,320],'Warehouse_Stock':[3135,3135]}).to_excel(writer,sheet_name='Stock_Status',index=False)
            pd.DataFrame({'Promo_ID':[1],'Store_Code':['DS_JLT'],'SKU_Code':['SKU001'],'Start_Date':['2026-01-16'],'End_Date':['2026-01-20'],'Regular_Price':[4.50],'Promo_Price':[3.15]}).to_excel(writer,sheet_name='Promo_Calendar',index=False)
            pd.DataFrame({'Sheet':['Sales_Data']*7+['SKU_Master']*8+['Stock_Status']*5+['Promo_Calendar']*7,'Column':['Row_ID','Date','Store_Code','SKU_Code','Sales_Qty','Selling_Price','Sales_Value','SKU_Code','SKU_Name','Brand','Category','Sub_Category','Base_Price','CBM_Per_Unit','Shelf_Life_Days','Date','Store_Code','SKU_Code','Current_Stock','Warehouse_Stock','Promo_ID','Store_Code','SKU_Code','Start_Date','End_Date','Regular_Price','Promo_Price'],'Format':['Integer','YYYY-MM-DD','Text','Text','Integer','Decimal','Decimal','Text','Text','Text','Text','Text','Decimal','Decimal','Integer','YYYY-MM-DD','Text','Text','Integer','Integer','Integer','Text','Text','YYYY-MM-DD','YYYY-MM-DD','Decimal','Decimal'],'Notes':['Sequential','Last 60 days','Consistent','Match SKU_Master','Units sold','Selling price','Qty×Price','Unique ID','Full name','Brand','Category','Sub-cat','Normal price AED','m³/unit','Days to expire','Today date','Match Sales','Match SKU_Master','Store units','WH units','Sequential','Match Sales','Match SKU_Master','Start date','End date','Normal price','Promo price']}).to_excel(writer,sheet_name='Instructions',index=False)
        st.download_button("📥 Input Template",tmpl.getvalue(),"stock_transfer_template.xlsx","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",use_container_width=True)
# ==================== MAIN CONTENT ====================
if not st.session_state.calculation_done or st.session_state.final_results is None:

    # Welcome Logo
    col1,col2,col3 = st.columns([2,1,2])
    with col2:
        try:
            st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRE3gAso9iaSgsjd-y9YXWeezeOq5MLqYzI8w&s",width=180)
        except:
            st.markdown("<div style='font-size:80px; text-align:center;'>🧡</div>",unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; padding:10px 20px 20px 20px;'>
        <h1 style='color:#2C1810 !important; font-size:34px;'>Stock Transfer Dashboard</h1>
        <p style='color:#8B7355; font-size:15px; max-width:500px; margin:0 auto 20px;'>
            Intelligent Stock Transfer & Replenishment System
        </p>
    </div>""",unsafe_allow_html=True)

    col_left,col_right = st.columns(2)
    with col_left:
        st.markdown("""
        <div style='background:#FFFFFF; border:2px solid rgba(255,111,0,0.2);
                    border-radius:16px; padding:25px; box-shadow:0 4px 15px rgba(44,24,16,0.06);'>
            <h3 style='color:#FF6F00 !important; margin-top:0;'>🚀 Getting Started</h3>
            <ol style='color:#3D2415; line-height:2.2; font-size:14px;'>
                <li><b style='color:#2C1810;'>Download</b> the input template below</li>
                <li><b style='color:#2C1810;'>Fill</b> your data in all 4 sheets</li>
                <li><b style='color:#2C1810;'>Upload</b> via sidebar → Upload Excel</li>
                <li><b style='color:#2C1810;'>Set</b> calculation date in sidebar</li>
                <li><b style='color:#2C1810;'>Click</b> RUN CALCULATION</li>
            </ol>
            <p style='color:#8B7355; font-size:12px; margin-top:10px;'>
                💡 Or use <b style='color:#FF6F00;'>Sample Data (Demo)</b> in sidebar to explore instantly!
            </p>
        </div>""",unsafe_allow_html=True)

    with col_right:
        st.markdown("""
        <div style='background:#FFFFFF; border:2px solid rgba(255,111,0,0.2);
                    border-radius:16px; padding:25px; box-shadow:0 4px 15px rgba(44,24,16,0.06);'>
            <h3 style='color:#FF6F00 !important; margin-top:0;'>📋 What You Need (1 Excel File)</h3>
            <table style='color:#3D2415; font-size:13px; width:100%; border-collapse:collapse;'>
                <tr style='border-bottom:1px solid #E8D5C0;'>
                    <td style='padding:8px 0;'><b style='color:#FF6F00;'>Sheet 1</b></td>
                    <td style='padding:8px;'><b>Sales_Data</b></td>
                    <td style='color:#8B7355;'>Last 60 days of sales</td>
                </tr>
                <tr style='border-bottom:1px solid #E8D5C0;'>
                    <td style='padding:8px 0;'><b style='color:#FF6F00;'>Sheet 2</b></td>
                    <td style='padding:8px;'><b>SKU_Master</b></td>
                    <td style='color:#8B7355;'>Product information</td>
                </tr>
                <tr style='border-bottom:1px solid #E8D5C0;'>
                    <td style='padding:8px 0;'><b style='color:#FF6F00;'>Sheet 3</b></td>
                    <td style='padding:8px;'><b>Stock_Status</b></td>
                    <td style='color:#8B7355;'>Today's stock levels</td>
                </tr>
                <tr>
                    <td style='padding:8px 0;'><b style='color:#FF6F00;'>Sheet 4</b></td>
                    <td style='padding:8px;'><b>Promo_Calendar</b></td>
                    <td style='color:#8B7355;'>Upcoming promotions</td>
                </tr>
            </table>
            <p style='color:#8B7355; font-size:12px; margin-top:12px;'>
                ✅ All 4 sheets in <b style='color:#2C1810;'>one Excel file</b><br>
                ✅ Sheet names must match exactly<br>
                ✅ See <b style='color:#FF6F00;'>Instructions</b> tab in template
            </p>
        </div>""",unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#8B7355; font-size:13px;'>👇 Download template with example data + instructions</p>",unsafe_allow_html=True)

    tmpl=io.BytesIO()
    with pd.ExcelWriter(tmpl,engine='openpyxl') as writer:
        pd.DataFrame({'Row_ID':[1,2,3,4,5],'Date':['2026-01-01']*2+['2026-01-02']*2+['2026-01-03'],'Store_Code':['DS_JLT','DS_MARINA','DS_JLT','DS_MARINA','DS_JLT'],'SKU_Code':['SKU001','SKU001','SKU001','SKU001','SKU002'],'Sales_Qty':[150,120,160,130,135],'Selling_Price':[4.50,4.50,4.50,4.50,4.20],'Sales_Value':[675,540,720,585,567]}).to_excel(writer,sheet_name='Sales_Data',index=False)
        pd.DataFrame({'SKU_Code':['SKU001','SKU002'],'SKU_Name':['Nestle Pure Life 6x500ml','Masafi 6x500ml Pack'],'Brand':['Nestle','Masafi'],'Category':['Beverages','Beverages'],'Sub_Category':['Water','Water'],'Base_Price':[4.50,4.20],'CBM_Per_Unit':[0.002,0.002],'Shelf_Life_Days':[180,180]}).to_excel(writer,sheet_name='SKU_Master',index=False)
        pd.DataFrame({'Date':['2026-01-15','2026-01-15'],'Store_Code':['DS_JLT','DS_MARINA'],'SKU_Code':['SKU001','SKU001'],'Current_Stock':[369,320],'Warehouse_Stock':[3135,3135]}).to_excel(writer,sheet_name='Stock_Status',index=False)
        pd.DataFrame({'Promo_ID':[1],'Store_Code':['DS_JLT'],'SKU_Code':['SKU001'],'Start_Date':['2026-01-16'],'End_Date':['2026-01-20'],'Regular_Price':[4.50],'Promo_Price':[3.15]}).to_excel(writer,sheet_name='Promo_Calendar',index=False)
        pd.DataFrame({'Sheet':['Sales_Data']*7+['SKU_Master']*8+['Stock_Status']*5+['Promo_Calendar']*7,'Column':['Row_ID','Date','Store_Code','SKU_Code','Sales_Qty','Selling_Price','Sales_Value','SKU_Code','SKU_Name','Brand','Category','Sub_Category','Base_Price','CBM_Per_Unit','Shelf_Life_Days','Date','Store_Code','SKU_Code','Current_Stock','Warehouse_Stock','Promo_ID','Store_Code','SKU_Code','Start_Date','End_Date','Regular_Price','Promo_Price'],'Notes':['Sequential','Last 60 days','Consistent','Match SKU_Master','Units sold','Selling price','Qty×Price','Unique ID','Full name','Brand','Category','Sub-cat','Normal price','m³/unit','Days expire','Today','Match Sales','Match SKU_Master','Store units','WH units','Sequential','Match Sales','Match SKU_Master','Start date','End date','Normal price','Promo price']}).to_excel(writer,sheet_name='Instructions',index=False)

    _,col_mid,_ = st.columns([1,2,1])
    with col_mid:
        st.download_button("📥 Download Input Template (Excel)",tmpl.getvalue(),"stock_transfer_template.xlsx","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",use_container_width=True)

else:
    results = st.session_state.filtered_results
    sales_enhanced = st.session_state.sales_enhanced
    today_ts = pd.Timestamp.now().normalize()

    if results is None or len(results)==0:
        st.warning("⚠️ No data matches current filters. Please adjust sidebar filters.")
        st.stop()

    tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8 = st.tabs([
        "🏠 Dashboard","📊 Stock Health","🚚 Transfers",
        "⚠️ Canni & Subs","📈 Trends","🏪 Warehouse",
        "💰 Opportunity Loss","📋 Data Table"
    ])

    # ==================== TAB 1: DASHBOARD ====================
    with tab1:
        st.markdown("<h2 style='text-align:center;'>🏠 Executive Dashboard</h2>",unsafe_allow_html=True)
        st.markdown("---")
        total_skus=len(results)
        if total_skus==0: st.info("No data."); st.stop()
        oos_c=len(results[results['Stock_Status']=='OOS']); crit_c=len(results[results['Stock_Status']=='Critical'])
        low_c=len(results[results['Stock_Status']=='Low']); ok_c=len(results[results['Stock_Status']=='OK'])
        over_c=len(results[results['Stock_Status']=='Overstock'])
        instock_c=total_skus-oos_c; instock_pct=instock_c/total_skus*100

        st.markdown(info_card("📋 <b style='color:#FF6F00;'>Stock Levels:</b> 🚫 <b>OOS</b>: Stock=0 | 🔴 <b>Critical</b>: &lt;50% Min | ⚠️ <b>Low</b>: &lt;Ideal | ✅ <b>OK</b>: Ideal→Max | 📈 <b>Overstock</b>: &gt;Max"),unsafe_allow_html=True)

        # Row 1: KPI
        c1,c2,c3,c4,c5,c6=st.columns(6)
        with c1: st.markdown(create_colored_kpi("Total SKUs",f"{total_skus:,}",f"In-Stock: {instock_pct:.0f}%","📦",KPI_COLORS['slate']),unsafe_allow_html=True)
        with c2: st.markdown(create_colored_kpi("OOS",f"{oos_c:,}",f"{oos_c/total_skus*100:.1f}%","🚫",KPI_COLORS['danger_dark']),unsafe_allow_html=True)
        with c3: st.markdown(create_colored_kpi("Critical",f"{crit_c:,}",f"{crit_c/total_skus*100:.1f}%","🔴",KPI_COLORS['danger']),unsafe_allow_html=True)
        with c4: st.markdown(create_colored_kpi("Low Stock",f"{low_c:,}",f"{low_c/total_skus*100:.1f}%","⚠️",KPI_COLORS['warning']),unsafe_allow_html=True)
        with c5: st.markdown(create_colored_kpi("OK Stock",f"{ok_c:,}",f"{ok_c/total_skus*100:.1f}%","✅",KPI_COLORS['success']),unsafe_allow_html=True)
        with c6: st.markdown(create_colored_kpi("Overstock",f"{over_c:,}",f"{over_c/total_skus*100:.1f}%","📈",KPI_COLORS['info']),unsafe_allow_html=True)

        st.markdown("<br>",unsafe_allow_html=True)

        # Row 2: Store Cards (In-Stock %)
        st.markdown("#### 🏪 Store Performance (In-Stock %)")
        store_sum=results.groupby('Store_Code').agg(Total=('SKU_Code','count'),OOS=('Stock_Status',lambda x:(x=='OOS').sum()),Critical=('Stock_Status',lambda x:(x=='Critical').sum()),Transfer=('Final_Transfer','sum'))
        store_sum['InStock_Pct']=((store_sum['Total']-store_sum['OOS'])/store_sum['Total']*100).round(1)
        sc_list=st.columns(len(store_sum))
        sc_colors=['#FF6F00','#e65100','#bf360c','#8b4513']
        for idx,(store,row) in enumerate(store_sum.iterrows()):
            with sc_list[idx]:
                st.markdown(create_colored_kpi(store,f"{row['InStock_Pct']:.1f}%",f"{int(row['Total'])} SKUs | OOS:{int(row['OOS'])} | Crit:{int(row['Critical'])} | Tfr:{fmt(row['Transfer'])}","🏪",sc_colors[idx%len(sc_colors)]),unsafe_allow_html=True)

        st.markdown("<br>",unsafe_allow_html=True)

        # Row 3: Status Donut + ABC Bar
        c1,c2=st.columns(2)
        with c1:
            st.markdown("#### 🎯 Stock Status Distribution")
            sc=results['Stock_Status'].value_counts().reindex([s for s in ['OOS','Critical','Low','OK','Overstock'] if s in results['Stock_Status'].values])
            if len(sc)>0:
                fig=go.Figure(data=[go.Pie(labels=sc.index,values=sc.values,hole=0.5,marker=dict(colors=[STATUS_COLORS.get(s,'#94a3b8') for s in sc.index]),textinfo='label+percent+value',textfont=dict(size=11,color='#ffffff'))])
                fig.update_layout(height=320,showlegend=False); st.plotly_chart(fig,use_container_width=True)
        with c2:
            st.markdown("#### 📊 ABC Classification")
            ac=results['ABC_Class'].value_counts().reindex(['A','B','C']).fillna(0)
            fig=go.Figure(data=[go.Bar(x=['A (Fast)','B (Medium)','C (Slow)'],y=ac.values,marker=dict(color=['#FF6F00','#8b5cf6','#94a3b8']),text=ac.values.astype(int),textposition='auto',textfont=dict(color='#ffffff',size=14))])
            fig.update_layout(height=320); st.plotly_chart(fig,use_container_width=True)

        st.markdown("<br>",unsafe_allow_html=True)

        # Row 4: In-Stock Heatmap
        st.markdown("#### 🗺️ In-Stock % by Category × Store")
        instock_pivot=results.groupby(['Category','Store_Code']).apply(lambda x:((x['Stock_Status']!='OOS').sum()/len(x)*100) if len(x)>0 else 0).unstack(fill_value=0)
        if not instock_pivot.empty:
            fig=go.Figure(data=go.Heatmap(z=instock_pivot.values,x=instock_pivot.columns,y=instock_pivot.index,colorscale='RdYlGn',zmin=0,zmax=100,text=np.round(instock_pivot.values,1),texttemplate='%{text}%',textfont=dict(size=12,color='#000000'),colorbar=dict(title=dict(text='In-Stock %',font=dict(color=CHART_TEXT)),tickfont=dict(color=CHART_TEXT))))
            fig.update_layout(height=320,xaxis_title="Store",yaxis_title="Category",margin=dict(t=20,b=40,l=100,r=30)); st.plotly_chart(fig,use_container_width=True)

        st.markdown("<br>",unsafe_allow_html=True)

        # Row 5: Category In-Stock Bar
        st.markdown("#### 📂 Category In-Stock %")
        cat_instock=results.groupby('Category').apply(lambda x:((x['Stock_Status']!='OOS').sum()/len(x)*100) if len(x)>0 else 0).sort_values(ascending=True)
        if len(cat_instock)>0:
            bar_c=['#ef4444' if v<70 else '#f59e0b' if v<85 else '#22c55e' for v in cat_instock.values]
            fig=go.Figure(data=[go.Bar(y=cat_instock.index,x=cat_instock.values,orientation='h',marker=dict(color=bar_c),text=[f"{v:.1f}%" for v in cat_instock.values],textposition='auto',textfont=dict(color='#ffffff',size=12))])
            fig.add_vline(x=85,line_dash="dash",line_color="#22c55e",annotation_text="Target 85%",annotation_font_color="#22c55e")
            fig.update_layout(height=250,xaxis=dict(title="In-Stock %",range=[0,105])); st.plotly_chart(fig,use_container_width=True)

        st.markdown("<br>",unsafe_allow_html=True)

        # Row 6: Brand Status Table
        st.markdown("#### 🏷️ Brand Stock Status Breakdown")
        brand_st=results.groupby('Brand').agg(SKUs=('SKU_Code','count'),Total_DRR=('DRR','sum'),OOS_n=('Stock_Status',lambda x:(x=='OOS').sum()),Crit_n=('Stock_Status',lambda x:(x=='Critical').sum()),Low_n=('Stock_Status',lambda x:(x=='Low').sum()),OK_n=('Stock_Status',lambda x:(x=='OK').sum()),Over_n=('Stock_Status',lambda x:(x=='Overstock').sum()))
        brand_st['InStock%']=((brand_st['SKUs']-brand_st['OOS_n'])/brand_st['SKUs']*100).round(1)
        brand_st['OOS%']=(brand_st['OOS_n']/brand_st['SKUs']*100).round(1)
        brand_st['Crit%']=(brand_st['Crit_n']/brand_st['SKUs']*100).round(1)
        brand_st['Low%']=(brand_st['Low_n']/brand_st['SKUs']*100).round(1)
        brand_st['OK%']=(brand_st['OK_n']/brand_st['SKUs']*100).round(1)
        brand_st['Over%']=(brand_st['Over_n']/brand_st['SKUs']*100).round(1)
        brand_st['Total_DRR']=brand_st['Total_DRR'].round(0).astype(int)
        brand_st=brand_st.sort_values('Total_DRR',ascending=False)
        brand_disp=brand_st[['SKUs','Total_DRR','InStock%','OOS_n','OOS%','Crit_n','Crit%','Low_n','Low%','OK_n','OK%','Over_n','Over%']]
        brand_disp.columns=['SKUs','DRR','InStock%','OOS','OOS%','Critical','Crit%','Low','Low%','OK','OK%','Over','Over%']
        st.dataframe(brand_disp,use_container_width=True,height=400)

        st.markdown("<br>",unsafe_allow_html=True)

        # Row 7: Quick Action Cards
        st.markdown("#### ⚡ Quick Actions Required")
        oos_loss_d=(results[results['Stock_Status']=='OOS']['DRR']*results[results['Stock_Status']=='OOS']['Base_Price']).sum()
        over_val=(results[results['Stock_Status']=='Overstock']['Current_Stock']*results[results['Stock_Status']=='Overstock']['Base_Price']).sum()
        c1,c2,c3=st.columns(3)
        with c1: st.markdown(create_action_card("🚫",f"{oos_c} OOS SKUs",fmt(oos_loss_d,"AED ")+"/day loss","→ Transfer Immediately",KPI_COLORS['danger_dark']),unsafe_allow_html=True)
        with c2: st.markdown(create_action_card("🔴",f"{crit_c} Critical SKUs","Will go OOS in hours","→ Prioritize Transfer",KPI_COLORS['danger']),unsafe_allow_html=True)
        with c3: st.markdown(create_action_card("📈",f"{over_c} Overstock SKUs",fmt(over_val,"AED ")+" tied up","→ Review & Redistribute",KPI_COLORS['info']),unsafe_allow_html=True)

    # ==================== TAB 2: STOCK HEALTH ====================
    with tab2:
        st.markdown("<h2 style='text-align:center;'>📊 Stock Health Analysis</h2>",unsafe_allow_html=True)
        st.markdown("---")
        if len(results)==0: st.info("No data."); st.stop()
        t2=len(results); avg_cov=results['Coverage_%'].mean()
        c1,c2,c3,c4,c5,c6=st.columns(6)
        with c1: st.markdown(create_colored_kpi("OOS",f"{len(results[results['Stock_Status']=='OOS']):,}",f"{len(results[results['Stock_Status']=='OOS'])/t2*100:.1f}%","🚫",KPI_COLORS['danger_dark']),unsafe_allow_html=True)
        with c2: st.markdown(create_colored_kpi("Critical",f"{len(results[results['Stock_Status']=='Critical']):,}",f"{len(results[results['Stock_Status']=='Critical'])/t2*100:.1f}%","🔴",KPI_COLORS['danger']),unsafe_allow_html=True)
        with c3: st.markdown(create_colored_kpi("Low",f"{len(results[results['Stock_Status']=='Low']):,}",f"{len(results[results['Stock_Status']=='Low'])/t2*100:.1f}%","⚠️",KPI_COLORS['warning']),unsafe_allow_html=True)
        with c4: st.markdown(create_colored_kpi("OK",f"{len(results[results['Stock_Status']=='OK']):,}",f"{len(results[results['Stock_Status']=='OK'])/t2*100:.1f}%","✅",KPI_COLORS['success']),unsafe_allow_html=True)
        with c5: st.markdown(create_colored_kpi("Overstock",f"{len(results[results['Stock_Status']=='Overstock']):,}",f"{len(results[results['Stock_Status']=='Overstock'])/t2*100:.1f}%","📈",KPI_COLORS['info']),unsafe_allow_html=True)
        with c6: st.markdown(create_colored_kpi("Avg Coverage",f"{avg_cov:.1f}%","of Ideal","📊",KPI_COLORS['purple']),unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        st.markdown("#### 📊 Coverage Category Summary")
        cov_order=['OOS','Critical','Very Low','Low','OK','Overstock']
        cov_s=results.groupby('Coverage_Category').agg(SKU_Count=('SKU_Code','count'),Stock=('Current_Stock','sum'),DRR=('DRR','sum'),Avg_Cov=('Coverage_%','mean'))
        cov_s=cov_s.reindex([c for c in cov_order if c in cov_s.index]).fillna(0); cov_s['Pct']=(cov_s['SKU_Count']/cov_s['SKU_Count'].sum()*100).round(1); cov_s['Avg_Cov']=cov_s['Avg_Cov'].round(1)
        c1,c2=st.columns(2)
        with c1: st.dataframe(cov_s,use_container_width=True)
        with c2:
            valid=[c for c in cov_order if c in cov_s.index and cov_s.loc[c,'SKU_Count']>0]
            if valid:
                fig=go.Figure(data=[go.Bar(x=valid,y=[cov_s.loc[c,'SKU_Count'] for c in valid],marker=dict(color=[COV_COLORS.get(c,'#94a3b8') for c in valid]),text=[int(cov_s.loc[c,'SKU_Count']) for c in valid],textposition='auto',textfont=dict(color='#ffffff',size=12))]); fig.update_layout(height=280); st.plotly_chart(fig,use_container_width=True)
        st.markdown("<br>",unsafe_allow_html=True)
        st.markdown("#### 📂 Category Summary")
        cat_sum=results.groupby('Category').agg(SKUs=('SKU_Code','count'),Stock=('Current_Stock','sum'),DRR=('DRR','sum'),Avg_DoS=('Days_Of_Stock','mean'),Avg_Cov=('Coverage_%','mean'),OOS=('Stock_Status',lambda x:(x=='OOS').sum()),Critical=('Stock_Status',lambda x:(x=='Critical').sum()),Low=('Stock_Status',lambda x:(x=='Low').sum()),OK=('Stock_Status',lambda x:(x=='OK').sum()),Overstock=('Stock_Status',lambda x:(x=='Overstock').sum()),L30_AED=('L30_Total_Value','sum'))
        cat_sum['Avg_DoS']=cat_sum['Avg_DoS'].round(1); cat_sum['Avg_Cov']=cat_sum['Avg_Cov'].round(1)
        st.dataframe(cat_sum,use_container_width=True)
        st.markdown("<br>",unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1:
            st.markdown("##### 📅 Avg Coverage % by Category")
            if len(cat_sum)>0:
                fig=go.Figure(data=[go.Bar(x=cat_sum.index,y=cat_sum['Avg_Cov'],marker=dict(color=cat_sum['Avg_Cov'],colorscale='RdYlGn',cmin=0,cmax=150),text=(cat_sum['Avg_Cov'].round(1).astype(str)+'%'),textposition='auto',textfont=dict(color='#000000',size=11))])
                fig.add_hline(y=100,line_dash="dash",line_color="#22c55e",annotation_text="Ideal",annotation_font_color="#22c55e"); fig.update_layout(height=300); st.plotly_chart(fig,use_container_width=True)
        with c2:
            st.markdown("##### 📦 OOS + Critical by Category")
            if len(cat_sum)>0:
                fig=go.Figure(); fig.add_trace(go.Bar(name='OOS',x=cat_sum.index,y=cat_sum['OOS'],marker_color='#7f1d1d',text=cat_sum['OOS'].astype(int),textposition='auto',textfont=dict(color='#ffffff')))
                fig.add_trace(go.Bar(name='Critical',x=cat_sum.index,y=cat_sum['Critical'],marker_color='#ef4444',text=cat_sum['Critical'].astype(int),textposition='auto',textfont=dict(color='#ffffff')))
                fig.update_layout(barmode='stack',height=300,legend=dict(orientation='h',y=1.1)); st.plotly_chart(fig,use_container_width=True)
        st.markdown("<br>",unsafe_allow_html=True)
        st.markdown("#### 📋 SKU Detail")
        scols=['Store_Code','SKU_Code','SKU_Name','Brand','Category','ABC_Class','Stock_Status','Coverage_%','Coverage_Category','DoS_Category','Days_Of_Stock','Current_Stock','Final_Ideal_Stock','Final_Max_Stock','DRR']
        st.dataframe(results[[c for c in scols if c in results.columns]].sort_values(['Stock_Status','Coverage_%']),use_container_width=True,height=400)

    # ==================== TAB 3: TRANSFERS ====================
    with tab3:
        st.markdown("<h2 style='text-align:center;'>🚚 Transfer Recommendations</h2>",unsafe_allow_html=True)
        st.markdown("---")
        if len(results)==0: st.info("No data."); st.stop()
        ttf=results['Final_Transfer'].sum(); ttfv=(results['Final_Transfer']*results['Base_Price']).sum()
        tfs=len(results[results['Has_Transfer']=='Yes']); ctf=len(results[results['Priority_Cat']=='Critical'])
        tsh=results['Transfer_Shortage_Qty'].sum(); tshv=results['Transfer_Shortage_Value'].sum()
        c1,c2,c3,c4,c5,c6=st.columns(6)
        with c1: st.markdown(create_colored_kpi("Total Transfer",fmt(ttf),"units","🚚",KPI_COLORS['primary']),unsafe_allow_html=True)
        with c2: st.markdown(create_colored_kpi("Value",fmt(ttfv,"AED "),"","💰",KPI_COLORS['success']),unsafe_allow_html=True)
        with c3: st.markdown(create_colored_kpi("SKUs",f"{tfs:,}","to transfer","📦",KPI_COLORS['purple']),unsafe_allow_html=True)
        with c4: st.markdown(create_colored_kpi("Critical",f"{ctf:,}","priority","🔴",KPI_COLORS['danger']),unsafe_allow_html=True)
        with c5: st.markdown(create_colored_kpi("Shortage",fmt(tsh),"units","⚠️",KPI_COLORS['warning']),unsafe_allow_html=True)
        with c6: st.markdown(create_colored_kpi("Short Value",fmt(tshv,"AED "),"","💸",KPI_COLORS['orange']),unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        st.markdown("#### 🏪 Store Transfer Summary")
        stf=results.groupby('Store_Code').agg(SKUs=('SKU_Code','count'),OOS=('Stock_Status',lambda x:(x=='OOS').sum()),Critical=('Stock_Status',lambda x:(x=='Critical').sum()),Low=('Stock_Status',lambda x:(x=='Low').sum()),Promo=('Promo_Tomorrow',lambda x:(x=='Yes').sum()),Transfer=('Final_Transfer','sum'),Shortage=('Transfer_Shortage_Qty','sum'),Short_AED=('Transfer_Shortage_Value','sum'),DRR=('DRR','sum'),L7_Qty=('L7_Total','sum'),L30_AED=('L30_Total_Value','sum'))
        st.dataframe(stf,use_container_width=True)
        st.markdown("<br>",unsafe_allow_html=True)
        st.markdown("#### 📂 Category Transfer Summary")
        ctf2=results.groupby('Category').agg(SKUs=('SKU_Code','count'),OOS=('Stock_Status',lambda x:(x=='OOS').sum()),Critical=('Stock_Status',lambda x:(x=='Critical').sum()),Transfer=('Final_Transfer','sum'),Shortage=('Transfer_Shortage_Qty','sum'),Short_AED=('Transfer_Shortage_Value','sum'),DRR=('DRR','sum'),L30_AED=('L30_Total_Value','sum'))
        st.dataframe(ctf2,use_container_width=True)
        st.markdown("<br>",unsafe_allow_html=True)
        c1,c2,c3=st.columns(3)
        with c1:
            pri_s=results.groupby('Priority_Cat').agg(SKUs=('SKU_Code','count'),Qty=('Final_Transfer','sum'))
            pri_s=pri_s.reindex([p for p in ['Critical','High','Medium','Low'] if p in pri_s.index]).fillna(0).astype(int)
            st.markdown("##### 🎯 Priority"); st.dataframe(pri_s,use_container_width=True)
        with c2:
            st.markdown("##### 🔝 Top 10")
            t10=results.nlargest(10,'Final_Transfer')[['SKU_Name','Final_Transfer','Priority_Cat']]
            if len(t10)>0:
                fig=go.Figure(data=[go.Bar(y=t10['SKU_Name'],x=t10['Final_Transfer'],orientation='h',marker=dict(color=[{'Critical':'#ef4444','High':'#f97316','Medium':'#f59e0b','Low':'#22c55e'}.get(p,'#94a3b8') for p in t10['Priority_Cat']]),text=t10['Final_Transfer'].astype(int),textposition='auto',textfont=dict(color='#ffffff',size=10))]); fig.update_layout(height=300,yaxis=dict(autorange='reversed')); st.plotly_chart(fig,use_container_width=True)
        with c3:
            st.markdown("##### 🏪 By Store")
            st2=results.groupby('Store_Code')['Final_Transfer'].sum().sort_values(ascending=True)
            if len(st2)>0:
                fig=go.Figure(data=[go.Bar(y=st2.index,x=st2.values,orientation='h',marker=dict(color='#FF6F00'),text=st2.values.astype(int),textposition='auto',textfont=dict(color='#ffffff',size=11))]); fig.update_layout(height=300); st.plotly_chart(fig,use_container_width=True)
        st.markdown("<br>",unsafe_allow_html=True)
        st.markdown("#### 📋 Transfer Detail")
        tcols=['Store_Code','SKU_Code','SKU_Name','Brand','Category','Priority_Cat','Stock_Status','Coverage_%','Current_Stock','Target_Stock','DRR','Final_Transfer','Action_Required']
        tdf=results[results['Has_Transfer']=='Yes'][[c for c in tcols if c in results.columns]].copy()
        if len(tdf)>0:
            st.dataframe(tdf.sort_values(['Priority_Cat','Final_Transfer'],key=lambda x:x.map({'Critical':0,'High':1,'Medium':2,'Low':3}) if x.name=='Priority_Cat' else -x,ascending=[True,True]),use_container_width=True,height=400)
            st.download_button("📥 Download Transfer Plan",tdf.to_csv(index=False),f"transfer_{datetime.now().strftime('%Y%m%d')}.csv","text/csv")
        else: st.info("No transfers needed.")

    # ==================== TAB 4: CANNI & SUBS ====================
    with tab4:
        st.markdown("<h2 style='text-align:center;'>⚠️ Cannibalization & Substitution</h2>",unsafe_allow_html=True)
        st.markdown("---")
        if len(results)==0: st.info("No data."); st.stop()
        st.markdown("### 🔴 Cannibalization Analysis")
        st.info("💡 When competitor on promo → your sales drop. Loss = DRR × Effect% × Price")
        cdf=results[results['Has_Cannibalization']=='Yes']; tlq=cdf['Canni_Loss_Qty'].sum(); tlv=cdf['Canni_Loss_Value'].sum()
        ae=cdf['Max_Canni_Effect_%'].mean()*100 if len(cdf)>0 else 0
        c1,c2,c3,c4,c5=st.columns(5)
        with c1: st.markdown(create_colored_kpi("Affected",f"{len(cdf):,}","SKUs","⚠️",KPI_COLORS['danger']),unsafe_allow_html=True)
        with c2: st.markdown(create_colored_kpi("Loss Qty",fmt(tlq),"units/day","📉",KPI_COLORS['orange']),unsafe_allow_html=True)
        with c3: st.markdown(create_colored_kpi("Loss Value",fmt(tlv,"AED "),"per day","💸",KPI_COLORS['purple']),unsafe_allow_html=True)
        with c4: st.markdown(create_colored_kpi("Avg Effect",f"{ae:.1f}%","","📊",KPI_COLORS['warning']),unsafe_allow_html=True)
        with c5: st.markdown(create_colored_kpi("Multiplier",f"{cdf['Canni_Multiplier'].mean():.2f}" if len(cdf)>0 else "1.00","","🔢",KPI_COLORS['primary']),unsafe_allow_html=True)
        if len(cdf)>0:
            st.markdown("<br>",unsafe_allow_html=True)
            tcs=results.groupby('Category')['L30_Total_Value'].sum(); tbs=results.groupby('Brand')['L30_Total_Value'].sum()
            c1,c2=st.columns(2)
            with c1:
                st.markdown("##### 📂 Category Cannibalization")
                cc=results.groupby('Category').agg(SKUs=('SKU_Code','count'),Affected=('Has_Cannibalization',lambda x:(x=='Yes').sum()),Avg_Eff=('Max_Canni_Effect_%',lambda x:x[x>0].mean()*100 if (x>0).any() else 0),Loss_Qty=('Canni_Loss_Qty','sum'),Loss_AED=('Canni_Loss_Value','sum'))
                cc['Avg_Eff']=cc['Avg_Eff'].round(1); cc['Impact%']=(cc['Loss_AED']/(tcs/30).clip(lower=0.01)*100).round(2)
                st.dataframe(cc,use_container_width=True)
            with c2:
                st.markdown("##### 🏷️ Brand Cannibalization (Top 10)")
                cb=results.groupby('Brand').agg(SKUs=('SKU_Code','count'),Affected=('Has_Cannibalization',lambda x:(x=='Yes').sum()),Loss_Qty=('Canni_Loss_Qty','sum'),Loss_AED=('Canni_Loss_Value','sum'))
                cb['Impact%']=(cb['Loss_AED']/(tbs/30).clip(lower=0.01)*100).round(2); cb=cb[cb['Affected']>0].nlargest(10,'Loss_Qty')
                st.dataframe(cb,use_container_width=True)
            c1,c2,c3=st.columns(3)
            with c1:
                fig=go.Figure(data=[go.Bar(x=cc.index,y=cc['Loss_Qty'],marker=dict(color='#ef4444'),text=cc['Loss_Qty'].astype(int),textposition='auto',textfont=dict(color='#ffffff'))]); fig.update_layout(height=260,title=dict(text="Loss Qty",font=dict(color=CHART_TEXT,size=13))); st.plotly_chart(fig,use_container_width=True)
            with c2:
                fig=go.Figure(data=[go.Bar(x=cc.index,y=cc['Loss_AED'],marker=dict(color='#f97316'),text=cc['Loss_AED'].round(0).astype(int),textposition='auto',textfont=dict(color='#ffffff'))]); fig.update_layout(height=260,title=dict(text="Loss AED",font=dict(color=CHART_TEXT,size=13))); st.plotly_chart(fig,use_container_width=True)
            with c3:
                fig=go.Figure(data=[go.Bar(x=cc.index,y=cc['Impact%'],marker=dict(color='#8b5cf6'),text=cc['Impact%'].astype(str)+'%',textposition='auto',textfont=dict(color='#ffffff'))]); fig.update_layout(height=260,title=dict(text="Impact % of Sales",font=dict(color=CHART_TEXT,size=13))); st.plotly_chart(fig,use_container_width=True)
        else: st.success("✅ No significant cannibalization.")
        st.markdown("---")
        st.markdown("### 🟢 Substitution Opportunities")
        st.info("💡 When competitor OOS → your sales increase. Gain = DRR × Effect% × Price")
        sdf=results[results['Has_Substitution']=='Yes']; tgq=sdf['Subs_Gain_Qty'].sum(); tgv=sdf['Subs_Gain_Value'].sum()
        c1,c2,c3,c4,c5=st.columns(5)
        with c1: st.markdown(create_colored_kpi("Gaining",f"{len(sdf):,}","SKUs","✅",KPI_COLORS['success']),unsafe_allow_html=True)
        with c2: st.markdown(create_colored_kpi("Gain Qty",fmt(tgq),"units/day","📈",KPI_COLORS['teal']),unsafe_allow_html=True)
        with c3: st.markdown(create_colored_kpi("Gain Value",fmt(tgv,"AED "),"per day","💰",KPI_COLORS['purple']),unsafe_allow_html=True)
        with c4: st.markdown(create_colored_kpi("Avg Gain",f"{sdf['Max_Subs_Effect_%'].mean()*100:.1f}%" if len(sdf)>0 else "0%","","📊",KPI_COLORS['primary']),unsafe_allow_html=True)
        with c5: st.markdown(create_colored_kpi("Multiplier",f"{sdf['Subs_Multiplier'].mean():.2f}" if len(sdf)>0 else "1.00","","🔢",KPI_COLORS['warning']),unsafe_allow_html=True)
        if len(sdf)>0:
            st.markdown("<br>",unsafe_allow_html=True)
            c1,c2=st.columns(2)
            with c1:
                sc2=results.groupby('Category').agg(SKUs=('SKU_Code','count'),Gaining=('Has_Substitution',lambda x:(x=='Yes').sum()),Gain_Qty=('Subs_Gain_Qty','sum'),Gain_AED=('Subs_Gain_Value','sum'))
                st.markdown("##### 📂 Category Substitution"); st.dataframe(sc2,use_container_width=True)
            with c2:
                sb=results.groupby('Brand').agg(Gaining=('Has_Substitution',lambda x:(x=='Yes').sum()),Gain_Qty=('Subs_Gain_Qty','sum'),Gain_AED=('Subs_Gain_Value','sum'))
                sb=sb[sb['Gaining']>0].nlargest(10,'Gain_Qty')
                st.markdown("##### 🏷️ Brand Substitution (Top 10)"); st.dataframe(sb,use_container_width=True)
            c1,c2=st.columns(2)
            with c1:
                fig=go.Figure(data=[go.Bar(x=sc2.index,y=sc2['Gain_Qty'],marker=dict(color='#22c55e'),text=sc2['Gain_Qty'].astype(int),textposition='auto',textfont=dict(color='#ffffff'))]); fig.update_layout(height=260,title=dict(text="Gain Qty",font=dict(color=CHART_TEXT,size=13))); st.plotly_chart(fig,use_container_width=True)
            with c2:
                fig=go.Figure(data=[go.Bar(x=sc2.index,y=sc2['Gain_AED'],marker=dict(color='#10b981'),text=sc2['Gain_AED'].round(0).astype(int),textposition='auto',textfont=dict(color='#ffffff'))]); fig.update_layout(height=260,title=dict(text="Gain AED",font=dict(color=CHART_TEXT,size=13))); st.plotly_chart(fig,use_container_width=True)
        else: st.info("ℹ️ No significant substitution.")

    # ==================== TAB 5: TRENDS ====================
    with tab5:
        st.markdown("<h2 style='text-align:center;'>📈 Trends & Performance</h2>",unsafe_allow_html=True)
        st.markdown("---")
        if len(results)==0: st.info("No data."); st.stop()
        fs=results['Store_Code'].unique().tolist(); fk=results['SKU_Code'].unique().tolist()
        sf=sales_enhanced[(sales_enhanced['Store_Code'].isin(fs))&(sales_enhanced['SKU_Code'].isin(fk))].copy()
        if st.session_state.sku_master is not None:
            skm=st.session_state.sku_master.set_index('SKU_Code')[['Category','Brand']].to_dict('index')
            sf['Category']=sf['SKU_Code'].map(lambda x:skm.get(x,{}).get('Category','')); sf['Brand']=sf['SKU_Code'].map(lambda x:skm.get(x,{}).get('Brand',''))
            fc=results['Category'].unique().tolist(); fb=results['Brand'].unique().tolist()
            if fc: sf=sf[sf['Category'].isin(fc)]
            if fb: sf=sf[sf['Brand'].isin(fb)]
        c1,c2,c3,c4,c5=st.columns(5)
        with c1: st.markdown(create_colored_kpi("Surge",f"{len(results[results['Trend_Flag']=='Surge']):,}",">15%","🔥",KPI_COLORS['success']),unsafe_allow_html=True)
        with c2: st.markdown(create_colored_kpi("Growing",f"{len(results[results['Trend_Flag']=='Growing']):,}","5-15%","📈",KPI_COLORS['teal']),unsafe_allow_html=True)
        with c3: st.markdown(create_colored_kpi("Stable",f"{len(results[results['Trend_Flag']=='Stable']):,}","±5%","➡️",KPI_COLORS['warning']),unsafe_allow_html=True)
        with c4: st.markdown(create_colored_kpi("Declining",f"{len(results[results['Trend_Flag']=='Declining']):,}","-5~-15%","📉",KPI_COLORS['orange']),unsafe_allow_html=True)
        with c5: st.markdown(create_colored_kpi("Dropping",f"{len(results[results['Trend_Flag']=='Dropping']):,}","<-15%","⬇️",KPI_COLORS['danger']),unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        if len(sf)>0:
            daily=sf.groupby('Date').agg(CS=('Clean_Sales','sum'),SV=('Sales_Value','sum')).reset_index().sort_values('Date')
            l7a=daily[daily['Date']>=today_ts-pd.Timedelta(days=7)]['CS'].mean() if len(daily[daily['Date']>=today_ts-pd.Timedelta(days=7)])>0 else 0
            l30a=daily[daily['Date']>=today_ts-pd.Timedelta(days=30)]['CS'].mean() if len(daily[daily['Date']>=today_ts-pd.Timedelta(days=30)])>0 else 0
            gov=safe_div(l7a-l30a,l30a,0)*100
            st.markdown("#### 📈 Day-wise Sales (Filter Synced)")
            fig=go.Figure()
            fig.add_trace(go.Scatter(x=daily['Date'],y=daily['CS'],mode='lines+markers',name='Daily',line=dict(color='#FF6F00',width=2),marker=dict(size=4)))
            if l7a>0: fig.add_trace(go.Scatter(x=daily['Date'],y=[l7a]*len(daily),mode='lines',name=f'L7 ({l7a:,.0f})',line=dict(color='#22c55e',width=3,dash='dash')))
            if l30a>0: fig.add_trace(go.Scatter(x=daily['Date'],y=[l30a]*len(daily),mode='lines',name=f'L30 ({l30a:,.0f})',line=dict(color='#8b5cf6',width=3,dash='dot')))
            l7d=daily[daily['Date']>=today_ts-pd.Timedelta(days=7)]
            if len(l7d)>0: fig.add_trace(go.Scatter(x=l7d['Date'],y=l7d['CS'],mode='lines+markers',name='L7',line=dict(color='#22c55e',width=4),marker=dict(size=8)))
            gc='#22c55e' if gov>=0 else '#ef4444'
            fig.add_annotation(x=daily['Date'].max(),y=l7a,text=f"<b>{'+' if gov>=0 else ''}{gov:.1f}%</b>",showarrow=True,arrowhead=2,arrowcolor=gc,font=dict(size=13,color=gc),bgcolor='rgba(255,255,255,0.9)',borderpad=4)
            fig.update_layout(height=380,hovermode='x unified',legend=dict(orientation='h',y=1.02,xanchor='center',x=0.5,bgcolor='rgba(255,255,255,0.8)',font=dict(color=CHART_TEXT))); st.plotly_chart(fig,use_container_width=True)
            st.markdown("<br>",unsafe_allow_html=True)
            l30d=daily[daily['Date']>=today_ts-pd.Timedelta(days=30)].copy(); l30al=l30d['CS'].mean() if len(l30d)>0 else 0
            c1,c2=st.columns(2)
            with c1:
                st.markdown("#### 📈 L7 Day-wise")
                l7dy=daily[daily['Date']>=today_ts-pd.Timedelta(days=7)].copy()
                if len(l7dy)>0:
                    fig=go.Figure(); fig.add_trace(go.Bar(x=l7dy['Date'],y=l7dy['CS'],marker=dict(color='#FF6F00')))
                    fig.add_trace(go.Scatter(x=l7dy['Date'],y=[l7dy['CS'].mean()]*len(l7dy),mode='lines',name='Avg',line=dict(color='#2C1810',width=2,dash='dash')))
                    fig.update_layout(height=280,legend=dict(bgcolor='rgba(255,255,255,0.8)',font=dict(color=CHART_TEXT))); st.plotly_chart(fig,use_container_width=True)
                else: st.info("No L7 data.")
            with c2:
                st.markdown("#### 📈 L30 Day-wise")
                if len(l30d)>0:
                    fig=go.Figure(); fig.add_trace(go.Bar(x=l30d['Date'],y=l30d['CS'],marker=dict(color='#FF6F00')))
                    fig.add_trace(go.Scatter(x=l30d['Date'],y=[l30al]*len(l30d),mode='lines',name='Avg',line=dict(color='#2C1810',width=2,dash='dash')))
                    fig.update_layout(height=280,legend=dict(bgcolor='rgba(255,255,255,0.8)',font=dict(color=CHART_TEXT))); st.plotly_chart(fig,use_container_width=True)
                else: st.info("No L30 data.")
            st.markdown("<br>",unsafe_allow_html=True)
            c1,c2=st.columns(2)
            with c1:
                st.markdown("#### 📊 Growth Day-wise (L30)")
                if len(l30d)>0 and l30al>0:
                    l30d=l30d.copy(); l30d['G']=((l30d['CS']-l30al)/l30al*100).round(1)
                    fig=go.Figure(data=[go.Bar(x=l30d['Date'],y=l30d['G'],marker=dict(color=['#22c55e' if g>=0 else '#ef4444' for g in l30d['G']]),text=l30d['G'].apply(lambda x:f"{x:+.1f}%"),textposition='auto',textfont=dict(color='#ffffff',size=9))])
                    fig.add_hline(y=0,line_dash="dash",line_color="#8B7355"); fig.update_layout(height=280); st.plotly_chart(fig,use_container_width=True)
            with c2:
                st.markdown("#### 📊 Growth Week-wise (8 Weeks)")
                if 'Week_Start' in sf.columns:
                    wk=sf.groupby('Week_Start')['Clean_Sales'].sum().reset_index().sort_values('Week_Start').tail(9)
                    if len(wk)>=2:
                        wk['P']=wk['Clean_Sales'].shift(1); wk['G']=((wk['Clean_Sales']-wk['P'])/wk['P'].clip(lower=0.01)*100).round(1); wk=wk.dropna().tail(8)
                        wk['L']=wk['Week_Start'].dt.strftime('W%V\n%d %b')
                        fig=go.Figure(data=[go.Bar(x=wk['L'],y=wk['G'],marker=dict(color=['#22c55e' if g>=0 else '#ef4444' for g in wk['G']]),text=wk['G'].apply(lambda x:f"{x:+.1f}%"),textposition='auto',textfont=dict(color='#ffffff',size=11))])
                        fig.add_hline(y=0,line_dash="dash",line_color="#8B7355"); fig.update_layout(height=280); st.plotly_chart(fig,use_container_width=True)
            st.markdown("<br>",unsafe_allow_html=True)
            st.markdown("#### 📊 Week-wise Trend Status")
            if 'Week_Start' in sf.columns and len(sf)>0:
                ws=sf.groupby(['Week_Start','Store_Code','SKU_Code'])['Clean_Sales'].sum().reset_index().sort_values(['Store_Code','SKU_Code','Week_Start'])
                ws['P4']=ws.groupby(['Store_Code','SKU_Code'])['Clean_Sales'].transform(lambda x:x.shift(1).rolling(4,min_periods=1).mean())
                ws['WR']=(ws['Clean_Sales']/ws['P4'].clip(lower=0.01)).fillna(1)
                ws['WT']=ws['WR'].apply(lambda r:'Surge' if r>1.15 else ('Growing' if r>1.05 else ('Dropping' if r<0.85 else ('Declining' if r<0.95 else 'Stable'))))
                lw=sorted(ws['Week_Start'].unique())[-8:]; wsf=ws[ws['Week_Start'].isin(lw)]
                twc=wsf.groupby(['Week_Start','WT']).size().unstack(fill_value=0)
                wlb=[pd.Timestamp(w).strftime('%d %b') for w in twc.index]
                fig=go.Figure()
                for tf2,tc2 in zip(['Surge','Growing','Stable','Declining','Dropping'],['#22c55e','#10b981','#f59e0b','#f97316','#ef4444']):
                    if tf2 in twc.columns: fig.add_trace(go.Bar(name=tf2,x=wlb,y=twc[tf2].values,marker=dict(color=tc2)))
                fig.update_layout(barmode='stack',height=320,legend=dict(orientation='h',y=1.1,xanchor='center',x=0.5,bgcolor='rgba(255,255,255,0.8)',font=dict(color=CHART_TEXT))); st.plotly_chart(fig,use_container_width=True)
        else: st.info("No sales data for filters.")
        st.markdown("<br>",unsafe_allow_html=True)
        st.markdown("#### 📊 Growth Tables")
        c1,c2=st.columns(2)
        with c1:
            cg=results.groupby('Category').agg(L7=('L7_Total','sum'),L30=('L30_Total','sum'),L30V=('L30_Total_Value','sum')).reset_index()
            cg['L7D']=(cg['L7']/7).round(1); cg['L30D']=(cg['L30']/30).round(1); cg['Growth%']=((cg['L7D']-cg['L30D'])/cg['L30D'].clip(lower=0.01)*100).round(1)
            st.markdown("##### 📂 Category Growth"); st.dataframe(cg.set_index('Category'),use_container_width=True)
        with c2:
            bg=results.groupby('Brand').agg(L7=('L7_Total','sum'),L30=('L30_Total','sum')).reset_index()
            bg['L7D']=(bg['L7']/7).round(1); bg['L30D']=(bg['L30']/30).round(1); bg['Growth%']=((bg['L7D']-bg['L30D'])/bg['L30D'].clip(lower=0.01)*100).round(1)
            st.markdown("##### 🏷️ Brand Growth"); st.dataframe(bg.set_index('Brand').sort_values('Growth%',ascending=False),use_container_width=True)
        st.markdown("<br>",unsafe_allow_html=True)
        st.markdown("#### 📊 Category × Brand DRR Matrix (Top 10)")
        tb=results.groupby('Brand')['DRR'].sum().nlargest(10).index.tolist()
        if tb:
            mx=results[results['Brand'].isin(tb)].groupby(['Category','Brand']).agg(Wkday=('Avg_Weekday_Normal','mean'),Wkend=('Avg_Weekend_Normal','mean'),Promo=('Avg_Weekday_Promo','mean'),Outliers=('Outlier_Count_L60','sum'),Canni=('Max_Canni_Effect_%',lambda x:(x*100).mean()),Subs=('Max_Subs_Effect_%',lambda x:(x*100).mean()),DRR=('DRR','sum')).round(1)
            st.dataframe(mx,use_container_width=True)

    # ==================== TAB 6: WAREHOUSE ====================
    with tab6:
        st.markdown("<h2 style='text-align:center;'>🏪 Warehouse & Shortage</h2>",unsafe_allow_html=True)
        st.markdown("---")
        if len(results)==0: st.info("No data."); st.stop()
        c1,c2,c3,c4,c5,c6=st.columns(6)
        with c1: st.markdown(create_colored_kpi("WH Stock",fmt(results['Warehouse_Stock'].sum()),"units","🏭",KPI_COLORS['primary']),unsafe_allow_html=True)
        with c2: st.markdown(create_colored_kpi("Short SKUs",f"{len(results[results['WH_Shortage']=='Yes']):,}","","⚠️",KPI_COLORS['warning']),unsafe_allow_html=True)
        with c3: st.markdown(create_colored_kpi("OOS Risk",f"{len(results[results['WH_OOS_Risk']=='Yes']):,}","","🔴",KPI_COLORS['danger']),unsafe_allow_html=True)
        with c4: st.markdown(create_colored_kpi("Fulfill%",f"{results['WH_Fulfill_%'].mean()*100:.1f}%","","✅",KPI_COLORS['success']),unsafe_allow_html=True)
        with c5: st.markdown(create_colored_kpi("Short Qty",fmt(results['Shortage_Qty'].sum()),"units","📦",KPI_COLORS['orange']),unsafe_allow_html=True)
        with c6: st.markdown(create_colored_kpi("Short Value",fmt(results['Shortage_Value'].sum(),"AED "),"","💸",KPI_COLORS['purple']),unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        st.markdown("#### 📂 Shortage by Category")
        shc=results.groupby('Category').agg(SKUs=('SKU_Code','count'),Short_SKUs=('WH_Shortage',lambda x:(x=='Yes').sum()),Need=('Total_Need','sum'),WH=('Warehouse_Stock','sum'),Short_Qty=('Shortage_Qty','sum'),Short_AED=('Shortage_Value','sum'),Fulfill=('WH_Fulfill_%','mean'),DRR=('DRR','sum'))
        shc['Days']=(shc['Short_Qty']/shc['DRR'].clip(lower=0.01)).round(1); shc['Fulfill']=(shc['Fulfill']*100).round(1)
        st.dataframe(shc,use_container_width=True)
        st.markdown("<br>",unsafe_allow_html=True)
        st.markdown("#### 🏪 Shortage by Store")
        shs=results.groupby('Store_Code').agg(SKUs=('SKU_Code','count'),Short_SKUs=('WH_Shortage',lambda x:(x=='Yes').sum()),Short_Qty=('Shortage_Qty','sum'),Short_AED=('Shortage_Value','sum'),Fulfill=('WH_Fulfill_%','mean'))
        shs['Fulfill']=(shs['Fulfill']*100).round(1); st.dataframe(shs,use_container_width=True)
        st.markdown("<br>",unsafe_allow_html=True)
        st.markdown("#### 📦 Top 10 Shortage SKUs")
        tsh=results.nlargest(10,'Shortage_Qty')[['SKU_Code','SKU_Name','Category','Brand','Total_Need','Warehouse_Stock','Shortage_Qty','Shortage_Value','WH_Fulfill_%','DRR','Stock_Status']].copy()
        tsh['WH_Fulfill_%']=(tsh['WH_Fulfill_%']*100).round(1); st.dataframe(tsh,use_container_width=True)
        st.markdown("<br>",unsafe_allow_html=True)
        c1,c2,c3=st.columns(3)
        with c1:
            fig=go.Figure(data=[go.Bar(x=shc.index,y=shc['Short_Qty'],marker=dict(color='#ef4444'),text=shc['Short_Qty'].astype(int),textposition='auto',textfont=dict(color='#ffffff'))]); fig.update_layout(height=260,title=dict(text="Shortage by Cat",font=dict(color=CHART_TEXT,size=13))); st.plotly_chart(fig,use_container_width=True)
        with c2:
            fig=go.Figure(); fig.add_trace(go.Bar(name='WH',x=shc.index,y=shc['WH'],marker_color='#22c55e')); fig.add_trace(go.Bar(name='Need',x=shc.index,y=shc['Need'],marker_color='#ef4444'))
            fig.update_layout(barmode='group',height=260,legend=dict(orientation='h',y=1.1,bgcolor='rgba(255,255,255,0.8)',font=dict(color=CHART_TEXT)),title=dict(text="WH vs Need",font=dict(color=CHART_TEXT,size=13))); st.plotly_chart(fig,use_container_width=True)
        with c3:
            fig=go.Figure(data=[go.Bar(x=shs.index,y=shs['Fulfill'],marker=dict(color=shs['Fulfill'],colorscale='RdYlGn',cmin=0,cmax=100),text=shs['Fulfill'].astype(str)+'%',textposition='auto',textfont=dict(color='#000000',size=12))])
            fig.add_hline(y=100,line_dash="dash",line_color="#22c55e"); fig.update_layout(height=260,title=dict(text="Fulfill % by Store",font=dict(color=CHART_TEXT,size=13))); st.plotly_chart(fig,use_container_width=True)

    # ==================== TAB 7: OPPORTUNITY LOSS ====================
    with tab7:
        st.markdown("<h2 style='text-align:center;'>💰 Opportunity Loss</h2>",unsafe_allow_html=True)
        st.markdown("---")
        if len(results)==0: st.info("No data."); st.stop()
        st.info("💡 Revenue lost or at risk RIGHT NOW.")
        odf=results[results['Stock_Status']=='OOS']; olq=odf['DRR'].sum(); olv=(odf['DRR']*odf['Base_Price']).sum()
        cdf2=results[results['Stock_Status']=='Critical']; clq=(cdf2['DRR']*0.5).sum(); clv=(cdf2['DRR']*0.5*cdf2['Base_Price']).sum()
        ldf=results[results['Stock_Status']=='Low']; llq=(ldf['DRR']*0.2).sum(); llv=(ldf['DRR']*0.2*ldf['Base_Price']).sum()
        slq=results['Shortage_Qty'].sum(); slv=results['Shortage_Value'].sum()
        cnlq=results['Canni_Loss_Qty'].sum(); cnlv=results['Canni_Loss_Value'].sum()
        gdf=results[results['Is_Gap']==1].copy(); gdf['GDV']=gdf['DRR']*gdf['Base_Price']; glq=gdf['DRR'].sum(); glv=gdf['GDV'].sum()
        tl=olv+clv+slv+cnlv+glv
        c1,c2,c3,c4,c5,c6=st.columns(6)
        with c1: st.markdown(create_colored_kpi("TOTAL LOSS",fmt(tl,"AED "),"per day","💰",KPI_COLORS['danger_dark']),unsafe_allow_html=True)
        with c2: st.markdown(create_colored_kpi("OOS",fmt(olv,"AED "),f"{len(odf)} SKUs","🚫",KPI_COLORS['danger']),unsafe_allow_html=True)
        with c3: st.markdown(create_colored_kpi("Critical",fmt(clv,"AED "),f"{len(cdf2)} SKUs","🔴",KPI_COLORS['orange']),unsafe_allow_html=True)
        with c4: st.markdown(create_colored_kpi("Shortage",fmt(slv,"AED "),f"{len(results[results['Shortage_Qty']>0])} SKUs","⚠️",KPI_COLORS['warning']),unsafe_allow_html=True)
        with c5: st.markdown(create_colored_kpi("Canni",fmt(cnlv,"AED "),f"{len(results[results['Canni_Loss_Qty']>0])} SKUs","📉",KPI_COLORS['purple']),unsafe_allow_html=True)
        with c6: st.markdown(create_colored_kpi("Gap",fmt(glv,"AED "),f"{len(gdf)} SKUs","🔍",KPI_COLORS['primary']),unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        st.markdown("#### 📊 Loss Waterfall (AED/Day)")
        lv=[olv,clv,llv,slv,cnlv,glv]; wft=sum(lv)
        fig=go.Figure(go.Waterfall(name="Loss",orientation="v",measure=["relative"]*6+["total"],x=['OOS','Critical','Low','Shortage','Canni','Gap','TOTAL'],y=lv+[wft],text=[fmt(v,"AED ") for v in lv+[wft]],textposition="outside",textfont=dict(color=CHART_TEXT,size=11),connector={"line":{"color":"#8B7355"}},increasing={"marker":{"color":"#ef4444"}},totals={"marker":{"color":"#7f1d1d"}}))
        fig.update_layout(height=400,showlegend=False,waterfallgap=0.3); st.plotly_chart(fig,use_container_width=True)
        st.markdown("<br>",unsafe_allow_html=True)
        st.markdown("#### 📋 Loss Summary")
        ls=pd.DataFrame({'Probability':['100%','~50%','~20%','100%','100%','100%'],'SKUs':[len(odf),len(cdf2),len(ldf),len(results[results['Shortage_Qty']>0]),len(results[results['Canni_Loss_Qty']>0]),len(gdf)],'Qty/Day':[round(olq),round(clq),round(llq),round(slq),round(cnlq),round(glq)],'AED/Day':[round(olv),round(clv),round(llv),round(slv),round(cnlv),round(glv)],'AED/Month':[round(v*30) for v in [olv,clv,llv,slv,cnlv,glv]],'Action':['Transfer NOW','Prioritize','Monitor','Expedite WH','Review promos','List SKUs']},index=['OOS','Critical','Low','Shortage','Canni','Gap'])
        st.dataframe(ls,use_container_width=True)
        if len(odf)>0:
            st.markdown("<br>",unsafe_allow_html=True); st.markdown("#### 🚫 OOS SKUs - Active Loss")
            os=odf[['Store_Code','SKU_Code','SKU_Name','Category','Brand','DRR','Base_Price','Priority_Cat']].copy()
            os['Loss_AED/Day']=(os['DRR']*os['Base_Price']).round(1); os['Loss_AED/Month']=(os['Loss_AED/Day']*30).round(1)
            st.dataframe(os.sort_values('Loss_AED/Day',ascending=False),use_container_width=True,height=250)
        if len(gdf)>0:
            st.markdown("<br>",unsafe_allow_html=True); st.markdown("#### 🔍 Assortment Gaps")
            gs=gdf[['Store_Code','SKU_Code','SKU_Name','Category','Brand','DRR','Base_Price','GDV']].copy()
            gs.columns=['Store','SKU','Name','Category','Brand','DRR','Price','Daily_AED']; gs['Monthly_AED']=(gs['Daily_AED']*30).round(1)
            st.dataframe(gs.sort_values('Daily_AED',ascending=False),use_container_width=True,height=250)
        st.markdown("<br>",unsafe_allow_html=True); st.markdown("#### 📉 Dying SKUs")
        rc2=results.copy(); rc2['L7v60']=((rc2['L7_Total']/7)/rc2['L60_Avg'].clip(lower=0.01)*100).round(1)
        rc2['Dying']=rc2.apply(lambda r:'Dying' if r['L7v60']<=30 else ('Severe Decline' if r['L7v60']<=50 else ('At Risk' if r['Trend_Flag']=='Dropping' else 'Healthy')),axis=1)
        ddf=rc2[rc2['Dying']!='Healthy'][['Store_Code','SKU_Code','SKU_Name','Category','Brand','L7v60','Trend_Flag','Dying','DRR','L7_Avg','L30_Avg','L60_Avg','Stock_Status']].sort_values('L7v60')
        if len(ddf)>0:
            c1,c2,c3=st.columns(3)
            with c1: st.markdown(create_colored_kpi("Dying",str(len(ddf[ddf['Dying']=='Dying'])),"L7<30% L60","💀",KPI_COLORS['danger_dark']),unsafe_allow_html=True)
            with c2: st.markdown(create_colored_kpi("Severe",str(len(ddf[ddf['Dying']=='Severe Decline'])),"L7<50%","📉",KPI_COLORS['danger']),unsafe_allow_html=True)
            with c3: st.markdown(create_colored_kpi("At Risk",str(len(ddf[ddf['Dying']=='At Risk'])),"Dropping","⚠️",KPI_COLORS['warning']),unsafe_allow_html=True)
            st.markdown("<br>",unsafe_allow_html=True); st.dataframe(ddf,use_container_width=True,height=300)
        else: st.success("✅ No dying SKUs!")

    # ==================== TAB 8: DATA TABLE ====================
    with tab8:
        st.markdown("<h2 style='text-align:center;'>📋 Complete Data View</h2>",unsafe_allow_html=True)
        st.markdown("---")
        if len(results)==0: st.info("No data."); st.stop()
        cg={'Identifiers':['Store_Code','SKU_Code','SKU_Name','Brand','Category','Sub_Category'],'Stock':['Current_Stock','Target_Stock','Days_Of_Stock','Stock_Status','Coverage_%','Coverage_Category','DoS_Category','Is_OOS'],'Transfer':['Final_Transfer','Priority_Cat','Action_Required','Allocated_Qty','Transfer_Shortage_Qty','Transfer_Shortage_Value','Transfer_Urgency'],'Canni':['Has_Cannibalization','Max_Canni_Effect_%','Canni_Loss_Qty','Canni_Loss_Value','Best_Canni_Comp_SKU','Canni_Multiplier'],'Subs':['Has_Substitution','Max_Subs_Effect_%','Subs_Gain_Qty','Subs_Gain_Value','Best_Subs_Comp_SKU','Subs_Multiplier'],'Trends':['L7_Total','L30_Total','L7_Avg','L30_Avg','L60_Avg','Trend_Flag','Trend_Ratio','Outlier_Count_L60'],'ABC':['ABC_Class','ABC_Label','ABC_Multiplier','Store_Tier','Tier_Priority'],'Forecast':['Final_Base_Avg','DRR','Final_Min_Stock','Final_Ideal_Stock','Final_Max_Stock'],'Warehouse':['Warehouse_Stock','Total_Need','WH_Shortage','WH_Fulfill_%','Shortage_Qty','Shortage_Value'],'Promo':['Promo_Tomorrow','Promo_Price_Tomorrow','Promo_Discount_%'],'Averages':['Avg_Weekday_Normal','Avg_Weekend_Normal','Avg_Weekday_Promo','Avg_Weekend_Promo'],'Assortment':['Is_Listed','Is_Gap']}
        c1,c2=st.columns([1,3])
        with c1:
            sa=st.checkbox("Select All",value=False); sg=st.multiselect("Groups:",list(cg.keys()),default=['Identifiers','Stock','Transfer'])
        with c2: search=st.text_input("🔍 Search",placeholder="Search...")
        if sa: sel=results.columns.tolist()
        else:
            sel=[]
            for g in sg: sel.extend([c for c in cg[g] if c in results.columns])
            sel=list(dict.fromkeys(sel))
        dd=results.copy()
        if search:
            try: dd=dd[dd.astype(str).apply(lambda x:x.str.contains(search,case=False,na=False)).any(axis=1)]
            except: pass
        st.markdown(f"**Showing: {len(dd):,} rows × {len(sel)} columns**")
        if sel: st.dataframe(dd[sel],use_container_width=True,height=500)
        st.markdown("<br>",unsafe_allow_html=True)
        c1,c2,c3,c4=st.columns(4)
        with c1: st.download_button("📥 CSV",dd[sel].to_csv(index=False) if sel else "",f"data_{datetime.now().strftime('%Y%m%d')}.csv","text/csv",use_container_width=True)
        with c2:
            out=io.BytesIO()
            with pd.ExcelWriter(out,engine='openpyxl') as w:
                if sel: dd[sel].to_excel(w,index=False,sheet_name='Data')
            st.download_button("📥 Excel",out.getvalue(),f"data_{datetime.now().strftime('%Y%m%d')}.xlsx","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",use_container_width=True)
        with c3: st.download_button("📥 Full Data",results.to_csv(index=False),f"full_{datetime.now().strftime('%Y%m%d')}.csv","text/csv",use_container_width=True)
        with c4:
            if sales_enhanced is not None: st.download_button("📥 Sales",sales_enhanced.to_csv(index=False),f"sales_{datetime.now().strftime('%Y%m%d')}.csv","text/csv",use_container_width=True)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown(f"""
<div style='text-align:center; color:#8B7355; padding:15px; font-size:11px;'>
    🧡 Stock Transfer Dashboard v3.0<br>
    {f"Last Calculated: {st.session_state.calc_date}" if st.session_state.calc_date else ""}
</div>""",unsafe_allow_html=True)