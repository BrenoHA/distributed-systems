#cliente
import Pyro5.api

def main():
    ip_servidor = "192.168.42.215"
    ns = Pyro5.api.locate_ns(host=ip_servidor)
    uri = ns.lookup("calculadora_remota")

    calculadora = Pyro5.api.Proxy(uri)
    while True:
        print("\nEscolha uma operação:")
        print("1 - Somar")
        print("2 - Subtrair")
        print("3 - Multiplicar")
        print("4 - Dividir")
        print("5 - Raiz Quadrada")
        print("6 - Exponenciação")
        print("0 - Sair")

        opcao = input("Digite o número da operação: ").strip()

        if opcao == "0":
            print("Encerrando o cliente...")
            break

        if opcao not in {"1", "2", "3", "4", "5", "6"}:
            print("Opção inválida! Digite novamente")
            continue

        try:
            n1 = float(input("Digite o primeiro número: "))

            if opcao != "5": 
                n2 = float(input("Digite o segundo número: "))
        except ValueError:
            print("Entrada inválida! Digite apenas números.")
            continue

        try:
            if opcao == "1":
                resultado = calculadora.soma(n1, n2)
            elif opcao == "2":
                resultado = calculadora.subtrai(n1, n2)
            elif opcao == "3":
                resultado = calculadora.multiplica(n1, n2)
            elif opcao == "4":
                resultado = calculadora.divide(n1, n2)
            elif opcao == "5":
                resultado = calculadora.raiz_quadrada(n1)
            elif opcao == "6":
                resultado = calculadora.exponencia(n1, n2)
            else:
                resultado = "Operação desconhecida."

            print(f"Resultado: {resultado}")
        except Exception as e:
            print(f"Erro ao realizar operação remota: {e}")

if __name__ == "__main__":
    main()