from flask import Blueprint, render_template, abort, request, flash, redirect, url_for
from CTFd.utils.decorators import require_verified_emails, during_ctf_time_only
from CTFd.models import Challenges, Solves, Hints, db
from CTFd.utils.user import authed
from datetime import datetime, timedelta  # Import timedelta for adding time

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
    if challenge.time_limit is None:
        challenge.time_limit = datetime.now() + timedelta(minutes=15)

    time_limit_timestamp = int(challenge.time_limit.timestamp())

    current_time = datetime.now()
    remaining_time_seconds = (challenge.time_limit - current_time).total_seconds()
    remaining_time_minutes = max(0, remaining_time_seconds // 60)
    remaining_time_h =  max(0, remaining_time_minutes // 60)
    remaining_time_minus_15_minutes = max(0, remaining_time_minutes - 15)

    
    hints = Hints.query.filter_by(challenge_id=challenge_id).all()
    solves = Solves.query.filter_by(challenge_id=challenge.id).all()
    return render_template(
        "challenge.html",
        challenge=challenge,
        solves=solves,
         time_limit_timestamp=time_limit_timestamp,
        remaining_time_minutes=remaining_time_minutes,
        remaining_time_minus_15_minutes=remaining_time_minus_15_minutes,
        hints=hints,
        max_attempts=challenge.max_attempts,
    )
