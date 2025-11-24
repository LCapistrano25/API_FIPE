import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.core.management.base import BaseCommand
from django.db import transaction

from fipe_car.models import FipeCar


class Command(BaseCommand):
    help = 'Import FIPE data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Start importing FIPE data...'))

        df = pd.read_csv('machine_learn/fipe_cars.csv')
        df = self.clean_data(df)

        if df is None or df.empty:
            self.stdout.write(self.style.ERROR("DataFrame is empty after cleaning!"))
            return

        self.insert_data_with_threads(df)

        self.stdout.write(self.style.SUCCESS('Successfully imported FIPE data!'))

    # -------------------------------------------------------------------------
    # CLEAN DATA
    # -------------------------------------------------------------------------
    def clean_data(self, df):
        """Limpa, transforma e renomeia os dados."""
        df = df.dropna()

        # Convertendo colunas
        df['year_model'] = pd.to_numeric(df['year_model'])
        df['engine_size'] = pd.to_numeric(df['engine_size'])
        df['avg_price_brl'] = pd.to_numeric(df['avg_price_brl'])

        # Criando coluna derivada
        df['anos_uso'] = df['year_of_reference'] - df['year_model']

        # Renomeando
        df.rename(columns={
            'fipe_code': 'fipe_id',
            'brand': 'marca',
            'model': 'modelo',
            'fuel': 'combustivel',
            'gear': 'cambio',
            'engine_size': 'potencia_motor',
            'year_model': 'ano_modelo',
            'avg_price_brl': 'preco_medio_FIPE'
        }, inplace=True)

        # Selecionando colunas relevantes
        df = df[
            [
                'fipe_id',
                'ano_modelo',
                'anos_uso',
                'marca',
                'modelo',
                'potencia_motor',
                'combustivel',
                'cambio',
                'preco_medio_FIPE'
            ]
        ]
        
        df_sample = df.sample(n=50000, random_state=42)

        return df_sample

    # -------------------------------------------------------------------------
    # INSERT SINGLE ROW
    # -------------------------------------------------------------------------
    def _insert_single_row(self, row):
        """Insere uma linha no banco."""
        try:
            obj = FipeCar.objects.create(
                fipe_id=row['fipe_id'],
                brand=row['marca'],
                model=row['modelo'],
                year=row['ano_modelo'],
                fuel_type=row['combustivel'],
                gear_type=row['cambio'],
                engine_size=row['potencia_motor'],
                price=row['preco_medio_FIPE'],
            )
            
            if obj:
                self.stdout.write(self.style.SUCCESS(f"Registro inserido: {row['fipe_id']}"))
            
            return True
        except Exception as e:
            return f"Erro ao inserir registro: {e}"

    # -------------------------------------------------------------------------
    # INSERT USING THREADS
    # -------------------------------------------------------------------------
    def insert_data_with_threads(self, df, max_workers=6):
        """Insere dados com multithreading para acelerar o processo."""
        self.stdout.write(self.style.WARNING("Iniciando inserção com Threads..."))

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(self._insert_single_row, row)
                for _, row in df.iterrows()
            ]

            total = len(futures)
            erros = 0

            for i, future in enumerate(as_completed(futures), 1):
                result = future.result()
                if result is not True:
                    erros += 1
                    self.stdout.write(self.style.ERROR(result))

                if i % 500 == 0:
                    self.stdout.write(f"Progresso: {i}/{total}")

        self.stdout.write(self.style.SUCCESS(
            f"Inserção concluída! Registros: {total}, Erros: {erros}"
        ))
