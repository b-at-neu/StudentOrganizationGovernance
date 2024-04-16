from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_POST

from student_org_gov.views_templates import post

from clubs import models
from student_org_gov.decorators import club_required, role_required
from users.models import RoleUser


@require_POST
@role_required(RoleUser.Roles.E_BOARD)
@club_required
def view(request, club_url):
    data = post(request)

    try:
        constitution = models.Constitution.objects.get(pk=data.get("pk"))
    except:
        return HttpResponseBadRequest(f"Constitution model data with pk '{data.get('pk')}' not found")
    
    articles_list = list(constitution.articles.all())

    for article in articles_list:

        try:
            article_data = next(filter(lambda i: i["pk"] == article.pk, data.get("articles")))
            print(article_data)
            #article_data = next(i for i in data.get("articles") if i["pk"] == article.pk)
        except StopIteration:
            # Remove article
            article.delete()
            continue

        # Update article data
        article.number = article_data.get("number")
        article.title = article_data.get("title")
        article.save()

        for section in article.sections.all():
            
            try:
                section_data = next(filter(lambda i: i["pk"] == section.pk, article_data.get("sections")))
            except StopIteration:
                # Remove section
                section.delete()
                continue

            # Update section data
            section.number = section_data.get("number")
            section.content = section_data.get("content")
            section.save()



    return JsonResponse({
        "result": "success"
    })