import pandas as pd
from dataclasses import dataclass
from typing import Dict, List
from datetime import datetime
import math  #p verificar nan

from codigos import list_despesas

@dataclass
class FinancialData:
    """Classe para armazenar dados financeiros por período"""
    entradas: List[Dict] = None
    saidas: List[Dict] = None
    movimentacoes: List[Dict] = None
    
    def __post_init__(self):
        self.entradas = self.entradas or []
        self.saidas = self.saidas or []
        self.movimentacoes = self.movimentacoes or []

class FinancialProcessor:
    """Processador de dados financeiros"""
    
    MONTHS = {
        '01': 'jan', '02': 'fev', '03': 'mar', '04': 'abr',
        '05': 'mai', '06': 'jun', '07': 'jul', '08': 'ago',
        '09': 'set', '10': 'out', '11': 'nov', '12': 'dez'
    }
    COD_RECEITA = "11101001"  
    YEARS = ['2023', '2024', '2025'] 

    @staticmethod
    def safe_float(value) -> float:
        """Converte valores para float de forma segura, tratando nan"""
        if value is None or (isinstance(value, float) and math.isnan(value)):
            return 0.0
        try:
            return float(str(value).replace(",", ".").strip())
        except (ValueError, TypeError):
            return 0.0

    @staticmethod
    def read_xlsx(file_path: str) -> List[Dict]:
        """Lê arquivo Excel e retorna registros"""
        df = pd.read_excel(file_path, dtype=str)
        df.columns = [col.strip() for col in df.columns]
        return df.to_dict(orient='records')

    @staticmethod
    def categorize_record(record: Dict) -> str:
        """Categoriza registro baseado na natureza"""
        natureza = str(record.get("Natureza", ""))
        if not natureza or natureza[0] == "n" or natureza.lower().startswith("nan"):
            return "ignore"
        try:
            first_digit = int(natureza[0])
            return {1: "entrada", 2: "saida", 3: "movimentacao"}.get(first_digit, "ignore")
        except (ValueError, IndexError):
            return "ignore"

    def __init__(self, file_path: str):
        self.records = self.read_xlsx(file_path)
        self.data = FinancialData()
        self.despesas_by_period = {}
        self.receita_by_period = {}
        self._initialize_periods()

    def _initialize_periods(self):
        """Inicializa períodos para os anos definidos"""
        for year in self.YEARS:
            for month in self.MONTHS:
                self.despesas_by_period[f"{self.MONTHS[month]}_{year}"] = 0
                self.receita_by_period[f"receita_bruta_{self.MONTHS[month]}_{year}"] = 0

    def process_records(self):
        """Processa todos os registros"""
        for record in self.records:
            category = self.categorize_record(record)
            if category == "entrada":
                self.data.entradas.append(record)
            elif category == "saida":
                self.data.saidas.append(record)
            elif category == "movimentacao":
                self.data.movimentacoes.append(record)

    def calculate_expenses(self):
        """Calcula despesas por período"""
        for saida in self.data.saidas:
            if str(saida.get('Natureza', '')) not in list_despesas:
                continue
                
            date_str = str(saida.get('Data', ''))
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                year = date.strftime('%Y')
                month = date.strftime('%m')
                key = f"{self.MONTHS[month]}_{year}"
                self.despesas_by_period[key] += self.safe_float(saida.get("Saida", 0))
            except ValueError:
                continue

    def calculate_revenue(self):
        """Calcula receita bruta por período com deslocamento de 1 mês"""
        for entrada in self.data.entradas:
            if str(entrada.get('Natureza', '')) != self.COD_RECEITA:
                continue
                
            date_str = str(entrada.get('Data', ''))
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                year = int(date.strftime('%Y'))
                month = int(date.strftime('%m'))
                
                if month == 12:
                    month = 1
                    year += 1
                else:
                    month += 1
                
                month_str = f"{month:02d}"
                key = f"receita_bruta_{self.MONTHS[month_str]}_{year}"
                self.receita_by_period[key] += self.safe_float(entrada.get("Entrada", 0))
            except ValueError:
                continue

    def get_despesas_2023(self) -> List[float]:
        """Retorna despesas de 2023 em ordem cronológica"""
        return [self.despesas_by_period[f"{month}_2023"] 
                for month in self.MONTHS.values()]

    def get_despesas_2024(self) -> List[float]:
        """Retorna despesas de 2024 em ordem cronológica"""
        return [self.despesas_by_period[f"{month}_2024"] 
                for month in self.MONTHS.values()]

    def get_receitas_2023(self) -> List[float]:
        """Retorna receitas de 2023 em ordem cronológica"""
        return [self.receita_by_period[f"receita_bruta_{month}_2023"] 
                for month in self.MONTHS.values()]

    def get_receitas_2024(self) -> List[float]:
        """Retorna receitas de 2024 em ordem cronológica"""
        return [self.receita_by_period[f"receita_bruta_{month}_2024"] 
                for month in self.MONTHS.values()]

    def get_receitas_2025(self) -> float:
        """Retorna receita de janeiro de 2025"""
        return self.receita_by_period["receita_bruta_jan_2025"]

def main():
    processor = FinancialProcessor("dados.xlsx")
    processor.process_records()
    processor.calculate_expenses()
    processor.calculate_revenue()
    
    despesas_2023 = processor.get_despesas_2023()
    despesas_2024 = processor.get_despesas_2024()
    receitas_2023 = processor.get_receitas_2023()
    receitas_2024 = processor.get_receitas_2024()
    receitas_2025_jan = processor.get_receitas_2025()
    
    print("Despesas 2023:", despesas_2023)
    print("Despesas 2024:", despesas_2024)
    print("Receitas 2023:", receitas_2023)
    print("Receitas 2024:", receitas_2024)
    print("Receita Janeiro 2025:", receitas_2025_jan)

if __name__ == "__main__":
    main()