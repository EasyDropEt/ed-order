from src.application.features.business.dtos.create_business_dto import (
    CreateBusinessDto,
    CreateLocationDto,
)
from src.application.features.common.dto.abc_dto_validator import (
    ABCDtoValidator,
    ValidationResponse,
)


class CreateLocationDtoValidator(ABCDtoValidator[CreateLocationDto]):
    def validate(self, dto: CreateLocationDto) -> ValidationResponse:
        errors = []

        if not dto["latitude"]:
            errors.append("Latitude is required")

        if not dto["longitude"]:
            errors.append("Longitude is required")

        if not dto["address"]:
            errors.append("Address is required")

        if not dto["city"]:
            errors.append("City is required")

        if not dto["postal_code"]:
            errors.append("Postal code is required")

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()


class CreateBusinessDtoValidator(ABCDtoValidator[CreateBusinessDto]):
    def validate(self, dto: CreateBusinessDto) -> ValidationResponse:
        errors = []
        # TODO: Properly validate the create user dto

        if not dto["business_name"]:
            errors.append("Business name is required")

        if not dto["owner_first_name"]:
            errors.append("Business owner first name is required")

        if not dto["owner_last_name"]:
            errors.append("Business owner last name is required")

        if not dto["phone_number"]:
            errors.append("Phone number is required")

        if not dto["email"]:
            errors.append("Email is required")

        if not dto["billing_details"]:
            errors.append("Billing details is required")

        errors.extend(
            CreateLocationDtoValidator().validate(dto["location"]).errors,
        )

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()
