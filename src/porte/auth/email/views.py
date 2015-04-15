from flask import redirect, url_for, render_template, session, request
from porte.auth.forms import RegistrationForm, LoginForm
from porte.auth.models import Provider
from porte.auth.helpers import current_user, register, login


def email_register():
    form = RegistrationForm()
    if form.validate():
        provider = Provider.query.filter_by(name='email').first()
        email = form.data['email']
        params = {
            'password': form.data['password']
        }
        # TODO split like this: ?
        # consumer = provider.register_consumer(uid, params)
        # user = consumer.create_user({'email': email})
        user = register(provider, email, params, {'email': email})
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
            email = form.data['email']
            params = {
                'password': form.data['password']
            }
            # provider.login(email, params)
            user = login(provider, email, params)
            session['id'] = user.id
        return redirect(request.form.get('next', url_for('auth.success')))
    user = current_user()
    return render_template('auth/email/login.html',
                           user=user,
                           action=url_for('auth.email_login'),
                           next=request.args.get('next'))
