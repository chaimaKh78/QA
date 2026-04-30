def clean(self):
    cleaned_data = super().clean()
    origin = cleaned_data.get('origin')
    destination = cleaned_data.get('destination')
    if origin and destination and origin == destination:
        raise forms.ValidationError(
            "L'aéroport de départ et d'arrivée doivent être différents."
        )
    return cleaned_data