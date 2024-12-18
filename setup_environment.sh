#!/bin/bash

# リポジトリのルートディレクトリを取得
PROJECT_ROOT=$(git rev-parse --show-toplevel)
if [ $? -ne 0 ]; then
    echo "Error: This script must be run inside a Git repository."
    exit 1
fi


setup_python_environment() {
    VENV_DIR="$PROJECT_ROOT/.venv"

    echo "Setting up Python environment..."

    # 仮想環境が存在しない場合は作成
    if [ ! -d "$VENV_DIR" ]; then
        echo "Creating virtual environment..."
        python3 -m venv "$VENV_DIR"
        echo "Virtual environment created at $VENV_DIR"
    else
        echo "Virtual environment already exists at $VENV_DIR"
    fi

    # 仮想環境をアクティブ化
    if [ "$(uname)" == "Darwin" ] || [ "$(uname)" == "Linux" ]; then
        source $VENV_DIR/bin/activate
    elif [ "$(uname)" == "MINGW"* ] || [ "$(uname)" == "CYGWIN"* ]; then
        source $VENV_DIR/Scripts/activate
    else
        echo "Unsupported OS. Please activate the virtual environment manually."
        exit 1
    fi
    echo "Virtual environment activated."

    # 依存関係をインストール
    echo "Upgrading pip..."
    pip install --upgrade pip
    echo "Installing dependencies..."
    pip install -e .
    echo "Dependencies installed."

    echo "Python environment setup complete!"
}


# メイン処理
main() {
    cd "$PROJECT_ROOT" || exit 1

    # Python環境のセットアップ
    setup_python_environment
    echo

    echo "All done!"
}

main