# Passo 1 - vamos usar o framework flet
import flet as ft


# Passo 2 - criando a função principal (main)
def main(pagina): 
    texto = ft.Text("Hashzap", theme_style=ft.TextThemeStyle.DISPLAY_LARGE)

    chat = ft.Column() 

    #TUNEL DE COMUNICAÇÃO - para aparecer para todos os usuarios ao mesmo tempo
    #1 - escolher a funcão q vai pssar pelo tunel
    #2 - criar o tunel
    #3 - sempre que queremos usar o tunel vamos enviar apra todos (sendall)
    def enviar_mensagem_tunel(mensagem):
        texto_mensagem = ft.Text(mensagem)
        chat.controls.append(texto_mensagem)
        pagina.update()

    pagina.pubsub.subscribe(enviar_mensagem_tunel)


    def enviar_mensagem(evento):
        #adicionar a mensagem no chat
        pagina.pubsub.send_all(f'{nome_usuario.value}: {campo_mensagem.value}')
        #limpar o campo mensagem
        campo_mensagem.value = ""
        pagina.update()


    campo_mensagem = ft.TextField(label="Digite sua mensagem", on_submit=enviar_mensagem)
    botao_enviar = ft.ElevatedButton("Enviar", on_click=enviar_mensagem)
    linha_enviar = ft.Row([campo_mensagem, botao_enviar])


    def entrar_chat(evento):
        #fechar o popup
        popup.open = False
        #tirar os botoes de iniciar chat e titulo
        pagina.remove(texto)
        pagina.remove(botao_iniciar)
        # criar o chat
        pagina.add(chat)
        #assim que adicionamos a coluna chat, vamos adicionar informacoes dentro
        pagina.pubsub.send_all(f'{nome_usuario.value} entrou no chat')
        # colocar o campo de digitar mensagem
        # criar botao de enviar
        pagina.add(linha_enviar)
        pagina.update()

    titulo_popup = ft.Text("Bem vindo ao Hashzap!")
    nome_usuario = ft.TextField(label="Escreva seu nome no chat")
    botao_entrar = ft.ElevatedButton("Entrar no chat", on_click=entrar_chat)

    #criar um popup - 2 passos
    popup = ft.AlertDialog(
        open=False, #apenas por garantia
        modal=True,
        title=titulo_popup,
        content=nome_usuario,
        #por padrao em acoes passamos uma lsita de botões
        actions=[botao_entrar]
    )

    #por padrão toda funcão atribuida a um botão precisa receber um evento
    def abrir_popup(evento):
        pagina.dialog = popup
        popup.open = True
        #sempre que editar a página depois que a página já tiver carregada, rodamos um "update" para atualizar o visual da pagina
        pagina.update()
        

    #botao precisa de duas informacoes, o texto e uma função
    botao_iniciar = ft.ElevatedButton("Iniciar Chat", on_click=abrir_popup)

    pagina.add(texto)
    pagina.add(botao_iniciar)

# Passo 3 - criar o aplicativo (passando como alvo nossa função principal)
# Vamos usar o formato WEB
    
ft.app(target=main, view=ft.AppView.WEB_BROWSER)