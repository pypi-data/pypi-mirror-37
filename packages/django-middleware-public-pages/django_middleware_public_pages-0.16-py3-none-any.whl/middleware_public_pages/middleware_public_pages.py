from django.http import HttpResponseRedirect
from django.core.urlresolvers import resolve, reverse, NoReverseMatch


class PublicPagesMiddleware(object):
    """
    This middleware will check if there is a version of this page for not-authenticated users. (the same URL-name with
    the suffix '_pub') and will redirect the request
    """

    def process_request(self, request):
        if not request.user.is_authenticated:
            url_name = resolve(request.path).url_name

            if not url_name.endswith("_pub"):
                url_name += "_pub"
                try:
                    rev_url = reverse(url_name)
                    return HttpResponseRedirect(rev_url, )
                except NoReverseMatch:
                    # There is no 'public' version of this url, continue the process normaly..
                    pass
