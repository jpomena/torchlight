# Torchlight

**Torchlight** é uma aplicação de desktop desenvolvida em Python para extrair, analisar e visualizar dados de gerenciamento de tarefas da plataforma ClickUp. A ferramenta automatiza a coleta de dados, calcula métricas de desempenho chave (como Reaction Time, Cycle Time e Lead Time) e apresenta as informações em um dashboard interativo.

## Visão Geral

O objetivo do Torchlight é fornecer insights sobre o fluxo de trabalho de equipes, permitindo uma análise detalhada da eficiência e produtividade. Através de uma interface gráfica intuitiva, os usuários podem filtrar tarefas por período, tag ou responsável, e visualizar tanto dados estatísticos consolidados quanto gráficos de tendência.

## Funcionalidades

- **Extração de Dados do ClickUp**: Automatiza o processo de login e extração de dados de tarefas de uma lista específica no ClickUp utilizando Selenium.
- **Cálculo de Métricas**: Calcula automaticamente métricas essenciais de fluxo de trabalho, incluindo:
  - **Reaction Time**: Tempo entre a criação de uma tarefa e o início do trabalho nela.
  - **Cycle Time**: Tempo que uma tarefa leva desde o início até a sua conclusão.
  - **Lead Time**: Tempo total desde a criação da tarefa até a sua entrega final.
- **Dashboard Interativo**: Uma interface gráfica construída com Dear PyGui que apresenta:
  - Tabela de métricas estatísticas agregadas por tag.
  - Tabela de tarefas detalhadas com capacidade de ordenação.
  - Filtros por data, tag e responsável.
- **Visualização de Dados**: Gráficos de dispersão com linhas de tendência (LOESS) para visualizar o comportamento das métricas ao longo do tempo para cada tag.
- **Armazenamento Local**: Utiliza um banco de dados SQLite local para armazenar os dados extraídos, permitindo análises offline e persistência dos dados.
- **Edição de Dados**: Permite a edição manual dos dados extraídos antes de importá-los para o banco de dados principal.

## Arquitetura

O projeto segue uma arquitetura **Model-View-Controller (MVC)** para garantir uma separação clara de responsabilidades e facilitar a manutenção e escalabilidade.

- **Model**: Responsável pela lógica de negócios e manipulação de dados. Inclui os módulos para interação com o banco de dados (`main_database.py`, `scrapper_database.py`), automação do navegador (`puppet_browser.py`), parsing de HTML (`html_parser.py`, `regex_engine.py`) e cálculos estatísticos (`tasks_dataframe.py`, `statistics_dataframe.py`).
- **View**: Responsável pela apresentação da interface do usuário. Inclui todos os módulos que criam e gerenciam os componentes gráficos (`main_window.py`, `overview_tab.py`, etc.).
- **Controller**: Atua como intermediário entre o Model e a View. Processa as interações do usuário, invoca a lógica de negócios no Model e atualiza a View com os resultados (`controller.py`, `scrapper_controller.py`).

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **Dear PyGui**: Para a construção da interface gráfica do usuário.
- **Pandas**: Para manipulação e análise de dados.
- **Selenium**: Para automação do navegador e extração de dados web.
- **Beautiful Soup**: Para parsing de HTML.
- **Holidays**: Para cálculo preciso de dias úteis, considerando feriados.
- **SQLite**: Para o armazenamento de dados local.

## Instalação e Execução

Siga os passos abaixo para configurar e executar o projeto em sua máquina local.

### Pré-requisitos

