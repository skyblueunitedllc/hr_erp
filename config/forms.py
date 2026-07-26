from django import forms

class MMDDYYYYDateInput(forms.DateInput):
    input_type = "text"

    def __init__(self, attrs=None, format=None):
        attrs = attrs or {}
        attrs.setdefault("placeholder", "mm/dd/yyyy")
        super().__init__(attrs=attrs, format=format or "%m/%d/%Y")
