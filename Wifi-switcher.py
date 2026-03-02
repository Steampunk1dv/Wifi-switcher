#!/usr/bin/env python3
"""Aplicativo simples para ligar e desligar o Wi‑Fi com dois botões."""

from __future__ import annotations

import platform
import shutil
import subprocess
import tkinter as tk
from tkinter import messagebox


WINDOWS_INTERFACE_NAME = "Wi-Fi"
LINUX_INTERFACE_NAME = "wlan0"


def run_command(command: list[str]) -> tuple[bool, str]:
    """Executa um comando no sistema e retorna sucesso + saída."""
    try:
        completed = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return False, f"Comando não encontrado: {command[0]}"
    except subprocess.CalledProcessError as error:
        output = (error.stderr or error.stdout or "").strip()
        return False, output or "Falha ao executar o comando."

    output = (completed.stdout or completed.stderr or "").strip()
    return True, output or "Comando executado com sucesso."


def get_wifi_command(enable: bool) -> list[str]:
    """Monta o comando correto para o sistema operacional atual."""
    system_name = platform.system().lower()

    if system_name == "windows":
        state = "enabled" if enable else "disabled"
        return [
            "netsh",
            "interface",
            "set",
            "interface",
            WINDOWS_INTERFACE_NAME,
            f"admin={state}",
        ]

    if system_name == "linux":
        if shutil.which("nmcli"):
            state = "on" if enable else "off"
            return ["nmcli", "radio", "wifi", state]

        state = "up" if enable else "down"
        return ["ip", "link", "set", LINUX_INTERFACE_NAME, state]

    raise RuntimeError(
        "Sistema operacional não suportado por este app. "
        "Use Windows ou Linux."
    )


def toggle_wifi(enable: bool) -> None:
    """Liga ou desliga o Wi‑Fi usando o comando do sistema."""
    action = "ligar" if enable else "desligar"

    try:
        command = get_wifi_command(enable)
    except RuntimeError as error:
        messagebox.showerror("Erro", str(error))
        return

    success, output = run_command(command)

    if success:
        messagebox.showinfo("Sucesso", f"Wi‑Fi {action} com sucesso.\n\n{output}")
    else:
        messagebox.showerror(
            "Falha",
            "Não foi possível alterar o estado do Wi‑Fi.\n"
            "Talvez seja necessário rodar como administrador.\n\n"
            f"Detalhes: {output}",
        )


def build_ui() -> tk.Tk:
    """Cria a interface gráfica com dois botões."""
    app = tk.Tk()
    app.title("Wi‑Fi Switcher")
    app.geometry("320x180")
    app.resizable(False, False)

    title = tk.Label(app, text="Controle de Wi‑Fi", font=("Arial", 16, "bold"))
    title.pack(pady=(20, 10))

    button_on = tk.Button(
        app,
        text="Ligar Wi‑Fi",
        bg="#2e7d32",
        fg="white",
        width=18,
        height=2,
        command=lambda: toggle_wifi(True),
    )
    button_on.pack(pady=6)

    button_off = tk.Button(
        app,
        text="Desligar Wi‑Fi",
        bg="#c62828",
        fg="white",
        width=18,
        height=2,
        command=lambda: toggle_wifi(False),
    )
    button_off.pack(pady=6)

    return app


if __name__ == "__main__":
    ui = build_ui()
    ui.mainloop()
