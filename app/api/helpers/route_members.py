from ..route.serializers import MemberSerializer
from ..route.models import Route

def add_route_member(request):
    serializer_class = MemberSerializer
    route = Route.objects.filter(created_by=request.user.id)[0]
    serializer = serializer_class(data={'route':route.id})
    serializer.is_valid(raise_exception=True)
    serializer.save(member=request.user)
