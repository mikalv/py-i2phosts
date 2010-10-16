from django.db import models

class i2phost(models.Model):
	# Hostname limit is 67 characters maximum, including the '.i2p'.
	name = models.CharField("I2P hostname", max_length=67, unique=True)
	# Maximum key length 616 bytes (to account for certs up to 100 bytes).
	b64hash = models.CharField("Base 64 hash", max_length=616)
	description = models.TextField("Description", blank=True)
	date_added = models.DateTimeField(auto_now_add=True)
	# Last time this host was up
	last_seen = models.DateTimeField(null=True)
	# Not-activated hosts will not appear in exported hosts.txt
	activated = models.BooleanField(default=False)
	# Indicator for hosts added from external source
	external = models.BooleanField(default=False)

	def __unicode__(self):
		return self.name
