from src.database.connection import cursor

def getScores():
    cursor.execute("""select
country,
score_income_costs,	
score_educational,
score_safety,
score_employment,	
score_hdi,
score_GDP_per_capita,
score_purchasing_power,	
score_equality,
score_health_quality
from countries_data""")
    result = cursor.fetchall()
    return result


def getDatas(country):
    cursor.execute(
    """
select 
	country,
	average_celsius,
	average_monthly_income,
	average_cost_of_living,
	inequality_index,
	educational_index,
	criminal_index,
	unemployment_rate,
	hdi_index,
	GDP_per_capita,
	purchasing_power_index,
	health_quality_index,
	unemployment_rate,
	foreign_resident_tax
from countries_data
where country = ?
""",
country
)
    result = {"data":[]}
    rows = cursor.fetchall()
    for row in rows:
        result["data"].append({
            "country": row[0],
	        "average_celsius": row[1],
	        "average_monthly_income": row[2],
	        "average_cost_of_living": row[3],
	        "inequality_index": row[3],
	        "educational_index": row[4],
	        "criminal_index": row[4],
	        "unemployment_rate": row[5],
	        "hdi_index": row[6],
	        "GDP_per_capita": row[7],
	        "purchasing_power_index": row[8],
	        "health_quality_index": row[9],
	        "unemployment_rate": row[10],
	        "foreign_resident_tax": row[11]
        }) # or simply data.append(list(row))
    return result