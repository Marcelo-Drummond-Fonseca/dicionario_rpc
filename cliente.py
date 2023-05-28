#Ver documentação em: https://rpyc.readthedocs.io/en/latest/

# Cliente de echo usando RPC
import rpyc #modulo que oferece suporte a abstracao de RPC

# endereco do servidor de echo
SERVIDOR = 'localhost'
PORTA = 10001

def iniciaConexao():
	'''Conecta-se ao servidor.
	Saida: retorna a conexao criada.'''
	conn = rpyc.connect(SERVIDOR, PORTA) 
	
	print(type(conn.root)) # mostra que conn.root eh um stub de cliente
	print(conn.root.get_service_name()) # exibe o nome da classe (servico) oferecido

	return conn

def fazRequisicoes(conn):
	'''Faz requisicoes ao servidor e exibe o resultado.
	Entrada: conexao estabelecida com o servidor'''
	# le as mensagens do usuario ate ele digitar 'fim'
	while True: 
		msg = input("Digite 'fim' para terminar, L para ler, E para escrever ou R para remover:")
		if msg == 'fim': break 
		if msg == 'L':
			chave = input("Digite a chave que deseja ler:")
			ret = conn.root.exposed_Ler(chave)
			print(ret)
		elif msg == 'E':
			chave = input("Digite a chave para qual deseja escrever:")
			valor = input("Digite o valor que deseja escrever:")
			ret = conn.root.exposed_Escrever(chave, valor)
			print(ret)
		elif msg == 'R':
			tipo = input("Digite C para remover uma chave ou E para remover um elemento de uma chave:")
			if tipo == 'C':
				chave = input("Digite a chave que deseja remover:")
				ret = conn.root.exposed_Remover_Chave(chave)
			if tipo == 'E':
				chave = input("Digite a chave de qual deseja remover:")
				valor = input("Digite o elemento que deseja remover:")
				ret = conn.root.exposed_Remover_Valor(chave, valor)
			print(ret)
		else: print("Comando não reconhecido")

	# encerra a conexao
	conn.close()

def main():
	'''Funcao principal do cliente'''
	#inicia o cliente
	conn = iniciaConexao()
	#interage com o servidor ate encerrar
	fazRequisicoes(conn)

# executa o cliente
if __name__ == "__main__":
	main()