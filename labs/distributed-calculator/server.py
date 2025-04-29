#servidor:
import Pyro5.api

@Pyro5.api.expose
class CalculadoraRemota:
    def soma(self, n1, n2):
        return n1 + n2

    def subtrai(self, n1, n2):
        return n1 - n2

    def multiplica(self, n1, n2):
        return n1 * n2

    def divide(self, n1, n2):
        if n2 == 0:
            return "Erro: Divisão por zero!"
        return n1 / n2
    
    def raiz_quadrada(self, n1):
        return n1 ** 0.5
    
    def exponencia(self, b, e):
        return b ** e

def main():
    ip_servidor = '192.168.42.215'
    daemon = Pyro5.api.Daemon(host=ip_servidor)
    ns = Pyro5.api.locate_ns(host=ip_servidor)
    uri = daemon.register(CalculadoraRemota())
    ns.register("calculadora_remota", uri)

    print("Servidor pronto. Aguardando:")
    daemon.requestLoop()

if __name__ == "__main__":
    main()