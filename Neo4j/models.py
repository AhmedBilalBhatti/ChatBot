from neomodel import StructuredNode, StringProperty, IntegerProperty,UniqueIdProperty, RelationshipTo, RelationshipFrom,DateProperty,DateTimeProperty,ArrayProperty
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
import base64
import json
import os

class signups(StructuredNode):
    username = StringProperty(unique_index=False)
    password = StringProperty()
    email = StringProperty(unique_index=True)
    date_of_birth = DateProperty()
    image = StringProperty(default=f"data:image/png;base64,{base64.b64encode(open(os.path.join(settings.BASE_DIR, 'static/images', 'd.png'), 'rb').read()).decode('utf-8')}")
    created_at = DateTimeProperty(default_now=True)
    nick_name = StringProperty(default=None)
    gender = StringProperty()
    has_ip = RelationshipTo('IP', 'HAS_IP')
    chats = RelationshipTo('User_Chat', 'HAS')
    excluded = RelationshipTo('Exclude', 'HAS_EXCLUDED')
    item = RelationshipTo('Items', 'HAS')
    item1 = RelationshipTo('Items', 'HAS_ANOTHER')
    frnd = RelationshipTo('Friends', 'KNOWS')
    friend = RelationshipFrom('Friends', 'IS_A_FRIEND_OF')
    friend1 = RelationshipFrom('Friends', 'IS_PARENT_OF')
    ff = RelationshipFrom('Friends', 'IS_MOTHER_OF')
    ff1 = RelationshipFrom('Friends', 'IS_FATHER_OF')
    friend2 = RelationshipFrom('Friends', 'IS_SIBLING_OF')
    fr = RelationshipFrom('Friends', 'IS_SISTER_OF')
    fr1 = RelationshipFrom('Friends', 'IS_BROTHER_OF')
    love = RelationshipFrom('Friends', 'LOVES')
    bot = RelationshipTo('Bot_resp', 'HAS')
    memory = RelationshipTo('Memory', 'HAS')
    u = RelationshipTo('Prolog', 'HAS_RULES_OF')


class IP(StructuredNode):
    email = StringProperty()
    ip = StringProperty()
    created_at = DateTimeProperty(default_now=True)


class Exclude(StructuredNode):
    email = StringProperty()
    names = StringProperty()
    user = RelationshipFrom('signups', 'HAS_EXCLUDED')
    of = RelationshipTo('E_names', 'OF')


class E_names(StructuredNode):
    email = StringProperty()
    names = StringProperty()


class Items(StructuredNode):
    email = StringProperty()
    item_name = StringProperty()
    charistic = RelationshipTo('Charistics', 'IS')


class Friends(StructuredNode):
    email = StringProperty()
    name = StringProperty()
    gender = StringProperty()


class Charistics(StructuredNode):
    email = StringProperty()
    item_char = StringProperty()


class Memory(StructuredNode):
    email = StringProperty()
    name = StringProperty()
    rel = RelationshipTo('MemoryStore', 'HAS')


class User_Chat(StructuredNode):
    email = StringProperty(unique_index=True)
    name = StringProperty()
    chat = ArrayProperty(StringProperty())
    created_at = DateTimeProperty(default_now=True)

    def save_message(self, message_content):
        if self.chat is None:
            self.chat = []

        self.chat.append(message_content)
        self.save()


class Bot_resp(StructuredNode):
    email = StringProperty()
    name = StringProperty()
    responses = ArrayProperty(StringProperty())
    created_at = DateTimeProperty(default_now=True)

    def save_message(self, message_content):
        if self.responses is None:
            self.responses = []

        self.responses.append(message_content)
        self.save()


class MemoryStore(StructuredNode):
    email = StringProperty()
    name = StringProperty()
    start_session = DateTimeProperty(default_now=True)
    end_session = DateTimeProperty()
    sentiments = StringProperty()
    memory_list = ArrayProperty(StringProperty())


    def save_message(self, message_type, message_content):
        if self.memory_list is None:
            self.memory_list = []

        message = f"{message_type}: {message_content}"
        self.memory_list.append(message)
        self.save()


class Prolog(StructuredNode):
    email = StringProperty()
    name = StringProperty()
    rule = ArrayProperty(StringProperty())

    def save_message(self, message_content):
        if self.rule is None:
            self.rule = []

        self.rule.append(message_content)
        self.save()


# ==============================================================================================


class Contact_Us(models.Model):
    Name = models.CharField(max_length=50)
    Gmail = models.EmailField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Contact_Us"

    def __str__(self):
        return self.Gmail


class Main_Page_Content(models.Model):
    heading = models.CharField(max_length=200)
    main_title =  models.TextField()
    img1 = models.ImageField(upload_to ="img/%y")
    img2 = models.ImageField(upload_to ="img/%y")
    title1 = models.CharField(max_length=200)
    title2 = models.CharField(max_length=200)
    explin1 = models.TextField()
    explin2 = models.TextField()
    class Meta:
        verbose_name_plural = "Main_Page_Content"

    def __str__(self):
        return self.heading


class About(models.Model):
    img = models.ImageField(upload_to ="img/%y")
    Maintxt1 =  models.TextField()
    Maintxt2 =  models.TextField()
    p1 = models.CharField(max_length=150)
    p2 = models.CharField(max_length=150) 
    p3 = models.CharField(max_length=150)
    p4 = models.CharField(max_length=150)
    p5 = models.CharField(max_length=150)
    p6 = models.CharField(max_length=150)
    txt1 =  models.TextField()
    txt2 =  models.TextField()

    class Meta:
        verbose_name_plural = "About"

    def __str__(self):
        return self.p1


class Help(models.Model):
    faq_question = models.TextField()
    faq_answer = models.TextField()
    class Meta:
        verbose_name_plural = "Help"

    def __str__(self):
        return self.faq_question