import datetime

from molo.yourtips.models import (
    YourTip, YourTipsEntry, YourTipsArticlePage
)
from molo.yourtips.tests.base import BaseYourTipsTestCase


class TestWagtailAdminActions(BaseYourTipsTestCase):

    def test_export_entry_csv(self):
        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )

        tip_page = YourTip(
            title='Test Tip',
            description='This is the description',
            slug='test-tip')
        self.tip_index.add_child(instance=tip_page)
        tip_page.save_revision().publish()

        YourTipsEntry.objects.create(
            optional_name='Test',
            tip_text='test body',
            allow_share_on_social_media=True,
        )

        response = self.client.post('/admin/yourtips/yourtipsentry/')
        date = str(datetime.datetime.now().date())
        expected_output = (
            'Content-Length: 132\r\n'
            'Content-Language: en\r\n'
            'Content-Disposition: attachment;'
            ' filename=yourtips_entries.csv\r\n'
            'Vary: Accept-Language, Cookie\r\n'
            'Cache-Control: no-cache, no-store, private, max-age=0'
            '\r\nX-Frame-Options: SAMEORIGIN\r\n'
            'Content-Type: csv\r\n\r\n'
            'id,submission_date,optional_name,user,tip_text,'
            'allow_share_on_social_media,converted_article_page\r\n'
            '1,' + date + ',Test,,test body,1,\r\n')
        self.assertEquals(str(response), expected_output)
        response = self.client.post(
            '/admin/yourtips/yourtipsentry/?drf__submission_date__gte=' +
            date + '&drf__submission_date__lte=' + date
        )
        expected_output = (
            'Content-Length: 132\r\n'
            'Content-Language: en\r\n'
            'Content-Disposition: attachment; '
            'filename=yourtips_entries.csv\r\n'
            'Vary: Accept-Language, Cookie\r\n'
            'Cache-Control: no-cache, no-store, private, max-age=0\r\n'
            'X-Frame-Options: SAMEORIGIN\r\n'
            'Content-Type: csv\r\n\r\n'
            'id,submission_date,optional_name,user,tip_text,'
            'allow_share_on_social_media,converted_article_page\r\n'
            '1,' + date + ',Test,,test body,1,\r\n')
        self.assertEquals(str(response), expected_output)
        response = self.client.post(
            '/admin/yourtips/yourtipsentry/?drf__submission_date__gte='
            '2017-01-01&drf__submission_date__lte=2017-01-01'
        )
        expected_output = (
            'Content-Length: 99\r\n'
            'Content-Language: en\r\n'
            'Content-Disposition: attachment; '
            'filename=yourtips_entries.csv\r\n'
            'Vary: Accept-Language, Cookie\r\n'
            'Cache-Control: no-cache, no-store, private, max-age=0\r\n'
            'X-Frame-Options: SAMEORIGIN\r\nContent-Type: csv\r\n\r\n'
            'id,submission_date,optional_name,user,tip_text,'
            'allow_share_on_social_media,converted_article_page\r\n')
        self.assertEquals(str(response), expected_output)

    def test_export_article_page_csv(self):
        self.client.login(
            username=self.superuser_name,
            password=self.superuser_password
        )

        tip_page = YourTip(
            title='Test Tip',
            description='This is the description',
            slug='test-tip')
        self.tip_index.add_child(instance=tip_page)
        tip_page.save_revision().publish()

        entry = YourTipsEntry.objects.create(
            optional_name='Test',
            tip_text='test body',
            allow_share_on_social_media=True,
        )
        self.client.get(
            '/django-admin/yourtips/yourtipsentry/%d/convert/' % entry.id
        )
        article = YourTipsArticlePage.objects.get(title='Tip-%s' % entry.id)
        article.save_revision().publish()

        response = self.client.post('/admin/yourtips/yourtipsarticlepage/')

        expected_output = (
            'Tip-1,1,test body,Test')
        self.assertContains(response, expected_output)

        response = self.client.post(
            '/admin/yourtips/yourtipsarticlepage/?'
            'drf__latest_revision_created_at__gte=2017-01-01'
            '&drf__latest_revision_created_at__lte=2017-01-01'
        )

        expected_output = (
            'Tip-1,1,test body,Test')
        self.assertNotContains(response, expected_output)
