# stockfish_demo
https://github.com/official-stockfish/Stockfish
https://jamesmccaffreyblog.com/2024/05/02/programmatically-analyzing-chess-games-using-stockfish-with-python/

python3 -m venv venv
pip install stockfish
source venv/bin/activate
pip install stockfish

macos
wget https://github.com/official-stockfish/Stockfish/releases/latest/download/stockfish-macos-m1-apple-silicon.tar

linux
https://github.com/official-stockfish/Stockfish/releases/latest/download/stockfish-android-armv8.tar

cd src
make -j profile-build
