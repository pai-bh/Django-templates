import os
import shutil
from django.core.management.commands.startapp import Command as StartAppCommand
from django.template import Template, Context
from django.conf import settings

class Command(StartAppCommand):
    help = 'Creates a Django app directory structure for the given app name in the apps directory.'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='The name of the application.')
        parser.add_argument('directory', nargs='?', help='Optional destination directory')
        parser.add_argument(
            '--template',
            help='The path or URL to load the template from.',
        )
        parser.add_argument(
            '--extension', '-e', dest='extensions',
            help='The file extension(s) to render (default: "py,txt").',
            default='py,txt',
        )
        parser.add_argument(
            '--name', '-n', dest='files',
            help='The file name(s) to render (default: "__init__.py").',
            default='__init__.py',
        )

    def handle(self, *args, **options):
        app_name = options['name']
        target_directory = options['directory'] or os.path.join('apps', app_name)
        options['directory'] = target_directory

        # Create the target directory if it doesn't exist
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)

        # Call the parent class handle method with updated options
        options['name'] = app_name
        options['extensions'] = options.get('extensions', 'py,txt')
        options['files'] = options.get('files', '__init__.py')

        super().handle(**options)

        # Add additional structure
        app_path = os.path.abspath(target_directory)
        self.create_additional_structure(app_path, app_name)

        # Update project's urls.py and settings.py
        self.add_app_to_project(app_name)

    def create_additional_structure(self, app_path, app_name):
        self.create_templates_structure(app_path, app_name)
        self.create_static_structure(app_name)
        self.create_apps_py(app_path, app_name)
        self.process_templates(app_path, app_name)

    def create_templates_structure(self, app_path, app_name):
        template_path = os.path.join(os.path.dirname(__file__), '../../app_skeleton')

        for root, dirs, files in os.walk(template_path):
            for filename in files:
                full_file_name = os.path.join(root, filename)
                relative_path = os.path.relpath(full_file_name, template_path)
                target_path = os.path.join(app_path, relative_path)
                target_dir = os.path.dirname(target_path)

                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)

                if "templates/example.html" in full_file_name:
                    target_path = os.path.join(app_path, 'templates', app_name, 'example.html')
                    target_dir = os.path.dirname(target_path)
                    if not os.path.exists(target_dir):
                        os.makedirs(target_dir)
                shutil.copy(full_file_name, target_path)

    def create_static_structure(self, app_name):
        static_dir = os.path.join(settings.BASE_DIR, 'static', app_name)
        os.makedirs(os.path.join(static_dir, 'css'), exist_ok=True)
        os.makedirs(os.path.join(static_dir, 'js'), exist_ok=True)
        os.makedirs(os.path.join(static_dir, 'images'), exist_ok=True)

    def create_apps_py(self, app_path, app_name):
        apps_template = '''from django.apps import AppConfig


class {{ camel_case_app_name }}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '{{ app_full_name }}'
'''

        camel_case_app_name = ''.join(word.title() for word in app_name.split('_'))
        apps_py_content = Template(apps_template).render(Context({
            'camel_case_app_name': camel_case_app_name,
            'app_full_name': f'apps.{app_name}'
        }))

        with open(os.path.join(app_path, 'apps.py'), 'w') as f:
            f.write(apps_py_content)

    def process_templates(self, app_path, app_name):
        for root, dirs, files in os.walk(app_path):
            for file in files:
                if file.endswith('.py') or file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        content = f.read()
                    content = content.replace('{{app_name}}', app_name)
                    with open(file_path, 'w') as f:
                        f.write(content)

    def add_app_to_project(self, app_name):
        base_dir = settings.BASE_DIR
        project_urls_path = os.path.join(base_dir, 'urls.py')
        project_settings_path = os.path.join(base_dir, 'settings/base.py')

        # Add app to project urls.py
        app_include_statement = f"    path('{app_name}/', include('apps.{app_name}.urls')),\n"
        with open(project_urls_path, 'r+') as urls_file:
            content = urls_file.readlines()
            if app_include_statement not in content:
                content.insert(-1, app_include_statement)
                urls_file.seek(0)
                urls_file.writelines(content)

        # Add app to project settings/base.py
        app_config = f"    'apps.{app_name}',\n"
        with open(project_settings_path, 'r+') as settings_file:
            content = settings_file.readlines()
            if app_config not in content:
                index = content.index("INSTALLED_APPS = [\n") + 1
                content.insert(index, app_config)
                settings_file.seek(0)
                settings_file.writelines(content)
