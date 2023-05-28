#Ver documentação em: https://rpyc.readthedocs.io/en/latest/

# Servidor de echo usando RPC 
import rpyc #modulo que oferece suporte a abstracao de RPC
import json

#servidor que utiliza multithreading
from rpyc.utils.server import ThreadedServer

# porta de escuta do servidor de echo
PORTA = 10001

class Dicionario:

    def lerDicionario(self, chave):
        '''Carrega o dicionario e retorna o valor desejado de acordo com a chave'''
        dicionario = json.load(open("dicionario.txt"))
        return str(dicionario.get(chave))

    def escreverDicionario(self, chave, texto):
        '''Carrega o dicionario e escreve o valor desejado na lista da chave'''
        dicionario = json.load(open("dicionario.txt"))
        if chave in dicionario:
            dicionario[chave].append(texto)
        else:
            dicionario[chave] = [texto]
        dicionario[chave].sort()
        json.dump(dicionario, open("dicionario.txt",'w'))

    def removerChaveDicionario(self, chave):
        '''Carrega o dicionario e remove o valor desejado na lista da chave'''
        dicionario = json.load(open("dicionario.txt"))
        if chave in dicionario:
            del dicionario[chave]
        json.dump(dicionario, open("dicionario.txt",'w'))

    def removerElementoDicionario(self, chave, texto):
        '''Carrega o dicionario e remove o valor desejado na lista da chave'''
        dicionario = json.load(open("dicionario.txt"))
        if chave in dicionario:
            if texto in dicionario[chave]:
                dicionario[chave].remove(texto)
        json.dump(dicionario, open("dicionario.txt",'w'))

# classe que implementa o servico de dicionario
class Servidor(rpyc.Service):

	dicionario = Dicionario()
    
	# executa quando uma conexao eh criada
	def on_connect(self, conn):
		print("Conexao iniciada: " + str(conn))

	# executa quando uma conexao eh fechada
	def on_disconnect(self, conn):
		print("Conexao finalizada: " + str(conn))

	# imprime a chave recebida e retorna o valor associado
	def exposed_Ler(self, chave):
		print("Requisição de leitura de chave " + chave)
		return self.dicionario.lerDicionario(chave)

	# imprime a chave e valor recebidos e adiciona o valor na chave
	def exposed_Escrever(self, chave, valor):
		print("Requisição de escrita do valor " + valor + " na chave " + chave)
		self.dicionario.escreverDicionario(chave, valor)
		return valor + " inserido na chave " + chave

	# imprime a chave recebida e remove a chave
	def exposed_Remover_Chave(self, chave):
		print("Requisição de remoçao de chave " + chave)
		self.dicionario.removerChaveDicionario(chave)
		return chave + " e todos os valores associados foram removidos"

	# imprime a chave e valor recebidos e remove o valor da chave
	def exposed_Remover_Valor(self, chave, valor):
		print("Requisição de remoçao do valor " + valor + " da chave " + chave)
		self.dicionario.removerElementoDicionario(chave, valor)
		return valor + " foi removido da chave " + chave

# dispara o servidor
if __name__ == "__main__":
	srv = ThreadedServer(Servidor, port = PORTA)
	srv.start()


### Tipos de servidores
#https://rpyc.readthedocs.io/en/latest/api/utils_server.html

#servidor que dispara uma nova thread a cada conexao
#from rpyc.utils.server import ThreadedServer

#servidor que atende uma conexao e termina
#from rpyc.utils.server import OneShotServer

### Configuracoes do protocolo RPC
#https://rpyc.readthedocs.io/en/latest/api/core_protocol.html#rpyc.core.protocol.DEFAULT_CONFIG