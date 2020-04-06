from django.test import TestCase
from django.test.client import Client
from cursos.models import Curso


class CursoManagerTestCase(TestCase):
    QUANT_CURSOS = 10
    TOTAL_CURSOS = 20

    def setUp(self):
        self.client = Client()

        for _ in range(self.QUANT_CURSOS):
            Curso.objects.create(nome='django para dev')
            Curso.objects.create(nome='python para dev')

    def tearDown(self):
        Curso.objects.all().delete()

    def test_cursos(self):
        busca = Curso.objects.busca('django')
        self.assertEqual(len(busca), self.QUANT_CURSOS)

        busca = Curso.objects.busca('python')
        self.assertEqual(len(busca), self.QUANT_CURSOS)

        busca = Curso.objects.busca('dev')
        self.assertEqual(len(busca), self.TOTAL_CURSOS)
