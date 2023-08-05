from Products.Five import BrowserView


class TopicView(BrowserView):
    """Vista dei cercatori"""
    IMG_TAG = u"""<img src="%s" alt="%s" title="%s" />"""

    def generateImgTag(self, icon, alt="", title=""):
        """Dato un'icona caricata dal tramite @@plone.getIcon ne genera un tag (X)HTML da usare
        per la modulistica
        """
        src = icon.url
        return self.IMG_TAG % (src, alt, title)
