#
# Name: dashboard.py
# Version: 1.0.0
# License: MIT (ou a licença que preferir)
# Usage:
#   1. Certifique-se de que 'dados.csv' e 'codebook.csv' estão na mesma pasta.
#   2. Instale as dependências: pip install pandas panel
#   3. Execute: python dashboard.py
#

import pandas as pd
import panel as pn
import random
import os
import re

pn.extension()

CSS_STYLE = """
<style>
body {
    background-color: #f0f4f8; 
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #333;
}
.card-container {
    display: flex;
    flex-wrap: wrap;
    gap: 24px;
    padding: 24px;
}
.info-box {
    background-color: #ffffff;
    border: 1px solid #d6e0eb;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    padding: 24px;
    flex: 1 1 320px; 
    min-width: 320px;
    max-width: 480px;
}
.info-box h2 {
    font-size: 1.6rem;
    font-weight: 600;
    margin-top: 0;
    margin-bottom: 20px;
    color: #004a99; 
}
.info-box .overall-stat {
    font-size: 1.1rem;
    font-weight: 500;
    color: #212529;
    margin-bottom: 24px;
    border-left: 4px solid #0056b3; 
    padding-left: 12px;
}
.info-box .breakdown-list {
    list-style: none;
    padding: 0;
    margin: 0 0 20px 0;
}
.info-box .breakdown-list li {
    padding: 12px 0;
    border-bottom: 1px solid #e9ecef;
}
.info-box .breakdown-list li:last-child {
    border-bottom: none;
}
.info-box .factor-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}
.info-box .factor-name {
    font-size: 0.95rem;
    color: #495057;
    overflow: hidden;
    text-overflow: ellipsis;
    padding-right: 10px;
}
.info-box .factor-percent {
    font-size: 0.95rem;
    font-weight: 600;
    color: #004a99;
    white-space: nowrap;
}
.info-box .progress-bar-container {
    width: 100%;
    background-color: #e9ecef;
    border-radius: 4px;
    height: 8px;
    overflow: hidden;
}
.info-box .progress-bar {
    height: 100%;
    background-color: #0056b3;
    border-radius: 4px;
    transition: width 0.3s ease-in-out;
}
.info-box .summary-text {
    font-size: 0.9rem;
    color: #6c757d;
    line-height: 1.6;
    padding-top: 15px;
    border-top: 1px solid #e9ecef;
    margin-top: 15px;
}
</style>
"""

def load_codebook(filename="codebook.csv"):
    """Carrega o codebook e cria um mapa de (categoria, fator) -> descrição."""
    codebook_map = {}
    try:
        try:
            df_codebook = pd.read_csv(filename, sep=';', encoding='utf-8')
        except UnicodeDecodeError:
            df_codebook = pd.read_csv(filename, sep=';', encoding='latin1')
            
        for _, row in df_codebook.iterrows():
            cat = row.get('category')
            fact = row.get('factor')
            desc = row.get('description')
            
            if pd.notna(cat) and pd.notna(fact) and pd.notna(desc):
                cat_clean = str(cat).replace('\r\n', ' ').replace('\n', ' ').strip().strip('"').strip()
                fact_clean = str(fact).replace('\r\n', ' ').replace('\n', ' ').strip().strip('"').strip()
                desc_clean = str(desc).replace('\r\n', ' ').replace('\n', ' ').strip().strip('"').strip()
                
                codebook_map[(cat_clean, fact_clean)] = desc_clean
                
    except FileNotFoundError:
        print(f"Ficheiro do codebook '{filename}' não encontrado.")
    except Exception as e:
        print(f"Erro ao ler o codebook: {e}")
        
    return codebook_map

