# Ambiente para teste de LLM's open source com Ollama

Este projeto reproduz um ambiente de teste local para LLM's opensource usando Ollama para servir os modelos e OpenWebUI para disponibilizar uma interface conversacional.

OBS: Neste projeto assumimos que queremos rodar apenas modelos usando apenas CPU, caso queira configurar para cenários de uso de GPU por favor verifique as configurações do [ollama correspondentes](https://hub.docker.com/r/ollama/ollama).
## Pre-requisitos

- docker e docker compose instalados e rodando

## O que é o Ollama

Projeto opensource que tem como objetivo facilitar a execução de diferentes LLM's localmente.

Referência = https://github.com/ollama/ollama

## O que é o OpenWebUI

Projeto opensource que fornece uma interface padronizada de chat conversacional para testar LLM's, pode ser usada em conjunto com o ollama que assume o papel de servir as LLM's localmente.

## Como executar passo a passo manualmente

### 1 - Rode o ollama
```sh
docker run -it -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

### 2 - Execute o modelo desejado
```sh
docker exec -it ollama ollama run llama3.1
```
o nome do modelo deve estar disponível no catálogo do [ollama](https://ollama.com/library)

### 3 - Execute o openwebUI
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main

### 4 - Abra a interface
Abra no seu navegador o endereço `http://localhost:3000`
OBS: A subida do container do openWebUI pode demorar um pouco, caso receba uma mensagem de erro, espere um pouco até tentar novamente. 


## Como executar usando o script utilitário

Execute o script informando o nome do modelo que deseja rodar, caso não informe nenhum será executado o modelo llama3.1.
o nome do modelo deve estar disponível no catálogo do [ollama](https://ollama.com/library)

```sh
./run.sh llama3.1
```

OBS: A subida do container do openWebUI pode demorar um pouco, caso receba uma mensagem de erro, espere um pouco até tentar novamente. 