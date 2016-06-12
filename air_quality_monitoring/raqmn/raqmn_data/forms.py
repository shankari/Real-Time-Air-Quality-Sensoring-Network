from django.forms import ModelForm
from raqmn_api.models import DylosData

class DylosDataForm(ModelForm):
	class Meta:
		model = DylosData
		fields = ['path','latitude','longitude','url_uuid']
