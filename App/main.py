from pratos import *
from produtos import *
from categoriaPrato import *
from categoriaProdutos import *
from precoPratoEspacoAlimentar import *
from precoProdutoEspacoAlimentar import *
from produtosFornecedores import *
from avaliacao import *
from fatura import *
import maingraca
import mainnecas

def menu_grupo():
    print(80 * "#")
    print("""
             1 - Menu Marcos Ramos
             
             2 - Menu Francisco Graça
             
             3 - Menu João Graça
                
                x - sair
            """)
    op = input("Qual apresentação será?")
    return op

def mostra_menu_le_opcao_main():
    print(80 * "#")
    print("""Menu Marcos Ramos:
                1 - Pratos
                2 - Produtos
                3 - Categoria dos Pratos
                4 - Categoria dos Produtos
                5 - Preços dos Pratos Dependendo dos Bares
                6 - Preços dos Produtos Dependendo dos Bares
                7 - Preços dos Produtos Dependendo dos Fornecedores
                8 - Avaliação dos Espaços Alimentares
                
            x - sair
        """)
    print(80 * "#")
    op = input("opção? ")
    print(80 * "#")
    return op

def main_grupo():
    print('''BEM VINDO A BASE DE DADOS BAR E CANTINAS DA UNIVERSIDADE DO ALGARVE
            
Através deste programa pode gerir os dados presentes na base de dados!''')
    while True:
        op1 = menu_grupo()
        if op1 == "1":
            main_marcos()
        elif op1 == "2":
            main_graca()
        elif op1 == "3":
            main_necas()
        elif op1 == "x":
            exit()
        else:
            print('opçao invalida')
            continue

def main_graca():
    maingraca.main()

def main_marcos():
    while True:
        op = mostra_menu_le_opcao_main()
        if op == "1":  # lista todos os clientes
            main_pratos()
        elif op == "3":  # lista todos os clientes
            main_categoriaPratos()
        elif op == "5":
            main_preco_prato_espacoalimentar()
        elif op == "2":
            main_produtos()
        elif op == "4":
            main_categoriaprodutos()
        elif op == "7":
            main_produtos_fornecedores()
        elif op == "6":
            main_preco_produto_espacoalimentar()
        elif op == "8":
            main_avaliacao()

        elif op == "x":
            print('''Projeto desenvolvido por:
Marcos Ramos a63059''')
            break

def main_necas():
    mainnecas.main()

if __name__ == "__main__":
    main_grupo()
