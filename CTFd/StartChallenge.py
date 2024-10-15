from flask import (
    Blueprint,
    render_template,
    abort,
    request,
    flash,
    redirect,
    url_for,
    session,
)
from CTFd.utils.decorators import (
    require_verified_emails,
    during_ctf_time_only,
    admins_only,
    authed_only,
)
from CTFd.models import Challenges, Solves, Hints, db
from CTFd.utils.user import authed
from datetime import datetime, timedelta  # Import timedelta for adding time

challenge = Blueprint("challenge", __name__)


@challenge.route("/challenges/<int:challenge_id>", methods=["GET"])
@require_verified_emails
@during_ctf_time_only
def view_challenge(challenge_id):
    if not authed():
        abort(403)

    challenge = Challenges.query.filter_by(id=challenge_id).first()

    if not challenge:
        abort(404)

    # Set time_limit to 15 minutes from now if it is None
    if challenge.time_limit is None:
        challenge.time_limit = datetime.now() + timedelta(minutes=15)

    time_limit_timestamp = int(challenge.time_limit.timestamp())

    current_time = datetime.now()
    remaining_time_seconds = (challenge.time_limit - current_time).total_seconds()
    remaining_time_minutes = max(0, remaining_time_seconds // 60)

    remaining_time_minus_15_minutes = max(0, remaining_time_minutes - 15)

    # Retrieve max_attempts from the challenge (Assuming it's a field in your Challenges model)
    max_attempts = (
        challenge.max_attempts if challenge.max_attempts is not None else 0
    )  # Replace with default value if necessary

    hints = Hints.query.filter_by(challenge_id=challenge_id)
    return render_template(
        "challenge.html",
        challenge=challenge,
        time_limit_timestamp=time_limit_timestamp,
        remaining_time_minutes=remaining_time_minutes,
        remaining_time_minus_15_minutes=remaining_time_minus_15_minutes,
        hints=hints,
        max_attempts=max_attempts,  # Pass max_attempts to the template
    )
