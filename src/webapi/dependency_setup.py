from typing import Annotated

from fastapi import Depends
from rmediator.mediator import Mediator

from src.application.contracts.infrastructure.message_queue.abc_producer import (
    ABCProducer,
)
from src.application.contracts.infrastructure.message_queue.abc_subscriber import (
    ABCSubscriber,
)
from src.application.contracts.infrastructure.persistence.abc_unit_of_work import (
    ABCUnitOfWork,
)
from src.application.features.business.handlers.commands import (
    CreateBusinessCommandHandler,
    CreateOrdersCommandHandler,
)
from src.application.features.business.handlers.queries import (
    GetAllBusinessesQueryHandler,
    GetBusinessByUserIdQueryHandler,
    GetBusinessOrdersQueryHandler,
    GetBusinessQueryHandler,
)
from src.application.features.business.requests.commands import (
    CreateBusinessCommand,
    CreateOrdersCommand,
)
from src.application.features.business.requests.queries import (
    GetAllBusinessQuery,
    GetBusinessByUserIdQuery,
    GetBusinessOrdersQuery,
    GetBusinessQuery,
)
from src.application.features.delivery_job.handlers.commands import (
    CreateDeliveryJobCommandHandler,
)
from src.application.features.delivery_job.handlers.queries import (
    GetDeliveryJobsQueryHandler,
)
from src.application.features.delivery_job.requests.commands import (
    CreateDeliveryJobCommand,
)
from src.application.features.delivery_job.requests.queries import GetDeliveryJobsQuery
from src.application.features.driver.handlers.commands import CreateDriverCommandHandler
from src.application.features.driver.handlers.queries import (
    GetDriverDeliveryJobsQueryHandler,
)
from src.application.features.driver.requests.commands import CreateDriverCommand
from src.application.features.driver.requests.queries import GetDriverDeliveryJobsQuery
from src.common.generic_helpers import get_config
from src.common.typing.config import Config, TestMessage
from src.infrastructure.persistence.db_client import DbClient
from src.infrastructure.persistence.unit_of_work import UnitOfWork
from src.infrastructure.rabbitmq.producer import RabbitMQProducer
from src.infrastructure.rabbitmq.subscriber import RabbitMQSubscriber


def get_db_client(config: Annotated[Config, Depends(get_config)]) -> DbClient:
    return DbClient(
        config["mongo_db_connection_string"],
        config["db_name"],
    )


def get_uow(db_client: Annotated[DbClient, Depends(get_db_client)]) -> ABCUnitOfWork:
    return UnitOfWork(db_client)


def get_producer(config: Annotated[Config, Depends(get_config)]) -> ABCProducer:
    producer = RabbitMQProducer[TestMessage](
        config["rabbitmq_url"],
        config["rabbitmq_queue"],
    )
    producer.start()

    return producer


def get_subscriber(config: Annotated[Config, Depends(get_config)]) -> ABCSubscriber:
    subscriber = RabbitMQSubscriber[TestMessage](
        config["rabbitmq_url"],
        config["rabbitmq_queue"],
        lambda x: print(x),
    )
    subscriber.start()

    return subscriber


def mediator(
    uow: Annotated[ABCUnitOfWork, Depends(get_uow)],
    producer: Annotated[ABCProducer, Depends(get_producer)],
) -> Mediator:
    mediator = Mediator()

    handlers = [
        # Delivery job handler
        (CreateDeliveryJobCommand, CreateDeliveryJobCommandHandler(uow)),
        (GetDeliveryJobsQuery, GetDeliveryJobsQueryHandler(uow)),
        # Driver handlers
        (CreateDriverCommand, CreateDriverCommandHandler(uow)),
        (GetDriverDeliveryJobsQuery, GetDriverDeliveryJobsQueryHandler(uow)),
        # Business handlers
        (CreateBusinessCommand, CreateBusinessCommandHandler(uow)),
        (CreateOrdersCommand, CreateOrdersCommandHandler(uow, producer)),
        (GetBusinessQuery, GetBusinessQueryHandler(uow)),
        (GetBusinessByUserIdQuery, GetBusinessByUserIdQueryHandler(uow)),
        (GetBusinessOrdersQuery, GetBusinessOrdersQueryHandler(uow)),
        (GetAllBusinessQuery, GetAllBusinessesQueryHandler(uow)),
    ]
    for command, handler in handlers:
        mediator.register_handler(command, handler)

    return mediator
