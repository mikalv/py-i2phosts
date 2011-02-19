import re
import datetime
import string
import random
import urllib2

from django import forms
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

import settings
from pyi2phosts.postkey.models import i2phost
from pyi2phosts.lib.utils import get_logger
from pyi2phosts.lib.validation import validate_hostname
from pyi2phosts.lib.validation import validate_b64hash

class AddForm(forms.ModelForm):
	"""
	This is our class for host-add form. It's based on django's ModelForm
	and uses our model "i2phost" (see postkey/models.py)
	"""
	class Meta:
		model = i2phost
		fields = ('name', 'b64hash', 'description')
		widgets = {
				'name': forms.TextInput(attrs={'size': '67'}),
				'b64hash': forms.Textarea(attrs={'rows': '1', 'cols': '100'}),
				'description': forms.Textarea(attrs={'rows': '2', 'cols': '72'})
				}
	def clean_name(self):
		"""Validate hostname"""
		data = self.cleaned_data['name']
		log.debug(u'hostname: %s', self.data['name'])
		data = validate_hostname(data)
		# Another set of reserved hostnames (suggested by zzz)
		if re.search(r'(^|\.)(i2p|i2p2|geti2p|mail|project|i2project|i2pproject|i2p-project).i2p$', data):
			raise forms.ValidationError(_('Trying to use hostname from additional reserved set'))
		return data
	def clean_b64hash(self):
		"""Validate base64 hash"""
		data = self.cleaned_data['b64hash']
		log.debug(u'hash: %s', self.data['b64hash'])
		data = validate_b64hash(data)
		return data
	def is_valid(self):
		"""Log validation errors"""
		is_valid = super(AddForm, self).is_valid()
		if not is_valid:
			for field in self.errors.keys():
				log.info('ValidationError: [%s]: \"%s\" %s',
						field, self.data[field], self.errors[field].as_text())
		return is_valid


class SubdomainVerifyForm(forms.Form):
	"""Form for displaying verification filename and code when verifying a subdomain"""
	filename = forms.CharField(widget=forms.TextInput(attrs={
		'size': '20',
		'readonly': 'readonly',
		'onclick': 'this.select();',
		}))

def save_host(request):
	"""Function for saving hosts after validation or subdomain verification"""
	# avoid race conditions
	try:
		h = i2phost.objects.get(name=request.session['hostname'])
	except i2phost.DoesNotExist:
		host = i2phost(name=request.session['hostname'],
				b64hash=request.session['b64hash'],
				description=request.session['description'],
				date_added=datetime.datetime.utcnow())
		host.save()
		return redirect('pyi2phosts.postkey.views.success')
	else:
		log.warning('refusing to save already existed host: %s', request.session['hostname'])
		request.session.flush()
		return redirect('/')

def addkey(request):
	if request.method == 'POST':
		form = AddForm(request.POST)
		if form.is_valid():
			request.session['hostname'] = form.cleaned_data['name']
			request.session['b64hash'] = form.cleaned_data['b64hash']
			request.session['description'] = form.cleaned_data['description']
			if form.cleaned_data['name'].count('.') > 1:
				return redirect('pyi2phosts.postkey.views.subdomain')
			else:
				log.debug('submit is valid, saving')
				s = save_host(request)
				return s
	else:
		form = AddForm()
	return render_to_response('postkey.html', {
		'title': settings.SITE_NAME,
		'form': form,
		}, context_instance=RequestContext(request))

def success(request):
	if 'hostname' in request.session:
		hn = request.session['hostname']
		request.session.flush()
		return render_to_response('success_submission.html', {
			'title': settings.SITE_NAME,
			'hostname': hn,
			})
	else:
		return redirect('/')

def subdomain(request):
	"""Subdomain verification"""
	if request.method == 'POST':
		form = SubdomainVerifyForm(request.POST)
		if form.is_valid():
			# do verification here, then redirect to success
			proxy_handler = urllib2.ProxyHandler({'http': settings.EEPROXY_URL})
			opener = urllib2.build_opener(proxy_handler)
			if 'topdomain' in request.session and 'v_filename' in request.session:
				url = 'http://' + request.session['topdomain'] + '/' + request.session['v_filename']
			else:
				log.warning('trying to call subdomain validation without a session')
				return redirect('/')
			log.info('starting http-verification of subdomain: %s', request.session['hostname'])
			try:
				log.debug('trying to open %s', url)
				resp = opener.open(url, timeout=60)
			except urllib2.URLError, e:
				if hasattr(e, 'reason'):
					log.warning('%s: failed to reach server, reason: %s', topdomain, e.reason)
				elif hasattr(e, 'code'):
					log.warning('%s can\'t finish the request, error code: %s',
							request.session['topdomain'], e.code)
					return render_to_response('subdomain_http_verify_failure.html', {
						'title': settings.SITE_NAME,
						'code': e.code,
						})
			else:
				log.debug('subdomain verification success, saving host')
				s = save_host(request)
				return s
	else:
		# generate verification code and display info page to user
		v_filename = ''.join([random.choice(string.letters + string.digits) for x in xrange(16)])
		if 'hostname' in request.session:
			m = re.match('.+\.(.+\.i2p$)', request.session['hostname'])
			topdomain = m.group(1)
		else:
			return redirect('/')
		# save needed variables in session data because otherwise it will be lost
		request.session['v_filename'] = v_filename
		request.session['topdomain'] = topdomain
		form = SubdomainVerifyForm({'filename': v_filename})
		return render_to_response('subdomain_http_verify.html', {
			'title': settings.SITE_NAME,
			'hostname': request.session['hostname'],
			'topdomain': topdomain,
			'form': form,
			}, context_instance=RequestContext(request))

log = get_logger(filename=settings.LOG_FILE, log_level=settings.LOG_LEVEL)
