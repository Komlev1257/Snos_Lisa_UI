def validate_ipa_user(username, password):
    # TODO: Подключи сюда свою IPA-валидацию
    return username == "test" and password == "test123"

def validate_secondary_auth(username, password):
    # TODO: Подключи сюда свою вторую проверку
    return username == "admin" and password == "admin123"
