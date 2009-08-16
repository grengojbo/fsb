# -*- coding: UTF-8 -*-
from django.core.management.base import NoArgsCommand
from django.core.management import call_command

class Command(NoArgsCommand):
    help = "Load FSbilling default data."
    
    def handle_noargs(self, **options):
        """Load FSadmin default data."""
        call_command('loaddata', 'tariffplan.xml', interactive=True)
