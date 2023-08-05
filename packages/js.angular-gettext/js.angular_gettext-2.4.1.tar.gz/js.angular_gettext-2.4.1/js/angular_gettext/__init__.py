from fanstatic import Library, Resource
import js.angular

library = Library('gettext', 'resources')

gettext = Resource(
    library, 'angular-gettext.js',
    minified='angular-gettext.min.js',
    depends=[js.angular.angular])
