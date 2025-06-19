#!/bin/bash
# DarkDeepSeek Terminal - Elite Cybersecurity Platform by WaiperOK
# Copyright (C) 2025 WaiperOK - https://github.com/WaiperOK/DarkDeepS

# Цвета для красивого вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ASCII арт
echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║██████╗  █████╗ ██████╗ ██╗  ██╗██████╗ ███████╗███████╗██████╗ ███████╗██╗  ██╗║"
echo "║██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔════╝██║ ██╔╝║"
echo "║██║  ██║███████║██████╔╝█████╔╝ ██║  ██║█████╗  █████╗  ██████╔╝███████╗█████╔╝ ║"
echo "║██║  ██║██╔══██║██╔══██╗██╔═██╗ ██║  ██║██╔══╝  ██╔══╝  ██╔═══╝ ╚════██║██╔═██╗ ║"
echo "║██████╔╝██║  ██║██║  ██║██║  ██╗██████╔╝███████╗███████╗██║     ███████║██║  ██╗║"
echo "║╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${CYAN}DarkDeepSeek Terminal - Elite Cybersecurity Platform by WaiperOK${NC}"
echo -e "${YELLOW}Copyright (C) 2025 WaiperOK - https://github.com/WaiperOK/DarkDeepS${NC}"
echo

# Проверка Python
echo -e "${BLUE}Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✓ Python3 found: $(python3 --version)${NC}"
elif command -v python &> /dev/null; then
    echo -e "${GREEN}✓ Python found: $(python --version)${NC}"
else
    echo -e "${RED}✗ Python not found! Please install Python 3.8+${NC}"
    exit 1
fi

# Проверка зависимостей
echo -e "${BLUE}Checking dependencies...${NC}"
if [ -f "requirements.txt" ]; then
    echo -e "${YELLOW}Installing requirements...${NC}"
    pip install -r requirements.txt
else
    echo -e "${YELLOW}requirements.txt not found, skipping dependency check${NC}"
fi

# Запуск приложения
echo -e "${GREEN}Starting DarkDeepSeek Terminal...${NC}"
echo

if command -v python3 &> /dev/null; then
    python3 run.py
elif command -v python &> /dev/null; then
    python run.py
else
    echo -e "${RED}Failed to start application${NC}"
    exit 1
fi 