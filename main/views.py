import aiohttp
from rest_framework import generics
from rest_framework.response import Response
from .models import Employee
from .serializers import EmployeeSerializer


class GetEmployeesView(generics.GenericAPIView):
    serializer_class = EmployeeSerializer
    url = "http://176.192.70.122:90/fitnes_t_nfc_mobile/hs/nfc_mobile/v1/"
    username = "FitnessKit"
    password = "vY0xodyg"
    auth = aiohttp.BasicAuth(login=username, password=password)

    body = {
        "Request_id": "e1477272-88d1-4acc-8e03-7008cdedc81e",
        "ClubId": "59115d1e-9052-11eb-810c-6eae8b56243b",
        "Method": "GetSpecialistList",
        "Parameters": {
            "ServiceId": ""
        }
    }

    async def get(self, request, *args, **kwargs):
        async with aiohttp.ClientSession() as session:

            async with session.post(url=self.url, json=self.body, auth=self.auth) as response:
                if response.status == 200:
                    response_data = response.json()
                    print(response_data)
                else:
                    return Response(f"ERROR: {response.status}")

        emps_data = list()
        for data in response_data:
            emp_data = {
                'id': data.get('id', ''),
                'name': data.get('name', ''),
                'last_name': data.get('last_name', ''),
                'phone': data.get('phone', ''),
                'image_url': data.get('image_url', ''),
            }
            emps_data.append(emp_data)
        serializer = self.get_serializer(data=emps_data, many=True)
        serializer.is_valid()
        return Response(serializer.data)
