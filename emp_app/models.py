from django.db import models

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100,null = False)
    location = models.CharField(max_length=100)
    
    def __str__(self):
      return self.name

    
    
class Role (models.Model):
    name = models.CharField(max_length=100,null = False)
    
    def __str__(self):
       return self.name
    

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2)
    hire_date = models.DateTimeField()
    row_number = models.PositiveIntegerField(default=0)  # Ensure this field is present
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)


    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"