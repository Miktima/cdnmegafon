from django.test import TestCase
from django.test import Client
from django.urls import reverse
from stat_cdnnow.models import Portals_stat

class StatCdnnowTests(TestCase):
    def setUp(self):
        self.client = Client()
    def test_portal_exist(self):
        # На странице должно быть сообщение, что список порталов не заполнен
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Не заполнен список порталов")
        Portals_stat.objects.create(portal="test", id_portal="code")
        response2 = self.client.get(reverse("index"))
        self.assertEqual(response2.status_code, 200)
        self.assertNotContains(response2, "Не заполнен список порталов")


    def test_no_portal(self):
        # должен быть выбран портал, если не выбран то должна появляться ошибка 
        response = self.client.post(reverse("results"), {
            "portal": "no_select",
            "year": "2022",
            "month": "1",
            "day": "20"
        })
        self.assertEqual(response.status_code, 302)



    

