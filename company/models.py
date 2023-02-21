from django.db import models


# Create your models here.
class Company(models.Model):
    company_name = models.CharField(verbose_name="name", max_length=100)
    profile_description = models.TextField(max_length=1000)
    business_stream = models.ForeignKey("BusinessStream", on_delete=models.CASCADE)
    establishment_date = models.DateField(verbose_name="establishment date")
    company_website_url = models.CharField(verbose_name="website url", max_length=500)

    def __str__(self):
        return f"name - {self.company_name}, establishment date - {self.establishment_date}"


class BusinessStream(models.Model):
    business_stream_name = models.CharField(verbose_name="name", max_length=100)

    def __str__(self):
        return f"{self.business_stream_name}"


class CompanyImage(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company_images")
    company_image = models.ImageField(upload_to="company_images/", blank=True)

    def __str__(self):
        return f"company - {self.company.name}"
