#!/bin/bash
# Script para instalar a ferramenta get_mr_diff diretamente do GitHub.

set -e

# Variáveis
REPO_URL="https://github.com/lucasliet/gitlab-mr-diff.git"
TMP_DIR=$(mktemp -d)

# Função para limpar o diretório temporário na saída
cleanup() {
  echo "Limpando..."
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

# Verifica se git e pipx estão instalados
command -v git >/dev/null 2>&1 || { echo >&2 "Erro: git não está instalado. Abortando."; exit 1; }
command -v pipx >/dev/null 2>&1 || { echo >&2 "Erro: pipx não está instalado. Abortando."; exit 1; }

# Clona o repositório
echo "Baixando o repositório..."
git clone "$REPO_URL" "$TMP_DIR"

# Instala com pipx
echo "Instalando com pipx..."
pipx install "$TMP_DIR"

echo "Instalação concluída com sucesso!"
echo "Use 'get_mr_diff --help' para começar."