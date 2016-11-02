# Modules
from django.conf.urls import url
from django_yaml_redirects import load_redirects
from django_template_finder_view import TemplateFinder

# Local
from webapp.views import custom_404, custom_500, MarkdownView

# Match any redirects first
urlpatterns = load_redirects()

# Try to find templates
urlpatterns.append(
    url(r'^(?P<path>core(/.*)?)$', MarkdownView.as_view())
)
urlpatterns.append(url(r'^(?P<template>.*)/?$', TemplateFinder.as_view()))

# Error handlers
handler404 = custom_404
handler500 = custom_500
