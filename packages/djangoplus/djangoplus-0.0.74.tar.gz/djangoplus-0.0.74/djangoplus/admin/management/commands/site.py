# -*- coding: utf-8 -*-
import os
from django.core.management.base import BaseCommand
from fabric.api import *

env.user = 'root'


class Command(BaseCommand):

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--update-samples', action='store_true', dest='update_samples', default=False,
                            help='Update samples at djangoplus.net')

    def handle(self, *args, **options):
        if options.get('update_samples'):
            execute(_update_samples, host='djangoplus.net')


def _update_samples():
    for project_name in ('petshop', 'loja', 'biblioteca', ):
        if os.path.exists('/Users/breno'):
            project_path = '/Users/breno/Documents/Workspace/djangoplus/djangoplus-demos/{}'.format(project_name)
            with lcd(project_path):
                local('pwd')
                if 'nothing to commit' not in local('git status', capture=True):
                    local('git commit -am \'.\'')
                    local('git push origin master')
            with cd('/var/opt/{}'.format(project_name)):
                run('pwd')
                run('git pull origin master')
                run('workon {} && python manage.py zip'.format(project_name))