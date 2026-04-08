import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="🚛 Coleta Centro - Dashboard",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Função para carregar dados
@st.cache_data(ttl=300)  # Cache por 5 minutos
def load_data():
    try:
        # Tenta carregar dados de um arquivo local
        df = pd.read_excel("coleta_centro_dados.xlsx")
        # Garante que a coluna \'Mês\' exista e seja do tipo string
        if \'Mês\' not in df.columns:
            st.error("Erro: A planilha não contém a coluna \'Mês\'. Por favor, verifique o formato.")
            return pd.DataFrame() # Retorna DataFrame vazio para evitar erros subsequentes
        df[\'Mês\'] = df[\'Mês\'].astype(str)
        return df
    except FileNotFoundError:
        st.warning("Arquivo \'coleta_centro_dados.xlsx\' não encontrado. Criando dados de exemplo.")
        return create_sample_data()
    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar a planilha: {e}")
        return pd.DataFrame()

def create_sample_data():
    """Cria dados de exemplo para demonstração"""
    meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    data = {
        \'Mês\': meses,
        \'Coleta AM\': [295, 1021, 408, 1192, 1045, 0, 0, 0, 0, 0, 0, 0],
        \'Coleta PM\': [760, 1636, 793, 1606, 1461, 0, 0, 0, 0, 0, 0, 0],
        \'Total de Sacos\': [1055, 2657, 1201, 2798, 2506, 0, 0, 0, 0, 0, 0, 0]
    }
    return pd.DataFrame(data)

def create_trend_data():
    """Cria dados de tendência diária para demonstração (ano 2025)"""
    dates = pd.date_range(start=\'2025-01-01\', end=\'2025-05-31\', freq=\'D\') # Alterado para 2025
    np.random.seed(42)
    
    trend_data = []
    for date in dates:
        am_sacos = np.random.randint(8, 25)
        pm_sacos = np.random.randint(15, 35)
        peso_kg = (am_sacos + pm_sacos) * np.random.uniform(18, 22)
        
        trend_data.append({
            \'Data\': date,
            \'Sacos_AM\': am_sacos,
            \'Sacos_PM\': pm_sacos,
            \'Total_Sacos\': am_sacos + pm_sacos,
            \'Peso_Total_kg\': round(peso_kg, 1)
        })
    
    return pd.DataFrame(trend_data)

def format_number(num):
    """Formata números para exibição"""
    if num >= 1000:
        return f"{num/1000:.1f}k"
    return str(int(num))

def create_metric_card(title, value, delta=None, delta_color="normal"):
    """Cria um cartão de métrica personalizado"""
    if delta:
        st.metric(
            label=title,
            value=value,
            delta=delta,
            delta_color=delta_color
        )
    else:
        st.metric(label=title, value=value)

# Título principal
st.markdown("""
<div style=\'text-align: center; padding: 20px;\'>
    <h1 style=\'color: #00D4FF; font-size: 3em; margin-bottom: 10px;\'>
        🚛 Coleta Centro
    </h1>
    <p style=\'color: #888; font-size: 1.2em;\'>
        Dashboard de Gestão de Resíduos e Segurança
    </p>
</div>
""", unsafe_allow_html=True)

# Carregamento de dados
df = load_data()
trend_df = create_trend_data()

# Verifica se o DataFrame principal está vazio
if df.empty:
    st.info("Nenhum dado disponível para exibição. Por favor, carregue uma planilha ou verifique o arquivo \'coleta_centro_dados.xlsx\'.")
    st.stop() # Para a execução do script se não houver dados

# Sidebar para filtros
with st.sidebar:
    st.header("🔧 Filtros")
    
    # Upload de arquivo
    uploaded_file = st.file_uploader(
        "📁 Carregar nova planilha",
        type=[\'xlsx\', \'csv\'],
        help="Faça upload de uma nova planilha para atualizar os dados"
    )
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(\".xlsx\"):
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)
            st.success("✅ Dados atualizados com sucesso!")
            st.experimental_rerun() # Recarrega a página para aplicar os novos dados
        except Exception as e:
            st.error(f"❌ Erro ao carregar arquivo: {e}")
    
    # Filtro de mês
    meses_disponiveis = df[\'Mês\'].unique().tolist()
    mes_selecionado = st.selectbox(
        "📅 Selecione o mês:",
        meses_disponiveis,
        index=0
    )
    
    # Filtro de período para tendência
    st.subheader("📊 Análise de Tendência")
    periodo_inicio = st.date_input(
        "Data início",
        value=trend_df[\'Data\'].min(),
        min_value=trend_df[\'Data\'].min(),
        max_value=trend_df[\'Data\'].max()
    )
    periodo_fim = st.date_input(
        "Data fim",
        value=trend_df[\'Data\'].max(),
        min_value=trend_df[\'Data\'].min(),
        max_value=trend_df[\'Data\'].max()
    )

# Filtrar dados
df_filtrado = df[df[\'Mês\'] == mes_selecionado]
trend_filtrado = trend_df[
    (trend_df[\'Data\'] >= pd.to_datetime(periodo_inicio)) &
    (trend_df[\'Data\'] <= pd.to_datetime(periodo_fim))
]

# Calcular métricas
if not df_filtrado.empty:
    total_sacos = df_filtrado[\'Total de Sacos\'].iloc[0]
    coleta_am = df_filtrado[\'Coleta AM\'].iloc[0]
    coleta_pm = df_filtrado[\'Coleta PM\'].iloc[0]
    peso_total = total_sacos * 20  # Estimativa de 20kg por saco
    
    # Calcular variação (simulada)
    variacao_sacos = np.random.randint(-15, 25)
    variacao_peso = np.random.randint(-10, 30)
else:
    total_sacos = coleta_am = coleta_pm = peso_total = 0
    variacao_sacos = variacao_peso = 0

# Layout principal
col1, col2, col3, col4 = st.columns(4)

with col1:
    create_metric_card(
        "🗑️ Total de Sacos",
        format_number(total_sacos),
        f"{variacao_sacos:+d}",
        "normal" if variacao_sacos >= 0 else "inverse"
    )

with col2:
    create_metric_card(
        "⚖️ Peso Total",
        f"{peso_total/1000:.1f} ton",
        f"{variacao_peso:+d}%",
        "normal" if variacao_peso >= 0 else "inverse"
    )

with col3:
    create_metric_card(
        "🌅 Coleta AM",
        format_number(coleta_am),
        f"{(coleta_am/total_sacos*100):.1f}%" if total_sacos > 0 else "0%"
    )

with col4:
    create_metric_card(
        "🌆 Coleta PM",
        format_number(coleta_pm),
        f"{(coleta_pm/total_sacos*100):.1f}%" if total_sacos > 0 else "0%"
    )

st.markdown("---")

# Gráficos principais
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Coleta por Período do Dia")
    if not df_filtrado.empty:
        fig_bar = go.Figure()
        
        fig_bar.add_trace(go.Bar(
            name=\'Manhã (AM)\',
            x=[\'Coleta\'],
            y=[coleta_am],
            marker_color=\'#00D4FF\',
            text=[f\'{coleta_am}\'
            textposition=\'auto\',
        ))
        
        fig_bar.add_trace(go.Bar(
            name=\'Tarde (PM)\',
            x=[\'Coleta\'],
            y=[coleta_pm],
            marker_color=\'#FF6B35\',
            text=[f\'{coleta_pm}\'
            textposition=\'auto\',
        ))
        
        fig_bar.update_layout(
            template="plotly_dark",
            plot_bgcolor=\'rgba(0,0,0,0)\',
            paper_bgcolor=\'rgba(0,0,0,0)\',
            showlegend=True,
            height=400,
            xaxis_title="Período",
            yaxis_title="Quantidade de Sacos",
            font=dict(color=\'white\')
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.subheader("🥧 Distribuição AM vs PM")
    if total_sacos > 0:
        fig_pie = go.Figure(data=[go.Pie(
            labels=[\'Manhã (AM)\', \'Tarde (PM)\\'],
            values=[coleta_am, coleta_pm],
            hole=0.4,
            marker_colors=[\'#00D4FF\', \'#FF6B35\'],
            textinfo=\'label+percent+value\',
            textfont_size=12,
        )])
        
        fig_pie.update_layout(
            template="plotly_dark",
            plot_bgcolor=\'rgba(0,0,0,0)\',
            paper_bgcolor=\'rgba(0,0,0,0)\',
            height=400,
            font=dict(color=\'white\'),
            showlegend=False
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)

# Gráfico de tendência
st.subheader("📈 Tendência de Coleta ao Longo do Tempo")
if not trend_filtrado.empty:
    fig_trend = go.Figure()
    
    fig_trend.add_trace(go.Scatter(
        x=trend_filtrado[\'Data\'],
        y=trend_filtrado[\'Total_Sacos\'],
        mode=\'lines+markers\',
        name=\'Total de Sacos\',
        line=dict(color=\'#00D4FF\', width=3),
        marker=dict(size=6, color=\'#00D4FF\')
    ))
    
    fig_trend.add_trace(go.Scatter(
        x=trend_filtrado[\'Data\'],
        y=trend_filtrado[\'Peso_Total_kg\']/10,  # Escala para visualização
        mode=\'lines+markers\',
        name=\'Peso Total (kg/10)\',
        line=dict(color=\'#FF6B35\', width=3),
        marker=dict(size=6, color=\'#FF6B35\'),
        yaxis=\'y2\'
    ))
    
    fig_trend.update_layout(
        template="plotly_dark",
        plot_bgcolor=\'rgba(0,0,0,0)\',
        paper_bgcolor=\'rgba(0,0,0,0)\',
        height=400,
        xaxis_title="Data",
        yaxis_title="Quantidade de Sacos",
        yaxis2=dict(
            title="Peso (kg/10)",
            overlaying=\'y\',
            side=\'right\'
        ),
        font=dict(color=\'white\'),
        hovermode=\'x unified\'
    )
    
    st.plotly_chart(fig_trend, use_container_width=True)

# Seção de análise mensal
st.markdown("---")
st.subheader("📋 Análise Mensal Completa")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Coleta por Mês")
    fig_monthly = px.bar(
        df,
        x=\'Mês\',
        y=[\'Coleta AM\', \'Coleta PM\'],
        title="Coleta Mensal por Período",
        color_discrete_map={
            \'Coleta AM\': \'#00D4FF\',
            \'Coleta PM\': \'#FF6B35\'
        },
        template="plotly_dark"
    )
    
    fig_monthly.update_layout(
        plot_bgcolor=\'rgba(0,0,0,0)\',
        paper_bgcolor=\'rgba(0,0,0,0)\',
        height=400,
        font=dict(color=\'white\')
    )
    
    st.plotly_chart(fig_monthly, use_container_width=True)

with col2:
    st.subheader("📈 Evolução do Total")
    fig_evolution = px.line(
        df,
        x=\'Mês\',
        y=\'Total de Sacos\',
        title="Evolução Mensal da Coleta",
        markers=True,
        color_discrete_sequence=[\'#00D4FF\'],
        template="plotly_dark"
    )
    
    fig_evolution.update_layout(
        plot_bgcolor=\'rgba(0,0,0,0)\',
        paper_bgcolor=\'rgba(0,0,0,0)\',
        height=400,
        font=dict(color=\'white\')
    )
    
    st.plotly_chart(fig_evolution, use_container_width=True)

# Tabela de dados
st.markdown("---")
st.subheader("📋 Dados Detalhados")
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# Footer
st.markdown("---")
st.markdown("""
<div style=\'text-align: center; color: #666; padding: 20px;\'>
    <p>🚛 Dashboard de Coleta Centro | Atualizado automaticamente</p>
    <p>💡 Para atualizar os dados, use o upload na barra lateral</p>
</div>
""", unsafe_allow_html=True)



