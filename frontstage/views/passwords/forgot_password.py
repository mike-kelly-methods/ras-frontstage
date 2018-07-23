import logging

from flask import redirect, render_template, request, url_for
from structlog import wrap_logger

from frontstage.controllers import oauth_controller, party_controller
from frontstage.exceptions.exceptions import ApiError, OAuth2Error
from frontstage.models import ForgotPasswordForm
from frontstage.views.passwords import passwords_bp


logger = wrap_logger(logging.getLogger(__name__))


BAD_AUTH_ERROR = 'Unauthorized user credentials'


@passwords_bp.route('/forgot-password', methods=['GET'])
def get_forgot_password():
    form = ForgotPasswordForm(request.form)
    template_data = {
        "error": {
            "type": {}
        }
    }
    return render_template('passwords/forgot-password.html', form=form, data=template_data)


@passwords_bp.route('/forgot-password', methods=['POST'])
def post_forgot_password():
    form = ForgotPasswordForm(request.form)

    if form.validate():
        email_address = request.form.get('email_address')

        try:
            oauth_controller.check_account_valid(email_address)
        except OAuth2Error as exc:
            error_message = exc.oauth2_error
            if BAD_AUTH_ERROR in error_message:
                exc.logger('Requesting password change for unregistered email on OAuth2 server', log_level='info')
                template_data = {"error": {"type": {"Email address is not registered"}}}
                return render_template('passwords/forgot-password.html', form=form, data=template_data)
            else:
                exc.logger(exc.message, oauth2_error=error_message, log_level='info')
            return render_template('passwords/reset-password.trouble.html')

        try:
            party_controller.reset_password_request(email_address)
        except ApiError as exc:
            if exc.status_code == 404:
                logger.error('Requesting password change for email registered'
                             ' on OAuth2 server but not in party service')
                template_data = {"error": {"type": {"Email address is not registered"}}}
                return render_template('passwords/forgot-password.html', form=form, data=template_data)
            raise exc

        logger.info('Successfully sent password change request email')
        return redirect(url_for('passwords_bp.forgot_password_check_email'))

    template_data = {
        "error": {
            "type": form.errors
        }
    }
    return render_template('passwords/forgot-password.html', form=form, data=template_data)


@passwords_bp.route('/forgot-password/check-email', methods=['GET'])
def forgot_password_check_email():
    return render_template('passwords/forgot-password.check-email.html')
