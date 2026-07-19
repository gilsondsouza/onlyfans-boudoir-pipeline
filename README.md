# 🎨 OnlyFans Boudoir Pipeline

> Pipeline autônomo de produção de conteúdo boudoir artístico para OnlyFans — 7 modelos + agente interativo

---

## 📖 Visão Geral

O **OnlyFans Boudoir Pipeline** é um sistema automatizado de ponta a ponta para criação, curadoria, agendamento e publicação de conteúdo boudoir artístico na plataforma OnlyFans. O pipeline gerencia simultaneamente **7 perfis de modelos** e conta com um **agente interativo de IA** capaz de personalizar estratégias de conteúdo, responder a métricas em tempo real e adaptar o calendário editorial de forma autônoma.

---

## ✨ Funcionalidades

| Funcionalidade | Descrição |
|---|---|
| 🤖 **Agente Interativo** | IA que conversa com o operador, sugere pautas, analisa engajamento e ajusta o pipeline dinamicamente |
| 📸 **Geração de Conteúdo** | Criação e curadoria assistida de imagens e vídeos boudoir artísticos |
| 📅 **Agendador Inteligente** | Calendário editorial automático baseado nos melhores horários de engajamento por perfil |
| 👤 **7 Perfis de Modelo** | Gestão simultânea de 7 modelos com personas, estilos e audiências distintos |
| 📊 **Analytics em Tempo Real** | Dashboard com métricas de subscrições, likes, mensagens e receita |
| 💬 **Automação de Mensagens** | Respostas automáticas personalizadas por perfil para fãs |
| 🔒 **Gestão de Acesso** | Controle seguro de credenciais e permissões por modelo |
| 📤 **Upload Automatizado** | Publicação programada direto na API do OnlyFans |

---

## 🏗️ Arquitetura

```
onlyfans-boudoir-pipeline/
├── src/
│   ├── agent/              # Agente interativo de IA (LLM)
│   │   ├── chat.py         # Interface de conversa com o operador
│   │   ├── planner.py      # Planejamento de conteúdo via IA
│   │   └── analyzer.py     # Análise de métricas e sugestões
│   ├── models/             # Perfis das 7 modelos
│   │   ├── base_model.py   # Classe base de perfil
│   │   └── profiles/       # Configurações individuais por modelo
│   ├── pipeline/           # Etapas do pipeline de produção
│   │   ├── ingest.py       # Ingestão de mídia bruta
│   │   ├── process.py      # Processamento e filtragem
│   │   ├── curate.py       # Curadoria e seleção de conteúdo
│   │   └── publish.py      # Publicação na plataforma
│   ├── scheduler/          # Agendamento de publicações
│   │   ├── calendar.py     # Calendário editorial
│   │   └── optimizer.py    # Otimização de horários
│   ├── uploader/           # Integração com a API do OnlyFans
│   │   ├── api_client.py   # Cliente da API
│   │   └── media.py        # Upload de mídia
│   └── analytics/          # Coleta e análise de dados
│       ├── collector.py    # Coleta de métricas
│       └── dashboard.py    # Visualização de dados
├── config/
│   ├── settings.yaml       # Configurações globais do pipeline
│   ├── models.yaml         # Definições dos perfis de modelos
│   └── schedule.yaml       # Regras de agendamento
├── docs/
│   ├── architecture.md     # Detalhes da arquitetura
│   ├── models.md           # Guia de configuração dos modelos
│   ├── agent.md            # Documentação do agente interativo
│   └── api.md              # Referência da API interna
├── tests/                  # Testes automatizados
├── .env.example            # Variáveis de ambiente (template)
├── requirements.txt        # Dependências Python
└── README.md
```

---

## 👤 Os 7 Perfis de Modelo

Cada modelo possui uma persona única, estilo visual e estratégia de conteúdo independentes:

| # | Perfil | Estilo | Nicho |
|---|--------|--------|-------|
| 1 | **Aurora** | Natural & Minimalista | Fotografia de arte & lifestyle |
| 2 | **Valentina** | Glamour & Elegante | Luxo, moda e boudoir clássico |
| 3 | **Sofia** | Vintage & Romântico | Estética retrô e pin-up artístico |
| 4 | **Luna** | Dark & Editorial | Fotografia conceitual e avant-garde |
| 5 | **Bianca** | Fitness & Empoderamento | Estilo de vida ativo e sensual |
| 6 | **Isabelle** | Boho & Alternativo | Arte corporal e fotografia indie |
| 7 | **Marina** | Praia & Tropical | Lifestyle costeiro e fotografia ao ar livre |

Cada perfil é configurável via `config/models.yaml` com parâmetros de:
- Persona e tom de voz para mensagens automáticas
- Paleta de cores e estilo visual preferido
- Frequência de postagem e horários de pico
- Preço e estrutura de assinatura

---

## 🤖 Agente Interativo

O agente interativo é o coração do sistema. Baseado em um modelo de linguagem (LLM), ele:

- **Conversa em linguagem natural** com o operador via terminal ou interface web
- **Analisa métricas** de engajamento e receita de todos os perfis simultaneamente
- **Sugere conteúdo** baseado em tendências, datas especiais e histórico de performance
- **Ajusta o calendário** de publicações de forma autônoma quando detecta queda no engajamento
- **Alerta sobre anomalias** como quedas de subscritores ou falhas de upload
- **Gera relatórios** semanais e mensais de performance por modelo

