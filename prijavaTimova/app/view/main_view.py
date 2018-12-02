from flask import Blueprint, request, jsonify

from ..controller.main_controller import get_all_teams, create_team, get_team, update_team,\
    delete_team, update_team_member, get_team_member, delete_team_member

teams = Blueprint('teams', __name__, url_prefix='/api/teams')
members = Blueprint('members', __name__, url_prefix='/api/members')


@teams.route('/', methods=['GET', 'POST'])
def teams_view():
    if request.method == 'GET':  # get all teams
        all_teams = get_all_teams()

        response_body = [t.to_dict() for t in all_teams]
        return jsonify(response_body), 200

    if request.method == 'POST':  # create a new team
        # mention validation issues
        body = request.json
        created = create_team(body)
        if created == -1:
            return jsonify({'error': 'team field blank'}), 400
        elif isinstance(created, tuple):
            if created[0] == 2:
                return jsonify({'error': 'team member number {} lacks field'.format(created[1])}), 400
            elif created[0] == 3:
                return jsonify({'error': 'wrong team count {}'.format(created[1])}), 400
        return jsonify(created), 201


@teams.route('/<string:team_uuid>', methods=['GET', 'PUT', 'DELETE'])
def single_team_view(team_uuid):
    if request.method == 'GET':  # get the team
        team = get_team(team_uuid)
        if team is None:
            return jsonify({'error': 'team with unique id {} not found'.format(team_uuid)}), 404

        response_body = team.to_dict()
        return jsonify(response_body), 200

    if request.method == 'PUT':  # update the team
        body = request.json
        updated = update_team(body, team_uuid)
        if updated is None:
            return jsonify({'error': 'team with unique id {} not found'.format(team_uuid)}), 404
        if updated == -1:
            return jsonify({'error': 'team field blank'}), 400
        elif isinstance(updated, tuple):
            if updated[0] == 2:
                return jsonify({'error': 'team member number {} lacks field'.format(updated[1])}), 400
            elif updated[0] == 3:
                return jsonify({'error': 'wrong team count {}'.format(updated[1])}), 400

        return jsonify(updated), 200

    if request.method == 'DELETE':  # remove the team
        success = delete_team(team_uuid)

        if not success:
            return jsonify({'error': 'team with unique id {} not found'.format(team_uuid)}), 404

        return jsonify({}), 204


@members.route('/<string:team_member_id>', methods=['GET', 'PUT', 'DELETE'])
def single_team_member_view(team_member_id):
    if request.method == 'GET':  # get the team member
        team_member = get_team_member(team_member_id)
        if team_member is None:
            return jsonify({'error': 'team member with unique id {} not found'.format(team_member_id)}), 404

        response_body = team_member.to_dict()
        return jsonify(response_body), 200

    if request.method == 'PUT':  # update the team member
        body = request.json
        updated = update_team_member(body, team_member_id)
        if updated is None:
            return jsonify({'error': 'team member with unique id {} not found'.format(team_member_id)}), 404
        if updated == 2:
            return jsonify({'error': 'team member field blank'}), 400

        return jsonify(updated), 200

    if request.method == 'DELETE':  # remove the team member
        success = delete_team_member(team_member_id)

        if success == 2:
            return jsonify({'error': 'members too low'}), 400
        elif not success:
            return jsonify({'error': 'team member with unique id {} not found'.format(team_member_id)}), 404

        return jsonify({}), 204
