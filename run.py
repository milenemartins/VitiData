import os
import sys
import argparse
import shutil
from dotenv import load_dotenv
from app import create_app

load_dotenv()

def clean_project():
    """Remove todos __pycache__, a pasta instance e arquivos .db na raiz."""
    root = os.path.abspath(os.path.dirname(__file__))

    # 1) Deleta todos os __pycache__ recursivamente
    for dirpath, dirnames, filenames in os.walk(root):
        if "__pycache__" in dirnames:
            cache_dir = os.path.join(dirpath, "__pycache__")
            shutil.rmtree(cache_dir)
            print(f"Removed cache: {cache_dir}")

    # 2) Remove pasta 'instance' (caso exista)
    instance_dir = os.path.join(root, "instance")
    if os.path.isdir(instance_dir):
        shutil.rmtree(instance_dir)
        print(f"Removed instance folder: {instance_dir}")

    # 3) Remove arquivos de banco de dados (.db) na raiz
    for fname in os.listdir(root):
        if fname.endswith(".db"):
            db_file = os.path.join(root, fname)
            os.remove(db_file)
            print(f"Removed DB file: {db_file}")

def main():
    parser = argparse.ArgumentParser(description="Run or clean VitiData API")
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove __pycache__, pasta instance e arquivos .db antes de iniciar"
    )
    args = parser.parse_args()

    if args.clean:
        clean_project()
        sys.exit(0)

    # Se não for --clean, inicia a API normalmente
    app = create_app()
    app.run(debug=True)

if __name__ == "__main__":
    main()