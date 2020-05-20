from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.urls import reverse

from ..models import *

def order_list_get_redirect_url(order_list_element, session):
    if not order_list_element.final_element:
        return order_list_element.redirect.get_absolute_url(session)
    else:
        return None
    


def order_list(request, element_id, session_id):
    # get audio file urls corresponding to recorded orders
    session = get_object_or_404(CallSession, pk=session_id)

    order_sessions = CallSession.objects.filter(order_placed=True)
    audio_files = [str(get_list_or_404(SpokenUserInput.objects.filter(session=order_session))[0].audio) for order_session in order_sessions]

    language = session.language
    order_list_element = get_object_or_404(OrderList, pk=element_id)
    redirect_url_POST = reverse('service-development:order_list', args = [element_id, session.id])
    
    if request.method == "POST" and 'choice' in request.POST:
        # We got an answer back, now delete it
        choice_number = int(request.POST["choice"][0])

        # Where to go if user wants to try again
        redirect_url_retry = reverse('service-development:order_list', args = [element_id, session.id])


        context = {
            "order_chosen_label": order_list_element.order_chosen_label.get_voice_fragment_url(language),
            "number": language.get_interface_numbers_voice_label_url_list[choice_number],
            "choice_number": choice_number,
            "chosen_order_audio": audio_files[choice_number-1],
            "order_confirm_label": order_list_element.order_confirm_label.get_voice_fragment_url(language),
            "redirect_url_retry": redirect_url_retry,
            "redirect_url_POST": redirect_url_POST
        }
        return render(request, 'delete_order.xml', context, content_type='text/xml')
    elif request.method == "POST" and 'deletethis' in request.POST:
        # Actually perform the delete here
        delete_number = int(request.POST["deletethis"][0])
        order_sessions[delete_number-1].order_placed = False
        order_sessions[delete_number-1].save()

        context = {
            'order_number_voice_label': order_list_element.order_number_label.get_voice_fragment_url(language),
            "number": language.get_interface_numbers_voice_label_url_list[delete_number],
            "hasbeenremoved": order_list_element.order_delete_label.get_voice_fragment_url(language),
            'redirect_url': order_list_get_redirect_url(order_list_element, session)
        }
        return render(request, 'do_delete.xml', context, content_type='text/xml')
    else:
        # Display order list and let user type an answer

        # This is the redirect URL to POST the chosen order
        # back to this method
        
        # Make context
        context = {
            'order_audio_urls': audio_files,
            'language': language,
            'order_number_voice_label': order_list_element.order_number_label.get_voice_fragment_url(language),
            'instructions_label': order_list_element.voice_label.get_voice_fragment_url(language),
            'redirect_url_POST': redirect_url_POST
        }

        return render(request, 'orderlist.xml', context, content_type='text/xml')


