import json
from flask import Flask, jsonify, make_response
from flask_restx import Api, Resource, fields

from src.server.instance import server
from src.database.adviseQueries import getDatas

app, api = server.app, server.api

def applyWeightedAverage(weights, datas):
    weightedAverageByCountry = []
    for row in datas:
        rowWeightedAverage = {
            'rank': 0,
            'country': row[0],
	        'average_celsius': row[1],
	        'cost_of_living': row[2],
	        'average_monthly_income': row[3],
	        'foreign_resident_tax': row[4],
	        'income_costs_idx': row[5],
	        'educational_idx': row[6],
	        'safety_idx': row[7],
	        'employment_idx': row[8],
	        'hdi_idx': row[9],
	        'GDP_per_capita_idx': row[10],
	        'purchasing_power_idx': row[11],
	        'equality_idx': row[12],
	        'health_quality_idx': row[13],
            'WeightedAverage': (
                (
                    row[5] * weights['costOfLifeWeight'] +
                    row[6] * weights['educationalWeight'] +
                    row[7] * weights['safetyWeight'] +
                    row[8] * weights['employmentWeight'] +
                    row[9] * weights['hdiWeight'] +
                    row[10] * weights['gdpPerCapitaWeight'] +
                    row[11] * weights['purchasingPowerWeight'] +
                    row[12] * weights['inequalityWeight'] +
                    row[13] * weights['healthQualityWeight'] 
                ) 
                /( weights['costOfLifeWeight'] 
                + weights['educationalWeight']
                + weights['safetyWeight']
                + weights['hdiWeight']
                + weights['gdpPerCapitaWeight']
                + weights['purchasingPowerWeight']
                + weights['inequalityWeight']
                + weights['healthQualityWeight'] )
            )
        }
        weightedAverageByCountry.append(rowWeightedAverage)
    sorted_list = sorted(weightedAverageByCountry, key=lambda k: k['WeightedAverage'], reverse=True) 
    for idx, row in enumerate(sorted_list):
        row['rank'] = idx + 1
    return sorted_list



resource_fields = api.model('Resource', {
    'inequalityWeight': fields.Integer,
    'costOfLifeWeight': fields.Integer,
    'educationalWeight': fields.Integer,
    'safetyWeight': fields.Integer,
    'employmentWeight': fields.Integer,
    'hdiWeight': fields.Integer,
    'gdpPerCapitaWeight': fields.Integer,
    'purchasingPowerWeight': fields.Integer,
    'healthQualityWeight': fields.Integer
})

@api.route('/recommendation')
class recommendation(Resource):
    @api.expect(resource_fields, validate=True)
    def post(self, ):
        requestBody = api.payload
        datas = getDatas()
        response = applyWeightedAverage(requestBody, datas)
        return {'data':response}, 200
