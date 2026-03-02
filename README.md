# Wi-Fi Switcher

Programa simples em Python com **dois botões**:
- **Ligar Wi‑Fi**
- **Desligar Wi‑Fi**

## Requisitos

- Python 3
- Tkinter (normalmente já vem com Python)

## Como executar

```bash
python3 wifi_switcher.py
```

## Observações importantes

- Em muitos sistemas, ligar/desligar Wi‑Fi exige permissões de administrador.
- No Linux, o app tenta usar `nmcli`. Se não existir, tenta `ip link` usando a interface padrão `wlan0`.
- No Windows, o app usa `netsh` na interface `Wi-Fi`.

Se o nome da sua interface for diferente, altere as constantes no topo do arquivo `wifi_switcher.py`.
Feito por fins educativos
