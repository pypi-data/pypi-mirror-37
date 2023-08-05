from django.core.urlresolvers import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView

from molo.core.templatetags.core_tags import get_pages

from molo.yourtips.forms import YourTipsEntryForm
from molo.yourtips.models import YourTip, YourTipsArticlePage


class YourTipsEntryView(CreateView):
    """
    A CreateView for tip entry form.
    :return: redirect to the thank you page on successful tip submission.
    """
    form_class = YourTipsEntryForm
    template_name = 'yourtips/your_tips_entry.html'

    def get_context_data(self, *args, **kwargs):
        context = (super(YourTipsEntryView, self)
                   .get_context_data(*args, **kwargs))
        tip_page = YourTip.objects.all().first()
        context.update({'tip_page': tip_page})
        return context

    def get_success_url(self):
        return reverse(
            'molo.yourtips:thank_you',
            args=[self.object.tip_page.slug])

    def form_valid(self, form):
        tip_page = YourTip.objects.all().first()
        form.instance.tip_page = (
            tip_page
            .get_main_language_page()
            .specific)
        if self.request.user.is_anonymous():
            form.instance.user = None
        else:
            form.instance.user = self.request.user
        return super(YourTipsEntryView, self).form_valid(form)


class ThankYouView(TemplateView):
    """
    A TemplateView for the thank you page.
    """
    template_name = 'yourtips/thank_you.html'

    def get_context_data(self, *args, **kwargs):
        context = (super(ThankYouView, self)
                   .get_context_data(*args, **kwargs))
        tip_page = YourTip.objects.all().first()
        context.update({'tip_page': tip_page})
        return context


class YourTipsRecentView(ListView):
    """
    A ListView for the recent tips.
    :return: All tips ordered by latest_revision_created_at field.
    """
    template_name = "yourtips/recent_tips.html"

    def get_queryset(self, *args, **kwargs):
        main = self.request.site.root_page
        context = {'request': self.request}
        locale = self.request.LANGUAGE_CODE
        articles = (YourTipsArticlePage.objects
                    .descendant_of(main)
                    .order_by('-latest_revision_created_at'))
        return get_pages(context, articles, locale)

    def get_context_data(self, *args, **kwargs):
        context = (super(YourTipsRecentView, self)
                   .get_context_data(*args, **kwargs))
        context.update({
            'view_title': 'Recent Tips',
            'your_tip_page_slug': YourTip.objects.first().slug
        })
        return context


class YourTipsPopularView(ListView):
    """
    A ListView for the popular tips (most liked).
    :return: All tips with at least one like ordered by number of likes.
    """
    template_name = "yourtips/popular_tips.html"

    def get_queryset(self, *args, **kwargs):
        main = self.request.site.root_page
        context = {'request': self.request}
        locale = self.request.LANGUAGE_CODE
        articles = (YourTipsArticlePage.objects
                    .descendant_of(main)
                    .filter(votes__isnull=False)
                    .order_by('-total_upvotes')
                    .distinct())
        return get_pages(context, articles, locale)

    def get_context_data(self, *args, **kwargs):
        context = (super(YourTipsPopularView, self)
                   .get_context_data(*args, **kwargs))
        context.update({
            'view_title': 'Popular Tips',
            'your_tip_page_slug': YourTip.objects.first().slug,
        })
        return context
