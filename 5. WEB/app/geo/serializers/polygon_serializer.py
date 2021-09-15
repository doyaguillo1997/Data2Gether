from django.contrib.gis.serializers.geojson import Serializer as GeoJSONSerializer


class Serializer(GeoJSONSerializer):
    """Serialize geo zones

    Args:
        GeoJSONSerializer ():
    """

    def get_dump_object(self, obj):
        """Dump one geo zone

        Args:
            obj: geo zone with historic and color info

        Returns:
            dict: dictionary with the attributtes
        """
        data = super(Serializer, self).get_dump_object(obj)

        data.update(centroid=obj.centroid.coords)
        data.update(level=obj.level.level)
        # Neighborhoods without historic data
        if obj.historic:
            data.update(color=obj.color)
            data.update(price=obj.historic.price)
            data.update(monthly_variation=obj.historic.monthly_variation)
            data.update(quarterly_variation=obj.historic.quarterly_variation)
            data.update(annual_variation=obj.historic.annual_variation)

        if obj.best_moment:
            data.update(best_moment_price=int(obj.best_moment.price))
            data.update(best_moment_date=obj.best_moment.date)

        return data
