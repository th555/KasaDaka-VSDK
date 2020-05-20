from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from ..models import *

def order_list_get_redirect_url(order_list_element, session):
    if not order_list_element.final_element:
        return order_list_element.redirect.get_absolute_url(session)
    else:
        return None
    


def order_list(request, element_id, session_id):
    # get audio file urls corresponding to recorded orders
    order_sessions = CallSession.objects.filter(order_placed=True)
    audio_files = [str(get_list_or_404(
        SpokenUserInput.objects.filter(session=order_session))[0].audio)
        for order_session in order_sessions]
    
    # Make context
    order_list_element = get_object_or_404(OrderList, pk=element_id)
    session = get_object_or_404(CallSession, pk=session_id)
    redirect_url = order_list_get_redirect_url(order_list_element,session)
    language = session.language
    context = {
        'order_audio_urls': audio_files,
        'redirect_url': order_list_get_redirect_url(order_list_element, session),
        'language': language,
        'order_number_voice_label': order_list_element.order_number_label.get_voice_fragment_url(language)
    }

    return render(request, 'orderlist.xml', context, content_type='text/xml')

