import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lab07.app import ServerApplication
from lab07.cli import CLI
from lab07.storage import load, save


DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")


def main() -> None:
    print("📂 Загрузка данных...")
    collection = load(DATA_FILE)
    print(f"✅ Загружено {len(collection)} серверов")
    
    app = ServerApplication(collection)
    cli = CLI(app)
    
    cli.run()
    
    print("💾 Сохранение данных...")
    save(app.collection, DATA_FILE)
    print("✅ Готово!")


if __name__ == "__main__":
    main()