# routes/sendticket.py

from flask import Blueprint, request, flash, render_template, abort
from CTFd.utils.decorators import require_verified_emails, during_ctf_time_only
from CTFd.utils.user import authed

sendticket = Blueprint("sendticket", __name__)


@sendticket.route("/sendticket")
@require_verified_emails
@during_ctf_time_only
def send_ticket():
    if not authed():
        abort(403)

        return render_template("send_ticket.html")

    return render_template("send_ticket.html")
