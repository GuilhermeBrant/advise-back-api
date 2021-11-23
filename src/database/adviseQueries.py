from src.database.connection import cursor

def getDatas():
    cursor.execute("""select
country,
average_celsius,
cost_of_living,
average_monthly_income,
foreign_resident_tax,
income_costs_idx,
educational_idx,
safety_idx,
employment_idx,
hdi_idx,
GDP_per_capita_idx,
purchasing_power_idx,
equality_idx,
health_quality_idx
from countries_data""")
    result = cursor.fetchall()
    return result
