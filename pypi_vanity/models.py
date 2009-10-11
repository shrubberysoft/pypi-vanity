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

    @classmethod
    def with_statistics(cls):
        """Return all packages annotated with statistics.  To examine
        the numbers, call the ``total_downloads`` method as usual."""
        return cls.objects.annotate(models.Sum('releases__total_downloads'))

    @property
    def total_downloads(self):
        # Nice: works both with annotate and directly
        sum_attr = 'releases__total_downloads__sum'
        if not hasattr(self, sum_attr):
            releases = self.releases.all()
            aggregate = releases.aggregate(models.Sum('total_downloads'))
            setattr(self, sum_attr, aggregate['total_downloads__sum'])
        return getattr(self, sum_attr) or 0


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
