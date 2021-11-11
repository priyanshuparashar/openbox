from django.forms import ModelForm
from .models import Rooms

class RoomsForm(ModelForm):
    class Meta:
        model = Rooms
        fields= '__all__'