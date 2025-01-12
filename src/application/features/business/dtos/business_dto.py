from typing import TypedDict

from ed_domain_model.entities.business import BillingDetail


class LocationDto(TypedDict):
    address: str
    latitude: float
    longitude: float
    postal_code: str
    city: str


class BusinessDto(TypedDict):
    business_name: str
    owner_first_name: str
    owner_last_name: str
    phone_number: str
    email: str
    location: LocationDto
    billing_details: list[BillingDetail]
