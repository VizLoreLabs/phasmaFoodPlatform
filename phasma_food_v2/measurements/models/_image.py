from django.db import models


class Image(models.Model):
    measurement = models.ForeignKey("measurements.Measurement",
                                    on_delete=models.CASCADE,
                                    related_name="images",
                                    null=True
                                    )
    camera = models.ImageField(upload_to='images/food', null=True, blank=True)
    name = models.CharField(max_length=254, default="phasma_default_image_name")

    def __str__(self) -> str:
        return str(self.camera)
