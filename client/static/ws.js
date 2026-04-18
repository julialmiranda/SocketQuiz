export class WS {
    constructor(ui) {
        this.socket = null;
        this.ui = ui;
        this.playerName = null;
    }

    connect(roomId) {
        const url = `ws://localhost:8888/ws?sala=${roomId}`;
        this.socket = new WebSocket(url);

        this.socket.onopen = () => {
            console.log('Conectado ao WebSocket');
        };

        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };

        this.socket.onclose = () => {
            console.log('WebSocket fechado');
            this.ui.setStatus('Conexão encerrada.');
        };
    }

    sendAnswer(option) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify({
                action: 'answer',
                option
            }));

            // 🎮 feedback imediato estilo Kahoot
            this.ui.setStatus('✅ Resposta enviada! Aguardando o outro jogador...');
            this.ui.disableOptions();
        }
    }

    handleMessage(data) {

        // 🔰 INICIALIZAÇÃO
        if (data.type === 'init') {
            this.playerName = data.player;
            this.ui.setStatus(`🎮 Você é o ${data.player}`);
        }

        // ⏳ ESPERA
        else if (data.type === 'wait') {
            this.ui.setStatus(`⏳ ${data.message}`);
        }

        // ❓ NOVA PERGUNTA
        else if (data.type === 'question') {
            this.ui.setStatus(`🔥 Pergunta ativa - ${this.playerName ?? 'Jogador'}`);

            this.ui.renderQuestion(data.state, (optionIndex) => {
                this.sendAnswer(optionIndex);
            });
        }

        // 🎯 RESULTADO
        else if (data.type === 'round_result') {
            this.ui.updateScoreboard(data.scores);

            // Mostra resultado 
            this.ui.showRoundResult(data.correct_option);

            this.ui.setStatus('🎯 Resposta revelada!');
        }

        //FIM
        else if (data.type === 'finished') {
            this.ui.showFinished(data.state);

            // Fechar conexão depois de 10s
            setTimeout(() => {
                if (this.socket) {
                    this.socket.close();
                }
            }, 10000);
        }

        else if (data.type === 'full') {
            this.ui.setStatus(`❌ ${data.message}`);
        }
    }
}