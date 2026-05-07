import sys
import subprocess
import importlib.util
import os
# ------------ DEP. OBRIGATORIAS ------------ #
def dep():
    dep_map = {
        "discord": "discord.py",
        "colorama": "colorama",
        "httpx": "httpx",
        "dotenv": "python-dotenv"    
    }
    dep_faltando = []
    for modulo, pacote in dep_map.items():
        if importlib.util.find_spec(modulo) is None:
            dep_faltando.append(pacote)
    
    if dep_faltando:
        print(f"[INFO]: Instalando dependencias: {', '.join(dep_faltando)}")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + dep_faltando)
        print(f"[INFO]: Instalação concluida. Reiniciando...")
        os.execv(sys.executable, [sys.executable] + sys.argv)
