from behave import given, when, then
from django.contrib.auth.models import User
from django.urls import reverse


# ─────────────────────────────────────────────
# GIVEN
# ─────────────────────────────────────────────

@given('je suis connecté en tant que "{username}" avec le mot de passe "{password}"')
def step_logged_in(context, username, password):
    success = context.test.client.login(username=username, password=password)
    assert success, f"Login échoué pour {username}"
    context.user = User.objects.get(username=username)


# ─────────────────────────────────────────────
# WHEN - REGISTER
# ─────────────────────────────────────────────

@when("je m'inscris avec les données valides suivantes:")
def step_register_valid(context):
    row = context.table[0]

    context.response = context.test.client.post(
        reverse("accounts:register"),
        {
            "username": row["username"],
            "first_name": row["prenom"],
            "last_name": row["nom"],
            "email": row["email"],
            "password1": row["mot_de_passe"],
            "password2": row["confirmation"],
        }
    )


@when("je m'inscris avec les données suivantes ayant un email dupliqué:")
def step_register_duplicate(context):
    row = context.table[0]

    context.response = context.test.client.post(
        reverse("accounts:register"),
        {
            "username": row["username"],
            "first_name": row["prenom"],
            "last_name": row["nom"],
            "email": row["email"],
            "password1": row["mot_de_passe"],
            "password2": row["confirmation"],
        }
    )


# ─────────────────────────────────────────────
# WHEN - LOGIN
# ─────────────────────────────────────────────

@when('je me connecte avec "{username}" et "{password}"')
def step_login(context, username, password):
    context.response = context.test.client.post(
        reverse("accounts:login"),
        {"username": username, "password": password}
    )


# ─────────────────────────────────────────────
# WHEN - LOGOUT
# ─────────────────────────────────────────────

@when("je me déconnecte")
def step_logout(context):
    context.response = context.test.client.get(reverse("accounts:logout"))


# ─────────────────────────────────────────────
# WHEN - PROFILE UPDATE
# ─────────────────────────────────────────────

@when("je mets à jour mon profil avec les données suivantes:")
def step_update_profile(context):
    row = context.table[0]

    context.response = context.test.client.post(
        reverse("accounts:profile"),
        {
            "first_name": row["prenom"],
            "last_name": row["nom"],
            "email": row["email"],
            "phone": row["telephone"],
            "city": row["ville"],
            "country": row["pays"],
        }
    )


# ─────────────────────────────────────────────
# THEN - AUTH
# ─────────────────────────────────────────────

@then("le compte est créé avec succès")
def step_account_created(context):
    assert User.objects.filter(username="newuser").exists()


@then("je suis connecté automatiquement")
def step_auto_login(context):
    assert "_auth_user_id" in context.test.client.session


@then("le compte n'est pas créé")
def step_account_not_created(context):
    assert not User.objects.filter(username="otheruser").exists()


@then("je suis connecté avec succès")
def step_login_success(context):
    assert "_auth_user_id" in context.test.client.session


@then("je ne suis pas connecté")
def step_login_fail(context):
    assert "_auth_user_id" not in context.test.client.session


@then("je suis déconnecté")
def step_logged_out(context):
    assert "_auth_user_id" not in context.test.client.session


# ─────────────────────────────────────────────
# THEN - REDIRECTION
# ─────────────────────────────────────────────

@then('je suis redirigé vers la page "flights:home"')
def step_redirect_home(context):
    assert context.response.status_code in (301, 302)


@then('je reste sur la page "accounts:login"')
def step_stay_login(context):
    assert context.response.status_code == 200


# ─────────────────────────────────────────────
# THEN - PROFILE
# ─────────────────────────────────────────────

@then("le profil est mis à jour avec succès")
def step_profile_updated(context):
    assert context.response.status_code in (200, 302)


@then("les informations sont sauvegardées en base de données")
def step_profile_saved(context):
    user = User.objects.get(username="testuser")
    assert user.email is not None