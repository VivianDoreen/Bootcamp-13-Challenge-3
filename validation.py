from flask import Flask, jsonify, request, url_for, abort, make_response

def make_public_user(user):
    new_user = {}
    for field in user:
        if field == 'public_id':
            new_user['uri'] = url_for('get_users', user_id=user['public_id'], _external=True)
        else:
            new_user[field] = user[field]
    return new_user