DEFAULT_APP = "asthma"

'''
You can include this in your html pages and refer to these variables:
For example:
	{{ appname }}
'''

import geoapp.analytics as analytics
#---------------------------------------------------------------------------------
def appcontext(request):
    context = {
        "appname": "Asthma",
        "weburl" : "https://asthma.geospaces.org/",
        "top_url": "asthma/topbar.html",
        "entire_top_url": "asthma/topbar.html",
        "APP_MENU" : 0,              # Show Application Menu in topbar
        "NO_LOGIN_MENU": 1,          # Show login menu in topbar
        "SSO": 0,                    # Show Signle Sign on
        "DO_NOT_SHOW_LOGIN" : 0,     # DO not allow usernme/passwd -> Just SSO
		"ALLOW_REGISTRATION": 1,     # Allow registering (self registration)
    }    
    analytics.loganalytics(request);
    
    return context
