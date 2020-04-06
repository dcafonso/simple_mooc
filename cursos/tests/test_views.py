from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.conf import settings
from cursos.models import Curso


class ContatoCursoTestCase(TestCase):
    def setUp(self):
        # cria um curso
        self.curso = Curso.objects.create(nome='Django', slug='Django')

    def tearDown(self):
        self.curso.delete()

    def test_contato_form_error(self):
        # testa o campo e-mail como obrigatório
        dados = {
            'nome': 'Fulano de Tal',
            'email': '',
            'mensagem': 'teste'
        }
        client = Client()
        path = reverse('cursos_detalhe', args=[self.curso.slug])
        response = client.post(path, dados)

        self.assertFormError(
            response,
            'form',
            'email',
            ['Este campo é obrigatório.']
        )

    def test_contato_form_success(self):
        # teste do form com todos os campo preenchidos
        dados = {
            'nome': 'Fulano de Tal',
            'email': 'fulano@django.com',
            'mensagem': 'teste'
        }
        client = Client()
        path = reverse('cursos_detalhe', args=[self.curso.slug])
        client.post(path, dados)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [settings.EMAIL_CONTATO])
