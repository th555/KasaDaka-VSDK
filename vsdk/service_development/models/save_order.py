from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from .vs_element import VoiceServiceElement

class SaveOrder(VoiceServiceElement):
    """
    An element that presents a Voice Label to the user.
    """
    _urls_name = 'service-development:save_order'
    final_element = models.BooleanField(_('This element will terminate the call'),default = False)
    _redirect = models.ForeignKey(
            VoiceServiceElement,
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            related_name='%(app_label)s_%(class)s_related',
            verbose_name=_('Redirect element'),
            help_text = _("The element to redirect to."))

    class Meta:
        verbose_name = _('Save Order Element')

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
        errors.extend(super(SaveOrder, self).validator())
        if not self.final_element and not self._redirect:
            errors.append(ugettext('Message %s does not have a redirect element and is not a final element')%self.name)
        elif not self.final_element:
            if self._redirect.id == self.id:
                errors.append(ugettext('There is a loop in %s')%str(self))


        return errors
