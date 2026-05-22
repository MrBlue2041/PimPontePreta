import json

CAMINHO_USUARIOS = "dados/usuarios.json"
CAMINHO_JOGOS = "dados/jogos.json"

menus = [
    "PONTE PRETA",
    "Cadastro",
    "Login",
    "Pagina Inicial",
    "Comprar Ingressos",
    "Meus Ingressos",
    "Seja Sócio",
    "Carteirinha Digital",
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


def pausar(texto="Pressione ENTER para continuar..."):
    input(f"\n{texto}")
    limparChat()


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

    if menu_atual == 3 and len(Account) != 0:
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
        pausar()


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
                            pausar("Pressione ENTER para tentar novamente...")
                    else:
                        print("Erro: CPF invalido.")
                        pausar("Pressione ENTER para tentar novamente...")

                case 1:
                    senha = input("Digite sua senha: ")

                    if buscarSenha(senha, cpf):
                        Account = carregarConta(cpf, senha)

                        if not Account:
                            print("Erro: Nao foi possivel carregar a conta, tente novamente.")
                            pausar("Pressione ENTER para tentar novamente...")
                        else:
                            if Account["mensalidade_paga"] == False:
                                print("Erro: Acesso negado, voce deve pagar sua mensalidade que esta em atraso.")
                                pausar()
                                return

                            menu_atual = 3
                            limparChat()
                            break
                    else:
                        print("Erro: Senha incorreta.")
                        pausar("Pressione ENTER para tentar novamente...")

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
                            pausar("Pressione ENTER para tentar novamente...")
                    else:
                        print("Erro: Email invalido.")
                        pausar("Pressione ENTER para tentar novamente...")

                case 2:
                    cpf = input("Digite seu CPF: ")

                    if len(cpf) == 11 and cpf.isdigit():
                        if not buscarCPF(cpf):
                            cadastro_etapa += 1
                        else:
                            print("Erro: Esse CPF ja esta em uso.")
                            pausar("Pressione ENTER para tentar novamente...")
                    else:
                        print("Erro: CPF invalido.")
                        pausar("Pressione ENTER para tentar novamente...")

                case 3:
                    data = input("Digite sua data de nascimento: ")

                    if len(data) == 10 and data[2] == "/" and data[5] == "/":
                        cadastro_etapa += 1
                    else:
                        print("Erro: Data de nascimento invalida.")
                        pausar("Pressione ENTER para tentar novamente...")

                case 4:
                    try:
                        renda = float(input("Digite sua renda: "))
                        cadastro_etapa += 1
                    except ValueError:
                        print("Erro: Digite apenas numeros.")
                        pausar("Pressione ENTER para tentar novamente...")

                case 5:
                    senha = input("Digite sua senha: ")
                    confirmar_senha = input("Confirme sua senha: ")

                    if len(senha) < 8:
                        print("Erro: Minimo 8 caracteres.")
                        pausar("Pressione ENTER para tentar novamente...")
                    elif senha != confirmar_senha:
                        print("Erro: As senhas nao coincidem.")
                        pausar("Pressione ENTER para tentar novamente...")
                    else:
                        cadastro_etapa += 1

                case 6:
                    if novoUsuario(nome, email, cpf, data, renda, senha):
                        print("Cadastro realizado com sucesso!")
                        pausar()
                        menu_atual = 0
                        break
                    else:
                        print("Erro: Realize o cadastro novamente!")
                        pausar()
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
        pausar()
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
            menu_atual = 3
            return

        if 1 <= select_socio < 5:
            limparChat()
            adquirirSocio(select_socio)
        else:
            limparChat()
            print("Por favor digite um numero valido ['1' a '4'].")
            pausar()

    except ValueError:
        limparChat()
        print("Por favor digite apenas numeros.")
        pausar()


def confirmarTrocaPlano(novo_socio):
    socio_atual = Account["socio"]

    if socio_atual == 0:
        return True

    if socio_atual == novo_socio:
        print(f"Voce ja possui o plano {socios[socio_atual]['nome']}.")
        pausar()
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
        pausar()
        return False

    except ValueError:
        print("Opcao invalida. Troca de plano cancelada.")
        pausar()
        return False


def adquirirSocio(socio):
    global Account
    global menu_atual

    if not confirmarTrocaPlano(socio):
        menu_atual = 3
        return

    if socio == 1:
        if float(Account["renda"]) > 1518.0:
            print("Erro: sua renda ultrapassa o limite permitido para o Plano Social.")
            pausar()
            menu_atual = 3
            return

    print(f"{'=' * 20} [{menus[menu_atual]}] {'=' * 20}")

    if socio == 1:
        print(f"Atraves da sua renda voce adquiriu o socio {socios[socio]['nome']} vitalicio, obrigado por apoiar nosso time.")
    else:
        print(f"Voce adquiriu o socio {socios[socio]['nome']} pelo valor de R$ {socios[socio]['valor']}, devera ser pago mensalmente.")
        print("Obrigado por apoiar nosso time.")

    print("=" * 40)
    pausar("Pressione ENTER para voltar...")

    Account["socio"] = socio
    Account["mensalidade_paga"] = True

    salvarContaAtualizada()

    menu_atual = 3
    
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

def calcularValorIngresso(valor, desconto):
    return valor - (valor * desconto / 100)

def createCompraIngresso():
    global Account
    global menu_atual

    if len(Account) == 0:
        print("Erro: voce precisa estar logado.")
        pausar()
        menu_atual = 0
        return

    jogos = carregarJogos()

    if len(jogos) == 0:
        print("Nenhum jogo disponivel no momento.")
        pausar()
        menu_atual = 3
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
            menu_atual = 3
            return

        jogo = buscarJogoPorId(jogos, select_jogo)

        if(jogo == None):
            limparChat()
            print("Erro: Jogo invalido.")
            pausar()
            menu_atual = 3
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
            menu_atual = 3
            return

        setor = buscarSetorPorId(jogo, select_setor)

        if(setor == None):
            limparChat()
            print("Erro: Setor invalido.")
            pausar()
            menu_atual = 3
            return

        socio = Account["socio"]
        desconto = socios[socio]["desconto"]

        valor_original = setor["valor"]
        valor_desconto = valor_original * desconto / 100
        valor_final = calcularValorIngresso(valor_original, valor_desconto)

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
                "valor_pago": valor_final,
                "validado": False
            }

            if "ingressos" not in Account:
                Account["ingressos"] = []

            Account["ingressos"].append(ingresso)
            salvarContaAtualizada()

            limparChat()
            print("Ingresso comprado com sucesso!")
            mostrarTicket(ingresso)
            pausar()

        else:
            limparChat()
            print("Compra cancelada.")
            pausar()

        menu_atual = 3

    except ValueError:
        limparChat()
        print("Digite apenas numeros.")
        pausar()
        menu_atual = 3

