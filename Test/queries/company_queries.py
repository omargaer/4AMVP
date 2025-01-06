from Test.models import *
# region Company
def get_all_groups():
    return CompanyGroup.objects.all()
def get_group_by_name(name):
    return CompanyGroup.objects.get(name=name)
# endregion Company

def get_all_companies():
    return Company.objects.all()
def get_company_by_name(name):
    return Company.objects.get(name=name)
def get_all_companies_by_group(group):
    return Company.objects.filter(group=group)