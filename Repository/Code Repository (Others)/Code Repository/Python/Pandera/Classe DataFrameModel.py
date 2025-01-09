# import pandera as pa
# import pandas as pd
# import os

# from pandera.typing import Series
# from typing import Optional
# from pandera.errors import SchemaError
# from datetime import datetime as dt


# class MetricasBases(pa.DataFrameModel):
#     column1: Series[int] = pa.Field(le=10)
#     column2: Series[float] = pa.Field(le=-1.4)
    
    
#     class Config:
#         strict = True
#         coerce = True
        
#     @classmethod
#     def validate_dataframe(cls, df: pd.DataFrame):
#         '''Valida o DataFrame e retorna erros personalizados.'''
        
#         try:
#             cls.validate(df)
#             print(f'Validação realizada com sucesso - {dt.now()} - {os.getlogin()}')
#         except SchemaError as e:
#             failure_cases = e.failure_cases
#             list_failure_cases = failure_cases['failure_case'].tolist()
            
#             tipo_erro = str(e.reason_code)
            
#             if "COLUMN_NOT_IN_DATAFRAME" in tipo_erro:
#                 raise ValueError(f"Erro: Colunas faltantes não encontradas no DataFrame ({list_failure_cases}) | {dt.now()} - {os.getlogin()}")
            
#             elif "COLUMN_NOT_IN_SCHEMA" in tipo_erro:
#                 raise ValueError(f"Erro: Colunas extras encontradas no DataFrame ({list_failure_cases}) | {dt.now()} - {os.getlogin()}")
            
#             elif 'DATAFRAME_CHECK' in tipo_erro:
#                 col_error = str(e)[7:str(e).find('failed')-1]
#                 raise ValueError(f'Erro: Valores sequentes da coluna {col_error} diferentes do experado ({list_failure_cases}) | {dt.now()} - {os.getlogin()}')
            
#             elif "SERIES_CONTAINS_NULL" in tipo_erro:
#                 col_error = str(e)[20:str(e).find('contains')-1]
#                 raise ValueError(f"Erro: Valores nulos encontrados nas colunas ({col_error}) do DataFrame | {dt.now()} - {os.getlogin()}")
            
#             elif "DATATYPE_COERCION" in tipo_erro:
#                 start_col = str(e).find('coercing') + len('coercing')
#                 col_error = str(e)[start_col+1:str(e).find("to type")-1]
#                 tipo = str(e)[str(e).find("to type")+ len('to type')+1:str(e).find(": Could")-1]
#                 raise ValueError(f"Erro: Erro ao tentar converter a(as) coluna(as) ({col_error}) pelo tipo {tipo} | {dt.now()} - {os.getlogin()}")
            
#             else:
#                 raise ValueError(f'Erro: {e} | {dt.now()} - {os.getlogin()}')



import pandera as pa
import pandas as pd
import os

from pandera.typing import Series
from typing import Optional
from pandera.errors import (SchemaError, SchemaInitError)
from datetime import datetime as dt
from typing import Dict, Any


def set_config(**kwargs):
    """Atualiza as opções de configuração global."""
    global config_options
    config_options.update(kwargs)


class MetricasBases(pa.DataFrameModel):
    # Definição do modelo
    column1: Series[int] = pa.Field(le=10)
    column2: Series[float] = pa.Field(le=-1.4)
    
    config_options: Dict[str, Any] = {
        "strict": False,
        "strict_level": "strict",
        "coerce": False,
        "ordered": False,
        "check_name": False,
        "exclude": None,
        "include": None
    }

    @classmethod
    def set_config(cls, **kwargs):
        """Atualiza as opções de configuração global."""
        cls.config_options.update(kwargs)
        return True

    class Config:
        """Configurações dinâmicas baseadas em config_options."""
        @property
        def strict(cls):
            return config_options.get("strict", False)

        @property
        def strict_level(cls):
            return config_options.get("strict_level", "strict")

        @property
        def coerce(cls):
            return config_options.get("coerce", False)

        @property
        def ordered(cls):
            return config_options.get("ordered", False)

        @property
        def check_name(cls):
            return config_options.get("check_name", False)

        @property
        def exclude(cls):
            return config_options.get("exclude", None)

        @property
        def include(cls):
            return config_options.get("include", None)

    @classmethod
    def validate_dataframe(cls, df: pd.DataFrame):
        """Valida o DataFrame e retorna erros personalizados."""
        try:
            cls.validate(df)
            print(f'Validação realizada com sucesso - {dt.now()} - {os.getlogin()}')
        except SchemaError as e:
            cls._handle_validation_error(e)
            print("teste\n\n\n\n", str(e.reason_code))
        except SchemaInitError as e:
            cls._handle_init_errors(e)
        
    @staticmethod
    def _handle_validation_error(e):
        """Trata erros de validação."""
        failure_cases = e.failure_cases
        list_failure_cases = failure_cases['failure_case'].tolist()
        tipo_erro = str(e.reason_code)
        print(tipo_erro, "MANO SIMMM")
        if "COLUMN_NOT_IN_DATAFRAME" in tipo_erro:
            raise ValueError(f"Erro: Colunas faltantes não encontradas no DataFrame ({list_failure_cases}) | {dt.now()} - {os.getlogin()}")

        elif "COLUMN_NOT_IN_SCHEMA" in tipo_erro:
            raise ValueError(f"Erro: Colunas extras encontradas no DataFrame ({list_failure_cases}) | {dt.now()} - {os.getlogin()}")

        elif "DATAFRAME_CHECK" in tipo_erro:
            col_error = str(e)[7:str(e).find('failed') - 1]
            raise ValueError(f"Erro: Valores sequentes da coluna {col_error} diferentes do esperado ({list_failure_cases}) | {dt.now()} - {os.getlogin()}")

        elif "SERIES_CONTAINS_NULL" in tipo_erro:
            col_error = str(e)[20:str(e).find('contains') - 1]
            raise ValueError(f"Erro: Valores nulos encontrados nas colunas ({col_error}) do DataFrame | {dt.now()} - {os.getlogin()}")

        elif "DATATYPE_COERCION" in tipo_erro:
            start_col = str(e).find('coercing') + len('coercing')
            col_error = str(e)[start_col + 1:str(e).find("to type") - 1]
            tipo = str(e)[str(e).find("to type") + len('to type') + 1:str(e).find(": Could") - 1]
            raise ValueError(f"Erro: Erro ao tentar converter a(as) coluna(as) ({col_error}) pelo tipo {tipo} | {dt.now()} - {os.getlogin()}")

        else:
            raise ValueError(f"Erro desconhecido: {e} | {dt.now()} - {os.getlogin()}")
    
    @staticmethod
    def _handle_init_errors(e: SchemaInitError):
        erro = str(e)
        print(erro)
        # if "COLUMN_NOT_IN_DATAFRAME" in tipo_erro:
        #     raise ValueError(f"Erro: Colunas faltantes não encontradas no DataFrame ({list_failure_cases}) | {dt.now()} - {os.getlogin()}")