def mostrarTicket(ingresso):
    status = "Validado" if ingresso.get("validado") == True else "Nao validado"

    print("-" * 40)
    print(f"Jogo: {ingresso['jogo']}")
    print(f"Data: {ingresso['data']} às {ingresso['horario']}")
    print(f"Estádio: {ingresso['estadio']}")
    print(f"Setor: {ingresso['setor']}")
    print(f"Tipo: {ingresso['tipo']}")
    print(f"Valor pago: R$ {ingresso['valor_pago']:.2f}")
    print(f"Status: {status}")
    print("-" * 40)
    
def createMeusIngressos():
    global Account
    global menu_atual

    if len(Account) == 0:
        print("Erro: voce precisa estar logado.")
        pausar()
        menu_atual = 0
        return

    if "ingressos" not in Account or len(Account["ingressos"]) == 0:
        print("Voce ainda nao possui ingressos.")
        pausar()
        menu_atual = 3
        return

    print(f"{'=' * 20} [Meus Ingressos] {'=' * 20}")

    index = 0

    for ingresso in Account["ingressos"]:
        print(f"[{index + 1}]")
        mostrarTicket(ingresso)

        index += 1

    print("[0] Voltar")
    print("=" * 40)

    try:
        select_ingresso = int(input("Digite o numero do ingresso para validar entrada: "))

        if(select_ingresso == 0):
            limparChat()
            menu_atual = 3
            return

        index_ingresso = select_ingresso - 1

        if(index_ingresso < 0 or index_ingresso >= len(Account["ingressos"])):
            limparChat()
            print("Erro: Ingresso invalido.")
            pausar()
            menu_atual = 3
            return

        ingresso = Account["ingressos"][index_ingresso]

        if(ingresso.get("validado") == True):
            limparChat()
            print("Erro: Este ingresso ja foi validado anteriormente.")
            pausar()
            menu_atual = 3
            return

        print(f"{'=' * 20} [Validar Entrada] {'=' * 20}")
        print(f"Ingresso: {ingresso['jogo']}")
        print(f"Setor: {ingresso['setor']}")
        print(f"Data: {ingresso['data']} às {ingresso['horario']}")
        print("=" * 40)

        confirmar = input("Confirmar validacao de entrada? [s/n]: ").lower()

        if(confirmar == "s"):
            Account["ingressos"][index_ingresso]["validado"] = True
            salvarContaAtualizada()

            limparChat()
            print("Entrada validada com sucesso!")
            pausar()
        else:
            limparChat()
            print("Validacao cancelada.")
            pausar()

        menu_atual = 3

    except ValueError:
        limparChat()
        print("Digite apenas numeros.")
        pausar()
        menu_atual = 3
        
def showCarteirinhaDigital():
    global Account
    global menu_atual

    if len(Account) == 0:
        print("Erro: voce precisa estar logado.")
        pausar()
        menu_atual = 0
        return

    socio = Account["socio"]
    socio_nome = socios[socio]["nome"]
    mensalidade = "Em dia" if Account["mensalidade_paga"] == True else "Em atraso"

    identificacao = f"PP-{Account['cpf'][-4:]}-{Account['cpf'][0]}"

    print("=" * 45)
    print("           CARTEIRINHA DIGITAL")
    print("=" * 45)
    print(f"Nome: {Account['nome']}")
    print(f"CPF: ***.***.***-{Account['cpf'][-2:]}")
    print(f"Categoria do plano: {socio_nome}")
    print(f"Situação da mensalidade: {mensalidade}")
    print(f"Identificação digital: {identificacao}")
    print("=" * 45)

    pausar("Pressione ENTER para voltar...")
    menu_atual = 3

while menu_atual != -1:
    match menu_atual:
        case 0:
            createMenu("Digite o menu em que voce deseja ir: ", 1, 3)

        case 1:
            createAcesso(False)

        case 2:
            createAcesso(True)

        case 3:
            createMenu("Digite o menu em que voce deseja ir: ", 4, 9)

        case 4:
            limparChat()
            createCompraIngresso()

        case 5:
            limparChat()
            createMeusIngressos()

        case 6:
            limparChat()
            createMenuSocios()

        case 7:
            limparChat()
            showCarteirinhaDigital()
        case 8:
            sairSistema()