- Python 3.8 ou superior
- Git
- Mozilla Firefox
- [GeckoDriver](https://github.com/mozilla/geckodriver/releases) (o WebDriver para o Firefox)

### Passos

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/jpomena/torchlight.git
    cd torchlight
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Para Windows
    python -m venv .venv
    .\.venv\Scripts\activate

    # Para macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure o WebDriver:**
    - Baixe o GeckoDriver compatível com sua versão do Firefox.
    - Extraia o executável (`geckodriver.exe` no Windows) e adicione o diretório onde ele se encontra à sua variável de ambiente `PATH`, ou coloque o executável diretamente na pasta raiz do projeto.

5.  **Execute a aplicação:**
    ```bash
    python main.py
    ```

## Como Usar

1.  **Iniciar a Extração**:
    - Na aplicação, vá para a janela de importação (geralmente através de um botão "Editar Atividades" -> "Importar Atividades do ClickUp").
    - Preencha seu usuário, senha do ClickUp e o nome exato da lista de onde deseja extrair os dados.
    - Clique em "Iniciar Extração". Uma janela do Firefox será aberta e o processo de extração começará. Acompanhe o progresso pela janela de log.

2.  **Analisar os Dados**:
    - Após a extração, os dados podem ser importados para o banco principal.
    - Na aba "Visão Geral", utilize os filtros de data, tag e responsável para analisar as métricas de desempenho.
    - Navegue pelas abas de cada tag para ver os gráficos de tendência detalhados.

## Licença

Este projeto é distribuído sob a licença GNU v3. Veja o arquivo `LICENSE` para mais detalhes.

---
# Torchlight

**Torchlight** é uma aplicação de desktop desenvolvida em Python para extrair, analisar e visualizar dados de gerenciamento de tarefas da plataforma ClickUp. A ferramenta automatiza a coleta de dados, calcula métricas de desempenho chave (como Reaction Time, Cycle Time e Lead Time) e apresenta as informações em um dashboard interativo.

## Visão Geral

O objetivo do Torchlight é fornecer insights sobre o fluxo de trabalho de equipes, permitindo uma análise detalhada da eficiência e produtividade. Através de uma interface gráfica intuitiva, os usuários podem filtrar tarefas por período, tag ou responsável, e visualizar tanto dados estatísticos consolidados quanto gráficos de tendência.

## Funcionalidades

- **Extração de Dados do ClickUp**: Automatiza o processo de login e extração de dados de tarefas de uma lista específica no ClickUp utilizando Selenium.
- **Cálculo de Métricas**: Calcula automaticamente métricas essenciais de fluxo de trabalho, incluindo:
  - **Reaction Time**: Tempo entre a criação de uma tarefa e o início do trabalho nela.
  - **Cycle Time**: Tempo que uma tarefa leva desde o início até a sua conclusão.
  - **Lead Time**: Tempo total desde a criação da tarefa até a sua entrega final.
- **Dashboard Interativo**: Uma interface gráfica construída com Dear PyGui que apresenta:
  - Tabela de métricas estatísticas agregadas por tag.
  - Tabela de tarefas detalhadas com capacidade de ordenação.
  - Filtros por data, tag e responsável.
- **Visualização de Dados**: Gráficos de dispersão com linhas de tendência (LOESS) para visualizar o comportamento das métricas ao longo do tempo para cada tag.
- **Armazenamento Local**: Utiliza um banco de dados SQLite local para armazenar os dados extraídos, permitindo análises offline e persistência dos dados.
- **Edição de Dados**: Permite a edição manual dos dados extraídos antes de importá-los para o banco de dados principal.

## Arquitetura

O projeto segue uma arquitetura **Model-View-Controller (MVC)** para garantir uma separação clara de responsabilidades e facilitar a manutenção e escalabilidade.

- **Model**: Responsável pela lógica de negócios e manipulação de dados. Inclui os módulos para interação com o banco de dados (`main_database.py`, `scrapper_database.py`), automação do navegador (`puppet_browser.py`), parsing de HTML (`html_parser.py`, `regex_engine.py`) e cálculos estatísticos (`tasks_dataframe.py`, `statistics_dataframe.py`).
- **View**: Responsável pela apresentação da interface do usuário. Inclui todos os módulos que criam e gerenciam os componentes gráficos (`main_window.py`, `overview_tab.py`, etc.).
- **Controller**: Atua como intermediário entre o Model e a View. Processa as interações do usuário, invoca a lógica de negócios no Model e atualiza a View com os resultados (`controller.py`, `scrapper_controller.py`).

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **Dear PyGui**: Para a construção da interface gráfica do usuário.
- **Pandas**: Para manipulação e análise de dados.
- **Selenium**: Para automação do navegador e extração de dados web.
- **Beautiful Soup**: Para parsing de HTML.
- **Holidays**: Para cálculo preciso de dias úteis, considerando feriados.
- **SQLite**: Para o armazenamento de dados local.

## Instalação e Execução

Siga os passos abaixo para configurar e executar o projeto em sua máquina local.

### Pré-requisitos

- Python 3.8 ou superior
- Git
- Mozilla Firefox
- [GeckoDriver](https://github.com/mozilla/geckodriver/releases) (o WebDriver para o Firefox)

### Passos

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/torchlight.git
    cd torchlight
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Para Windows
    python -m venv .venv
    .\.venv\Scripts\activate

    # Para macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure o WebDriver:**
    - Baixe o GeckoDriver compatível com sua versão do Firefox.
    - Extraia o executável (`geckodriver.exe` no Windows) e adicione o diretório onde ele se encontra à sua variável de ambiente `PATH`, ou coloque o executável diretamente na pasta raiz do projeto.

5.  **Execute a aplicação:**
    ```bash
    python main.py
    ```

## Como Usar

1.  **Iniciar a Extração**:
    - Na aplicação, vá para a janela de importação (geralmente através de um botão "Editar Atividades" -> "Importar Atividades do ClickUp").
    - Preencha seu usuário, senha do ClickUp e o nome exato da lista de onde deseja extrair os dados.
    - Clique em "Iniciar Extração". Uma janela do Firefox será aberta e o processo de extração começará. Acompanhe o progresso pela janela de log.

2.  **Analisar os Dados**:
    - Após a extração, os dados podem ser importados para o banco principal.
    - Na aba "Visão Geral", utilize os filtros de data, tag e responsável para analisar as métricas de desempenho.
    - Navegue pelas abas de cada tag para ver os gráficos de tendência detalhados.

## Licença

Este projeto é distribuído sob a licença [NOME DA LICENÇA]. Veja o arquivo `LICENSE` para mais detalhes.

---
# Torchlight

**Torchlight** é uma aplicação de desktop desenvolvida em Python para extrair, analisar e visualizar dados de gerenciamento de tarefas da plataforma ClickUp. A ferramenta automatiza a coleta de dados, calcula métricas de desempenho chave (como Reaction Time, Cycle Time e Lead Time) e apresenta as informações em um dashboard interativo.

## Visão Geral

O objetivo do Torchlight é fornecer insights sobre o fluxo de trabalho de equipes, permitindo uma análise detalhada da eficiência e produtividade. Através de uma interface gráfica intuitiva, os usuários podem filtrar tarefas por período, tag ou responsável, e visualizar tanto dados estatísticos consolidados quanto gráficos de tendência.

## Funcionalidades

- **Extração de Dados do ClickUp**: Automatiza o processo de login e extração de dados de tarefas de uma lista específica no ClickUp utilizando Selenium.
- **Cálculo de Métricas**: Calcula automaticamente métricas essenciais de fluxo de trabalho, incluindo:
  - **Reaction Time**: Tempo entre a criação de uma tarefa e o início do trabalho nela.
  - **Cycle Time**: Tempo que uma tarefa leva desde o início até a sua conclusão.
  - **Lead Time**: Tempo total desde a criação da tarefa até a sua entrega final.
- **Dashboard Interativo**: Uma interface gráfica construída com Dear PyGui que apresenta:
  - Tabela de métricas estatísticas agregadas por tag.
  - Tabela de tarefas detalhadas com capacidade de ordenação.
  - Filtros por data, tag e responsável.
- **Visualização de Dados**: Gráficos de dispersão com linhas de tendência (LOESS) para visualizar o comportamento das métricas ao longo do tempo para cada tag.
- **Armazenamento Local**: Utiliza um banco de dados SQLite local para armazenar os dados extraídos, permitindo análises offline e persistência dos dados.
- **Edição de Dados**: Permite a edição manual dos dados extraídos antes de importá-los para o banco de dados principal.

## Arquitetura

O projeto segue uma arquitetura **Model-View-Controller (MVC)** para garantir uma separação clara de responsabilidades e facilitar a manutenção e escalabilidade.

- **Model**: Responsável pela lógica de negócios e manipulação de dados. Inclui os módulos para interação com o banco de dados (`main_database.py`, `scrapper_database.py`), automação do navegador (`puppet_browser.py`), parsing de HTML (`html_parser.py`, `regex_engine.py`) e cálculos estatísticos (`tasks_dataframe.py`, `statistics_dataframe.py`).
- **View**: Responsável pela apresentação da interface do usuário. Inclui todos os módulos que criam e gerenciam os componentes gráficos (`main_window.py`, `overview_tab.py`, etc.).
- **Controller**: Atua como intermediário entre o Model e a View. Processa as interações do usuário, invoca a lógica de negócios no Model e atualiza a View com os resultados (`controller.py`, `scrapper_controller.py`).

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **Dear PyGui**: Para a construção da interface gráfica do usuário.
- **Pandas**: Para manipulação e análise de dados.
- **Selenium**: Para automação do navegador e extração de dados web.
- **Beautiful Soup**: Para parsing de HTML.
- **Holidays**: Para cálculo preciso de dias úteis, considerando feriados.
- **SQLite**: Para o armazenamento de dados local.

## Instalação e Execução

Siga os passos abaixo para configurar e executar o projeto em sua máquina local.

### Pré-requisitos

- Python 3.8 ou superior
- Git
- Mozilla Firefox
- [GeckoDriver](https://github.com/mozilla/geckodriver/releases) (o WebDriver para o Firefox)

### Passos

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/torchlight.git
    cd torchlight
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Para Windows
    python -m venv .venv
    .\.venv\Scripts\activate

    # Para macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure o WebDriver:**
    - Baixe o GeckoDriver compatível com sua versão do Firefox.
    - Extraia o executável (`geckodriver.exe` no Windows) e adicione o diretório onde ele se encontra à sua variável de ambiente `PATH`, ou coloque o executável diretamente na pasta raiz do projeto.

5.  **Execute a aplicação:**
    ```bash
    python main.py
    ```

## Como Usar

1.  **Iniciar a Extração**:
    - Na aplicação, vá para a janela de importação (geralmente através de um botão "Editar Atividades" -> "Importar Atividades do ClickUp").
    - Preencha seu usuário, senha do ClickUp e o nome exato da lista de onde deseja extrair os dados.
    - Clique em "Iniciar Extração". Uma janela do Firefox será aberta e o processo de extração começará. Acompanhe o progresso pela janela de log.

2.  **Analisar os Dados**:
    - Após a extração, os dados podem ser importados para o banco principal.
    - Na aba "Visão Geral", utilize os filtros de data, tag e responsável para analisar as métricas de desempenho.
    - Navegue pelas abas de cada tag para ver os gráficos de tendência detalhados.

## Licença

Este projeto é distribuído sob a licença [NOME DA LICENÇA]. Veja o arquivo `LICENSE` para mais detalhes.

---
<a href="https://www.flaticon.com/br/icones-gratis/tocha" title="tocha ícones">Tocha ícones criados por Freepik - Flaticon</a>