from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from ..models import SaveOrder

def save_order_get_redirect_url(save_order_element,session):
    if not save_order_element.final_element:
        return save_order_element.redirect.get_absolute_url(session)
    else:
        return None


def save_order(request, element_id, session_id):
    save_order_element = get_object_or_404(SaveOrder, pk=element_id)
    session = get_object_or_404(CallSession, pk=session_id)
    session.record_step(save_order_element)
    redirect_url = save_order_get_redirect_url(save_order_element,session)
    session.order_placed = True
    session.save()
    context = {'redirect_url': redirect_url}
    
    return render(request, 'save_order.xml', context, content_type='text/xml')

