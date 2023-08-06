## Script (Python) "my_camcom_worklist"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=limitAt=0
##title=Lista revisione camerale
##

if context.portal_membership.isAnonymousUser():
    return ([], False)

wf_results = list(context.portal_workflow.getWorklistsResults())
if not wf_results:
    return ([], False)

wf_results.sort(lambda x, y: cmp(x.modified(), y.modified()))
member = context.portal_membership.getAuthenticatedMember()
portal_workflow = context.portal_workflow

hasReviewLev2 = False

elem_count = 0

# Ulteriore filtro, se sono un caposervizio vedo quelli del capoufficio SOLO se ho un parametro
# particolare.
# Altrimenti ricontrollo tutti gli elementi ed elimino quelli non nello stato giusto.

tmpList = []
for j in wf_results:
    if portal_workflow.getInfoFor(j, 'review_state', '???')=='attesa':
        if (
                member.has_permission('CamCom: Approvazione livello 1',j) and \
                not member.has_permission('CamCom: Approvazione livello 2',j)
                ) or \
                (
                 member.has_permission('CamCom: Approvazione livello 2',j) and \
                 context.REQUEST.get('showcuff')=='y'
                ):
            tmpList.append(j)
            elem_count+=1
            if limitAt and elem_count>=limitAt:
                break

    elif portal_workflow.getInfoFor(j, 'review_state', '???')=='attesa_cser' and not context.REQUEST.get('showcuff',None):
        if member.has_permission('CamCom: Approvazione livello 2',j):
            hasReviewLev2 = True
            tmpList.append(j)
            elem_count+=1
            if limitAt and elem_count>=limitAt:
                break

wf_results = tmpList
return (wf_results, hasReviewLev2)