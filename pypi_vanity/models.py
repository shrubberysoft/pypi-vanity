from django.db import models


class Package(models.Model):
    """Package entry on PyPI."""

    name = models.CharField(max_length=128)
    track_hidden = models.BooleanField(default=True,
                            verbose_name=u'Track hidden releases')

    class Meta:
        db_table = 'package'
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def total_downloads(self):
        total = self.releases.all().aggregate(models.Sum('total_downloads'))
        return total['total_downloads__sum'] or 0


class Release(models.Model):
    """Release of the package."""

    package = models.ForeignKey(Package, related_name='releases')
    version = models.CharField(max_length=32)
    total_downloads = models.IntegerField(default=0, verbose_name='Downloads')

    def __unicode__(self):
        return u'%s %s' % (self.package, self.version)

    class Meta:
        db_table = 'release'


class DownloadHistory(models.Model):
    """Historical download data."""

    release = models.ForeignKey(Release, related_name='download_history')
    date = models.DateTimeField(auto_now_add=True)
    total_downloads = models.IntegerField()

    class Meta:
        db_table = 'release_downloads'
