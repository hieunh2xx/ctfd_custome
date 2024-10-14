from flask import Blueprint, render_template, abort, request, flash, redirect, url_for
from CTFd.utils.decorators import require_verified_emails, during_ctf_time_only
from CTFd.models import Challenges, Solves, Hints, db
from CTFd.utils.user import authed

challenge = Blueprint("challenge", __name__)


@challenge.route("/challenges/<int:challenge_id>", methods=["GET", "POST"])
@require_verified_emails
@during_ctf_time_only
def view_challenge(challenge_id):
    challenge = Challenges.query.filter_by(id=challenge_id).first()
    if not challenge:
        abort(404)

    if not authed():
        abort(403)

    # if request.method == "POST":
    #     action = request.form.get("action")
    #     # if action == "start" and challenge.start == False:

    #         db.session.commit()

    #         flash("Challenge started successfully", "success")
    #     # elif action == "stop" and challenge.start == True:
    #         db.session.commit()
    #         flash("Challenge stopped successfully", "success")

    hints = Hints.query.filter_by(challenge_id=challenge_id).all()
    solves = Solves.query.filter_by(challenge_id=challenge.id).all()
    return render_template(
        "challenge.html",
        challenge=challenge,
        solves=solves,
        hints=hints,
        max_attempts=challenge.max_attempts,
    )
