from django.contrib import admin

from pypi_vanity.models import Package, Release


class ReleaseInline(admin.TabularInline):
    model = Release


class PackageAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'total_downloads')
    inlines = [ReleaseInline]

admin.site.register(Package, PackageAdmin)
