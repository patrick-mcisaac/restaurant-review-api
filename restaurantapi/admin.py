from django.contrib import admin
from restaurantapi.models import Restaurant, City, Review, DiningExperience


# Register your models here.


class RestaurantAdmin(admin.ModelAdmin):

    list_display = [
        "name",
    ]


class ReviewAdminSerializer(admin.ModelAdmin):
    list_display = (
        "user__username",
        "restaurant_location__restaurant__name",
        "restaurant_location__city__name",
        "score",
    )


class DiningExperienceAdmin(admin.ModelAdmin):
    list_display = ("description",)


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(City, RestaurantAdmin)
admin.site.register(Review, ReviewAdminSerializer)
admin.site.register(DiningExperience, DiningExperienceAdmin)
