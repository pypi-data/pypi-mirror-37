import os
import time
import urllib.request
from bs4 import BeautifulSoup
from channels.test import ChannelLiveServerTestCase
from django.core.files import File
from django.conf import settings
from django.contrib.auth.models import User
from django.test import Client, TestCase, LiveServerTestCase
from pyvirtualdisplay import Display
from selenium import webdriver
from yogasoft.settings import BASE_DIR
from .models import (
    BlogPost,
    BlogPostImage,
    ImageContentClass,
    PortfolioContent,
    Tag,
    UserYoga
)

# Create your tests here.

class ChannelsTestCase(ChannelLiveServerTestCase):
    """Using selenium. Make two tabs. Write comment in one tab.
    Check if another tab has this comment. If has channels work."""

    def setUp(self):
        user = User(
            last_name='Saakashvili',
            first_name='Michael',
            email='michael@gmail.com',
            username='saakashvili',
        )
        user.set_password('ppassword')
        user.save()
        user_yoga = UserYoga.objects.get(user=user)
        user_yoga.auth_by_sn = True
        user_yoga.is_admin = True
        user_yoga.save()

        bp = BlogPost.objects.create(
            author=user,
            name='Testing Channels',
            nameUA='Тестуємо Канали',
            text='We use channels for async requests and websockets.',
            textUA='Канали в річці це круто.',

        )
        bp.save()

        blog_image = BlogPostImage()
        blog_image.content = bp
        file = open(BASE_DIR + '/blog2.png', 'wb')
        file.write(urllib.request.urlopen('https://s3-eu-west-1.amazonaws.com/yogasoftbucket0/content_images/1.png').read())
        file.close()
        blog_image.image.save("blog2.png", File(open(BASE_DIR+'/blog2.png', "rb")))
        blog_image.save()
        self.blog_image = blog_image
        self.blog_post_id = bp.id
        self.blog_image = blog_image

        self.display = Display(visible=0, size=(1400, 1000))
        self.display.start()
        self.selenium = webdriver.Firefox()
        super(ChannelsTestCase, self).setUp()

    def tearDown(self):
        try:
            os.remove(BASE_DIR + '/blog2.png')
            self.blog_image.delete()
        except:
            pass
        self.selenium.quit()
        self.display.stop()
        super(ChannelsTestCase, self).tearDown()

    def test_channels(self):
        selenium = self.selenium

        # open first tab
        selenium.get('%s%s%s' % (self.live_server_url, '/app/blog/', self.blog_post_id))

        # open second tab
        selenium.execute_script('''window.open("about:blank", "_blank");''')
        selenium.switch_to.window(selenium.window_handles[1])
        selenium.get('%s%s%s' % (self.live_server_url, '/app/blog/', self.blog_post_id))
        # login
        time.sleep(1)
        el_login = selenium.find_element_by_class_name('dropdown')        
        time.sleep(1)
        el_login.click()
        login = selenium.find_element_by_name('username')
        login.send_keys('saakashvili')
        password = selenium.find_element_by_name('password')
        password.send_keys('ppassword')
        time.sleep(1)
        submit_button = selenium.find_element_by_xpath("//div[@id='sign_in']/button[1]")
        submit_button.click()
        time.sleep(5)


        selenium.get('%s%s%s' % (self.live_server_url, '/app/blog/', self.blog_post_id))

        text_area = selenium.find_element_by_id('id_message')
        text_area.send_keys('here is test message')

        submit_comment = selenium.find_element_by_xpath("//input[@value='Add comment']")
        submit_comment.click()
        time.sleep(1)
        # switch to first tab
        selenium.switch_to.window(selenium.window_handles[0])
        time.sleep(2)

        p_text = selenium.find_element_by_xpath("//div[@class='media']/div[@class='media-body']/p[1]").text

        self.assertEquals(p_text, 'here is test message', 'channels dont work message is not correct')






class LanguageTestCase(TestCase):
    """ here we test english and ukrainian language"""

    def setUp(self):
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')

    def test_ukrainian_words_using_cookie(self):

        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: 'uk'})
        response = self.client.get('/app/index/')

        html_doc = response.content

        soup = BeautifulSoup(html_doc, 'html.parser')

        texts =[ text.strip() for text in  soup.findAll(text=True)]

        set_texts = set(texts)
        set_uk_words = {'Домашня сторінка', 'Портфоліо', 'Відгуки', 'Блог', 'Створити акаунт', 'Пароль', 'Втратив пароль ?', 'Хмара тегів'}

        self.assertEquals(len(set_texts & set_uk_words), 8, 'wrong number of words in test_ukrainian_words_using_cookie')

    def test_english_words_using_header(self):

        response = self.client.get('/app/index/', HTTP_ACCEPT_COOKIE_NAME='en')

        html_doc = response.content

        soup = BeautifulSoup(html_doc, 'html.parser')

        texts = [text.strip() for text in soup.findAll(text=True)]

        set_texts = set(texts)
        set_uk_words = {'Home', 'Blog', 'Testimonials', 'Contact us', 'Create account', 'Password', 'Lost password ?',
                        'Tag cloud'}

        self.assertEquals(len(set_texts & set_uk_words), 8,
                          'wrong number of words in test_english_words_using_header')


