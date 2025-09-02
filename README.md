# Utilitário de Diff para Merge Requests do GitLab

Este script busca os diffs de um Merge Request específico de um projeto no GitLab e os exibe no terminal com formatação e cores, similar ao `git diff`.

## Requisitos

- Python 3.7+
- `pipx` (para instalação de ferramentas de linha de comando Python)

## Instalação

### Instalação Rápida (Recomendado)

Você pode instalar a ferramenta com um único comando usando `curl`:

```bash
curl -sSL https://raw.githubusercontent.com/lucasliet/gitlab-mr-diff/main/install.sh | bash
```

### Instalação Manual

Se preferir, você pode clonar o repositório e instalar manualmente:

1.  **Clone o repositório:**
    ```bash
git clone https://github.com/lucasliet/gitlab-mr-diff.git
```

2.  **Navegue até o diretório:**
    ```bash
cd gitlab-mr-diff
```

3.  **Instale com `pipx`:**
    ```bash
pipx install .
```

## Configuração

Antes de usar, você precisa configurar as seguintes variáveis de ambiente:

-   `GITLAB_PRODESP_TOKEN`: Seu Token de Acesso Pessoal do GitLab.
    ```bash
export GITLAB_PRODESP_TOKEN='seu_token_privado_aqui'
```

-   `GITLAB_PROJECT_PREFIX` (Opcional): O prefixo do projeto no GitLab. O padrão é `ssp/dipol/`.
    ```bash
export GITLAB_PROJECT_PREFIX='meu/grupo/'
```

## Como Usar

Depois de instalado e configurado, você pode usar o comando da seguinte forma:

```bash
get_mr_diff <caminho_parcial_projeto> <mr_iid>
```

### Argumentos

-   `<caminho_parcial_projeto>`: O caminho do projeto dentro do grupo `ssp/dipol/`. Por exemplo, `frontend/dipol-de`.
-   `<mr_iid>`: O IID (Internal ID) do Merge Request que você quer visualizar.

### Exemplo

```bash
get_mr_diff frontend/dipol-de 640
```

## Desinstalação

Se você deseja desinstalar a ferramenta, pode usar o seguinte comando:

```bash
pipx uninstall gitlab-mr-diff
```