import unittest
from datetime import date, timedelta
from app.utils import CalculadoraAlertas

class TestCalculadoraAlertas(unittest.TestCase):
    
    def setUp(self):
        # Inicializamos a nossa classe antes de cada teste
        self.calculadora = CalculadoraAlertas(dias_aviso=30)
        self.hoje = date.today()

    def test_vacina_atrasada(self):
        # Teste 1: Simula uma data de retorno de 5 dias atrás
        data_passada = (self.hoje - timedelta(days=5)).strftime('%Y-%m-%d')
        resultado = self.calculadora.analisar_vencimento(data_passada)
        self.assertEqual(resultado, 'atrasado')

    def test_vacina_proxima_vencimento(self):
        # Teste 2: Simula uma data para daqui a 15 dias (dentro do limite de 30 dias)
        data_proxima = (self.hoje + timedelta(days=15)).strftime('%Y-%m-%d')
        resultado = self.calculadora.analisar_vencimento(data_proxima)
        self.assertEqual(resultado, 'proximo')

    def test_vacina_em_dia(self):
        # Teste 3: Simula uma data para daqui a 60 dias (folgada, sem alerta)
        data_futura = (self.hoje + timedelta(days=60)).strftime('%Y-%m-%d')
        resultado = self.calculadora.analisar_vencimento(data_futura)
        self.assertEqual(resultado, 'ok')

if __name__ == '__main__':
    unittest.main()