from concierge_paas_plugin.models import Configuration
def getdefault():
    return Configuration.objects.get(default=True)