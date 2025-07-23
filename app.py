# app.py
import streamlit as st
import pandas as pd
from datetime import datetime
#ch

st.set_page_config(page_title="Chatbot com Personalidade", layout="wide")

st.title("💬 Personalidade do Chatbot")

# Menu lateral para escolher o modo
modo = st.sidebar.radio("Escolha o modo:", ["📝 Preencher BFI-44", "🎛️ Definir facetas manualmente"])

# ----------------------------------------
# MODO 1: Preencher BFI-44
# ----------------------------------------
if modo == "📝 Preencher BFI-44" :
    st.header("📋 Questionário de Personalidade (BFI-44)")
    
    # Lista simplificada de itens do BFI-44 (adicione os 44 reais)
    itens_bfi = [
    {"id": 1, "texto": "É extrovertido, sociável."},
    {"id": 2, "texto": "Tende a encontrar falhas nos outros."},
    {"id": 3, "texto": "Faz as coisas com eficiência."},
    {"id": 4, "texto": "É ansioso, facilmente perturbado."},
    {"id": 5, "texto": "Tem uma imaginação ativa."},
    {"id": 6, "texto": "É reservado."},
    {"id": 7, "texto": "É prestativo e altruísta com os outros."},
    {"id": 8, "texto": "É descuidado."},
    {"id": 9, "texto": "Se sente relaxado, lida bem com o estresse."},
    {"id": 10, "texto": "Tem poucos interesses artísticos."},
    {"id": 11, "texto": "É falante."},
    {"id": 12, "texto": "É simpático e caloroso."},
    {"id": 13, "texto": "É confiável, faz o que promete."},
    {"id": 14, "texto": "Se enerva facilmente."},
    {"id": 15, "texto": "É original, tem ideias novas."},
    {"id": 16, "texto": "É reservado com estranhos."},
    {"id": 17, "texto": "É considerado com os sentimentos dos outros."},
    {"id": 18, "texto": "Faz as coisas de maneira descuidada."},
    {"id": 19, "texto": "É emocionalmente estável, não se perturba facilmente."},
    {"id": 20, "texto": "É inventivo."},
    {"id": 21, "texto": "Fala com entusiasmo."},
    {"id": 22, "texto": "Tem uma natureza firme."},
    {"id": 23, "texto": "Faz as coisas com eficiência."},
    {"id": 24, "texto": "Se preocupa muito."},
    {"id": 25, "texto": "Tem uma imaginação viva."},
    {"id": 26, "texto": "Tende a ser quieto."},
    {"id": 27, "texto": "É gentil e atencioso."},
    {"id": 28, "texto": "Prefere trabalho desorganizado."},
    {"id": 29, "texto": "Raramente se sente ansioso ou com medo."},
    {"id": 30, "texto": "Tem poucos interesses criativos."},
    {"id": 31, "texto": "É extrovertido, animado."},
    {"id": 32, "texto": "Ajuda os outros espontaneamente."},
    {"id": 33, "texto": "Tem senso de dever."},
    {"id": 34, "texto": "Fica chateado facilmente."},
    {"id": 35, "texto": "Valoriza experiências artísticas e estéticas."},
    {"id": 36, "texto": "É tímido e silencioso."},
    {"id": 37, "texto": "Sente compaixão com facilidade."},
    {"id": 38, "texto": "É desorganizado."},
    {"id": 39, "texto": "Raramente se sente deprimido ou triste."},
    {"id": 40, "texto": "Tem imaginação ativa."},
    {"id": 41, "texto": "É assertivo."},
    {"id": 42, "texto": "Tende a ser cético quanto às intenções dos outros."},
    {"id": 43, "texto": "Planeja com antecedência."},
    {"id": 44, "texto": "É emocionalmente vulnerável."}
]

    
    respostas = {}
    
    with st.form("bfi_form"):
        for item in itens_bfi:
            respostas[item["id"]] = st.radio(
                f"{item['id']}. {item['texto']}",
                [1, 2, 3, 4, 5],
                horizontal=True
            )
        
        submit = st.form_submit_button("Enviar respostas e salvar CSV")
    
    if submit:
        df_respostas = pd.DataFrame(list(respostas.items()), columns=["Item", "Resposta"])
        
        # Nome do arquivo baseado no timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"respostas_bfi_{timestamp}.csv"
        
        df_respostas.to_csv(nome_arquivo, index=False)
        st.success("✅ Respostas salvas com sucesso!")
        st.download_button("📥 Baixar CSV", data=df_respostas.to_csv(index=False), file_name=nome_arquivo, mime="text/csv")

# ----------------------------------------
# MODO 2: Definir manualmente as facetas
# ----------------------------------------
else:
    st.header("🎛️ Definir níveis das facetas manualmente")

    facetas = [
    {"nome": "Sociabilidade", "descricao": "Tendência a ser sociável, falante e buscar interação social."},
    {"nome": "Assertividade", "descricao": "Inclinação a tomar a liderança e expressar opiniões com confiança."},
    {"nome": "Nível de energia", "descricao": "Grau de entusiasmo, dinamismo e vigor nas ações cotidianas."},
    {"nome": "Cortesia", "descricao": "Tendência a ser educado, respeitoso e tratar os outros com consideração."},
    {"nome": "Altruísmo", "descricao": "Disposição para ajudar, mostrar empatia e se preocupar com os outros."},
    {"nome": "Organização", "descricao": "Capacidade de manter ordem, planejamento e estrutura nas atividades."},
    {"nome": "Disciplina", "descricao": "Determinação para seguir metas, regras e concluir tarefas com foco."},
    {"nome": "Ansiedade", "descricao": "Propensão a se preocupar, sentir tensão e reagir ao estresse."},
    {"nome": "Vulnerabilidade", "descricao": "Tendência a se sentir emocionalmente instável ou facilmente sobrecarregado."},
    {"nome": "Abertura à estética", "descricao": "Sensibilidade a arte, beleza e experiências sensoriais."},
    {"nome": "Imaginação", "descricao": "Capacidade criativa, fantasiosa e voltada à invenção de ideias."},
    {"nome": "Curiosidade intelectual", "descricao": "Desejo de aprender, explorar conceitos e buscar entendimento profundo."}
]

    niveis = {}
    with st.form("facetas_form"):
        for faceta in facetas:
            niveis[faceta] = st.selectbox(f"{faceta}:", ["Baixo", "Médio", "Alto"], help=faceta['descrição'])
        
        gerar_perfil = st.form_submit_button("Gerar perfil descritivo")

    if gerar_perfil:
        st.subheader("🧠 Perfil gerado com base nas facetas:")
        for faceta, nivel in niveis.items():
            st.markdown(f"**{faceta}**: {nivel}")

        # Aqui você pode gerar o texto que será usado como system prompt no chatbot
        perfil_texto = "Você é um chatbot com a seguinte personalidade:\n"
        for faceta, nivel in niveis.items():
            perfil_texto += f"- {faceta}: {nivel.lower()}.\n"

        st.text_area("🧾 Perfil para o prompt do chatbot:", perfil_texto, height=200)

