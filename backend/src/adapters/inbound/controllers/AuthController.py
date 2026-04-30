from flask import Blueprint, jsonify, request

from src.config.firebase_config import firebase_auth
from src.infrastructure.database.FirestoreRepository import FirestoreRepository


router = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)

repo = FirestoreRepository()


@router.route(
    "/me",
    methods=["GET"]
)
def auth_me():

    auth_header = request.headers.get(
        "Authorization"
    )

    if not auth_header:
        return jsonify({
            "success": False,
            "message": "Token no enviado"
        }), 401

    token = auth_header.replace(
        "Bearer ",
        ""
    ).strip()

    try:
        # Añadimos clock_skew_seconds para tolerar pequeñas diferencias de tiempo
        decoded_token = firebase_auth.verify_id_token(
            token,
            check_revoked=False,
            clock_skew_seconds=10  # <--- Esto da un margen de 10 segundos
        )

        uid = decoded_token["uid"]

        email = decoded_token.get(
            "email",
            ""
        )

        name = decoded_token.get(
            "name",
            email
        )

        user = repo.create_user_if_not_exists(
            {
                "uid": uid,
                "email": email,
                "name": name
            }
        )

        return jsonify({
            "success": True,
            "user": user
        }), 200

    except Exception as e:

        print(
            "Firebase verify error:",
            str(e)
        )

        return jsonify({
            "success": False,
            "error": str(e)
        }), 401
