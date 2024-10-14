from flask import abort, render_template, request, url_for

from CTFd.admin import admin


@admin.route("/admin/viewticket")
def view_tickets():
    return render_template("admin/Ticket/view_ticket.html")
