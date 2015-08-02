from django import forms

class URLForm(forms.Form):
    url = forms.URLField(label='Your Web site')


    def clean(self):
        cleaned_data = super(URLForm, self).clean()
        try:
            url = cleaned_data.get("url").lower()
        except ( NameError, AttributeError ):
            raise forms.ValidationError("")
        if "pinterest.com" not in url:
            raise forms.ValidationError("url does not belong to pinterest.com")

        # Always return the full collection of cleaned data.
        return cleaned_data  