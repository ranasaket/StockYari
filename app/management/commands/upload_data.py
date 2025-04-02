from django.db import models
from django.core.management.base import BaseCommand
from datetime import datetime
import csv
from app.models import DailyPrice, Index

class Command(BaseCommand):
    help = 'Import NSE historical index data from CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, newline='', encoding='utf-8') as file:
            # reader = csv.DictReader(file)
            reader = csv.DictReader(file, delimiter='\t')
    
            for row in reader:
                print("row : ", row)
                DailyPrice.objects.create(
                    index=Index.objects.get(name=row['index']),
                    date=datetime.strptime(row['date'], '%d-%b-%y').date(),

                    open_price=row['open_price'],
                    high_price=row['high_price'],
                    low_price=row['low_price'],
                    close_price=row['close_price'],
                    shares_traded=row['shares_traded'],
                    turnover=row['turnover']
                )
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))