class MainPagesPresentTestCase(TestCase):

    def setUp(self):
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')

    def test_main_pages_exists(self):

        response = self.client.get('/app/index/')
        self.assertEqual(response.status_code, 200, 'wrong response code at test_main_pages_exists')

        response = self.client.get('/app/blog/')
        self.assertEqual(response.status_code, 200, 'wrong response code at test_main_pages_exists')

        response = self.client.get('/app/portfolio/')
        self.assertEqual(response.status_code, 200, 'wrong response code at test_main_pages_exists')

        response = self.client.get('/app/testimonials/')
        self.assertEqual(response.status_code, 200, 'wrong response code at test_main_pages_exists')

        response = self.client.get('/app/contact_us/')
        self.assertEqual(response.status_code, 200, 'wrong response code at test_main_pages_exists')


class MemcahedTestCase(LiveServerTestCase):

    def setUp(self):

        tag = Tag.objects.create(name='AWS S3')
        pr = PortfolioContent.objects.create(
            name='scraper 5',
            nameUA='скрапер 5',
            description='scraping amazon',
            descriptionUA='скрапимо амазон',
            technologies='AWS',
            link='',
            client='',
        )
        pr.tags.add(tag)
        pr.save()

        image = ImageContentClass()
        image.content = pr
        file = open(BASE_DIR+'/test.png', 'wb')
        file.write(urllib.request.urlopen('https://s3-eu-west-1.amazonaws.com/yogasoftbucket0/content_images/0.png').read())
        file.close()
        image.image.save("NowHiring.png", File(open(BASE_DIR+"/test.png", "rb")))
        image.save()
        self.image = image
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()
        self.selenium = webdriver.Firefox()
        super(MemcahedTestCase, self).setUp()

    def tearDown(self):
        try:
            os.remove(BASE_DIR+'/test.png')
            self.image.delete()
        except:
            pass

        self.selenium.quit()
        self.display.stop()
        super(MemcahedTestCase, self).tearDown()


    def test_memcached(self):

        selenium = self.selenium
        #why4 I dont know        
        selenium.get('%s%s' % (MemcahedTestCase.live_server_url, '/app/portfolio/4'))
        time.sleep(1)
        res0 = selenium.page_source
        time.sleep(2)
        selenium.get('%s%s' % (MemcahedTestCase.live_server_url, '/app/portfolio/4'))
        time.sleep(2)
        res1 = selenium.page_source
        selenium.get('%s%s' % (MemcahedTestCase.live_server_url, '/app/portfolio/4'))
        time.sleep(2)
        res2 = selenium.page_source

        self.assertEquals(res1, res2, 'memcache dont work. Check settings or memcache daemon.')


class PortfolioTestCase(TestCase):

    def setUp(self):
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        tag = Tag.objects.create(name='AWS S3')

        pr = PortfolioContent.objects.create(
            name='scraper 5',
            nameUA = 'скрапер 5',
            description = 'scraping amazon',
            descriptionUA = 'скрапимо амазон',
            technologies = 'AWS',
            link = '',
            client= '',
        )
        pr.tags.add(tag)
        pr.save()


    def testPortfolioExists(self):
        portfolio_content = PortfolioContent.objects.all()
        self.assertGreaterEqual(len(portfolio_content), 1, 'portfolio content object was not created')
        self.assertEqual(len(portfolio_content), 1, 'portfolio content object was not created')
        self.assertEqual(len(portfolio_content[0].tags.all()), 1, 'portfolio content object was not created')

    def testTagExist(self):
        self.assertEqual(len(Tag.objects.all()), 1, 'test if created tag exists')
        self.assertEqual(Tag.objects.all()[0].name, 'AWS S3', 'tag name is incorrect')

    def testMainPage(self):

        response = self.client.get('/app/index/')
        self.assertEqual(response.status_code, 200, 'wrong response code')

        html_doc = response.content
        soup = BeautifulSoup(html_doc, 'html.parser')

        self.assertEqual(soup.title.string, 'Yogasoft', 'wrong title for main page')

        div_class_myclas = soup.find_all("div", {"class": "myclas"})

        self.assertEqual(len(div_class_myclas), 1, 'wrong count div myclass')

        div_class_tagcloud = div_class_myclas[0].find_all("div", {"class": "tagcloud"})

        self.assertEqual(len(div_class_tagcloud), 1, 'wrong count div tagcloud')

        ul = div_class_tagcloud[0].find_all("ul")

        self.assertEqual(len(ul), 1, 'wrong ul count')

        li = ul[0].find_all("li")

        self.assertEqual(len(li), 1, 'wrong li count')

        a = li[0].find_all("a")

        self.assertEqual(len(a), 1, 'wrong a count')
        self.assertEqual(a[0].string, "AWS S3", 'wrong tag name')


class UserTestCase(TestCase):
    """Tests if we can login correctly."""
    def setUp(self):

        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')

        user = User(
            last_name='Poroshenko',
            first_name='Petro',
            email='poroshenko@gmail.com',
            username='poroshenko3',
        )
        user.set_password('ppassword')
        user.save()
        user_yoga = UserYoga.objects.get(user=user)
        user_yoga.auth_by_sn=False
        user_yoga.is_admin=True
        user_yoga.save()

    def testUserExists(self):

        response = self.client.get('/app/index/')
        self.assertEqual(response.status_code, 200, 'wrong response status code')

        response = self.client.post('/accounts/login/',
                                    {'username': 'poroshenko3', 'password': 'ppassword'},
                                    follow=True) #follow = True for redirect from page

        html_doc = response.content

        soup = BeautifulSoup(html_doc, 'html.parser')

        result_a = [link.get('href') for link in soup.find_all('a') if link.get('href')=='/accounts/logout/' ]
        self.assertEqual(len(result_a), 1, 'wrong len of logout a')


