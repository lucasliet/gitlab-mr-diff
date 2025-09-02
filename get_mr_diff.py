#!/usr/bin/env python3
'''
Script para buscar os diffs de um Merge Request do GitLab e formatá-los.

COMO USAR:
1. Salve este script como 'get_mr_diff.py'.
2. Instale a biblioteca 'requests':
   pip install requests
3. Exporte seu Token de Acesso Pessoal do GitLab como uma variável de ambiente:
   export GITLAB_PRIVATE_TOKEN='seu_token_aqui'
4. Execute o script passando o caminho parcial do projeto e o IID do Merge Request:
   python get_mr_diff.py <caminho_parcial_projeto> <mr_iid>

EXEMPLO:
   python get_mr_diff.py frontend/dipol-de 634
'''
import os
import sys
import requests
from urllib.parse import quote

# --- Configuração ---
# Altere estes valores se necessário
GITLAB_URL = "https://gitlab.prodesp.sp.gov.br"
# O caminho base que será prefixado ao caminho do projeto fornecido
# Pode ser sobrescrito pela variável de ambiente GITLAB_PROJECT_PREFIX
PROJECT_BASE_PATH = os.getenv("GITLAB_PROJECT_PREFIX", "ssp/dipol/")
# --- Fim da Configuração ---

def get_gitlab_token():
    """Obtém o token do GitLab da variável de ambiente."""
    token = os.getenv("GITLAB_PRODESP_TOKEN")
    if not token:
        print("Erro: A variável de ambiente 'GITLAB_PRODESP_TOKEN' não foi definida.", file=sys.stderr)
        print("Por favor, defina-a com seu token de acesso pessoal do GitLab.", file=sys.stderr)
        sys.exit(1)
    return token

def fetch_mr_diffs(project_path, mr_iid, token):
    """Busca os diffs do Merge Request na API do GitLab."""
    # Codifica o caminho do projeto para ser seguro para URL (ex: 'ssp/dipol' -> 'ssp%2Fdipol')
    encoded_project_path = quote(project_path, safe='')
    
    api_url = f"{GITLAB_URL}/api/v4/projects/{encoded_project_path}/merge_requests/{mr_iid}/diffs"
    headers = {"PRIVATE-TOKEN": token}
    
    try:
        response = requests.get(api_url, headers=headers, timeout=30)
        # Lança uma exceção para respostas com erro (4xx ou 5xx)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer a requisição para a API do GitLab: {e}", file=sys.stderr)
        sys.exit(1)

def format_as_git_diff(diffs):
    """Formata a resposta da API no estilo 'git diff' com cores."""
    COLOR_RED = "\033[31m"
    COLOR_GREEN = "\033[32m"
    COLOR_RESET = "\033[0m"

    for diff_item in diffs:
        print(f"diff --git a/{diff_item['old_path']} b/{diff_item['new_path']}")
        print(f"--- a/{diff_item['old_path']}")
        print(f"+++ b/{diff_item['new_path']}")
        
        # Divide o bloco de diff em linhas e aplica a cor
        for line in diff_item['diff'].split('\n'):
            if line.startswith('+'):
                print(f"{COLOR_GREEN}{line}{COLOR_RESET}")
            elif line.startswith('-'):
                print(f"{COLOR_RED}{line}{COLOR_RESET}")
            else:
                print(line)
        print()  # Adiciona uma linha em branco para espaçamento


def main():
    """Função principal do script."""
    if len(sys.argv) != 3:
        print(f"Uso: python {sys.argv[0]} <caminho_parcial_projeto> <mr_iid>", file=sys.stderr)
        print(f"Exemplo: python {sys.argv[0]} frontend/dipol-de 634", file=sys.stderr)
        sys.exit(1)

    partial_project_path = sys.argv[1]
    mr_iid = sys.argv[2]
    
    # Constrói o caminho completo do projeto
    full_project_path = f"{PROJECT_BASE_PATH}{partial_project_path}"
    
    token = get_gitlab_token()
    diffs_data = fetch_mr_diffs(full_project_path, mr_iid, token)
    
    if diffs_data:
        format_as_git_diff(diffs_data)

if __name__ == "__main__":
    main()