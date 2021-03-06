from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import dns.resolver
dnsbllookup = Flask(__name__)

@dnsbllookup.route('/')
def form():
    return render_template('form_submit.html')

@dnsbllookup.route('/lookup/', methods=['POST'])
def lookup():
    # Let us reverse this address for the DNSBL lookup
    ip = request.form['ip']
    reversedaddress = reverse(ip)
    compiledquery = reversedaddress + ".dnsbl.ircops.org"
    try:
        dns.resolver.query(compiledquery, 'A')
        ipstatus = True
        reason = dns.resolver.query(compiledquery, 'TXT')
        for rdata in reason:
            reasonoutput = str(rdata)
    except dns.resolver.NXDOMAIN:
        ipstatus = False

    if ipstatus is True:
        output = ip + " is on the ircops DNSBL. " + "Reason: " + reasonoutput
    else:
        output = ip + " is not on the ircops DNSBL."

    return render_template('form_action.html', output=output, ip=ip)

def reverse(ip):
    splitlist = ip.split('.')[::-1]
    reversedaddress = '.'.join(splitlist)
    return reversedaddress
