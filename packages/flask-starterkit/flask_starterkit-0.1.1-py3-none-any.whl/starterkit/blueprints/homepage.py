# -*- coding: utf-8 -*-

from flask import Blueprint, request, render_template

from flask_babel import lazy_gettext as _

homepage_blueprint = Blueprint("homepage", __name__)


@homepage_blueprint.route("/")
def index():
    extra_context = {"whom": request.args.get("hello", _("world")).title()}
    return render_template("starterkit/blueprints/homepage/index.html", **extra_context)
