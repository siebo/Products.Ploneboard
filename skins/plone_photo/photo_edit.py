## Script (Python) "image_edit"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=precondition='', field_file='', field_id='', title=None, description=None
##title=Edit a photo
##
from Products.CMFPlone import transaction_note
qst='portal_status_message=Photo+changed.'
REQUEST=context.REQUEST

if not field_id:
    field_id=context.getId()
    REQUEST.set('field_id', field_id)

file,id=field_file, field_id

context.edit(
     precondition=precondition,
     file=file)

errors=context.validate_image_edit()
if REQUEST.has_key('errors'):
    form=getattr( context, context.getTypeInfo().getActionById( 'edit' ) )
    return form()

filename=getattr(file,'filename', '')
if file and filename: #context.isIDAutoGenerated(id):
    id=filename[max( string.rfind(filename, '/')
                   , string.rfind(filename, '\\')
                   , string.rfind(filename, ':') )+1:]

if not context.isIDAutoGenerated(id): 
    context.REQUEST.set('id', id)

if hasattr(context, 'extended_edit'):
    REQUEST.set('portal_status_message', 'Photo+changed.')
    edit_hook=getattr(context,'extended_edit')
    response=edit_hook(redirect=0)
    if response:
        return response

context.rename_object(redirect=0, id=id)
tmsg='/'.join(context.portal_url.getRelativeContentPath(context)[:-1])+'/'+context.title_or_id()+' has been modified.'
transaction_note(tmsg)
target_action = context.getTypeInfo().getActionById( 'view' )
context.REQUEST.RESPONSE.redirect( '%s/%s?%s' % ( context.absolute_url()
                                                , target_action
                                                , qst
                                                ) )