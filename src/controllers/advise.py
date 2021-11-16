import json
from flask import Flask, jsonify, make_response
from flask_restx import Api, Resource, fields

from src.server.instance import server
from src.database.adviseQueries import getScores, getDatas

app, api = server.app, server.api

def applyWeightedAverage(weights, scoresByCountry):
    weightedAverageByCountry = []
    for row in scoresByCountry:
        rowWeightedAverage = {
            'country': row[0],
            'WeightedAverage': (
                (
                    row[1] * weights['costOfLifeWeight'] +
                    row[2] * weights['educationalWeight'] +
                    row[3] * weights['safetyWeight'] +
                    row[4] * weights['employmentWeight'] +
                    row[5] * weights['hdiWeight'] +
                    row[6] * weights['gdpPerCapitaWeight'] +
                    row[7] * weights['purchasingPowerWeight'] +
                    row[8] * weights['inequalityWeight'] +
                    row[9] * weights['healthQualityWeight'] 
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
    return sorted_list[0]['country']



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
        scoresByCountry = getScores()
        countryMatch = applyWeightedAverage(requestBody, scoresByCountry)
        response = getDatas(countryMatch)
        return response, 200
