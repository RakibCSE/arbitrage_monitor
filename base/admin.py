from django.contrib import admin
from .models import ExtendSignup, Profile, CoinDetails


class ExtendSignupAdmin(admin.ModelAdmin):
    list_display = ('user', 'type')


admin.site.register(ExtendSignup, ExtendSignupAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'city', 'profile_picture')


admin.site.register(Profile, ProfileAdmin)


class CoinDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'symbol',
        'price',
        'percent_change_1h',
        'percent_change_24h',
        'percent_change_7d',
        'volume_24h',
        'market_cap',
    )


admin.site.register(CoinDetails, CoinDetailsAdmin)
