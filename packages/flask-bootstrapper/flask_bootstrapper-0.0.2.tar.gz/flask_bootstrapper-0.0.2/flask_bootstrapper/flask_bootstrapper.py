import os
import pip
import codecs
from git import Repo

from django_crud_generator.django_crud_generator import render_template_with_args_in_file

# from django_bootstrapper.conf import *
PROJECT_ROOT_KEY = "project_root"
PROJECT_NAME_KEY = "project_name"


INVALID_OPTION_MESSAGE = "Invalid option"
VALIDATING_OPTIONS_MESSAGE = "Validating options"
OPTIONS_VALIDATED_MESSAGE = "Options validated"
INSTALLING_FLASK_MESSAGE = "Installing Flask"
CREATING_DIRECTORY_MESSAGE = "Creating directory"
DIRECTORY_ALREADY_EXISTS_MESSAGE = "Directory already exists"
CREATING_FLASK_PROJECT_MESSAGE = "Creating Flask project"
FLASK_PROJECT_CREATED_MESSAGE = "Flask project created"
INITIALIZING_GIT_REPOSITORY_MESSAGE = "Initializing git repository"

BASE_TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")


class FlaskBootstrapper(object):

    OPTION_DICT = {
        PROJECT_ROOT_KEY: "project",
        PROJECT_NAME_KEY: "blog_project",
    }

    def __init__(self):
        self.repository = None

    def update_options(self):
        for key, value in self.OPTION_DICT.items():
            string_to_show = "{} [{}]: ".format(key, value) if value else "{}: ".format(key)

            readed_value = input(string_to_show)
            self.OPTION_DICT[key] = readed_value if readed_value else value

    def valid_options(self):
        print(VALIDATING_OPTIONS_MESSAGE)
        self.OPTION_DICT[PROJECT_ROOT_KEY] = os.path.abspath(
            self.OPTION_DICT[PROJECT_ROOT_KEY]
        )
        return True

    @staticmethod
    def install_flask():
        print(INSTALLING_FLASK_MESSAGE)
        pip.main(['install', 'flask-sqlalchemy'])

    @staticmethod
    def create_directory(path):
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def create_file(path):
        return codecs.open(
            path,
            'w+',
            encoding='UTF-8'
        )

    @staticmethod
    def create_file_with_template_in_folder(file, path, templates_path, **kwargs):
        render_template_with_args_in_file(
            FlaskBootstrapper.create_file(
                os.path.join(
                    path,
                    file
                )
            ),
            os.path.join(templates_path, "{}.tmpl".format(file)),
            **kwargs
        )

    @staticmethod
    def create_flask_project(name, path):
        print(CREATING_FLASK_PROJECT_MESSAGE)

        # First create the main directory
        FlaskBootstrapper.create_directory(path)
        # With the readme
        FlaskBootstrapper.create_file_with_template_in_folder(
            "README.md",
            path,
            BASE_TEMPLATES_DIR,
            **{"project_name": name}
        )

        # And the project module folder
        project_folder = os.path.join(
            path,
            name
        )
        templates_project_folder = os.path.join(
            BASE_TEMPLATES_DIR,
            "project"
        )
        FlaskBootstrapper.create_directory(
            project_folder
        )
        # Creating files in the module level
        files_to_create = ["app", "config", "database"]
        for f in files_to_create:
            FlaskBootstrapper.create_file_with_template_in_folder(
                "{}.py".format(f),
                project_folder,
                templates_project_folder,
                **{}
            )

        # And the blueprint folder
        blueprint_folder = os.path.join(
            project_folder,
            "blueprints"
        )

    def initialize_git_repo(self, path):
        print(INITIALIZING_GIT_REPOSITORY_MESSAGE)
        self.repository = Repo.init(path)

    def execute(self):
        self.update_options()

        if not self.valid_options():
            print(INVALID_OPTION_MESSAGE)
            exit(1)
        else:
            print(OPTIONS_VALIDATED_MESSAGE)

        self.install_flask()
        self.create_directory(
            path=self.OPTION_DICT[PROJECT_ROOT_KEY]
        )
        self.create_flask_project(
            name=self.OPTION_DICT[PROJECT_NAME_KEY],
            path=self.OPTION_DICT[PROJECT_ROOT_KEY],
        )
        self.initialize_git_repo(
            path=self.OPTION_DICT[PROJECT_ROOT_KEY],
        )


def execute_from_command_line():
    flask_bootstrapper = FlaskBootstrapper()
    flask_bootstrapper.execute()


if __name__ == '__main__':
    execute_from_command_line()
