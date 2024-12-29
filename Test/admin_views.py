from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET

from Test.models import BranchOffice, BranchOfficeLocation, Device, IndividualEntity


@staff_member_required
@require_GET
def load_branch_offices(request):
    company_id = request.GET.get('company_id')
    branch_offices = BranchOffice.objects.filter(company_id=company_id).order_by('type__name')
    data = [{'id': bo.id, 'name': str(bo)} for bo in branch_offices]
    return JsonResponse(data, safe=False)

@staff_member_required
@require_GET
def load_locations(request):
    branch_office_id = request.GET.get('branch_office_id')
    locations = BranchOfficeLocation.objects.filter(branchOffice_id=branch_office_id).order_by('room')
    return JsonResponse(list(locations.values('id', 'room', 'room_name')), safe=False)

@staff_member_required
@require_GET
def get_applicants(request):
    branch_office_id = request.GET.get('branch_office')
    branch_office = get_object_or_404(BranchOffice, id=branch_office_id)
    applicants = IndividualEntity.objects.filter(
        accounts__branchOffices=branch_office
    ).distinct()
    applicants_data = [{'id': applicant.id, 'full_name': applicant.full_name} for applicant in applicants]
    return JsonResponse({'applicants': applicants_data})

