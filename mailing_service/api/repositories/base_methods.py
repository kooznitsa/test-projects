from sqlmodel.ext.asyncio.session import AsyncSession


async def upsert_value(session: AsyncSession, result, model_from_orm):
    """Upsert a value.

    It is used to create a value in the database if it does not already exist,
    else it is used to update the existing one.

    Args:
      session:
        with Session(engine) as session: ...
      result:
        The model data.
      model_from_orm:
        The model from_orm(model_create) data.

    Returns:
      The upserted model.
    """

    # if the entity does not exist, create it
    if result is None:
        result = model_from_orm

    # sync the data
    for k, v in model_from_orm.dict(exclude_unset=True).items():
        setattr(result, k, v)

    # persist the data to the database
    session.add(result)
    await session.commit()
    await session.refresh(result)

    return result
