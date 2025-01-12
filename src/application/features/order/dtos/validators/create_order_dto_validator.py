from datetime import UTC, datetime

from ed_domain_model.entities.order import ParcelSize

from src.application.features.common.dto.abc_dto_validator import (
    ABCDtoValidator,
    ValidationResponse,
)
from src.application.features.order.dtos.create_order_dto import (
    CreateConsumerDto,
    CreateOrderDto,
)


class CreateConsumerDtoValidator(ABCDtoValidator[CreateConsumerDto]):
    def validate(self, dto: CreateConsumerDto) -> ValidationResponse:
        errors = []

        if not dto["first_name"]:
            errors.append("First name of consmer is required.")

        if not dto["last_name"]:
            errors.append("Last name of consmer is required.")

        if not dto["phone_number"]:
            errors.append("Phone number of consmer is required")

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()


class CreateOrderDtoValidator(ABCDtoValidator[CreateOrderDto]):
    def validate(self, dto: CreateOrderDto) -> ValidationResponse:
        consumer_dto_validation = CreateConsumerDtoValidator().validate(dto["consumer"])
        errors = consumer_dto_validation.errors

        if dto["latest_time_of_delivery"] <= datetime.now(UTC):
            errors.append("Latest time of delivery must be in the future.")

        if not dto["parcel"]["weight"]:
            errors.append("Weight of parcel is required.")

        if not dto["parcel"]["dimensions"]["height"]:
            errors.append("Height dimension of parcel is required.")

        if not dto["parcel"]["dimensions"]["width"]:
            errors.append("Width dimension of parcel is required.")

        if not dto["parcel"]["dimensions"]["length"]:
            errors.append("Length dimension of parcel is required.")

        if not isinstance(dto["parcel"]["size"], ParcelSize):
            errors.append(
                f"Parcel size has to be one of {ParcelSize.SMALL}, {ParcelSize.MEDIUM} or {ParcelSize.LARGE}."
            )

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()
