import re
from django.core.management import BaseCommand, call_command
from django.db import connection, connections
from django.template.defaultfilters import slugify

from dashboard.models import Templates, TemplateGroup


class Command(BaseCommand):


     def handle(self, *args, **options):
        cursor = connections['app'].cursor()
        sql="select * from template_group_table where status = 'Y'"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            group_id = row[0]
            group_name = row[1]
            try:
                group=TemplateGroup.objects.get(group_id=group_id)
                group.group_name=group_name
                group.save()
            except:
                group=TemplateGroup()
                group.group_id=group_id
                group.group_name = group_name
                group.save()

        sql="select * from writewell.templates where status ='Y' and template_type=1"
        cursor.execute(sql)
        result=cursor.fetchall()
        for idx,row in enumerate(result):
            print("Synced "+str(idx)+" templates \n")
            ext_id=row[0]
            title=row[1]
            slug=slugify(title)
            title = re.sub('\W+', ' ', title)
            desc=row[5];
            group_id=row[6]
            try:
                template=Templates.objects.get(slug=slug)
                template.description=desc
                template.ext_id=ext_id
                template.template_group_id=group_id
                template.save()
            except:
                try:
                    template=Templates()
                    template.ext_id=ext_id
                    template.title=title
                    template.slug=slug
                    template.description=desc
                    template.template_group_id = group_id
                    template.save()
                except:
                    print("Error with "+title)
        call_command('rebuild_index', "--noinput")





