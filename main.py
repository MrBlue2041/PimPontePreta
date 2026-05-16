import json

CAMINHO_USUARIOS = "dados/usuarios.json"
CAMINHO_JOGOS = "dados/jogos.json"

menus = [
    "PONTE PRETA",
    "Cadastro",
    "Login",
    "Sair",
    "Pagina Inicial",
    "Comprar Ingressos",
    "Meus Ingressos",
    "Seja Sócio",
    "Sair"
]

socios = {
    0: {"nome": "Nao socio", "desconto": 0, "valor": 0},
    1: {"nome": "Plano Social", "desconto": 80, "valor": "Por Renda"},
    2: {"nome": "Bronze", "desconto": 20, "valor": 50},
    3: {"nome": "Prata", "desconto": 50, "valor": 100},
    4: {"nome": "Ouro", "desconto": 100, "valor": 200}
}

Account = {}
menu_atual = 0


def limparChat():
    print("\n" * 40)


def carregarUsuarios():
    try:
        with open(CAMINHO_USUARIOS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def salvarUsuarios(usuarios):
    with open(CAMINHO_USUARIOS, "w", encoding="utf-8") as arquivo:
        json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)


def salvarContaAtualizada():
    global Account

    usuarios = carregarUsuarios()

    for i, usuario in enumerate(usuarios):
        if usuario["cpf"] == Account["cpf"]:
            usuarios[i] = Account
            salvarUsuarios(usuarios)
            return True

    return False


def mostrarPlanoAtual():
    if len(Account) == 0:
        return

    plano_id = Account["socio"]
    plano = socios[plano_id]

    print(f"Plano atual: {plano['nome']}")
    print(f"Desconto: {plano['desconto']}%")

    if plano_id != 0:
        print(f"Mensalidade paga: {'Sim' if Account['mensalidade_paga'] else 'Não'}")

    print()


def sairSistema():
    global Account
    global menu_atual

    Account = {}
    menu_atual = 0
    limparChat()
    print("Sua sessao foi terminada com sucesso!")


def createMenu(text, inicio, final):
    global menu_atual

    print(f"{'=' * 20} [{menus[menu_atual]}] {'=' * 20}")

    if menu_atual == 4 and len(Account) != 0:
        print(f"\nOlá Sr(a) {Account['nome']}, seja bem vindo Ponte Pretano.\n")
        mostrarPlanoAtual()

    for i in range(inicio, final):
        print(f"[{i}] {menus[i]}")

    print("=" * 40)

    try:
        select_menu = int(input(text))

        if inicio <= select_menu < final:
            menu_atual = select_menu
            limparChat()
        else:
            limparChat()
            print("Por favor digite um numero valido.")

    except ValueError:
        limparChat()
        print("Por favor digite apenas numeros.")


def createAcesso(login):
    global menu_atual
    global Account

    if login:
        login_etapa = 0

        while True:
            match login_etapa:
                case 0:
                    cpf = input("Digite seu CPF: ")

                    if len(cpf) == 11 and cpf.isdigit():
                        if buscarCPF(cpf):
                            login_etapa += 1
                        else:
                            print("Erro: Esse CPF nao esta cadastrado.")
                    else:
                        print("Erro: CPF invalido.")

                case 1:
                    senha = input("Digite sua senha: ")

                    if buscarSenha(senha, cpf):
                        Account = carregarConta(cpf, senha)

                        if not Account:
                            print("Erro: Nao foi possivel carregar a conta, tente novamente.")
                        else:
                            if Account["mensalidade_paga"] == False:
                                print("Erro: Acesso negado, voce deve pagar sua mensalidade que esta em atraso.")
                                return

                            menu_atual = 4
                            limparChat()
                            break
                    else:
                        print("Erro: Senha incorreta.")

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

                    if len(cpf) == 11 and cpf.isdigit():
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
                    except ValueError:
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
                    if novoUsuario(nome, email, cpf, data, renda, senha):
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

    usuarios = carregarUsuarios()
    usuarios.append(novo_usuario)
    salvarUsuarios(usuarios)

    return True


