from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from .vs_element import VoiceServiceElement
from .user_input import UserInputCategory
from .voicelabel import VoiceLabel

class OrderList(VoiceServiceElement):
    """
    An element that presents the list of available orders to the seller.
    """
    _urls_name = 'service-development:order_list'

    input_category_order = models.ForeignKey(
        UserInputCategory,
        verbose_name = _('Input category'),
        help_text = _('Select the category that holds the recorded orders.'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='input_category_order2',
    )

    order_number_label = models.ForeignKey(
            VoiceLabel,
            verbose_name = _('Order number label'),
            help_text = _('The label that is played before playing each order number, i.e. [Order number] one: some order'),
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            )

    final_element = models.BooleanField(_('This element will terminate the call'),default = False)
    _redirect = models.ForeignKey(
            VoiceServiceElement,
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            related_name='%(app_label)s_%(class)s_related',
            verbose_name=_('Redirect element'),
            help_text = _("The element to redirect to after the message has been played."))

    class Meta:
        verbose_name = _('Order list')

    @property
    def redirect(self):
        """
        Returns the actual subclassed object that is redirected to,
        instead of the VoiceServiceElement superclass object (which does
        not have specific fields and methods).
        """
        if self._redirect :
            return VoiceServiceElement.objects.get_subclass(id = self._redirect.id)
        else: 
            return None

    def __str__(self):
        return _("Message: ") + self.name

    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True
    is_valid.short_description = _('Is valid')

    def validator(self):
        errors = []
        errors.extend(super(OrderList, self).validator())
        if not self.final_element and not self._redirect:
            errors.append(ugettext('Message %s does not have a redirect element and is not a final element')%self.name)
        elif not self.final_element:
            if self._redirect.id == self.id:
                errors.append(ugettext('There is a loop in %s')%str(self))


        return errors
