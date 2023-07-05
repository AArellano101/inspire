from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible

class Captcha(forms.Form):
    captcha = ReCaptchaField( 
        public_key='6LdV2ocmAAAAAFyg3oAK-FDqiCTyzyOcEnVojbJt',
        private_key='6LdV2ocmAAAAAM_3R6XGXG2z-iC6DsLX7dlKFVfz'
    )