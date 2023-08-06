from django.db import models

from ambition_subject.choices import POS_NEG_NA
from edc_constants.choices import YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE


class BiosynexSemiQuantitativeCragMixin(models.Model):

    bios_crag = models.CharField(
        verbose_name='Biosynex Semi-quantitative CrAg performed?',
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text='Gaborone and Blantyre only',
        max_length=5,
    )

    crag_control_result = models.CharField(
        verbose_name='Control result',
        choices=POS_NEG_NA,
        default=NOT_APPLICABLE,
        help_text='Gaborone and Blantyre only',
        max_length=5)

    crag_t1_result = models.CharField(
        verbose_name='T1 result',
        choices=POS_NEG_NA,
        default=NOT_APPLICABLE,
        help_text='Gaborone and Blantyre only',
        max_length=5)

    crag_t2_result = models.CharField(
        verbose_name='T2 result',
        choices=POS_NEG_NA,
        default=NOT_APPLICABLE,
        help_text='Gaborone and Blantyre only',
        max_length=5)

    class Meta:
        abstract = True
