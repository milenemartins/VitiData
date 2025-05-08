from app.scraper import (
    scrape_producao_pages,
    scrape_exportacao,
    scrape_all_processamento,
    scrape_importacao,
    scrape_comercializacao_page
)

def menu():
    print("\n=== VitiData Scraper ===")
    print("1 - Produção")
    print("2 - Exportação")
    print("3 - Processamento")
    print("4 - Importação")
    print("5 - Comercialização")
    print("0 - Sair")

    opcao = input("Escolha uma opção: ")
    return opcao

if __name__ == "__main__":
    while True:
        opcao = menu()

        if opcao == "1":
            dados = scrape_producao_pages()
        elif opcao == "2":
            dados = scrape_exportacao()
        elif opcao == "3":
            dados = scrape_all_processamento()
        elif opcao == "4":
            dados = scrape_importacao()
        elif opcao == "5":
            dados = scrape_comercializacao_page()
        elif opcao == "0":
            print("Encerrando.")
            break
        else:
            print("Opção inválida.")
            continue

        print(f"\nTotal de registros obtidos: {len(dados)}\n")
