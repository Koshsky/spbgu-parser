import json
import re
import os
from typing import Any, Dict, List


def verify_snils(snils: str) -> bool:
    pattern = r'\b\d\d\d-\d\d\d-\d\d\d \d\d\b'
    return re.match(pattern, snils) is not None or snils.isdigit()


def search_snils(SNILS: str) -> List[Dict[str, Any]]:
    res = []
    titles = os.listdir('parsed_data/')
    for title in titles:
        with open(f'parsed_data/{title}', 'r', encoding='UTF-8') as f:
            data = json.load(f)
            if SNILS in data['Конкурс']:
                res.append(data)
    return res


def format_snils_result(snils: str, json: Dict[str, Any]) -> str:
    ball = json['Конкурс'][snils]['Баллы']

    res = f"{json['Направление']}\n" \
          f"Бюджетных мест: {json['Бюджетных мест']}\n\n" \
          f"Приоритет: {json['Конкурс'][snils]['Приоритет']}\n" \
          f"Сумма баллов: {ball}\n" \
          f"Место в списке: {json['Конкурс'][snils]['Место в списке']}/{json['Бюджетных мест']}\n"

    return res
