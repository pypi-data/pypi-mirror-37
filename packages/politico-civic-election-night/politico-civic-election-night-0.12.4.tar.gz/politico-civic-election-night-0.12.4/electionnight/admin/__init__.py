from django.contrib import admin

from electionnight.models import (
    PageContent,
    PageContentType,
    PageType,
    CandidateColorOrder,
)

from .page_content import PageContentAdmin
from .color_order import CandidateColorOrderAdmin

admin.site.register(PageContent, PageContentAdmin)
admin.site.register(PageContentType)
admin.site.register(PageType)
admin.site.register(CandidateColorOrder, CandidateColorOrderAdmin)
