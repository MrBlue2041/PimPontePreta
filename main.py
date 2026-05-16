import json

menus = ["PIM", "Cadastro", "Login", "Sair", "Pagina Inicial", "Comprar Ingressos", "Meus Ingressos", "Seja Sócio", "Sair"]

socios = {
    0: {
        "nome": "Nao socio",
        "desconto": 0,
        "valor": 0
    },
    1: {
        "nome": "Plano Social",
        "desconto": 80,
        "valor": "Por Renda"
    },
    2: {
        "nome": "Bronze",
        "desconto": 20,
        "valor": 50
    },
    3: {
        "nome": "Prata",
        "desconto": 50,
        "valor": 100
    },
    4: {
        "nome": "Ouro",
        "desconto": 100,
        "valor": 200
    }
}

Account = {}

tentativas_login = 0
menu_atual = 0

#FUNCAO ALEATORIAS

def limparChat():
    print("\n" * 40)

# PARTE MENU INICIAIS
def createMenu(text, inicio, final):
    global menu_atual
    global Account
    
    print(f"{'=' * 20} [{menus[menu_atual]}] {'=' * 20}")
    
    if menu_atual == 4:
        if len(Account) != 0:
            print(f"\nOlá Sr(a) {Account['nome']}, seja bem vindo Ponte Pretano.\n")
            
    for menu in menus[inicio:final]:
        print(f"[{menus.index(menu)}] {menu}")
        
    print("=" * 40)
    
    try:
        select_menu = int(input(text))

        if (select_menu >= inicio and select_menu < final):
            menu_atual = select_menu
            limparChat()
            print(f"{'=' * 20} [{menus[menu_atual]}] {'=' * 20}")
        else:
            limparChat()
            print("Por favor digite um numero valido ['1' ou '2']")

    except:
        limparChat()
        print("Por favor digite apenas numeros.")
        
#PARTE LOGIN E REGISTRO

def createAcesso(login):
    global menu_atual
    
    if login == True:
        login_etapa = 0
        
        while True:
            match login_etapa:
                case 0:
                    cpf = input("Digite seu CPF: ")

                    if len(cpf) == 11 and cpf != None:
                        if buscarCPF(cpf):
                            login_etapa += 1
                        else:
                            print("Erro: Esse CPF nao esta cadastrado.")
                    else:
                        print("Erro: CPF invalido.")
                case 1: 
                    global Account
                    
                    senha = input("Digite sua senha: ")

                    if buscarSenha(senha, cpf):
                        Account = carregarConta(cpf, senha)
                        
                        if not Account:
                            print("Erro: Nao foi possivel carregar a conta, tente novamente.")
                        else:
                            if  Account["mensalidade_paga"] == False:
                                return print("Erro: Acesso negado, voce deve pagar sua mensalidade que esta em atraso")
                            
                            menu_atual = 4
                            break
                    else:
                        login_etapa = 1
            
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
                    data = input("Digite sua data de nascimento: ")

                    if len(data) == 10 and data[2] == "/" and data[5] == "/":
                            cadastro_etapa += 1
                    else:
                        print("Erro: Data de nascimento invalida.")
                case 4:
                    try:
                        renda = float(input("Digite sua renda: "))
                        cadastro_etapa += 1

                    except:
                        print("Erro: Digite apenas numeros.")
                case 5:
                    senha = input("Digite sua senha: ")
                    confirmar_senha = input("Confirme sua senha: ")

                    if len(senha) < 8:
                        print("Erro: Minimo 8 caracteres.")

                    elif senha != confirmar_senha:
                        print("Erro: As senhas nao coincidem.")

                    else:
                        cadastro_etapa += 1
                case 6:
                    if(novoUsuario(nome, email, cpf, data, renda, senha)):
                        print("Cadastro realizado com sucesso!")
                        createMenu("Digite o menu em que voce deseja ir: ", 1, 3)
                        break
                    else:
                        print("Erro: Realize o cadastro novamente!")
                        cadastro_etapa = 0
                    

def novoUsuario(nome, email, cpf, nascimento, renda, senha):
    novo_usuario = {
        "nome": nome,
        "email": email,
        "cpf": cpf,
        "nascimento": nascimento,
        "renda": renda,
        "senha": senha,
        "socio": 0,
        "mensalidade_paga": True
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

def buscarCPF(cpf):

    try:
        with open("usuarios.json", "r") as arquivo:
            usuarios = json.load(arquivo)

    except (FileNotFoundError, json.JSONDecodeError):
        return False

    for usuario in usuarios:

        if usuario["cpf"] == cpf:
            return True

    return False

def buscarSenha(senha, cpf):

    try:
        with open("usuarios.json", "r") as arquivo:
            usuarios = json.load(arquivo)

    except (FileNotFoundError, json.JSONDecodeError):
        return False

    for usuario in usuarios:

        if usuario["senha"] == senha and usuario["cpf"] == cpf:
            return True

    return False

def carregarConta(cpf, senha):
    try:
        with open("usuarios.json", "r") as arquivo:
            usuarios = json.load(arquivo)
            
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

    for usuario in usuarios:

        if usuario["senha"] == senha and usuario["cpf"] == cpf:
            return usuario
        
    return {}

# PARTE DO MENU DE SEJA SOCIO

def createMenuSocios():
    global menu_atual
    
    if len(Account) != 0:
         
        for index, socio in list(socios.items())[1:]:
            if(index == 1):
                print(f"[{index}] {socio['nome']} - {socio['valor']}")
            else:
                print(f"[{index}] {socio['nome']} - R$ {socio['valor']}")
                
        print("=" * 40)
        
        try:
            select_socio = int(input(f"\nOlá Sr(a) {Account['nome']}, escolha o socio em que voce deseja aderir.\n"))

            if (select_socio >= 0 and select_socio < 5):
                adquirirSocio(select_socio)         
            else:
                limparChat()
                print("Por favor digite um numero valido ['1' a '5']")

        except:
            limparChat()
            print("Por favor digite apenas numeros.")
            
def adquirirSocio(socio):
    global Account
    
    if socio == 1:
        if float(Account["renda"]) > 1518.0:
            return -1
        
    print(f"{'=' * 20} [{menus[menu_atual]}] {'=' * 20}")
    
    if(socio == 1):
        print(f"Atraves da sua renda voce adquiriu o socio {socios[socio]['nome']} vitalicio, obrigado por apoiar nosso time.")
    else:
        print(f"Voce adquiriu o socio {socios[socio]['nome']} pelo valor de R$ {socios[socio]['valor']}, devera ser pago mensalmente. \nObrigado por apoiar nosso time.")
    
    print("="*40)
    
    Account["socio"] = socio
    Account["mensalidade_paga"] = True    
            
while menu_atual != -1:
    match(menu_atual):
        case 0:
            createMenu("Digite o menu em que voce deseja ir: ", 1, 4)
        case 1:
            createAcesso(False)
        case 2:
            createAcesso(True)
        case 3:
            break
        case 4:
            createMenu("Digite o menu em que voce deseja ir: ", 5, 9)
        case 7:
            createMenuSocios()
            
            