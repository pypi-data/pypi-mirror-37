import copy
import logging
import os
import re
from datetime import datetime
from functools import wraps
from uuid import uuid4

from flask import request
from flask_api import status
from google.auth.transport import requests
from google.oauth2 import id_token

from .constants import Constants

HTTP_REQUEST = requests.Request()
PROJECT_ID = os.environ.get('PROJECT')
UNAUTH = {"Message": "User has not permissions"}, status.HTTP_401_UNAUTHORIZED
constants = Constants()


def firebase_auth(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        id_token_firebase = request.headers.get('Authorization')
        if not id_token_firebase:
            return UNAUTH
        try:
            claims = id_token.verify_firebase_token(id_token_firebase.split(' ').pop(), HTTP_REQUEST)
        except Exception as ex:
            logging.warning(ex)
            return UNAUTH
        logging.info(claims)
        if not (claims.get('aud') == PROJECT_ID or claims.get('iss') == os.environ.get('ISSUER') % PROJECT_ID):
            return UNAUTH
        kwargs["auth_user"] = {"id": claims.get('sub'), "role": claims.get('role')}
        return f(*args, **kwargs)

    return wrapped


def validate_email(email):
    if email is not None:
        return email.split("@")[0] if re.fullmatch(
            "^[_a-z0-9-+]+(\.[_a-z0-9-]+)*@[a-z0-9-+]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", email) is not None else None


def build_statistic_event(event, id_user, role, id_receptor=None, id_job=None, extra_params=None):
    statistic_event = {
        "idEvent": str(uuid4()),
        "idUser": id_user,
        "userRole": role,
        "isAnonymous": False,
        **event
    }
    id_sender_name = "idUserCandidate" if role == "Candidate" else "idUserEmployer"
    statistic_event[id_sender_name] = id_user
    if id_receptor:
        id_receptor_name = "idUserEmployer" if role == "Candidate" else "idUserCandidate"
        statistic_event[id_receptor_name] = id_receptor
    if extra_params:
        statistic_event["properties"].update(extra_params)
    if id_job:
        statistic_event["idJob"] = id_job

    return {"event": statistic_event, "appsflyer": statistic_event.get("appsflyer")}


def emails_substitutions(substitutions, id_user):
    emails_substitution = {
        "{{ asm_group_unsubscribe_raw_url }}": "www.merlinjobs.com/unsubscribe?id={}".format(id_user),
        "{{ unsubscribe_sendgrid_default }}": "<%asm_group_unsubscribe_raw_url%>",
        "https://www.merlinjobs.com/": constants.get_constant("FINAL_URL"),
        **substitutions
    }
    return emails_substitution


def algolia_request(obj_type, obj):
    search_request = {
        "algolia": True,
        "body": {
            "newImplementation": True,
            "keyClient": constants.get_constant("KEY_SECURE_CLIENT"),
            "{}List".format(obj_type): [obj]
        },
        "url": "/{}Update".format(obj_type)
    }
    return search_request
