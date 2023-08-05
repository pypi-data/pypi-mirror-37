## Script (Python) "notificaHome"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=state_change_info
##title=
##
mail_host = context.MailHost
plone_utils = context.plone_utils

message = """E' stato sottoposto a revisione un nuovo contenuto destinato alla home-page.

Titolo del documento: "%s"

%s""" % (context.title_or_id(), context.absolute_url())

member = context.portal_membership.getAuthenticatedMember()
memail = member.getProperty('email')

subject = "Notifica revisione contenuto"

encoding = plone_utils.getSiteEncoding()

mail_host.send(message,
               send_to_address,
               memail,
               subject=subject,
               subtype='plain',
               charset=encoding,
               debug=False,
               From=memail)
