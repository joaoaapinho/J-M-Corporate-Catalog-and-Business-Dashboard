# Converting plain-text passwords into hashed ones to save on the config.yaml.
import streamlit_authenticator as stauth

hashed_passwords = stauth.Hasher(['Capstone#23#', 'AdvProg#23#', '#JustCoding23']).generate()

print(hashed_passwords)