def buscarEmail(email):
    usuarios = carregarUsuarios()

    for usuario in usuarios:
        if usuario["email"] == email:
            return True

    return False


def buscarCPF(cpf):
    usuarios = carregarUsuarios()

    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return True

    return False


def buscarSenha(senha, cpf):
    usuarios = carregarUsuarios()

    for usuario in usuarios:
        if usuario["senha"] == senha and usuario["cpf"] == cpf:
            return True

    return False


def carregarConta(cpf, senha):
    usuarios = carregarUsuarios()

    for usuario in usuarios:
        if usuario["senha"] == senha and usuario["cpf"] == cpf:
            return usuario

    return {}


def createMenuSocios():
    global menu_atual

    if len(Account) == 0:
        print("Erro: voce precisa estar logado.")
        menu_atual = 0
        return

    print(f"{'=' * 20} [{menus[menu_atual]}] {'=' * 20}")

    mostrarPlanoAtual()

    for index, socio in list(socios.items())[1:]:
        if index == 1:
            print(f"[{index}] {socio['nome']} - {socio['valor']}")
        else:
            print(f"[{index}] {socio['nome']} - R$ {socio['valor']}")

    print("[0] Voltar")
    print("=" * 40)

    try:
        select_socio = int(input(f"\nOlá Sr(a) {Account['nome']}, escolha o socio em que voce deseja aderir: "))

        if select_socio == 0:
            limparChat()
            menu_atual = 4
            return

        if 1 <= select_socio < 5:
            limparChat()
            adquirirSocio(select_socio)
        else:
            limparChat()
            print("Por favor digite um numero valido ['1' a '4'].")

    except ValueError:
        limparChat()
        print("Por favor digite apenas numeros.")


def confirmarTrocaPlano(novo_socio):
    socio_atual = Account["socio"]

    if socio_atual == 0:
        return True

    if socio_atual == novo_socio:
        print(f"Voce ja possui o plano {socios[socio_atual]['nome']}.")
        return False

    print(f"Voce ja possui o plano {socios[socio_atual]['nome']}.")
    print(f"Deseja trocar para o plano {socios[novo_socio]['nome']}?")
    print("[1] Sim")
    print("[2] Nao")

    try:
        escolha = int(input("Escolha uma opcao: "))

        if escolha == 1:
            return True

        print("Troca de plano cancelada.")
        return False

    except ValueError:
        print("Opcao invalida. Troca de plano cancelada.")
        return False


def adquirirSocio(socio):
    global Account
    global menu_atual

    if not confirmarTrocaPlano(socio):
        menu_atual = 4
        return

    if socio == 1:
        if float(Account["renda"]) > 1518.0:
            print("Erro: sua renda ultrapassa o limite permitido para o Plano Social.")
            menu_atual = 4
            return

    print(f"{'=' * 20} [{menus[menu_atual]}] {'=' * 20}")

    if socio == 1:
        print(f"Atraves da sua renda voce adquiriu o socio {socios[socio]['nome']} vitalicio, obrigado por apoiar nosso time.")
    else:
        print(f"Voce adquiriu o socio {socios[socio]['nome']} pelo valor de R$ {socios[socio]['valor']}, devera ser pago mensalmente.")
        print("Obrigado por apoiar nosso time.")

    print("=" * 40)

    Account["socio"] = socio
    Account["mensalidade_paga"] = True

    salvarContaAtualizada()

    menu_atual = 4
    
