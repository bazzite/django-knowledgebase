#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-knowledgebase
------------

Tests for `django-knowledgebase` models module.
"""

from __future__ import absolute_import, unicode_literals

from markupfield.fields import Markup

from django_knowledgebase.base.choices import STATUS
from django_knowledgebase.models import Article
from ..tests import ArticleCategorySetUpMixin


class ArticleTest(ArticleCategorySetUpMixin):

    def test_create_new_article(self):
        obj1 = self.articles_one[2]
        obj2 = self.custom_article[0]

        self.assertTrue(obj1.title)
        self.assertTrue(obj1.created)
        self.assertTrue(obj1.modified)

        self.assertEqual(obj1.title, str(obj1))
        self.assertEqual(obj1.title, 'Article3')
        self.assertEqual(obj1.created_by, self.user_one)

        self.assertIsInstance(obj1.content, Markup)

        self.assertEqual(obj2.title, 'Custom Article')
        self.assertEqual(obj2.content.markup_type, 'markdown')
        self.assertEqual(obj2.content.raw, '# Title')
        self.assertEqual(obj2.content.rendered, '<h1>Title</h1>')

    def test_article_querysets(self):
        self.assertEqual(len(Article.objects.by_author(self.user_one)), 15)
        self.assertEqual(len(Article.objects.published()), 6)
        self.assertEqual(len(Article.objects.unpublished()), 13)

    def test_article_status(self):
        self.assertEqual(self.articles_one[0].status, STATUS.draft)
        self.assertEqual(self.articles_two[0].status, STATUS.published)
        self.assertEqual(self.articles_three[0].status, STATUS.draft)

    def tearDown(self):
        pass
