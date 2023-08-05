from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from secretballot import enable_voting_on

from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel, FieldRowPanel,
    MultiFieldPanel
)

from molo.core.utils import generate_slug
from molo.core.models import (
    ArticlePage, TranslatablePageMixinNotRoutable,
    PreventDeleteMixin, Main, index_pages_after_copy,
)


class YourTipsIndexPage(Page, PreventDeleteMixin):
    """
    The YourTips page is created inside this index.
    """
    parent_page_types = ['core.Main']
    subpage_types = ['yourtips.YourTip']

    def copy(self, *args, **kwargs):
        site = kwargs['to'].get_site()
        main = site.root_page
        YourTipsIndexPage.objects.child_of(main).delete()
        super(YourTipsIndexPage, self).copy(*args, **kwargs)


@receiver(index_pages_after_copy, sender=Main)
def create_yourtips_index_page(sender, instance, **kwargs):
    index_title = 'Your Tips'
    if not instance.get_children().filter(title=index_title).exists():
        yourtips_tip_page_index = YourTipsIndexPage(
            title=index_title,
            slug='yourtips-{}'.format(generate_slug(instance.title)))
        instance.add_child(instance=yourtips_tip_page_index)
        yourtips_tip_page_index.save_revision().publish()


class YourTipsSectionIndexPage(Page, PreventDeleteMixin):
    """
    All the converted tips are listed under this index.
    """
    parent_page_types = ['core.Main']
    subpage_types = []

    def copy(self, *args, **kwargs):
        site = kwargs['to'].get_site()
        main = site.root_page
        YourTipsSectionIndexPage.objects.child_of(main).delete()
        super(YourTipsSectionIndexPage, self).copy(*args, **kwargs)


@receiver(index_pages_after_copy, sender=Main)
def create_yourtips_section_index_page(sender, instance, **kwargs):
    index_title = 'Converted Tips'
    if not instance.get_children().filter(title=index_title).exists():
        yourtips_tip_section_page_index = YourTipsSectionIndexPage(
            title=index_title,
            slug='tips-{}'.format(generate_slug(instance.title)))
        instance.add_child(instance=yourtips_tip_section_page_index)
        yourtips_tip_section_page_index.save_revision().publish()


class YourTip(TranslatablePageMixinNotRoutable, Page):
    """
    This model links the views and store settings for the yourtips module.
    Note that:
    * title: Is used throughout the module where the name of
        the module need to be displayed.
    * description: Is used to display the YourTip description.
    * homepage_action_copy: Is used to change the text of the banner.
    * extra_style_hints: Is used to change style of the link on the main page.
    """
    parent_page_types = [
        'yourtips.YourTipsIndexPage'
    ]
    subpage_types = []
    description = models.TextField(null=True, blank=True)

    extra_style_hints = models.TextField(
        default='',
        null=True, blank=True,
        help_text=_(
            "Styling options that can be applied to this section "
            "and all its descendants"))

    homepage_action_copy = models.CharField(
        null=True, blank=True,
        verbose_name="Homepage Banner Copy",
        max_length=255)

    language = models.ForeignKey('core.SiteLanguage',
                                 blank=True,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 )
    translated_pages = models.ManyToManyField("self", blank=True)

    def get_effective_extra_style_hints(self):
        return self.extra_style_hints

    @staticmethod
    def get_number_of_tips():
        return YourTipsArticlePage.objects.all(
        ).count()

    @staticmethod
    def get_number_of_popular_tips():
        return YourTipsArticlePage.objects.filter(
            votes__gte=1
        ).distinct().count()

    class Meta:
        verbose_name = 'YourTip'
        verbose_name_plural = 'YourTips'


YourTip.content_panels = [
    FieldPanel('title', classname='full title'),
    FieldPanel('description'),
]

YourTip.settings_panels = [
    MultiFieldPanel(
        [
            FieldRowPanel(
                [
                    FieldPanel('extra_style_hints'),
                    FieldPanel('homepage_action_copy')
                ], classname="label-above"
            )
        ],
        "Meta")
]


class YourTipsEntry(models.Model):
    """
    This model is used to store the user submitted tip entries.
    Note that:
    * If the user is logged in, the user will be saved in the user field.
    * The optional_name field allows the user to
        enter a name to display with his/her tip.
    """
    submission_date = models.DateField(null=True, blank=True,
                                       auto_now_add=True)
    optional_name = models.CharField(null=True, blank=True, max_length=30)
    user = models.ForeignKey('auth.User', blank=True, null=True)
    tip_text = models.CharField(max_length=140)
    allow_share_on_social_media = models.BooleanField()

    converted_article_page = models.ForeignKey(
        'yourtips.YourTipsArticlePage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='tip_entries',
        help_text=_(
            'Your tip article page to which the entry was converted to')
    )

    class Meta:
        verbose_name = 'YourTips Entry'
        verbose_name_plural = 'YourTips Entries'


class YourTipsArticlePage(ArticlePage):
    """
    This model is used to store the converted tip entry as an ArticlePage.
    Note that:
    * A converted tip can be promoted to show on the homepage by enabling
        the featured_in_homepage setting and setting a date range.
    * tag field: The first tag displays as a heading for the tip.
    * image field: The first image displays as an icon for the tip.
    """
    parent_page_types = ['yourtips.YourTipsSectionIndexPage']
    subpage_types = []

    featured_homepage_promote_panels = [
        FieldPanel('featured_in_homepage'),
        FieldPanel('featured_in_homepage_start_date'),
        FieldPanel('featured_in_homepage_end_date'),
    ]


YourTipsArticlePage.promote_panels = [
    MultiFieldPanel(
        YourTipsArticlePage.featured_homepage_promote_panels,
        "Featuring in Homepage"
    )
]
enable_voting_on(YourTipsArticlePage)
