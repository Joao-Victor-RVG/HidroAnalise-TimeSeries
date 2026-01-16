#!/bin/bash
# Script de limpeza rápida - Alternative shell script

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

OUTPUT_DIR="output/graficos"

if [ ! -d "$OUTPUT_DIR" ]; then
    echo -e "${RED}❌ Erro: Pasta 'output/graficos' não encontrada!${NC}"
    exit 1
fi

show_help() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════════════╗"
    echo "║           HidroAnalise-TimeSeries: Script de Limpeza              ║"
    echo "╚════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "OPÇÕES:"
    echo "  ./clean.sh              # Remove apenas gráficos (PNG)"
    echo "  ./clean.sh --all        # Remove gráficos (PNG) + dados (CSV)"
    echo "  ./clean.sh --png        # Remove apenas PNG"
    echo "  ./clean.sh --csv        # Remove apenas CSV"
    echo "  ./clean.sh --help       # Mostra esta mensagem"
    echo ""
}

clean_png() {
    echo -e "${YELLOW}🗑️  Removendo arquivos PNG...${NC}\n"
    
    count=0
    
    # Remover PNG das pastas por estação
    for folder in campoalegre goianesia marzagao tresranchos Comparacao; do
        if [ -d "$OUTPUT_DIR/$folder" ]; then
            for file in $OUTPUT_DIR/$folder/*.png; do
                if [ -f "$file" ]; then
                    rm "$file"
                    echo -e "${GREEN}  ✓${NC} Removido: $folder/$(basename $file)"
                    ((count++))
                fi
            done
        fi
    done
    
    # Remover PNG dos gráficos GLM
    if [ -d "$OUTPUT_DIR/GLM_Predicoes" ]; then
        for subfolder in campoalegre goianesia marzagao tresranchos; do
            if [ -d "$OUTPUT_DIR/GLM_Predicoes/$subfolder" ]; then
                for file in $OUTPUT_DIR/GLM_Predicoes/$subfolder/*.png; do
                    if [ -f "$file" ]; then
                        rm "$file"
                        echo -e "${GREEN}  ✓${NC} Removido: GLM_Predicoes/$subfolder/$(basename $file)"
                        ((count++))
                    fi
                done
            fi
        done
    fi
    
    echo -e "\n${GREEN}✅ Total de PNG removidos: $count${NC}"
    return $count
}

clean_csv() {
    echo -e "${YELLOW}🗑️  Removendo arquivos CSV...${NC}\n"
    
    count=0
    
    # Remover CSV das pastas por estação
    for folder in campoalegre goianesia marzagao tresranchos Comparacao; do
        if [ -d "$OUTPUT_DIR/$folder" ]; then
            for file in $OUTPUT_DIR/$folder/*.csv; do
                if [ -f "$file" ]; then
                    rm "$file"
                    echo -e "${GREEN}  ✓${NC} Removido: $folder/$(basename $file)"
                    ((count++))
                fi
            done
        fi
    done
    
    # Remover CSV GLM
    if [ -f "$OUTPUT_DIR/GLM_Predicoes/metricas_glm.csv" ]; then
        rm "$OUTPUT_DIR/GLM_Predicoes/metricas_glm.csv"
        echo -e "${GREEN}  ✓${NC} Removido: GLM_Predicoes/metricas_glm.csv"
        ((count++))
    fi
    
    echo -e "\n${GREEN}✅ Total de CSV removidos: $count${NC}"
    return $count
}

# Processar argumentos
case "${1:-default}" in
    --all)
        echo -e "${YELLOW}╔════════════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${YELLOW}║        🧹 HidroAnalise-TimeSeries: Limpeza de Gráficos            ║${NC}"
        echo -e "${YELLOW}╚════════════════════════════════════════════════════════════════════╝${NC}\n"
        echo -e "${RED}⚠️  AVISO: Esta operação vai remover PNG + CSV!${NC}\n"
        read -p "Tem certeza? (s/n): " confirm
        if [ "$confirm" = "s" ]; then
            clean_png
            clean_csv
            echo -e "\n${GREEN}═══════════════════════════════════════════════════════════════════${NC}"
            echo -e "${GREEN}✅ Limpeza concluída!${NC}"
            echo -e "${GREEN}═══════════════════════════════════════════════════════════════════${NC}\n"
        else
            echo -e "${RED}❌ Operação cancelada.${NC}\n"
        fi
        ;;
    --csv)
        echo -e "${YELLOW}╔════════════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${YELLOW}║        🧹 HidroAnalise-TimeSeries: Limpeza de Dados              ║${NC}"
        echo -e "${YELLOW}╚════════════════════════════════════════════════════════════════════╝${NC}\n"
        echo -e "${RED}⚠️  AVISO: Esta operação vai remover CSV!${NC}\n"
        read -p "Tem certeza? (s/n): " confirm
        if [ "$confirm" = "s" ]; then
            clean_csv
            echo -e "\n${GREEN}═══════════════════════════════════════════════════════════════════${NC}"
            echo -e "${GREEN}✅ Limpeza concluída!${NC}"
            echo -e "${GREEN}═══════════════════════════════════════════════════════════════════${NC}\n"
        else
            echo -e "${RED}❌ Operação cancelada.${NC}\n"
        fi
        ;;
    --png)
        echo -e "${YELLOW}╔════════════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${YELLOW}║        🧹 HidroAnalise-TimeSeries: Limpeza de Gráficos            ║${NC}"
        echo -e "${YELLOW}╚════════════════════════════════════════════════════════════════════╝${NC}\n"
        echo -e "${RED}⚠️  AVISO: Esta operação vai remover PNG!${NC}\n"
        read -p "Tem certeza? (s/n): " confirm
        if [ "$confirm" = "s" ]; then
            clean_png
            echo -e "\n${GREEN}═══════════════════════════════════════════════════════════════════${NC}"
            echo -e "${GREEN}✅ Limpeza concluída!${NC}"
            echo -e "${GREEN}═══════════════════════════════════════════════════════════════════${NC}\n"
        else
            echo -e "${RED}❌ Operação cancelada.${NC}\n"
        fi
        ;;
    --help|-h)
        show_help
        ;;
    default)
        echo -e "${YELLOW}╔════════════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${YELLOW}║        🧹 HidroAnalise-TimeSeries: Limpeza de Gráficos            ║${NC}"
        echo -e "${YELLOW}╚════════════════════════════════════════════════════════════════════╝${NC}\n"
        echo -e "${RED}⚠️  AVISO: Esta operação vai remover PNG (gráficos)!${NC}\n"
        read -p "Tem certeza? (s/n): " confirm
        if [ "$confirm" = "s" ]; then
            clean_png
            echo -e "\n${GREEN}═══════════════════════════════════════════════════════════════════${NC}"
            echo -e "${GREEN}✅ Limpeza concluída!${NC}"
            echo -e "${GREEN}═══════════════════════════════════════════════════════════════════${NC}\n"
        else
            echo -e "${RED}❌ Operação cancelada.${NC}\n"
        fi
        ;;
esac
