from django.apps import AppConfig
from django.conf import settings

class CoreConfig(AppConfig):
	name = "core"

	def ready(self):
		from . import scheduler
		scheduler.start()