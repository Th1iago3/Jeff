# Jeff

### 1. Instalação
```bash
python3 instl.py
```

### 2. Configuração
Edite `res/assets/config.json` com suas informações:
```json
{
  "server_id": "id_do_seu_servidor",
  "moderadores": ["ids_dos_moderadores"],
  "comandos": ["ping", "help"]
}
```

### 3. Iniciar
```bash
sh iniciar.sh
```

## Estrutura

```
Jeff/
├── main.py              # Ponto de entrada
├── loader.py            # Carregador de módulos
├── instl.py            # Instalador das bibliotecas
├── cogs/                # Módulos funcionais
│   ├── comandos.py      # Comandos gerais
│   ├── comandos_adm.py  # Comandos administrativos
│   └── events.py        # Eventos do bot
└── res/assets/
    └── config.json      # Configurações
    └── infos_secrets.env # Arquivo .env com informacoes sensiveis (token, etc...)

```

## Como usar

1. **Configurar o servidor** — Atualize o `server_id` em `config.json`
2. **Adicionar comandos** — Edite a lista `comandos` na configuração
3. **Gerenciar moderadores** — Adicione IDs dos moderadores autorizados
4. **Executar** — O bot processará comandos automaticamente

Em desenvolvimento...
