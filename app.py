import streamlit as st
import openai
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Chatbot com Personalidade", layout="wide")

st.title("💬 Personalidade do Chatbot")

# Inicializa o estado da sessão para controle de acesso e API
if 'api_client_ready' not in st.session_state:
    st.session_state['api_client_ready'] = False
if 'api_source' not in st.session_state:
    st.session_state['api_source'] = "None"

st.sidebar.title("Configuração da API") # Mudança de "Acesso ao Aplicativo" para "Configuração da API"

# INSERIR A PRÓPRIA API
with st.sidebar.expander("Insira Sua Chave de API da OpenAI"): # Nome do expander ajustado
    user_api_key = st.text_input("Sua Chave de API:", type="password", key="user_api_key_input").strip()
    if st.button("Configurar API", key="configure_user_api"):
        if user_api_key:
            try:
                st.session_state.client = openai.OpenAI(api_key=user_api_key)
                # Testar a chave com uma chamada simples 
                st.session_state.client.models.list()
                st.success("Chave de API configurada com sucesso!")
                st.session_state['api_client_ready'] = True
                st.session_state['api_source'] = "Usuário"
            except Exception as e:
                st.error(f"Erro ao configurar a chave de API: {e}. Verifique se a chave é válida.")
                st.session_state['api_client_ready'] = False
        else:
            st.warning("Por favor, insira sua chave de API.")
            st.session_state['api_client_ready'] = False

st.sidebar.markdown(f"Status da API: **{st.session_state.get('api_source', 'Não Configurada')}**") # Texto de status ajustado

# Somente carrega o restante do aplicativo se a API estiver pronta
if not st.session_state['api_client_ready']:
    st.info("Por favor, configure sua chave de API da OpenAI na barra lateral para usar o aplicativo.")
    st.stop() # Impede a execução do restante do script

# Menu lateral
modo = st.sidebar.radio("Escolha o modo:", ["📝 Preencher BFI-44", "🎛️ Definir facetas manualmente", "🤖 Chatbot"])

# ----------------------------------------
# MODO 1: Preencher BFI-44 - ainda não está pronto. A ideia é gerar uma descrição verbal de facetas.
# ----------------------------------------
if modo == "📝 Preencher BFI-44" :
    st.header("📋 Questionário de Personalidade (BFI-44)")
    
    # Lista simplificada de itens do BFI-44 - a ser revisada
    items_bfi = [
    {"id": 1, "text": "É extrovertido, sociável."},
    {"id": 2, "text": "Tende a encontrar falhas nos outros."},
    {"id": 3, "text": "Faz as coisas com eficiência."},
    {"id": 4, "text": "É ansioso, facilmente perturbado."},
    {"id": 5, "text": "Tem uma imaginação ativa."},
    {"id": 6, "text": "É reservado."},
    {"id": 7, "text": "É prestativo e altruísta com os outros."},
    {"id": 8, "text": "É descuidado."},
    {"id": 9, "text": "Se sente relaxado, lida bem com o estresse."},
    {"id": 10, "text": "Tem poucos interesses artísticos."},
    {"id": 11, "text": "É falante."},
    {"id": 12, "text": "É simpático e caloroso."},
    {"id": 13, "text": "É confiável, faz o que promete."},
    {"id": 14, "text": "Se enerva facilmente."},
    {"id": 15, "text": "É original, tem ideias novas."},
    {"id": 16, "text": "É reservado com estranhos."},
    {"id": 17, "text": "É considerado com os sentimentos dos outros."},
    {"id": 18, "text": "Faz as coisas de maneira descuidada."},
    {"id": 19, "text": "É emocionalmente estável, não se perturba facilmente."},
    {"id": 20, "text": "É inventivo."},
    {"id": 21, "text": "Fala com entusiasmo."},
    {"id": 22, "text": "Tem uma natureza firme."},
    {"id": 23, "text": "Faz as coisas com eficiência."},
    {"id": 24, "text": "Se preocupa muito."},
    {"id": 25, "text": "Tem uma imaginação viva."},
    {"id": 26, "text": "Tende a ser quieto."},
    {"id": 27, "text": "É gentil e atencioso."},
    {"id": 28, "text": "Prefere trabalho desorganizado."},
    {"id": 29, "text": "Raramente se sente ansioso ou com medo."},
    {"id": 30, "text": "Tem poucos interesses criativos."},
    {"id": 31, "text": "É extrovertido, animado."},
    {"id": 32, "text": "Ajuda os outros espontaneamente."},
    {"id": 33, "text": "Tem senso de dever."},
    {"id": 34, "text": "Fica chateado facilmente."},
    {"id": 35, "text": "Valoriza experiências artísticas e estéticas."},
    {"id": 36, "text": "É tímido e silencioso."},
    {"id": 37, "text": "Sente compaixão com facilidade."},
    {"id": 38, "text": "É desorganizado."},
    {"id": 39, "text": "Raramente se sente deprimido ou triste."},
    {"id": 40, "text": "Tem imaginação ativa."},
    {"id": 41, "text": "É assertivo."},
    {"id": 42, "text": "Tende a ser cético quanto às intenções dos outros."},
    {"id": 43, "text": "Planeja com antecedência."},
    {"id": 44, "text": "É emocionalmente vulnerável."}
]

    
    responses = {}
    
    with st.form("bfi_form"):
        for item in items_bfi:
            responses[item["id"]] = st.radio(
                f"{item['id']}. {item['text']}",
                [1, 2, 3, 4, 5],
                horizontal=True
            )
        
        submit = st.form_submit_button("Enviar respostas e salvar CSV")
    
    if submit:
        df_responses = pd.DataFrame(list(responses.items()), columns=["Item", "Resposta"])
        
        # Nome do arquivo baseado no timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"responses_bfi_{timestamp}.csv"
        
        df_responses.to_csv(filename, index=False)
        st.success("✅ Respostas salvas com sucesso!")
        st.download_button("📥 Baixar CSV", data=df_responses.to_csv(index=False), file_name=filename, mime="text/csv")

