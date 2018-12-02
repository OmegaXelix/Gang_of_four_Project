from flask import Blueprint, request, jsonify

from ..controller.main_controller import get_flights, get_flight, reserve

flight = Blueprint('flight', __name__, url_prefix='/api/flight')


@flight.route('/', methods=['GET'])
def flights_view():
    start_city = request.args.get('start_city', default=None, type=str)
    finish_city = request.args.get('finish_city', default=None, type=str)
    date = request.args.get('date', default=None, type=str)
    body = {}

    if start_city is not None:
        body['start_city'] = start_city
    if finish_city is not None:
        body['finish_city'] = finish_city
    if date is not None:
        body['date'] = date

    if request.method == 'GET':  # get flights
        all_flights = get_flights(body)

        response_body = [t.to_dict() for t in all_flights]
        return jsonify(response_body), 200


@flight.route('/<string:flight_id>', methods=['GET', 'POST'])
def single_flight_view(flight_id):
    if request.method == 'GET':  # get the team
        flight = get_flight(flight_id)
        if flight is None:
            return jsonify({'error': 'flight with unique id {} not found'.format(flight_id)}), 404

        response_body = flight.to_dict()
        return jsonify(response_body), 200

    if request.method == 'POST':  # update the team
        body = request.json
        updated = reserve(body, flight_id)
        if updated is None:
            return jsonify({'error': 'flight with unique id {} not found'.format(flight_id)}), 404
        if updated == -1:
            return jsonify({'error': 'flight id {} is fully booked'.format(flight_id)}), 200

        return jsonify({'success': 'your seat id is {} (booked)'.format(updated)}), 200

