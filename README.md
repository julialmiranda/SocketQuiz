🧠 Quiz Multiplayer em Tempo Real com WebSockets

Sistema de quiz multiplayer desenvolvido com foco em **comunicação em tempo real**, permitindo que dois jogadores participem de uma disputa interativa baseada em perguntas sobre Python.

🎯 Objetivo

Demonstrar na prática como conceitos de **Sistemas Distribuídos** e **comunicação assíncrona** podem ser aplicados em um sistema interativo.

⚙️ Funcionalidades

- 🎮 Partidas multiplayer em tempo real (2 jogadores)
- 🔗 Criação de salas via link compartilhável
- ❓ Perguntas fixas sobre Python
- ⚡ Envio simultâneo de respostas
- 🧠 Feedback visual (resposta correta e incorreta)
- ⏱️ Timer por pergunta
- 📊 Atualização automática do placar
- 🔄 Sincronização em tempo real com WebSockets
- 🎨 Interface moderna e responsiva


🛠️ Tecnologias Utilizadas

**Backend**
- Python
- Tornado (WebSocket server)

**Frontend**
- JavaScript (ES6 Modules)
- HTML
- Tailwind CSS

**Comunicação**
- WebSockets


🧩 Conceitos Aplicados

- Comunicação bidirecional (WebSockets)
- Gerenciamento de estado no servidor
- Sincronização entre múltiplos clientes
- Arquitetura cliente-servidor
- Programação assíncrona
- Separação de responsabilidades (backend vs frontend)


🎮 Como funciona

1. Um jogador cria uma sala
2. Um link é gerado automaticamente
3. O segundo jogador entra pela URL
4. O quiz inicia automaticamente
5. Ambos respondem as perguntas
6. O sistema avalia e atualiza o placar em tempo real
7. Ao final, o vencedor é exibido


🎓 Objetivo Acadêmico

Projeto desenvolvido com fins acadêmicos para demonstrar como aplicações em tempo real dependem diretamente do **desempenho do sistema operacional**, da **gestão de processos** e da **comunicação entre clientes e servidor**.


🔥 Diferencial

Diferente de aplicações tradicionais, este sistema utiliza **WebSockets** para manter uma comunicação contínua e instantânea, proporcionando uma experiência fluida e sincronizada entre os jogadores.
