"""Script para treinar o modelo de classificação de vibes.

Este script:
1. Carrega o dataset completo do Kaggle
2. Rotula cada música usando as regras heurísticas existentes
3. Treina um classificador Random Forest
4. Salva o modelo treinado para uso na aplicação
"""

import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from src.config import FEATURE_COLS, VIBE_LABELS_EXTENDED
from src.dataset_manager import load_kaggle_dataset

# Diretório para salvar o modelo
MODEL_DIR = Path("models")
MODEL_FILE = MODEL_DIR / "vibe_classifier.pkl"
SCALER_FILE = MODEL_DIR / "vibe_scaler.pkl"


def calculate_vibe_scores(row: pd.Series) -> dict[str, float]:
    """Calcula scores heurísticos para cada vibe baseado em features.

    Mesmo algoritmo usado anteriormente, mas aplicado linha por linha.
    """
    dance = row.get("danceability", 0)
    energ = row.get("energy", 0)
    acous = row.get("acousticness", 0)
    instr = row.get("instrumentalness", 0)
    lived = row.get("liveness", 0)
    valen = row.get("valence", 0)
    tempo = row.get("tempo", 0)
    speec = row.get("speechiness", 0)
    loudn = row.get("loudness", 0)

    # Normalizar tempo para 0-1 (range: 0-246 BPM)
    tempo_norm = tempo / 246.0 if tempo > 0 else 0

    # Normalizar loudness para 0-1 (range: -60 a 5 dB)
    loudn_norm = (loudn - (-60)) / (5 - (-60)) if loudn >= -60 else 0
    loudn_norm = np.clip(loudn_norm, 0, 1)

    return {
        "Party / Upbeat": (
            0.30 * energ
            + 0.25 * dance
            + 0.15 * valen
            + 0.15 * loudn_norm
            + 0.10 * tempo_norm
            + 0.05 * speec
        ),
        "Chill / Acoustic": (
            0.35 * acous
            + 0.25 * lived
            + 0.15 * (1 - energ)
            + 0.15 * (1 - loudn_norm)
            + 0.10 * (1 - dance)
        ),
        "Happy / Feel-good": (
            0.35 * valen
            + 0.25 * dance
            + 0.20 * energ
            + 0.10 * tempo_norm
            + 0.10 * loudn_norm
        ),
        "Dark / Intense": (
            0.30 * energ
            + 0.25 * (1 - valen)
            + 0.20 * loudn_norm
            + 0.15 * speec
            + 0.10 * (1 - acous)
        ),
        "Instrumental / Dreamy": (
            0.40 * instr
            + 0.20 * energ
            + 0.15 * acous
            + 0.15 * lived
            + 0.10 * (1 - speec)
        ),
        "Romantic / Smooth": (
            0.30 * acous
            + 0.25 * valen
            + 0.20 * (1 - energ)
            + 0.15 * (1 - loudn_norm)
            + 0.10 * dance
        ),
        "Energetic / Aggressive": (
            0.35 * energ
            + 0.25 * loudn_norm
            + 0.20 * speec
            + 0.15 * (1 - acous)
            + 0.05 * tempo_norm
        ),
        "Melancholic / Sad": (
            0.30 * (1 - valen)
            + 0.28 * acous
            + 0.20 * (1 - loudn_norm)
            + 0.12 * (1 - energ)
            + 0.10 * lived
        ),
    }


def assign_vibe_label(row: pd.Series) -> str:
    """Atribui a vibe com maior score para uma música."""
    scores = calculate_vibe_scores(row)
    return max(scores, key=scores.get)


