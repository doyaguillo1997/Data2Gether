from app.properties.models import Property


def update_estimated_price(property_id: int, estimated_price: float):
    """Update estimated price of a property

    Args:
        property_id (int): Property id to update
        estimated_price (float): New value
    """
    Property.objects.filter(pk=property_id).update(estimated_price=estimated_price)
