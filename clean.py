#!/usr/bin/env python3
"""
Script de Limpeza - Remove gráficos e arquivos temporários

Uso:
    python clean.py              # Remove apenas PNG
    python clean.py --all        # Remove PNG + CSV
    python clean.py --help       # Mostra ajuda
"""

import os
import shutil
from pathlib import Path
import sys

OUTPUT_DIR = Path("output/graficos")

def limpar_png():
    """Remove todos os arquivos PNG dos gráficos."""
    print("🗑️  Removendo arquivos PNG...\n")
    
    total_removidos = 0
    
    # Pastas a limpar
    pastas = ["campoalegre", "goianesia", "marzagao", "tresranchos", "Comparacao"]
    subpastas_glm = ["campoalegre", "goianesia", "marzagao", "tresranchos"]
    
    # Limpar gráficos por estação
    for pasta in pastas:
        pasta_path = OUTPUT_DIR / pasta
        if pasta_path.exists():
            pngs = list(pasta_path.glob("*.png"))
            for png in pngs:
                png.unlink()
                total_removidos += 1
                print(f"  ✓ Removido: {pasta}/{png.name}")
    
    # Limpar gráficos GLM
    glm_dir = OUTPUT_DIR / "GLM_Predicoes"
    if glm_dir.exists():
        for subpasta in subpastas_glm:
            subpasta_path = glm_dir / subpasta
            if subpasta_path.exists():
                pngs = list(subpasta_path.glob("*.png"))
                for png in pngs:
                    png.unlink()
                    total_removidos += 1
                    print(f"  ✓ Removido: GLM_Predicoes/{subpasta}/{png.name}")
    
    print(f"\n✅ Total de PNG removidos: {total_removidos}")
    return total_removidos

def limpar_csv():
    """Remove todos os arquivos CSV gerados."""
    print("\n🗑️  Removendo arquivos CSV...\n")
    
    total_removidos = 0
    
    # Pastas a limpar
    pastas = ["campoalegre", "goianesia", "marzagao", "tresranchos", "Comparacao"]
    
    # Limpar CSVs por estação
    for pasta in pastas:
        pasta_path = OUTPUT_DIR / pasta
        if pasta_path.exists():
            csvs = list(pasta_path.glob("*.csv"))
            for csv in csvs:
                csv.unlink()
                total_removidos += 1
                print(f"  ✓ Removido: {pasta}/{csv.name}")
    
    # Limpar CSV GLM
    glm_dir = OUTPUT_DIR / "GLM_Predicoes"
    if glm_dir.exists():
        csv_principal = glm_dir / "metricas_glm.csv"
        if csv_principal.exists():
            csv_principal.unlink()
            total_removidos += 1
            print(f"  ✓ Removido: GLM_Predicoes/metricas_glm.csv")
    
    print(f"\n✅ Total de CSV removidos: {total_removidos}")
    return total_removidos

def mostrar_ajuda():
    """Mostra informações de uso."""
    print("""
╔════════════════════════════════════════════════════════════════════╗
║           HidroAnalise-TimeSeries: Script de Limpeza              ║
╚════════════════════════════════════════════════════════════════════╝

OPÇÕES:
  python clean.py              # Remove apenas gráficos (PNG)
  python clean.py --all        # Remove gráficos (PNG) + dados (CSV)
  python clean.py --png        # Remove apenas PNG (explícito)
  python clean.py --csv        # Remove apenas CSV
  python clean.py --help       # Mostra esta mensagem

EXEMPLOS:

  1. Limpar só os gráficos gerados:
     $ python clean.py

  2. Limpar gráficos e arquivos de dados:
     $ python clean.py --all

  3. Limpar apenas CSVs:
     $ python clean.py --csv

DIRETÓRIOS AFETADOS:
  ✓ output/graficos/campoalegre/
  ✓ output/graficos/goianesia/
  ✓ output/graficos/marzagao/
  ✓ output/graficos/tresranchos/
  ✓ output/graficos/Comparacao/
  ✓ output/graficos/GLM_Predicoes/

ESTRUTURA DE PASTAS PRESERVADA:
  As pastas não serão deletadas, apenas os arquivos dentro delas.

CUIDADO:
  ⚠️  Esta operação não pode ser desfeita!
  ⚠️  Certifique-se antes de executar.
""")

def main():
    """Função principal."""
    if not OUTPUT_DIR.exists():
        print("❌ Erro: Pasta 'output/graficos' não encontrada!")
        sys.exit(1)
    
    # Processar argumentos
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    
    if "--help" in args or "-h" in args:
        mostrar_ajuda()
        return
    
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║        🧹 HidroAnalise-TimeSeries: Limpeza de Gráficos            ║")
    print("╚════════════════════════════════════════════════════════════════════╝\n")
    
    # Confirmar antes de deletar
    print("⚠️  AVISO: Esta operação vai remover arquivos gerados!\n")
    
    if "--all" in args:
        print("Modo: REMOVER PNG + CSV\n")
        confirmacao = input("Tem certeza? (s/n): ").strip().lower()
        if confirmacao == "s":
            png_count = limpar_png()
            csv_count = limpar_csv()
            print(f"\n{'='*70}")
            print(f"✅ Limpeza concluída! Total: {png_count + csv_count} arquivos removidos")
            print(f"{'='*70}\n")
        else:
            print("❌ Operação cancelada.\n")
    
    elif "--csv" in args:
        print("Modo: REMOVER APENAS CSV\n")
        confirmacao = input("Tem certeza? (s/n): ").strip().lower()
        if confirmacao == "s":
            csv_count = limpar_csv()
            print(f"\n{'='*70}")
            print(f"✅ Limpeza concluída! Total: {csv_count} arquivos removidos")
            print(f"{'='*70}\n")
        else:
            print("❌ Operação cancelada.\n")
    
    else:  # Padrão: remove PNG
        print("Modo: REMOVER PNG (gráficos)\n")
        confirmacao = input("Tem certeza? (s/n): ").strip().lower()
        if confirmacao == "s":
            png_count = limpar_png()
            print(f"\n{'='*70}")
            print(f"✅ Limpeza concluída! Total: {png_count} gráficos removidos")
            print(f"{'='*70}\n")
        else:
            print("❌ Operação cancelada.\n")

if __name__ == "__main__":
    main()