def label_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Rotula todo o dataset usando as regras heurísticas."""
    print("📊 Iniciando rotulação do dataset...")
    print(f"   Total de músicas: {len(df):,}")

    # Remove linhas com NaN nas features
    df_clean = df.dropna(subset=FEATURE_COLS).copy()
    print(f"   Músicas válidas (sem NaN): {len(df_clean):,}")

    # Aplica rotulação
    print("🏷️  Aplicando regras heurísticas para rotular...")
    df_clean["vibe"] = df_clean.apply(assign_vibe_label, axis=1)

    # Mostra distribuição
    print("\n📈 Distribuição de vibes no dataset:")
    vibe_counts = df_clean["vibe"].value_counts()
    for vibe, count in vibe_counts.items():
        pct = (count / len(df_clean)) * 100
        print(f"   {vibe:25s}: {count:7,} ({pct:5.2f}%)")

    return df_clean


def train_classifier(df_labeled: pd.DataFrame):
    """Treina o classificador Random Forest."""
    print("\n🤖 Iniciando treinamento do classificador...")

    # Prepara features e labels
    X = df_labeled[FEATURE_COLS].values
    y = df_labeled["vibe"].values

    print(f"   Features shape: {X.shape}")
    print(f"   Labels shape: {y.shape}")
    print(f"   Classes únicas: {len(np.unique(y))}")

    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"\n📊 Split dos dados:")
    print(f"   Treino: {len(X_train):,} músicas")
    print(f"   Teste:  {len(X_test):,} músicas")

    # Normalização
    print("\n⚙️  Normalizando features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Treinamento
    print("\n🎯 Treinando Random Forest Classifier...")
    print("   Parâmetros:")
    print("   - n_estimators: 200")
    print("   - max_depth: 20")
    print("   - min_samples_split: 5")
    print("   - random_state: 42")
    print("   - n_jobs: -1 (todos os cores)")

    classifier = RandomForestClassifier(
        n_estimators=200,
        max_depth=20,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1,
        verbose=1,
    )

    classifier.fit(X_train_scaled, y_train)

    print("\n✅ Treinamento concluído!")

    # Avaliação
    print("\n📈 Avaliando modelo...")
    train_score = classifier.score(X_train_scaled, y_train)
    test_score = classifier.score(X_test_scaled, y_test)

    print(f"   Acurácia (treino): {train_score:.4f} ({train_score*100:.2f}%)")
    print(f"   Acurácia (teste):  {test_score:.4f} ({test_score*100:.2f}%)")

    # Predições
    y_pred = classifier.predict(X_test_scaled)

    # Classification Report
    print("\n📊 Relatório de Classificação:")
    print(classification_report(y_test, y_pred, zero_division=0))

    # Confusion Matrix
    print("\n🔢 Matriz de Confusão:")
    cm = confusion_matrix(y_test, y_pred, labels=VIBE_LABELS_EXTENDED)
    print("Linhas=Real, Colunas=Predito")
    print(f"Classes: {VIBE_LABELS_EXTENDED}")
    print(cm)

    # Feature Importance
    print("\n🎼 Importância das Features:")
    feature_importance = pd.DataFrame({
        'feature': FEATURE_COLS,
        'importance': classifier.feature_importances_
    }).sort_values('importance', ascending=False)

    for _, row in feature_importance.iterrows():
        print(f"   {row['feature']:20s}: {row['importance']:.4f}")

    return classifier, scaler, test_score


def save_model(classifier, scaler):
    """Salva o modelo e scaler treinados."""
    print(f"\n💾 Salvando modelo em {MODEL_FILE}...")

    MODEL_DIR.mkdir(exist_ok=True)

    # Salva classificador
    with open(MODEL_FILE, "wb") as f:
        pickle.dump(classifier, f)

    # Salva scaler
    with open(SCALER_FILE, "wb") as f:
        pickle.dump(scaler, f)

    print("✅ Modelo salvo com sucesso!")
    print(f"   Classificador: {MODEL_FILE}")
    print(f"   Scaler: {SCALER_FILE}")


def main():
    """Pipeline completo de treinamento."""
    print("=" * 70)
    print("🎵 TREINAMENTO DO CLASSIFICADOR DE VIBES")
    print("=" * 70)

    # 1. Carrega dataset
    print("\n📥 ETAPA 1: Carregando dataset...")
    df = load_kaggle_dataset()
    print(f"✅ Dataset carregado: {len(df):,} músicas")

    # 2. Rotula dataset
    print("\n🏷️  ETAPA 2: Rotulando dataset...")
    df_labeled = label_dataset(df)

    # 3. Treina classificador
    print("\n🤖 ETAPA 3: Treinando classificador...")
    classifier, scaler, accuracy = train_classifier(df_labeled)

    # 4. Salva modelo
    print("\n💾 ETAPA 4: Salvando modelo...")
    save_model(classifier, scaler)

    # Resumo final
    print("\n" + "=" * 70)
    print("✅ TREINAMENTO CONCLUÍDO COM SUCESSO!")
    print("=" * 70)
    print(f"📊 Dataset rotulado: {len(df_labeled):,} músicas")
    print(f"🎯 Acurácia no teste: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"💾 Modelo salvo em: {MODEL_FILE}")
    print("\n🚀 Você pode agora usar o modelo na aplicação!")
    print("   Execute: streamlit run app.py")
    print("=" * 70)


if __name__ == "__main__":
    main()
