from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Company, Employee
import pandas as pd

class UploadEmployeeData(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(file)
            df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        required_columns = ['first_name', 'last_name', 'phone_number', 'company_name']
        for col in required_columns:
            if col not in df.columns:
                return Response({'error': f'Missing required column: {col}'}, status=status.HTTP_400_BAD_REQUEST)

        company_names = df['company_name'].unique()

        existing_companies = Company.objects.filter(name__in=company_names)
        existing_names = set(existing_companies.values_list('name', flat=True))
        new_companies = [Company(name=name) for name in company_names if name not in existing_names]
        Company.objects.bulk_create(new_companies)

        all_companies = {company.name: company.id for company in Company.objects.filter(name__in=company_names)}

        employee_objs = [
            Employee(
                first_name=row['first_name'],
                last_name=row['last_name'],
                phone_number=str(row['phone_number']),
                company_id=all_companies[row['company_name']]
            )
            for _, row in df.iterrows()
        ]

        Employee.objects.bulk_create(employee_objs)

        return Response({"message": "Data imported successfully"}, status=status.HTTP_201_CREATED)
