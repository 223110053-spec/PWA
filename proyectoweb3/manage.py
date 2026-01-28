import os, sys
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dani.settings')
    try:
        from django.core.management import execute_from_command_line
    except Exception as exc:
        print('Django is required to run this project. Install with: pip install django')
        raise
    execute_from_command_line(sys.argv)
