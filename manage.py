import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def main():
    env_path = Path(__file__).resolve().parent / '.env'
    load_dotenv(dotenv_path=env_path)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.getenv('DJANGO_SETTINGS_MODULE'))

    # RUN_MAIN 환경 변수를 확인하여 프린트문이 두 번 실행되지 않도록 함
    if os.environ.get('RUN_MAIN') or os.environ.get('WERKZEUG_RUN_MAIN'):
        # 현재 사용 중인 settings 파일 출력
        settings_module = os.getenv('DJANGO_SETTINGS_MODULE')

        print('########################################################################')
        print(f"# Using settings module: [{settings_module}]")
        print('########################################################################')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
