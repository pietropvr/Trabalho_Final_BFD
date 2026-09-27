from datetime import datetime, date

class CalculadoraAlertas:
    """
    Classe responsável por aplicar as regras de negócio de saúde do pet,
    calculando se os retornos médicos estão em dia, próximos ou atrasados.
    """
    def __init__(self, dias_aviso=30):
        # O construtor define a antecedência padrão para o alerta
        self.dias_aviso = dias_aviso

    def analisar_vencimento(self, data_retorno_str):
        if not data_retorno_str:
            return 'sem_data'
        
        try:
            # Converte a string do banco de dados ('AAAA-MM-DD') para um objeto de data
            data_retorno = datetime.strptime(data_retorno_str, '%Y-%m-%d').date()
            hoje = date.today()
            diferenca = (data_retorno - hoje).days

            if diferenca < 0:
                return 'atrasado'
            elif 0 <= diferenca <= self.dias_aviso:
                return 'proximo'
            else:
                return 'ok'
        except ValueError:
            return 'erro_formato'