import pandas as pd
from openpyxl import Workbook
from items_management.models import InventoryItems
from reports.models import StocktalkingReport


def create_report():
    try:
        report_id = 1
        report = StocktalkingReport.objects.get(id=report_id)
        items = report.items.all()

        data = []
        data.append({
            'N': "N",
            'Object name': "Наименование объекта",
            'Item Number': "Номер объекта учета",
            'Assessed Value': "Оценочная стоимость",
            'Amount': "Количество",
            'Sum': "Сумма",
            'Status inventory object': "Статус объекта учета",
            'Assessed amount': "Оценочное количество",
            'Cost assessed': "Балансовая стоимость",
            'Shortage amount': "Количество недостача",
            'Shortage sum': "Сумма недосдачи",
            'Overpluss amount': "Количество излишков",
            'Overpluss sum': "Сумма излишков",
            'Financially Responsible Person': "Финансово ответственное лицо",
            'Properties': "Примечание"
        })

        for counter, item in enumerate(items, start=1):
            latest_relation = item.relationitemsreports_set.all().latest('datatime') if item.relationitemsreports_set.exists() else None

            assessed_amount = latest_relation.assessed_amount if latest_relation else None

            data.append({
                'N': counter,
                'Object name': item.name,
                'Item Number': item.item_number,
                'Assessed Value': item.value,
                'Amount': item.amount,
                'Sum': item.amount * item.value,
                'Status inventory object': item.status.name if item.status else None,
                'Assessed amount': assessed_amount,
                'Cost assessed':item.assessed_value,
                'Shortage amount': assessed_amount - item.amount,
                'Shortage sum': (assessed_amount - item.amount) * item.assessed_value,
                'Overpluss amount': item.amount - assessed_amount,
                'Overpluss sum': (item.amount - assessed_amount) * item.assessed_value,
                'Financially Responsible Person': item.financially_responsible_person.username if item.financially_responsible_person else None,
                'Properties': latest_relation.note if latest_relation else None
            })

        df = pd.DataFrame(data)

        file_path = "./reports/items_report.xlsx"
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, header=False)

        print("Excel файл успешно сохранен:", file_path)

    except Exception as e:
        print("Ошибка при создании отчета:", e)

# Вызов функции для создания отчета
create_report()