### Exemplo de uso do agente:

```
Operador: Qual modelo teve melhor desempenho essa semana?

Agente: Esta semana, a **Valentina** liderou com +23% de novas assinaturas
e R$ 4.200 em receita. Destaque para o post de quinta-feira (18h) que
gerou 340 likes. Recomendo replicar o formato para Aurora na próxima semana.
Quer que eu ajuste o calendário?
```

---

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.11+
- Conta OnlyFans com acesso à API
- Chave de API para o modelo de LLM (OpenAI, Anthropic, etc.)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/gilsondsouza/onlyfans-boudoir-pipeline.git
cd onlyfans-boudoir-pipeline

# Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas credenciais
```

### Configuração

```bash
# Configure os perfis dos modelos
nano config/models.yaml

# Defina as regras de agendamento
nano config/schedule.yaml

# Ajuste as configurações globais
nano config/settings.yaml
```

### Execução

```bash
# Iniciar o pipeline completo
python -m src.pipeline run

# Iniciar apenas o agente interativo
python -m src.agent chat

# Visualizar o dashboard de analytics
python -m src.analytics dashboard

# Executar agendador em modo daemon
python -m src.scheduler start --daemon
```

---

## ⚙️ Configuração

### Variáveis de Ambiente (`.env`)

```env
# API OnlyFans
OF_API_KEY=sua_chave_aqui
OF_API_SECRET=seu_secret_aqui

# LLM para o Agente
LLM_PROVIDER=openai           # openai | anthropic | local
LLM_API_KEY=sua_chave_llm

# Banco de dados
DATABASE_URL=sqlite:///pipeline.db

# Storage de mídia
MEDIA_STORAGE=local           # local | s3 | gcs
MEDIA_PATH=./media

# Notificações
TELEGRAM_BOT_TOKEN=opcional
TELEGRAM_CHAT_ID=opcional
```

### Estrutura de `config/models.yaml`

```yaml
models:
  aurora:
    display_name: "Aurora"
    credentials:
      username: "aurora_official"
      # Credenciais lidas do vault de secrets
    posting:
      frequency: 2/day
      peak_hours: [18, 20, 22]
      timezone: "America/Sao_Paulo"
    style:
      aesthetic: "natural_minimalist"
      color_palette: ["#F5E6D3", "#E8D5B7", "#C4A882"]
    pricing:
      subscription: 9.99
      ppv_enabled: true
```

---

## 📊 Pipeline de Produção

O conteúdo passa pelas seguintes etapas:

```
Mídia Bruta → Ingestão → Processamento → Curadoria (IA) → Agendamento → Upload → Publicação
                ↑                              ↓
           Agente IA ←←←←← Analytics & Feedback ←←←←←←←←←←←←←←←←
```

1. **Ingestão**: Mídia bruta é importada de pastas locais, Google Drive ou S3
2. **Processamento**: Redimensionamento, marca d'água e otimização de qualidade
3. **Curadoria**: O agente de IA seleciona as melhores peças e sugere legendas
4. **Agendamento**: O otimizador define o melhor horário por perfil e plataforma
5. **Upload**: Envio automatizado via API do OnlyFans
6. **Analytics**: Coleta de métricas pós-publicação para retroalimentar o ciclo

---

## 🔒 Segurança

- Credenciais armazenadas em vault de secrets (nunca em texto plano)
- Todas as comunicações com a API via HTTPS
- Logs de auditoria de todas as ações automatizadas
- Separação total de credenciais entre os 7 perfis
- Variáveis sensíveis carregadas apenas em runtime

---

## 🧪 Testes

```bash
# Executar todos os testes
pytest

# Executar testes com cobertura
pytest --cov=src --cov-report=html

# Testar apenas o agente
pytest tests/test_agent.py

# Testar apenas o pipeline
pytest tests/test_pipeline.py
```

---

## 📚 Documentação

Documentação detalhada disponível em `docs/`:

- [`docs/architecture.md`](docs/architecture.md) — Arquitetura detalhada do sistema
- [`docs/models.md`](docs/models.md) — Guia completo de configuração dos modelos
- [`docs/agent.md`](docs/agent.md) — Documentação do agente interativo
- [`docs/api.md`](docs/api.md) — Referência da API interna

---

## 🤝 Contribuição

1. Fork o repositório
2. Crie uma branch: `git checkout -b feature/minha-feature`
3. Commit suas mudanças: `git commit -m 'feat: adiciona minha feature'`
4. Push: `git push origin feature/minha-feature`
5. Abra um Pull Request

---

## 📄 Licença

Distribuído sob a licença MIT. Veja [`LICENSE`](LICENSE) para mais informações.

---

## ⚠️ Aviso Legal

Este projeto é uma ferramenta de automação de produção de conteúdo. O operador é inteiramente responsável por garantir que todo o conteúdo publicado esteja em conformidade com os Termos de Serviço do OnlyFans e com as leis aplicáveis em sua jurisdição. O projeto não gera nem armazena conteúdo explícito — apenas automatiza o fluxo de trabalho de publicação.

---

<p align="center">
  Feito com ❤️ para criadores de conteúdo independentes
</p>
