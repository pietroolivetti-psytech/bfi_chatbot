# app.py
import streamlit as st
import openai
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Chatbot com Personalidade", layout="wide")

st.title("💬 Personalidade do Chatbot")

# Defina sua senha (idealmente, também em secrets.toml)
# Ex: APP_PASSWORD = "sua_senha_secreta_aqui" em .streamlit/secrets.toml
SENHA_CORRETA = st.secrets.get("APP_PASSWORD", "minhasenhaforte") # Use uma senha forte de verdade!

# Inicializa o estado da sessão para controle de acesso e API
if 'api_client_ready' not in st.session_state:
    st.session_state['api_client_ready'] = False
if 'api_source' not in st.session_state:
    st.session_state['api_source'] = "Nenhuma"

st.sidebar.title("Acesso ao Aplicativo")

# Opção 1: Usar a API secreta (com senha)
with st.sidebar.expander("Usar Minha API (com senha)"):
    password_input = st.text_input("Senha:", type="password", key="password_input")
    if st.button("Acessar com Senha", key="access_with_password"):
        if password_input == SENHA_CORRETA:
            st.success("Login bem-sucedido! Usando sua API secreta.")
            st.session_state.client = openai.OpenAI(api_key=st.secrets['OPENAI_API_KEY'])
            st.session_state['api_client_ready'] = True
            st.session_state['api_source'] = "Secreta"
        else:
            st.error("Senha incorreta.")
            st.session_state['api_client_ready'] = False

# Opção 2: Usuário insere a própria API
with st.sidebar.expander("Usar Minha Própria API"):
    user_api_key = st.text_input("Sua Chave de API da OpenAI:", type="password", key="user_api_key_input")
    if st.button("Configurar API", key="configure_user_api"):
        if user_api_key:
            try:
                st.session_state.client = openai.OpenAI(api_key=user_api_key)
                # Opcional: Testar a chave com uma chamada simples para validar
                # st.session_state.client.models.list()
                st.success("Chave de API configurada com sucesso!")
                st.session_state['api_client_ready'] = True
                st.session_state['api_source'] = "Usuário"
            except Exception as e:
                st.error(f"Erro ao configurar a chave de API: {e}. Verifique se a chave é válida.")
                st.session_state['api_client_ready'] = False
        else:
            st.warning("Por favor, insira sua chave de API.")
            st.session_state['api_client_ready'] = False

st.sidebar.markdown(f"Status da API: **{st.session_state.get('api_source', 'Nenhuma')}**")

# Somente renderize o restante do aplicativo se a API estiver pronta
if not st.session_state['api_client_ready']:
    st.info("Por favor, acesse o aplicativo usando uma senha ou configurando sua chave de API na barra lateral.")
    st.stop() # Impede a execução do restante do script

# --- SEU CÓDIGO DO APLICATIVO PRINCIPAL COMEÇA AQUI ---

# Menu lateral para escolher o modo
modo = st.sidebar.radio("Escolha o modo:", ["📝 Preencher BFI-44", "🎛️ Definir facetas manualmente", "Chatbot"])

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
elif modo == "🎛️ Definir facetas manualmente":
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
        for faceta_info in facetas:
            nome_faceta = faceta_info["nome"]
            descricao_faceta = faceta_info["descricao"]
            
            niveis[nome_faceta] = st.selectbox(f"{nome_faceta}:", ["Baixo", "Médio", "Alto"], help=descricao_faceta)
        
        gerar_perfil = st.form_submit_button("Gerar perfil descritivo")

    if gerar_perfil:
        st.subheader("🧠 Perfil gerado com base nas facetas:")
        for faceta, nivel in niveis.items():
            st.markdown(f"**{faceta}**: {nivel}")

        # ---
        # Aqui é onde a mudança acontece para incluir as descrições
        # ---
        perfil_texto = "Você é um chatbot com a seguinte personalidade:\n"
        for faceta_info in facetas:
            nome_faceta = faceta_info["nome"]
            descricao_faceta = faceta_info["descricao"]
            nivel = niveis[nome_faceta] # Obtém o nível selecionado para esta faceta
            
            perfil_texto += f"- **{nome_faceta}** ({descricao_faceta}): {nivel.lower()}.\n"

        st.text_area("🧾 Perfil para o prompt do chatbot:", perfil_texto, height=300)
        


elif modo == "Chatbot":
    
    st.header("Chatbot")

    # Inicializa o cliente OpenAI com a nova sintaxe
    # É uma boa prática inicializar o cliente uma vez e reutilizá-lo
    if "client" not in st.session_state:
        st.session_state.client = openai.OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

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

            # Nova forma de chamar a API de Chat Completions
            # Adiciona o system prompt com o perfil se ele estiver disponível
            messages_for_api = []
            # Certifique-se de que 'perfil_texto' está definido e acessível aqui.
            # Se 'perfil_texto' vem da seção de facetas, você precisará garantir que
            # ele seja gerado antes ou armazenado em st.session_state.
            
            # Exemplo de como você poderia integrar o perfil_texto como um system prompt
            # Assumindo que perfil_texto está disponível (você pode passá-lo via session_state)
            if 'perfil_texto' in st.session_state and st.session_state.perfil_texto:
                messages_for_api.append({"role": "system", "content": st.session_state.perfil_texto})

            # Adiciona as mensagens do histórico do chat
            for m in st.session_state.messages:
                messages_for_api.append({'role': m['role'], 'content': m["content"]})
            
            # Faz a chamada à API
            try:
                for chunk in st.session_state.client.chat.completions.create(
                    model=st.session_state['openai_model'],
                    messages=messages_for_api, # Usamos as mensagens com o system prompt
                    stream=True,
                ):
                    full_response += chunk.choices[0].delta.content or ""
                    message_placeholder.markdown(full_response + "|") # Adiciona um cursor piscando
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({'role': 'assistant', 'content': full_response})
            except Exception as e:
                st.error(f"Ocorreu um erro ao chamar a API: {e}")
                st.session_state.messages.append({'role': 'assistant', 'content': f"Desculpe, algo deu errado: {e}"})