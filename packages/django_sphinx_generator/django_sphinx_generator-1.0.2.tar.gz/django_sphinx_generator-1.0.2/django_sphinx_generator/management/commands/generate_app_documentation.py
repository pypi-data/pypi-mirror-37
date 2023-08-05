
from django.core.management.base import BaseCommand
from django_sphinx_generator.generator import DocumentGenerator


class Command(BaseCommand):
    help = 'Generate sphinx documentation for apps'

    def handle(self, *args, **options):
        documentgenerator = DocumentGenerator()
        documentgenerator.create_document_tree()
