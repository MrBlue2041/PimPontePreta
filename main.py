import json

menu_all = ["PIM", "Cadastro", "Login", "Sair", "Pagina Inicial", "Comprar Ingressos", "Meus Ingressos"]

tentativas_acesso = 0
menu_atual = 0

def createMenu(text, inicio, final):
    global menu_atual
    
    print(f"{'=' * 20} [{menu_all[menu_atual]}] {'=' * 20}")
    for menu in menu_all[1:3]:
        print(f"[{menu_all.index(menu)}] {menu}")
    print("=" * 40)
    try:
        select_menu = int(input(text))

        if (select_menu >= inicio and select_menu < final):
            menu_atual = select_menu
            print("\n" * 40)
            print(f"{'=' * 20} [{menu_all[menu_atual]}] {'=' * 20}")
        else:
            print("\n" * 40)
            print("Por favor digite um numero valido ['1' ou '2']")

    except:
        print("\n" * 40)
        print("Por favor digite apenas numeros.")

def createAcesso(login):
    if login == True:
        return print("loginnn")
    else:
        cadastro_etapa = 0
        
        while True:
            match cadastro_etapa:
                case 0:
                    nome = input("Digite seu nome: ")
                    cadastro_etapa += 1
                case 1:
                    email = input("Digite seu email: ").lower()

                    if "@" in email:
                        if not buscarEmail(email):
                            cadastro_etapa += 1
                        else:
                            print("Erro: Esse email ja esta em uso.")
                    else:
                        print("Erro: Email invalido.")
                case 2:
                    cpf = input("Digite seu CPF: ")

                    if len(cpf) == 11 and cpf != None:
                        if not buscarCPF(cpf):
                            cadastro_etapa += 1
                        else:
                            print("Erro: Esse CPF ja esta em uso.")
                    else:
                        print("Erro: CPF invalido.")
                case 3:
                    try:
                        renda = float(input("Digite sua renda: "))
                        cadastro_etapa += 1

                    except:
                        print("Erro: Digite apenas numeros.")
                case 4:
                    senha = input("Digite sua senha: ")
                    confirmar_senha = input("Confirme sua senha: ")

                    if len(senha) < 8:
                        print("Erro: Minimo 8 caracteres.")

                    elif senha != confirmar_senha:
                        print("Erro: As senhas nao coincidem.")

                    else:
                        cadastro_etapa += 1
                case 5:
                    if(novoUsuario(nome, email, cpf, renda, senha)):
                        print("Cadastro realizado com sucesso!")
                        createMenu("Digite o menu em que voce deseja ir: ", 1, 3)
                        break
                    else:
                        print("Erro: Realize o cadastro novamente!")
                        cadastro_etapa = 0
                    

def novoUsuario(nome, email, cpf, renda, senha):
    novo_usuario = {
        "nome": nome,
        "email": email,
        "cpf": cpf,
        "renda": renda,
        "senha": senha
    }
  
    try:
        with open("usuarios.json", "r") as arquivo:
            usuarios = json.load(arquivo)
            
    except (FileNotFoundError, json.JSONDecodeError):
        usuarios = []
        
    usuarios.append(novo_usuario)
    
    with open("usuarios.json", "w") as arquivo:
        json.dump(usuarios, arquivo, indent=4)
        
    return True

def buscarEmail(email):
    try:
        with open("usuarios.json", "r") as arquivo:
            usuarios = json.load(arquivo)

    except (FileNotFoundError, json.JSONDecodeError):
        return False

    for usuario in usuarios:

        if usuario["email"] == email:
            return True

    return False

def buscarCPF(email):

    try:
        with open("usuarios.json", "r") as arquivo:
            usuarios = json.load(arquivo)

    except (FileNotFoundError, json.JSONDecodeError):
        return False

    for usuario in usuarios:

        if usuario["CPF"] == email:
            return True

    return False

        
while menu_atual != -1:
    match(menu_atual):
        case 0:
            createMenu("Digite o menu em que voce deseja ir: ", 1, 3)
            
        case 1:
            createAcesso(False)
            break
        case 2:
            createAcesso(True)
            break
            