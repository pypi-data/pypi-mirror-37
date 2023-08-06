# -*- coding: utf-8 -*-

from SeleniumLibrary.base import keyword, LibraryComponent
from SeleniumLibrary.keywords import JavaScriptKeywords
from os.path import abspath, dirname


def get_base_path():
    return dirname(abspath(__file__))


class WaitForTestabilityKeyword(LibraryComponent):


    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        self.js_keywords = JavaScriptKeywords(self.ctx)
        self.base_path = get_base_path()
        self.READY_CALLBACK = "var readyCallback = arguments[arguments.length - 1]"

    @keyword
    def wait_for_testability_ready(self):
        self.js_keywords.execute_async_javascript("{0}; window.testability.when.ready(function() {readyCallback()});".format(self.READY_CALLBACK))

    @keyword 
    def wait_for_document_ready(self):
        self.js_keywords.execute_async_javascript("{0}; var checkReadyState=function() { document.readyState !== 'complete' ? setTimeout(checkReadyState, 11) : readyCallback();};".format(self.READY_CALLBACK))