def load_and_process_data(filename="dados.csv"):
    """Carrega e processa o CSV, dividindo a coluna 'label'."""
    try:
        try:
            df = pd.read_csv(filename, sep=';', encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(filename, sep=';', encoding='latin1')
            
    except FileNotFoundError:
        print("Ficheiro CSV 'dados.csv' não encontrado.")
        return pd.DataFrame(columns=["id", "setor", "categoria", "fator", "response_id"])
    except Exception as e:
        print(f"Erro ao ler o CSV: {e}")
        return pd.DataFrame(columns=["id", "setor", "categoria", "fator", "response_id"])

    if 'label' not in df.columns or 'response_id' not in df.columns:
        print("Erro: Coluna 'label' ou 'response_id' não encontrada.")
        return pd.DataFrame(columns=["id", "setor", "categoria", "fator", "response_id"])

    df = df.dropna(subset=['label', 'response_id'])
    df = df[df['label'].str.upper() != 'NC']
    df[['categoria', 'fator']] = df['label'].astype(str).str.split('-', n=1, expand=True)
    
    if 'categoria' in df.columns:
        df['categoria'] = df['categoria'].str.replace(r'[\r\n]+', ' ', regex=True).str.strip().str.strip('"').str.strip()
    if 'fator' in df.columns:
        df['fator'] = df['fator'].str.replace(r'[\r\n]+', ' ', regex=True).str.strip().str.strip('"').str.strip()
    
    df = df.dropna(subset=['categoria', 'fator', 'setor'])
    
    return df

def get_summary_stats(category, percents, total_cat_respondents, codebook_map):
    """Gera o texto de resumo e a estatística principal."""
    if percents.empty:
        return "Sem dados", "Nenhuma resposta registada para esta categoria."

    most_common_fator = percents.idxmax()
    most_common_percent = percents.max()

    overall_stat = f"<strong>{percents.get(most_common_fator, 0):.0f}%</strong> mencionaram '{most_common_fator}'."
    summary_text = f"De <strong>{total_cat_respondents}</strong> respondentes nesta categoria, a resposta mais frequente foi '{most_common_fator}' ({most_common_percent:.0f}%)."
    
    description = codebook_map.get((category, most_common_fator), "")
    
    if description:
        description = description.strip().strip('"')
        if len(description) > 0:
            description_formatted = description[0].lower() + description[1:]
        else:
            description_formatted = ""
        summary_text += f" Isso pode indicar um foco em: {description_formatted}."

    return overall_stat, summary_text

df_full = load_and_process_data()
codebook_map = load_codebook()

if not df_full.empty:
    setor_options = ['Todos'] + sorted(df_full['setor'].unique().tolist())
else:
    setor_options = ['Todos']
    
setor_widget = pn.widgets.Select(name='Filtrar por Setor', options=setor_options, value='Todos')

reload_button = pn.widgets.Button(name='Recarregar Dados', button_type='primary', icon='refresh')

def reload_data(event):
    """Chamado quando o botão Recarregar Dados é clicado."""
    global df_full, codebook_map
    print("Recarregando dados...")
    
    df_full = load_and_process_data()
    codebook_map = load_codebook()
    
    if not df_full.empty:
        setor_options = ['Todos'] + sorted(df_full['setor'].unique().tolist())
    else:
        setor_options = ['Todos']
    
    old_value = setor_widget.value
    setor_widget.options = setor_options
    
    if old_value in setor_options:
        setor_widget.value = old_value
    else:
        setor_widget.value = 'Todos'
    
    print("Dados recarregados e filtros atualizados.")

reload_button.on_click(reload_data)


@pn.depends(setor=setor_widget.param.value)
def display_boxes(setor):
    """
    Função reativa que redesenha os boxes com base no filtro.
    """
    if df_full.empty:
        return pn.pane.Markdown("### Erro ao carregar os dados. Verifique o ficheiro 'dados.csv'.")
    
    if setor == 'Todos':
        dff = df_full.copy()
    else:
        dff = df_full[df_full['setor'] == setor].copy()
    
    total_respondents = dff['response_id'].nunique()
    
    if total_respondents == 0:
        return pn.pane.Markdown("### Nenhum dado encontrado para este filtro.")
    
    header = pn.pane.Markdown(f"### Mostrando resultados para: {setor} ({total_respondents} respondentes únicos)",
                               margin=(0, 0, 10, 24))
    
    all_boxes_html = []
    categories = sorted(dff['categoria'].unique())
    
    for cat in categories:
        cat_df = dff[dff['categoria'] == cat]
        
        total_cat_respondents = cat_df['response_id'].nunique()
        
        if total_cat_respondents == 0:
            continue
            
        counts = cat_df['fator'].value_counts()
        percents = (counts / counts.sum()) * 100
        
        overall, summary = get_summary_stats(cat, percents, total_cat_respondents, codebook_map)
        
        percents_main = percents[percents >= 5]
        percent_outros = percents[percents < 5].sum()
        
        percents_display = percents_main.copy() 
        if percent_outros > 0:
            percents_display['Outros'] = percent_outros
        
        breakdown_html = "<ul class='breakdown-list'>"
        for fator, percent in percents_display.sort_values(ascending=False).items():
            breakdown_html += f"""
            <li>
                <div class="factor-info">
                    <span class="factor-name" title="{fator}">{fator}</span>
                    <strong class="factor-percent">{percent:.1f}%</strong>
                </div>
                <div class="progress-bar-container">
                    <div class="progress-bar" style="width: {percent:.1f}%;"></div>
                </div>
            </li>
            """
        breakdown_html += "</ul>"
        
        box_html = f"""
        <div class='info-box'>
            <h2>{cat}</h2>
            <p class='overall-stat'>{overall}</p>
            {breakdown_html}
            <p class='summary-text'>{summary}</p>
        </div>
        """
        all_boxes_html.append(box_html)
    
    return pn.Column(
        header,
        pn.pane.HTML(f"<div class='card-container'>{''.join(all_boxes_html)}</div>")
    )

pn.config.raw_css.append(CSS_STYLE)

template = pn.template.FastListTemplate(
    title="Pesquisa Varinha Mágica",
    sidebar=[pn.Column("## Filtros", setor_widget, pn.layout.Spacer(height=20), reload_button)], 
    main=[display_boxes], 
    accent_base_color="#004a99", 
    header_background="#004a99",
)

print("Iniciando o servidor... Pressione CTRL+C para parar.")
print("Acesse seu dashboard no navegador em: http://localhost:5006")
pn.serve(template, port=5006, show=True)

