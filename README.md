# 🕹️ Platformer Adventure — Pygame Zero

Projeto desenvolvido como parte do desafio técnico **Python Base – Teste para novos tutores**.  
O jogo é um **platformer 2D** completo, com sistema de menu, inimigos animados, coleta de moedas, condição de vitória e trilha sonora.

---

## 📌 Funcionalidades

- 🎮 **Menu interativo**

  - Start Game
  - Music ON/OFF
  - Sounds ON/OFF
  - Quit

- 🧍 **Personagem jogável**

  - Movimento lateral
  - Pulo com física e gravidade
  - Animações (idle e walk)

- 👾 **Inimigos**

  - Patrulha inteligente em plataformas
  - Colisão letal

- 🪙 **Sistema de coleta**

  - Duas moedas posicionadas estrategicamente
  - Contador de moedas em tempo real

- 🏁 **Objetivo do jogo**

  - Colete as 2 moedas
  - Alcance a bandeira final para vencer

- 🎵 **Áudio**

  - Música de fundo
  - Sons de pulo, colisão e coleta

- 🧠 **Sistema de estados**
  - MENU → PLAYING → GAME_OVER / WIN

---

## 🛠️ Tecnologias

- **Python 3**
- **Pygame Zero**
- **Assets gráficos:** Kenney.nl

---

## 📂 Estrutura do Projeto

```text
PyGame/
│
├── main.py
├── README.md
│
├── images/
│   ├── player_*.png
│   ├── enemy_*.png
│   ├── coin_gold.png
│   ├── flag_green_*.png
│   └── terrain_*.png
│
├── sounds/
│   ├── jump.ogg
│   ├── hit.ogg
│   └── coin.ogg
│
└── music/
    └── background.ogg
```

---

## ▶️ Como Executar

1. Instale o Pygame Zero:

```bash
pip install pgzero
```

2. Execute o jogo:

```bash
python main.py
```

---

## 🎯 Controles

| Tecla | Ação             |
| ----- | ---------------- |
| ← / → | Mover personagem |
| ↑     | Pular            |
| Mouse | Navegar no menu  |

---

## 🏆 Condição de Vitória

O jogador vence ao:

1. Coletar **as 2 moedas**
2. Encostar na **bandeira final**

---

## 📸 Demonstração

_(adicione aqui prints do jogo, se desejar)_

---

## 📄 Licença

Projeto desenvolvido para fins educacionais e avaliativos.
Assets gráficos fornecidos por **Kenney.nl**.

---

Desenvolvido por **Paulo** 🚀
