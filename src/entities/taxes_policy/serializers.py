from collections import OrderedDict
from typing import Dict, Any
from common import decimal
from common.utils import InfinityLimit
from entities.tax.models import Tax


class TaxOutputSerializer:
    data: Dict[str, Any]

    def __init__(self, tax: Tax, detailed: bool = False):
        self.data = OrderedDict(
            annual_salary_amount=decimal.to_string(tax.annual_salary_amount),
            year=str(tax.year),
            total_tax_amount=decimal.to_string(tax.range_lines.total_amount),
        )
        if detailed:
            self.data['details'] = [
                OrderedDict(
                    amount_from=decimal.to_string(tax_range_line.policy_range.amount_from),
                    amount_to=decimal.to_string(tax_range_line.policy_range.amount_to) if not isinstance(
                            tax_range_line.policy_range.amount_to, InfinityLimit
                        ) else "*",
                    percent=str(tax_range_line.policy_range.percent),
                    tax_amount=decimal.to_string(tax_range_line.amount),
                ) for tax_range_line in tax.range_lines
            ]