# SISTEMA DE INGRESSOS
def carregarJogos():
    try:
        with open(CAMINHO_JOGOS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def buscarJogoPorId(jogos, id_jogo):
    for jogo in jogos:
        if jogo["id"] == id_jogo:
            return jogo

    return None

def buscarSetorPorId(jogo, id_setor):
    for setor in jogo["setores"]:
        if setor["id"] == id_setor:
            return setor

    return None

def createCompraIngresso():
    global Account
    global menu_atual

    if len(Account) == 0:
        print("Erro: voce precisa estar logado.")
        menu_atual = 0
        return

    jogos = carregarJogos()

    if len(jogos) == 0:
        print("Nenhum jogo disponivel no momento.")
        menu_atual = 4
        return

    print(f"{'=' * 20} [Comprar Ingressos] {'=' * 20}")

    for jogo in jogos:
        print("-" * 40)
        print(f"[{jogo['id']}] Ponte Preta x {jogo['adversario']}")
        print(f"Data: {jogo['data']} às {jogo['horario']}")
        print(f"Estádio: {jogo['estadio']}")
        print("-" * 40)

    print("[0] Voltar")
    print("=" * 40)

    try:
        select_jogo = int(input("Escolha o jogo: "))

        if(select_jogo == 0):
            limparChat()
            menu_atual = 4
            return

        jogo = buscarJogoPorId(jogos, select_jogo)

        if(jogo == None):
            limparChat()
            print("Erro: Jogo invalido.")
            menu_atual = 4
            return

        limparChat()

        print(f"{'=' * 20} [Escolha o Setor] {'=' * 20}")
        print(f"Jogo: Ponte Preta x {jogo['adversario']}")
        print(f"Data: {jogo['data']} às {jogo['horario']}")
        print(f"Estádio: {jogo['estadio']}")
        print("=" * 40)

        for setor in jogo["setores"]:
            print(f"[{setor['id']}] {setor['nome']}")
            print(f"{setor['tipo']}")
            print(f"R$ {setor['valor']:.2f}")
            print("-" * 40)

        print("[0] Voltar")
        print("=" * 40)

        select_setor = int(input("Escolha o setor: "))

        if(select_setor == 0):
            limparChat()
            menu_atual = 4
            return

        setor = buscarSetorPorId(jogo, select_setor)

        if(setor == None):
            limparChat()
            print("Erro: Setor invalido.")
            menu_atual = 4
            return

        socio = Account["socio"]
        desconto = socios[socio]["desconto"]

        valor_original = setor["valor"]
        valor_desconto = valor_original * desconto / 100
        valor_final = valor_original - valor_desconto

        limparChat()

        print(f"{'=' * 20} [Resumo da Compra] {'=' * 20}")
        print(f"Jogo: Ponte Preta x {jogo['adversario']}")
        print(f"Data: {jogo['data']} às {jogo['horario']}")
        print(f"Estádio: {jogo['estadio']}")
        print(f"Setor: {setor['nome']}")
        print(f"Tipo: {setor['tipo']}")
        print(f"Plano atual: {socios[socio]['nome']}")
        print(f"Valor original: R$ {valor_original:.2f}")
        print(f"Desconto: {desconto}%")
        print(f"Valor final: R$ {valor_final:.2f}")
        print("=" * 40)

        confirmar_compra = input("Deseja confirmar a compra? [s/n]: ").lower()

        if(confirmar_compra == "s"):
            ingresso = {
                "jogo_id": jogo["id"],
                "jogo": f"Ponte Preta x {jogo['adversario']}",
                "data": jogo["data"],
                "horario": jogo["horario"],
                "estadio": jogo["estadio"],
                "setor": setor["nome"],
                "tipo": setor["tipo"],
                "valor_original": valor_original,
                "desconto": desconto,
                "valor_pago": valor_final
            }

            if "ingressos" not in Account:
                Account["ingressos"] = []

            Account["ingressos"].append(ingresso)
            salvarContaAtualizada()

            limparChat()
            print("Ingresso comprado com sucesso!")

        else:
            limparChat()
            print("Compra cancelada.")

        menu_atual = 4

    except ValueError:
        limparChat()
        print("Digite apenas numeros.")
        menu_atual = 4

while menu_atual != -1:
    match menu_atual:
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

        case 5:
            limparChat()
            createCompraIngresso()
            menu_atual = 4

        case 6:
            limparChat()
            print("Sistema de meus ingressos ainda nao implementado.")
            menu_atual = 4

        case 7:
            createMenuSocios()

        case 8:
            sairSistema()