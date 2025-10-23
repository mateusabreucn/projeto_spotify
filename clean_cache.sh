#!/bin/bash
# Script para limpar TODOS os caches do projeto

echo "🧹 Limpando todos os caches..."
echo ""

# 1. Limpa cache do Streamlit
echo "1️⃣  Limpando cache do Streamlit..."
rm -rf ~/.streamlit/cache
echo "   ✅ Streamlit cache limpo"
echo ""

# 2. Limpa __pycache__ do projeto
echo "2️⃣  Limpando __pycache__..."
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
echo "   ✅ __pycache__ limpo"
echo ""

# 3. Limpa cache do kagglehub
echo "3️⃣  Limpando cache do kagglehub..."
rm -rf ~/.cache/kagglehub
echo "   ✅ Kagglehub cache limpo"
echo ""

# 4. Limpa cache customizado do projeto
echo "4️⃣  Limpando cache customizado (spotify_analyzer)..."
rm -rf ~/.cache/spotify_analyzer
echo "   ✅ Spotify analyzer cache limpo"
echo ""

# 5. Limpa arquivo .streamlit/
echo "5️⃣  Limpando .streamlit/"
rm -rf .streamlit/
echo "   ✅ .streamlit/ limpo"
echo ""

echo "✅ Limpeza concluída!"
echo ""
echo "📝 Próximas ações:"
echo "   1. Execute: streamlit run app.py"
echo "   2. A app irá baixar o novo dataset"
echo "   3. Verifique se é o dataset correto"
