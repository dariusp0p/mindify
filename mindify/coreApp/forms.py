from django import forms

class CreateEventForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control form-floating",
            "placeholder": "Enter event title",
            "id": "title",
        }
    ))
    description = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control form-floating",
            "placeholder": "Enter event description",
            "id": "event-description",
        }
    ))
    date_posted = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={
                'type': 'date',  # Use a date input for better customization
                "class": "form-control form-floating",
                "id": "event-date",
                "placeholder": "dd.mm.yyyy",  # Placeholder for the desired format
            }
        ),
        input_formats=['%d.%m.%Y'],  # Specify the input format
    )
    event_picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        "class": "form-control form-floating",
        "id": "event-image",
    }))
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control form-floating",
            "id": "event-tags",
            "placeholder": "Enter tags separated by commas",
        })
    )
    content = forms.FileField(widget=forms.FileInput(attrs={
        "class": "form-control form-floating",
        "id": "event-file",
    }), required=False)
    price = forms.IntegerField(required=False, min_value=0, widget=forms.NumberInput(attrs={
        "class": "form-control form-floating",
        "placeholder": "Enter price (optional)",
        "id": "event-price",
    }))