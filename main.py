menu_all = ["Pagina acesso", "Cadastro", "Login", "Sair", "Pagina Inicial", "Comprar Ingressos", "Meus Ingressos"]

tentativas_acesso = 0
menu_atual = 0

def createMenu(text, inicio, final):
    print("=" * 40)
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
            print("[!] Por favor digite um numero valido ['1' ou '2']")

    except:
        print("\n" * 40)
        print("[!] Por favor digite apenas numeros.")



while menu_atual != -1:
    match(menu_atual):
        case 0:
            createMenu("Digite o menu em que voce deseja ir: ", 1, 3)
            break
        case 1:
            print("em breve")
            break
        case 2:
            print("em breve")
            break