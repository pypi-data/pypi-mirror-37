import os
import pip
from git import Repo

# from django_bootstrapper.conf import *
DJANGO_VERSION_KEY = "django_version"
TEMPLATE_SUBMODULE_NAME_KEY = "template_folder_name"
PROJECT_ROOT_KEY = "project_root"
PROJECT_NAME_KEY = "project_name"
VERBOSITY_KEY = 0

INVALID_OPTION_MESSAGE = "Invalid option"
VALIDATING_OPTIONS_MESSAGE = "Validating options"
OPTIONS_VALIDATED_MESSAGE = "Options validated"
INSTALLING_DJANGO_MESSAGE = "Installing django"
CREATING_DIRECTORY_MESSAGE = "Creating directory"
DIRECTORY_ALREADY_EXISTS_MESSAGE = "Directory already exists"
CREATING_DJANGO_PROJECT_MESSAGE = "Creating Django project"
DJANGO_PROJECT_CREATED_MESSAGE = "Django project created"
INITIALIZING_GIT_REPOSITORY_MESSAGE = "Initializing git repository"
CREATING_SUBMODULES_MESSAGE = "Creating submodules"
SUBMODULE_ADDED_MESSAGE = "{} submodule added"


class DjangoBootstrapper(object):

    OPTION_DICT = {
        DJANGO_VERSION_KEY: 2.1,
        TEMPLATE_SUBMODULE_NAME_KEY: "contraslash/template_cdn_bootstrap",
        PROJECT_ROOT_KEY: "",
        PROJECT_NAME_KEY: "",
        VERBOSITY_KEY: 0
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
    def install_django(version):
        print(INSTALLING_DJANGO_MESSAGE)
        pip.main(['install', 'django~={}'.format(version)])

    @staticmethod
    def create_django_project(name, path, verbosity):
        print(CREATING_DJANGO_PROJECT_MESSAGE)
        from django.core.management import execute_from_command_line
        # command.handle('project', name, path, verbosity=verbosity)
        execute_from_command_line(['django-admin', 'startproject', name, path])
        print(DJANGO_PROJECT_CREATED_MESSAGE)

    def initialize_git_repo(self, path, template_repo):
        print(INITIALIZING_GIT_REPOSITORY_MESSAGE)
        self.repository = Repo.init(path)
        print(CREATING_SUBMODULES_MESSAGE)
        self.repository.create_submodule(
            "base",
            os.path.join(path,"base"),
            "https://github.com/contraslash/base-django",
        )
        print(SUBMODULE_ADDED_MESSAGE.format("base"))
        applications_folder = os.path.join(path, "applications")
        if not os.path.exists(applications_folder):
            os.makedirs(applications_folder)
        open(os.path.join(applications_folder, "__init__.py"), "w+")
        self.repository.create_submodule(
            "authentication",
            os.path.join(path, "applications/authentication"),
            "https://github.com/contraslash/authentication-django",
        )
        print(SUBMODULE_ADDED_MESSAGE.format("authentication"))
        self.repository.create_submodule(
            "template",
            os.path.join(path, "applications/base_template"),
            "https://github.com/{}".format(template_repo),
        )
        print(SUBMODULE_ADDED_MESSAGE.format("base_template"))


    @staticmethod
    def create_directory(path):
        if not os.path.exists(path):
            os.makedirs(path)

    def execute(self):
        self.update_options()

        if not self.valid_options():
            print(INVALID_OPTION_MESSAGE)
            exit(1)
        else:
            print(OPTIONS_VALIDATED_MESSAGE)

        self.install_django(
            version=self.OPTION_DICT[DJANGO_VERSION_KEY]
        )
        self.create_directory(
            path=self.OPTION_DICT[PROJECT_ROOT_KEY]
        )
        self.create_django_project(
            name=self.OPTION_DICT[PROJECT_NAME_KEY],
            path=self.OPTION_DICT[PROJECT_ROOT_KEY],
            verbosity=self.OPTION_DICT[VERBOSITY_KEY]
        )
        self.initialize_git_repo(
            path=self.OPTION_DICT[PROJECT_ROOT_KEY],
            template_repo=self.OPTION_DICT[TEMPLATE_SUBMODULE_NAME_KEY]
        )


def execute_from_command_line():
    django_bootstrapper = DjangoBootstrapper()
    django_bootstrapper.execute()


if __name__ == '__main__':
    execute_from_command_line()