# ----------------------------------------
# MODO 2: Definir manualmente as facetas - não estão todas!
# ----------------------------------------
elif modo == "🎛️ Definir facetas manualmente":
    st.header("🎛️ Definir níveis das facetas manualmente")


    facets = [
        {"name": "Sociabilidade", "description": "Tendência a ser sociável, falante e buscar interação social."},
        {"name": "Assertividade", "description": "Inclinação a tomar a liderança e expressar opiniões com confiança."},
        {"name": "Nível de energia", "description": "Grau de entusiasmo, dinamismo e vigor nas ações cotidianas."},
        {"name": "Cortesia", "description": "Tendência a ser educado, respeitoso e tratar os outros com consideração."},
        {"name": "Altruísmo", "description": "Disposição para ajudar, mostrar empatia e se preocupar com os outros."},
        {"name": "Organização", "description": "Capacidade de manter ordem, planejamento e estrutura nas atividades."},
        {"name": "Disciplina", "description": "Determinação para seguir metas, regras e concluir tarefas com foco."},
        {"name": "Ansiedade", "description": "Propensão a se preocupar, sentir tensão e reagir ao estresse."},
        {"name": "Vulnerabilidade", "description": "Tendência a se sentir emocionalmente instável ou facilmente sobrecarregado."},
        {"name": "Abertura à estética", "description": "Sensibilidade a arte, beleza e experiências sensoriais."},
        {"name": "Imaginação", "description": "Capacidade criativa, fantasiosa e voltada à invenção de ideias."},
        {"name": "Curiosidade intelectual", "description": "Desejo de aprender, explorar conceitos e buscar entendimento profundo."}
    ]

    levels = {}
    with st.form("facets_form"):
        for facets_info in facets:
            facetname = facets_info["name"]
            description_facets = facets_info["description"]
            
            levels[facetname] = st.selectbox(f"{facetname}:", ["Baixo", "Médio", "Alto"], help=description_facets)
        
        gerar_perfil = st.form_submit_button("Gerar perfil descritivo")

    if gerar_perfil:
        st.subheader("🧠 Perfil gerado com base nas facetas:")
        for faceta, level in levels.items():
            st.markdown(f"**{faceta}**: {level}")

        # Aqui é onde a mudança acontece para incluir as descrições
        #text_profile = "Você é um chatbot com a seguinte personalidade:\n"
        text_profile = "Você simulará ser uma pessoa com a seguinte personalidade:\n"
        for facets_info in facets:
            facetname = facets_info["name"]
            description_facets = facets_info["description"]
            level = levels[facetname] 
            
            text_profile += f"- **{facetname}** ({description_facets}): {level.lower()}.\n"
            
        st.session_state.text_profile = text_profile  
        st.text_area("🧾 Perfil para o prompt do chatbot:", text_profile, height=300)       

# ----------------------------------------
# MODO 3: Chatbot com personalidade - só funciona se definir as facetas
# ----------------------------------------

elif modo == "🤖 Chatbot":
    
    st.header("Chatbot Personality", help=st.session_state.text_profile)
    #st.button("Ver perfil do chatbot", help=st.session_state.text_profile)

        
    # Comentei por ter retirado o secrets.toml
    #if "client" not in st.session_state:
    #    st.session_state.client = openai.OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

    if "openai_model" not in st.session_state:
        st.session_state['openai_model'] = "gpt-4o-mini"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Exibe mensagens anteriores
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    # Captura a entrada do usuário
    if prompt := st.chat_input("Escreva aqui"):
        # Adiciona a mensagem do usuário ao histórico e exibe
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message(name="user"):
            st.markdown(prompt)
        
        # Prepara a mensagem para o assistente
        with st.chat_message(name="assistant", avatar="🤖"):
            message_placeholder = st.empty()
            full_response = ""
            messages_for_api = []
            

            if 'text_profile' in st.session_state and st.session_state.text_profile:
                messages_for_api.append({"role": "system", "content": st.session_state.text_profile})


            # Adiciona as mensagens do histórico do chat
            for m in st.session_state.messages:
                messages_for_api.append({'role': m['role'], 'content': m["content"]})
            
            # Faz a chamada à API
            try:
                for chunk in st.session_state.client.chat.completions.create(
                    model=st.session_state['openai_model'],
                    messages=messages_for_api, # mensagens com o system prompt
                    stream=True,
                ):
                    full_response += chunk.choices[0].delta.content or ""
                    message_placeholder.markdown(full_response + "|") 
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({'role': 'assistant', 'content': full_response})
            except Exception as e:
                st.error(f"Ocorreu um erro ao chamar a API: {e}")
                st.session_state.messages.append({'role': 'assistant', 'content': f"Desculpe, algo deu errado: {e}"})
#st.sidebar.text_area(f"System prompt: {messages_for_api[0]['content']}")