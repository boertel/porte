from flask import redirect, url_for, render_template, session, request
from porte.auth.forms import RegistrationForm, LoginForm
from porte.auth.models import Provider
from porte.auth.helpers import current_user, consumerize


def email_register():
    form = RegistrationForm()
    if form.validate():
        provider = Provider.query.filter_by(name='email').first()
        email = form.data['email']
        consumer_data = {
            'email': email,
            'password': form.data['password'],
        }
        user = consumerize(provider, consumer_data, {'email': email})
        session['id'] = user.id
        if 'next' in request.form:
            return redirect(request.form['next'])
        return redirect(url_for('auth.success'))
    return render_template('auth/email/register.html',
                           errors=form.errors,
                           form=form,
                           next=request.args.get('next'),
                           action=url_for('auth.email_register'))


def email_login():
    if request.method == 'POST':
        form = LoginForm()
        if form.validate():
            provider = Provider.query.filter_by(name='email').first()
            consumer_data = {
                'email': form.data.email,
                'password': form.data.password
            }
            # TODO "get_consumer and exists" already happens in the consumerize
            consumer = provider.get_consumer(**consumer_data)
            if consumer.exists():
                user = consumerize(provider, consumer_data,
                                   {'email': form.data.email})
                session['id'] = user.id
        return redirect(request.form.get('next', url_for('auth.success')))
    user = current_user()
    return render_template('auth/email/login.html',
                           user=user,
                           action=url_for('auth.email_login'),
                           next=request.args.get('next'))
